"""
Hibrido RSA + Fernet con firma interna y hash de sesion (with open para .pem).
"""

import json
import base64
import hashlib
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _hash_mensaje_sesion(token_sesion: str, mensaje: bytes) -> str:
    return hashlib.sha256(token_sesion.encode() + mensaje).hexdigest()


def generar_claves(nombre: str):
    print(f"Generando claves RSA para {nombre}...")
    priv = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
    )
    return priv, priv.public_key()


def guardar_claves(priv, pub, nombre: str) -> None:
    print(f"Guardando claves de {nombre} en .pem...")
    ruta_priv = os.path.join(BASE_DIR, f"rsa_privada_{nombre}.pem")
    ruta_pub = os.path.join(BASE_DIR, f"rsa_publica_{nombre}.pem")

    with open(ruta_priv, mode="wb") as f:
        f.write(
            priv.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption(),
            )
        )
    with open(ruta_pub, mode="wb") as f:
        f.write(
            pub.public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )


def cargar_claves(nombre: str):
    print(f"Cargando claves de {nombre} desde .pem...")
    ruta_priv = os.path.join(BASE_DIR, f"rsa_privada_{nombre}.pem")
    ruta_pub = os.path.join(BASE_DIR, f"rsa_publica_{nombre}.pem")

    with open(ruta_priv, mode="rb") as f:
        priv = serialization.load_pem_private_key(f.read(), password=None)
    with open(ruta_pub, mode="rb") as f:
        pub = serialization.load_pem_public_key(f.read())
    return priv, pub


def empaquetar_con_firma_y_sesion(mensaje: bytes, priv_origen, token_sesion: str) -> bytes:
    print("   -> Firmando (RSA PSS) y empaquetando mensaje + firma + hash_msg...")
    firma_bytes = priv_origen.sign(
        mensaje,
        asym_padding.PSS(
            mgf=asym_padding.MGF1(hashes.SHA256()),
            salt_length=asym_padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    payload = {
        "mensaje": base64.b64encode(mensaje).decode(),
        "firma": base64.b64encode(firma_bytes).decode(),
        "hash_msg": _hash_mensaje_sesion(token_sesion, mensaje),
    }
    return json.dumps(payload).encode()


def desempaquetar_y_verificar(payload_bytes: bytes, pub_emisor, token_sesion: str) -> tuple[bytes, bool, bool]:
    payload = json.loads(payload_bytes.decode())
    mensaje = base64.b64decode(payload["mensaje"])
    firma_bytes = base64.b64decode(payload["firma"])
    hash_recibido = payload["hash_msg"]

    hash_ok = hash_recibido == _hash_mensaje_sesion(token_sesion, mensaje)
    if not hash_ok:
        print("   ERROR: hash_msg no coincide con token de sesion + mensaje")

    try:
        pub_emisor.verify(
            firma_bytes,
            mensaje,
            asym_padding.PSS(
                mgf=asym_padding.MGF1(hashes.SHA256()),
                salt_length=asym_padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        firma_ok = True
    except InvalidSignature:
        firma_ok = False
        print("   ERROR: firma RSA interna no valida")

    return mensaje, hash_ok, firma_ok


def cifrar_hibrido(mensaje: bytes, priv_origen, pub_destino, token_sesion: str):
    print(" [Cifrado] Hibrido RSA + firma interna + hash de sesion...")
    payload = empaquetar_con_firma_y_sesion(mensaje, priv_origen, token_sesion)
    clave_fernet = Fernet.generate_key()
    payload_cifrado = Fernet(clave_fernet).encrypt(payload)
    clave_fernet_cifrada = pub_destino.encrypt(
        clave_fernet,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return clave_fernet_cifrada, payload_cifrado


def descifrar_hibrido(clave_fernet_cifrada, payload_cifrado, priv_destino, pub_emisor, token_sesion: str):
    print(" [Descifrado] Hibrido RSA + verificacion hash y firma...")
    clave_fernet = priv_destino.decrypt(
        clave_fernet_cifrada,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    payload_bytes = Fernet(clave_fernet).decrypt(payload_cifrado)
    return desempaquetar_y_verificar(payload_bytes, pub_emisor, token_sesion)


def enviar_mensaje(origen, destino, priv_origen, pub_destino, mensaje: bytes, token_sesion: str):
    print(f"\n=================[ {origen} ENVIA A {destino} ]=================")
    print(f'Mensaje original: "{mensaje.decode()}"')
    paquete = cifrar_hibrido(mensaje, priv_origen, pub_destino, token_sesion)
    print(">> Paquete: (clave_fernet_cifrada, payload_cifrado) <<")
    return paquete


def recibir_mensaje(origen, destino, priv_destino, pub_emisor, clave_cifrada, payload_cifrado, token_sesion: str):
    print(f"\n=================[ {destino} RECIBE DE {origen} ]=================")
    mensaje, hash_ok, firma_ok = descifrar_hibrido(
        clave_cifrada, payload_cifrado, priv_destino, pub_emisor, token_sesion
    )
    if hash_ok and firma_ok:
        print(f'Mensaje aceptado: "{mensaje.decode()}"')
        return mensaje
    print("Mensaje rechazado (hash de sesion o firma invalidos)")
    return None
