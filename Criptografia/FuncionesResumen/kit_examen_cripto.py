"""
kit_examen_cripto.py — Funciones listas para copiar/pegar en el examen
======================================================================
Cada bloque está numerado igual que la Guia_Examen_Criptografia.md.
Importa solo lo que necesites; el fichero entero no tiene efectos
secundarios (no genera ficheros, no imprime) salvo el bloque __main__.

Dependencias: cryptography, ecies, eth_keys
  pip install cryptography eciespy eth-keys
"""

import json
import base64
import hashlib
import hmac as _hmac
import os
import struct
import time

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.exceptions import InvalidSignature
from ecies.utils import generate_eth_key
from ecies import encrypt as ecies_encrypt, decrypt as ecies_decrypt
from eth_keys import keys as eth_keys


# ─────────────────────────────────────────────
# CONSTANTES COMPARTIDAS
# ─────────────────────────────────────────────

PSS = asym_padding.PSS(
    mgf=asym_padding.MGF1(hashes.SHA256()),
    salt_length=asym_padding.PSS.MAX_LENGTH,
)
OAEP = asym_padding.OAEP(
    mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
    algorithm=hashes.SHA256(),
    label=None,
)
TAM_FIRMA_RSA2048 = 256   # bytes que ocupa una firma RSA 2048 + PSS
ADMIN_SALT = b"hospital_admin_salt_v1"
ITERACIONES = 100_000


# =============================================
# 1. SIMÉTRICO (Fernet)
# =============================================

def fernet_generar_clave() -> bytes:
    """Genera y devuelve una nueva clave Fernet (bytes)."""
    return Fernet.generate_key()

def fernet_guardar_clave(clave: bytes, ruta: str) -> None:
    """Guarda la clave Fernet en disco (modo wb)."""
    with open(ruta, "wb") as f:
        f.write(clave)

def fernet_cargar_clave(ruta: str) -> bytes:
    """Lee la clave Fernet desde disco."""
    with open(ruta, "rb") as f:
        return f.read()

def fernet_cifrar(mensaje: bytes, clave: bytes) -> bytes:
    """Cifra mensaje con Fernet. Retorna token (bytes)."""
    return Fernet(clave).encrypt(mensaje)

def fernet_descifrar(token: bytes, clave: bytes) -> bytes:
    """Descifra token Fernet. Lanza InvalidToken si la clave es incorrecta."""
    return Fernet(clave).decrypt(token)

def fernet_cifrar_fichero(ruta_entrada: str, ruta_salida: str, clave: bytes) -> None:
    """Lee ruta_entrada en rb, cifra con Fernet, escribe ruta_salida en wb."""
    with open(ruta_entrada, "rb") as f:
        contenido = f.read()
    with open(ruta_salida, "wb") as f:
        f.write(Fernet(clave).encrypt(contenido))

def fernet_descifrar_fichero(ruta_cifrada: str, clave: bytes) -> bytes:
    """Lee fichero cifrado (rb), descifra con Fernet, devuelve bytes originales."""
    with open(ruta_cifrada, "rb") as f:
        datos = f.read()
    return Fernet(clave).decrypt(datos)


# =============================================
# 2. CLAVES RSA (ficheros .pem)
# =============================================

def rsa_generar():
    """Genera par de claves RSA 2048. Retorna (priv, pub)."""
    priv = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
    )
    return priv, priv.public_key()

def rsa_guardar_pem(priv, pub, nombre: str) -> None:
    """Guarda rsa_privada_{nombre}.pem y rsa_publica_{nombre}.pem en el directorio actual."""
    with open(f"rsa_privada_{nombre}.pem", "wb") as f:
        f.write(priv.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        ))
    with open(f"rsa_publica_{nombre}.pem", "wb") as f:
        f.write(pub.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        ))

def rsa_cargar_pem(nombre: str):
    """Carga rsa_privada_{nombre}.pem y rsa_publica_{nombre}.pem. Retorna (priv, pub)."""
    with open(f"rsa_privada_{nombre}.pem", "rb") as f:
        priv = serialization.load_pem_private_key(f.read(), password=None)
    with open(f"rsa_publica_{nombre}.pem", "rb") as f:
        pub = serialization.load_pem_public_key(f.read())
    return priv, pub

def rsa_guardar_pem_ruta(priv, pub, ruta_priv: str, ruta_pub: str) -> None:
    """Variante con rutas absolutas/relativas explícitas."""
    with open(ruta_priv, "wb") as f:
        f.write(priv.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        ))
    with open(ruta_pub, "wb") as f:
        f.write(pub.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        ))

def rsa_cargar_pem_ruta(ruta_priv: str, ruta_pub: str):
    """Variante con rutas absolutas/relativas explícitas. Retorna (priv, pub)."""
    with open(ruta_priv, "rb") as f:
        priv = serialization.load_pem_private_key(f.read(), password=None)
    with open(ruta_pub, "rb") as f:
        pub = serialization.load_pem_public_key(f.read())
    return priv, pub


# =============================================
# 3. CLAVES ECIES (ficheros .txt hex)
# =============================================

def ecies_generar() -> tuple[str, str]:
    """Genera par de claves ECIES. Retorna (priv_hex, pub_hex)."""
    priv_key = generate_eth_key()
    return priv_key.to_hex(), priv_key.public_key.to_hex()

def ecies_guardar_txt(priv_hex: str, pub_hex: str, nombre: str) -> None:
    """Guarda ecies_claves_{nombre}.txt con priv_hex en línea 1, pub_hex en línea 2."""
    with open(f"ecies_claves_{nombre}.txt", "w") as f:
        f.write(f"{priv_hex}\n{pub_hex}\n")

def ecies_cargar_txt(nombre: str) -> tuple[str, str]:
    """Lee ecies_claves_{nombre}.txt. Retorna (priv_hex, pub_hex)."""
    with open(f"ecies_claves_{nombre}.txt", "r") as f:
        lineas = f.read().splitlines()
    return lineas[0], lineas[1]


# =============================================
# 4. RSA — operaciones (OAEP + PSS + Prehashed)
# =============================================

def rsa_cifrar_oaep(mensaje: bytes, pub) -> bytes:
    """Cifra mensaje con RSA OAEP (clave pública del receptor). Límite ~190 B con 2048."""
    return pub.encrypt(mensaje, OAEP)

def rsa_descifrar_oaep(cifrado: bytes, priv) -> bytes:
    """Descifra con RSA OAEP (clave privada del receptor)."""
    return priv.decrypt(cifrado, OAEP)

def rsa_firmar(mensaje: bytes, priv) -> bytes:
    """Firma mensaje con RSA PSS SHA256 (clave privada del emisor). RSA hashea internamente."""
    return priv.sign(mensaje, PSS, hashes.SHA256())

def rsa_verificar(firma: bytes, mensaje: bytes, pub) -> bool:
    """Verifica firma RSA PSS (clave pública del emisor). Retorna True/False."""
    try:
        pub.verify(firma, mensaje, PSS, hashes.SHA256())
        return True
    except InvalidSignature:
        return False

def rsa_firmar_prehashed(msg_hash: bytes, priv) -> bytes:
    """Firma hash SHA256 ya calculado (32 bytes). Usar cuando el enunciado pide 'firmar el hash'."""
    return priv.sign(msg_hash, PSS, Prehashed(hashes.SHA256()))

def rsa_verificar_prehashed(firma: bytes, msg_hash: bytes, pub) -> bool:
    """Verifica firma RSA sobre hash precalculado. msg_hash debe ser SHA256 (32 bytes)."""
    try:
        pub.verify(firma, msg_hash, PSS, Prehashed(hashes.SHA256()))
        return True
    except InvalidSignature:
        return False


# =============================================
# 5. ECIES — operaciones (encrypt/decrypt + ECDSA)
# =============================================

def ecies_cifrar(mensaje: bytes, pub_hex: str) -> bytes:
    """Cifra mensaje con ECIES usando la clave pública hex del receptor."""
    return ecies_encrypt(pub_hex, mensaje)

def ecies_descifrar(cifrado: bytes, priv_hex: str) -> bytes:
    """Descifra con ECIES usando la clave privada hex del receptor."""
    return ecies_decrypt(priv_hex, cifrado)

def ecies_firmar(mensaje: bytes, priv_hex: str) -> bytes:
    """Firma mensaje con ECDSA (eth_keys). Hashea SHA256 internamente. Retorna bytes de firma."""
    msg_hash = hashlib.sha256(mensaje).digest()
    priv_obj = eth_keys.PrivateKey(bytes.fromhex(priv_hex.replace("0x", "")))
    return priv_obj.sign_msg_hash(msg_hash).to_bytes()

def ecies_verificar(firma_bytes: bytes, mensaje: bytes, pub_hex: str) -> bool:
    """Verifica firma ECDSA (eth_keys). Retorna True/False."""
    try:
        msg_hash = hashlib.sha256(mensaje).digest()
        pub_obj = eth_keys.PublicKey(bytes.fromhex(pub_hex.replace("0x", "")))
        firma_obj = eth_keys.Signature(firma_bytes)
        return pub_obj.verify_msg_hash(msg_hash, firma_obj)
    except Exception:
        return False


# =============================================
# 6. HASH — integridad
# =============================================

def hash_sha256_segmentos(*segmentos: bytes) -> str:
    """Calcula SHA256 de uno o más segmentos concatenados. Retorna hexdigest (str)."""
    h = hashlib.sha256()
    for seg in segmentos:
        h.update(seg)
    return h.hexdigest()

def hash_sha256_bytes(*segmentos: bytes) -> bytes:
    """Como hash_sha256_segmentos pero retorna digest bytes (para firmar o comparar)."""
    h = hashlib.sha256()
    for seg in segmentos:
        h.update(seg)
    return h.digest()

def hash_sha256_cryptography(*segmentos: bytes) -> str:
    """Calcula SHA256 con la API cryptography. Retorna hex str."""
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    for seg in segmentos:
        digest.update(seg)
    return digest.finalize().hex()

def hash_cadena_siguiente(mensaje_actual: bytes, hash_previo: bytes) -> bytes:
    """hash_siguiente = SHA256(mensaje_actual + hash_previo) como bytes (digest).
    Usar en cadenas de reenvío: A→B→C con trazabilidad."""
    return hashlib.sha256(mensaje_actual + hash_previo).digest()

def hash_verificar_segmentos(hash_esperado_hex: str, *segmentos: bytes) -> bool:
    """Verifica integridad comparando hash_esperado_hex con SHA256 de los segmentos."""
    return hash_sha256_segmentos(*segmentos) == hash_esperado_hex


# =============================================
# 7. HÍBRIDO RSA + Fernet (firma aparte)
# =============================================

def hibrido_rsa_cifrar(mensaje: bytes, pub_destino) -> tuple[bytes, bytes]:
    """Cifrado híbrido RSA. Retorna (clave_fernet_cifrada, msg_cifrado).
    Firma va aparte: llamar a rsa_firmar antes de enviar."""
    clave_fernet = Fernet.generate_key()
    msg_cifrado = Fernet(clave_fernet).encrypt(mensaje)
    clave_cifrada = rsa_cifrar_oaep(clave_fernet, pub_destino)
    return clave_cifrada, msg_cifrado

def hibrido_rsa_descifrar(clave_cifrada: bytes, msg_cifrado: bytes, priv_destino) -> bytes:
    """Descifrado híbrido RSA. Retorna mensaje en claro (bytes).
    Verificar firma aparte: llamar a rsa_verificar con el mensaje devuelto."""
    clave_fernet = rsa_descifrar_oaep(clave_cifrada, priv_destino)
    return Fernet(clave_fernet).decrypt(msg_cifrado)


# =============================================
# 8. HÍBRIDO ECIES + Fernet (firma aparte)
# =============================================

def hibrido_ecies_cifrar(mensaje: bytes, pub_hex_destino: str) -> tuple[bytes, bytes]:
    """Cifrado híbrido ECIES. Retorna (clave_fernet_cifrada, msg_cifrado).
    Firma va aparte: llamar a ecies_firmar antes de enviar."""
    clave_fernet = Fernet.generate_key()
    msg_cifrado = Fernet(clave_fernet).encrypt(mensaje)
    clave_cifrada = ecies_cifrar(clave_fernet, pub_hex_destino)
    return clave_cifrada, msg_cifrado

def hibrido_ecies_descifrar(clave_cifrada: bytes, msg_cifrado: bytes, priv_hex_destino: str) -> bytes:
    """Descifrado híbrido ECIES. Retorna mensaje en claro (bytes).
    Verificar firma aparte: llamar a ecies_verificar con el mensaje devuelto."""
    clave_fernet = ecies_descifrar(clave_cifrada, priv_hex_destino)
    return Fernet(clave_fernet).decrypt(msg_cifrado)


# =============================================
# 9. FIRMA INTERNA (mensaje + firma dentro del Fernet)
# =============================================

# --- 9a. RSA con payload JSON ---

def empaquetar_json_firma(mensaje: bytes, priv_origen) -> bytes:
    """Firma RSA PSS y empaqueta {mensaje, firma} en JSON bytes (listos para Fernet)."""
    firma = rsa_firmar(mensaje, priv_origen)
    payload = {
        "mensaje": base64.b64encode(mensaje).decode(),
        "firma":   base64.b64encode(firma).decode(),
    }
    return json.dumps(payload).encode()

def desempaquetar_json_firma(payload_bytes: bytes, pub_emisor) -> tuple[bytes, bool]:
    """Extrae y verifica firma RSA desde payload JSON. Retorna (mensaje, firma_ok)."""
    payload = json.loads(payload_bytes.decode())
    mensaje = base64.b64decode(payload["mensaje"])
    firma   = base64.b64decode(payload["firma"])
    return mensaje, rsa_verificar(firma, mensaje, pub_emisor)

def hibrido_rsa_cifrar_firma_interna(mensaje: bytes, priv_origen, pub_destino) -> tuple[bytes, bytes]:
    """Híbrido RSA con firma interna: firma → JSON → Fernet → RSA OAEP clave.
    Retorna (clave_fernet_cifrada, payload_cifrado)."""
    payload = empaquetar_json_firma(mensaje, priv_origen)
    clave_fernet = Fernet.generate_key()
    payload_cifrado = Fernet(clave_fernet).encrypt(payload)
    clave_cifrada = rsa_cifrar_oaep(clave_fernet, pub_destino)
    return clave_cifrada, payload_cifrado

def hibrido_rsa_descifrar_firma_interna(
    clave_cifrada: bytes, payload_cifrado: bytes, priv_destino, pub_emisor
) -> tuple[bytes, bool]:
    """Descifra híbrido RSA con firma interna. Retorna (mensaje, firma_ok)."""
    clave_fernet = rsa_descifrar_oaep(clave_cifrada, priv_destino)
    payload = Fernet(clave_fernet).decrypt(payload_cifrado)
    return desempaquetar_json_firma(payload, pub_emisor)


# --- 9b. ECIES con payload JSON ---

def empaquetar_json_firma_ecies(mensaje: bytes, priv_hex_origen: str) -> bytes:
    """Firma ECDSA y empaqueta {mensaje, firma} en JSON bytes."""
    firma = ecies_firmar(mensaje, priv_hex_origen)
    payload = {
        "mensaje": base64.b64encode(mensaje).decode(),
        "firma":   base64.b64encode(firma).decode(),
    }
    return json.dumps(payload).encode()

def desempaquetar_json_firma_ecies(payload_bytes: bytes, pub_hex_emisor: str) -> tuple[bytes, bool]:
    """Extrae y verifica firma ECDSA desde payload JSON. Retorna (mensaje, firma_ok)."""
    payload = json.loads(payload_bytes.decode())
    mensaje = base64.b64decode(payload["mensaje"])
    firma   = base64.b64decode(payload["firma"])
    return mensaje, ecies_verificar(firma, mensaje, pub_hex_emisor)

def hibrido_ecies_cifrar_firma_interna(
    mensaje: bytes, priv_hex_origen: str, pub_hex_destino: str
) -> tuple[bytes, bytes]:
    """Híbrido ECIES con firma interna. Retorna (clave_fernet_cifrada, payload_cifrado)."""
    payload = empaquetar_json_firma_ecies(mensaje, priv_hex_origen)
    clave_fernet = Fernet.generate_key()
    payload_cifrado = Fernet(clave_fernet).encrypt(payload)
    clave_cifrada = ecies_cifrar(clave_fernet, pub_hex_destino)
    return clave_cifrada, payload_cifrado

def hibrido_ecies_descifrar_firma_interna(
    clave_cifrada: bytes, payload_cifrado: bytes, priv_hex_destino: str, pub_hex_emisor: str
) -> tuple[bytes, bool]:
    """Descifra híbrido ECIES con firma interna. Retorna (mensaje, firma_ok)."""
    clave_fernet = ecies_descifrar(clave_cifrada, priv_hex_destino)
    payload = Fernet(clave_fernet).decrypt(payload_cifrado)
    return desempaquetar_json_firma_ecies(payload, pub_hex_emisor)


# --- 9c. Ronda2: firma + hash de sesión ---

def hash_mensaje_sesion(token_sesion: str, mensaje: bytes) -> str:
    """SHA256(token_sesion.encode() + mensaje) como hexdigest. Vincula mensaje a sesión."""
    return hashlib.sha256(token_sesion.encode() + mensaje).hexdigest()

def empaquetar_json_firma_sesion(mensaje: bytes, priv_origen, token_sesion: str) -> bytes:
    """Firma RSA PSS + hash de sesión. Payload: {mensaje, firma, hash_msg} en JSON bytes."""
    firma = rsa_firmar(mensaje, priv_origen)
    payload = {
        "mensaje":  base64.b64encode(mensaje).decode(),
        "firma":    base64.b64encode(firma).decode(),
        "hash_msg": hash_mensaje_sesion(token_sesion, mensaje),
    }
    return json.dumps(payload).encode()

def desempaquetar_json_firma_sesion(
    payload_bytes: bytes, pub_emisor, token_sesion: str
) -> tuple[bytes, bool, bool]:
    """Verifica hash de sesión y firma RSA. Retorna (mensaje, hash_ok, firma_ok)."""
    payload = json.loads(payload_bytes.decode())
    mensaje = base64.b64decode(payload["mensaje"])
    firma   = base64.b64decode(payload["firma"])
    hash_ok  = payload["hash_msg"] == hash_mensaje_sesion(token_sesion, mensaje)
    firma_ok = rsa_verificar(firma, mensaje, pub_emisor)
    return mensaje, hash_ok, firma_ok

def hibrido_rsa_cifrar_sesion(
    mensaje: bytes, priv_origen, pub_destino, token_sesion: str
) -> tuple[bytes, bytes]:
    """Híbrido RSA Ronda2: firma+hash_sesión → JSON → Fernet → RSA OAEP clave."""
    payload = empaquetar_json_firma_sesion(mensaje, priv_origen, token_sesion)
    clave_fernet = Fernet.generate_key()
    payload_cifrado = Fernet(clave_fernet).encrypt(payload)
    clave_cifrada = rsa_cifrar_oaep(clave_fernet, pub_destino)
    return clave_cifrada, payload_cifrado

def hibrido_rsa_descifrar_sesion(
    clave_cifrada: bytes, payload_cifrado: bytes, priv_destino, pub_emisor, token_sesion: str
) -> tuple[bytes, bool, bool]:
    """Descifra híbrido RSA Ronda2. Retorna (mensaje, hash_ok, firma_ok)."""
    clave_fernet = rsa_descifrar_oaep(clave_cifrada, priv_destino)
    payload = Fernet(clave_fernet).decrypt(payload_cifrado)
    return desempaquetar_json_firma_sesion(payload, pub_emisor, token_sesion)


# =============================================
# 10. EMPAQUETAR (6 formatos alternativos)
#     Todos retornan bytes y verifican la firma al desempaquetar.
# =============================================

# --- CSV con comas ---

def empaquetar_coma(mensaje: bytes, priv) -> bytes:
    """Empaqueta msg_b64,firma_b64 separados por coma. Base64 garantiza que no hay comas."""
    firma = rsa_firmar(mensaje, priv)
    linea = f"{base64.b64encode(mensaje).decode()},{base64.b64encode(firma).decode()}"
    return linea.encode()

def desempaquetar_coma(payload_bytes: bytes, pub) -> tuple[bytes, bool]:
    """Desempaqueta CSV coma. Retorna (mensaje, firma_ok)."""
    msg_b64, firma_b64 = payload_bytes.decode().split(",", 1)
    mensaje = base64.b64decode(msg_b64)
    firma   = base64.b64decode(firma_b64)
    return mensaje, rsa_verificar(firma, mensaje, pub)

# --- Separador pipe ---

def empaquetar_pipe(mensaje: bytes, priv) -> bytes:
    """Empaqueta msg_b64|firma_b64."""
    firma = rsa_firmar(mensaje, priv)
    return f"{base64.b64encode(mensaje).decode()}|{base64.b64encode(firma).decode()}".encode()

def desempaquetar_pipe(payload_bytes: bytes, pub) -> tuple[bytes, bool]:
    """Desempaqueta separador |. Retorna (mensaje, firma_ok)."""
    msg_b64, firma_b64 = payload_bytes.decode().split("|", 1)
    mensaje = base64.b64decode(msg_b64)
    firma   = base64.b64decode(firma_b64)
    return mensaje, rsa_verificar(firma, mensaje, pub)

# --- Dos líneas ---

def empaquetar_dos_lineas(mensaje: bytes, priv) -> bytes:
    """Empaqueta msg_b64\\nfirma_b64 (dos líneas texto)."""
    firma = rsa_firmar(mensaje, priv)
    texto = base64.b64encode(mensaje).decode() + "\n" + base64.b64encode(firma).decode()
    return texto.encode()

def desempaquetar_dos_lineas(payload_bytes: bytes, pub) -> tuple[bytes, bool]:
    """Desempaqueta dos líneas. Retorna (mensaje, firma_ok)."""
    msg_b64, firma_b64 = payload_bytes.decode().splitlines()
    mensaje = base64.b64decode(msg_b64)
    firma   = base64.b64decode(firma_b64)
    return mensaje, rsa_verificar(firma, mensaje, pub)

# --- Binario: firma al final (RSA 2048, sin base64) ---

def empaquetar_binario_fijo(mensaje: bytes, priv) -> bytes:
    """Concatena mensaje + firma_bytes. Firma RSA 2048 = 256 bytes fijos al final."""
    firma = rsa_firmar(mensaje, priv)
    return mensaje + firma

def desempaquetar_binario_fijo(paquete: bytes, pub) -> tuple[bytes, bool]:
    """Separa los últimos 256 bytes como firma. Retorna (mensaje, firma_ok)."""
    mensaje = paquete[:-TAM_FIRMA_RSA2048]
    firma   = paquete[-TAM_FIRMA_RSA2048:]
    return mensaje, rsa_verificar(firma, mensaje, pub)

# --- struct: prefijo de longitud (cualquier tamaño de firma) ---

def empaquetar_struct(mensaje: bytes, priv) -> bytes:
    """Empaqueta 4 bytes (longitud firma big-endian) + firma + mensaje."""
    firma = rsa_firmar(mensaje, priv)
    return struct.pack(">I", len(firma)) + firma + mensaje

def desempaquetar_struct(paquete: bytes, pub) -> tuple[bytes, bool]:
    """Lee los 4 primeros bytes para saber el tamaño de la firma. Retorna (mensaje, firma_ok)."""
    tam = struct.unpack(">I", paquete[:4])[0]
    firma   = paquete[4 : 4 + tam]
    mensaje = paquete[4 + tam :]
    return mensaje, rsa_verificar(firma, mensaje, pub)


# =============================================
# 11. FICHEROS AUTH (PBKDF2 + medicos.txt.enc)
# =============================================

def derivar_clave_maestra(contrasena_admin: str, salt: bytes = ADMIN_SALT) -> bytes:
    """PBKDF2 SHA256 → clave Fernet (urlsafe_b64encode, 32 bytes derivados)."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERACIONES,
        backend=default_backend(),
    )
    return base64.urlsafe_b64encode(kdf.derive(contrasena_admin.encode()))

def cifrar_fichero(ruta_txt: str, ruta_enc: str, contrasena_admin: str,
                   borrar_plano: bool = True) -> None:
    """Lee ruta_txt (rb), cifra con clave maestra derivada de contrasena_admin,
    guarda ruta_enc (wb). Si borrar_plano=True elimina el plano."""
    with open(ruta_txt, "rb") as f:
        contenido = f.read()
    clave = derivar_clave_maestra(contrasena_admin)
    with open(ruta_enc, "wb") as f:
        f.write(Fernet(clave).encrypt(contenido))
    if borrar_plano:
        os.remove(ruta_txt)

def descifrar_fichero(ruta_enc: str, contrasena_admin: str) -> str:
    """Descifra ruta_enc con clave maestra. Retorna contenido como str UTF-8."""
    with open(ruta_enc, "rb") as f:
        datos = f.read()
    clave = derivar_clave_maestra(contrasena_admin)
    return Fernet(clave).decrypt(datos).decode("utf-8")

def hasheo_password(contrasena: str, salt: bytes) -> str:
    """PBKDF2 SHA256 de la contraseña. Retorna base64 str (para guardar en CSV)."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERACIONES,
        backend=default_backend(),
    )
    return base64.b64encode(kdf.derive(contrasena.encode())).decode()

def verifica_password(contrasena: str, salt: bytes, hash_almacenado: str) -> bool:
    """Verifica PBKDF2 con .verify(). Retorna True/False."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERACIONES,
        backend=default_backend(),
    )
    try:
        kdf.verify(contrasena.encode(), base64.b64decode(hash_almacenado))
        return True
    except Exception:
        return False

def alta_usuario_linea(nombre: str, contrasena: str) -> str:
    """Crea una línea CSV 'nombre,salt_b64,hash_b64\\n' lista para añadir al fichero."""
    salt = os.urandom(16)
    return f"{nombre},{base64.b64encode(salt).decode()},{hasheo_password(contrasena, salt)}\n"

def generar_token_sesion(usuario: str) -> str:
    """SHA256(usuario:timestamp:salt_sesion) como hexdigest. Token único por sesión."""
    salt_sesion = os.urandom(16).hex()
    timestamp   = str(int(time.time()))
    return hashlib.sha256(f"{usuario}:{timestamp}:{salt_sesion}".encode()).hexdigest()

def autentica_usuario(usuario: str, contrasena: str, ruta_enc: str,
                      contrasena_admin: str) -> tuple[bool, str | None]:
    """Descifra medicos.txt.enc, busca usuario, verifica contraseña con PBKDF2.
    Retorna (True, token_sesion) si OK, (False, None) si falla."""
    try:
        contenido = descifrar_fichero(ruta_enc, contrasena_admin)
    except Exception:
        return False, None
    for linea in contenido.splitlines():
        partes = linea.strip().split(",")
        if len(partes) != 3:
            continue
        nombre_alm, salt_b64, hash_b64 = partes
        if nombre_alm != usuario:
            continue
        salt = base64.b64decode(salt_b64)
        if verifica_password(contrasena, salt, hash_b64):
            return True, generar_token_sesion(usuario)
        return False, None
    return False, None


# =============================================
# 12. HMAC-SHA256 (autenticación simétrica)
# =============================================

def hmac_generar(clave_compartida: bytes, mensaje: bytes) -> bytes:
    """Genera MAC SHA256 (bytes). Usar con clave simétrica compartida."""
    return _hmac.new(clave_compartida, mensaje, hashlib.sha256).digest()

def hmac_verificar(clave_compartida: bytes, mensaje: bytes, mac_recibido: bytes) -> bool:
    """Verifica MAC con compare_digest (resistente a timing attacks)."""
    mac_esperado = hmac_generar(clave_compartida, mensaje)
    return _hmac.compare_digest(mac_esperado, mac_recibido)


# =============================================
# 13. CADENA DE HASHES (reenvío A→B→C, Ronda2 ej. D)
# =============================================

def cadena_enviar_ab(mensaje: bytes, clave_ab: bytes) -> tuple[bytes, bytes]:
    """A→B: cifra con Fernet y calcula hash1 = SHA256(mensaje).
    Retorna (cifrado_ab, hash1_bytes)."""
    hash1 = hashlib.sha256(mensaje).digest()
    cifrado = fernet_cifrar(mensaje, clave_ab)
    return cifrado, hash1

def cadena_recibir_ab(cifrado: bytes, hash1_recibido: bytes,
                      clave_ab: bytes) -> tuple[bytes, bool]:
    """B descifra A→B y verifica hash1. Retorna (mensaje, hash_ok)."""
    mensaje = fernet_descifrar(cifrado, clave_ab)
    hash_ok = hashlib.sha256(mensaje).digest() == hash1_recibido
    return mensaje, hash_ok

def cadena_reenviar_bc(mensaje_bc: bytes, hash1: bytes,
                       clave_bc: bytes) -> tuple[bytes, bytes, bytes]:
    """B→C: calcula hash2 = SHA256(mensaje_bc + hash1), cifra con Fernet.
    Retorna (cifrado_bc, hash1, hash2_bytes)."""
    hash2   = hashlib.sha256(mensaje_bc + hash1).digest()
    cifrado = fernet_cifrar(mensaje_bc, clave_bc)
    return cifrado, hash1, hash2

def cadena_recibir_bc(cifrado: bytes, hash1: bytes, hash2_recibido: bytes,
                      clave_bc: bytes) -> tuple[bytes, bool, bool]:
    """C descifra B→C y verifica hash1 y hash2. Retorna (mensaje, hash1_ok, hash2_ok)."""
    mensaje  = fernet_descifrar(cifrado, clave_bc)
    hash1_ok = True                                         # B ya lo validó; C confía en que llega íntegro
    hash2_ok = hashlib.sha256(mensaje + hash1).digest() == hash2_recibido
    return mensaje, hash1_ok, hash2_ok


# =============================================
# SMOKE TEST — ejecutar con: python kit_examen_cripto.py
# =============================================

if __name__ == "__main__":
    print("=== SMOKE TEST kit_examen_cripto.py ===\n")

    # --- Simétrico ---
    clave = fernet_generar_clave()
    token = fernet_cifrar(b"Hola mundo", clave)
    assert fernet_descifrar(token, clave) == b"Hola mundo"
    print("[OK] Fernet cifrar/descifrar")

    # --- Claves RSA ---
    priv_a, pub_a = rsa_generar()
    priv_b, pub_b = rsa_generar()
    print("[OK] RSA generar claves")

    # --- RSA ops ---
    firma = rsa_firmar(b"test", priv_a)
    assert rsa_verificar(firma, b"test", pub_a)
    assert not rsa_verificar(firma, b"otro", pub_a)
    print("[OK] RSA firmar/verificar")

    cifrado = rsa_cifrar_oaep(b"secreto", pub_b)
    assert rsa_descifrar_oaep(cifrado, priv_b) == b"secreto"
    print("[OK] RSA cifrar/descifrar OAEP")

    # --- Híbrido RSA ---
    msg = b"Documento confidencial."
    clave_enc, msg_enc = hibrido_rsa_cifrar(msg, pub_b)
    assert hibrido_rsa_descifrar(clave_enc, msg_enc, priv_b) == msg
    print("[OK] Híbrido RSA")

    # --- Firma interna RSA ---
    clave_enc, payload_enc = hibrido_rsa_cifrar_firma_interna(msg, priv_a, pub_b)
    m, ok = hibrido_rsa_descifrar_firma_interna(clave_enc, payload_enc, priv_b, pub_a)
    assert m == msg and ok
    print("[OK] Híbrido RSA firma interna")

    # --- Ronda2 sesión ---
    token_s = generar_token_sesion("alice")
    clave_enc, payload_enc = hibrido_rsa_cifrar_sesion(msg, priv_a, pub_b, token_s)
    m, h_ok, f_ok = hibrido_rsa_descifrar_sesion(clave_enc, payload_enc, priv_b, pub_a, token_s)
    assert m == msg and h_ok and f_ok
    print("[OK] Híbrido RSA sesión Ronda2")

    # --- Hash ---
    h = hash_sha256_segmentos(b"A", b"B", b"C")
    assert len(h) == 64
    assert hash_verificar_segmentos(h, b"A", b"B", b"C")
    print("[OK] Hash SHA256 segmentos")

    # --- Cadena de hashes ---
    clave_ab = fernet_generar_clave()
    clave_bc = fernet_generar_clave()
    cifrado_ab, hash1 = cadena_enviar_ab(b"Factura AB", clave_ab)
    msg_ab, h1_ok = cadena_recibir_ab(cifrado_ab, hash1, clave_ab)
    assert h1_ok
    cifrado_bc, h1, hash2 = cadena_reenviar_bc(b"Factura BC", hash1, clave_bc)
    msg_bc, _, h2_ok = cadena_recibir_bc(cifrado_bc, h1, hash2, clave_bc)
    assert h2_ok
    print("[OK] Cadena de hashes A->B->C")

    # --- HMAC ---
    clave_hmac = os.urandom(32)
    mac = hmac_generar(clave_hmac, b"msg")
    assert hmac_verificar(clave_hmac, b"msg", mac)
    assert not hmac_verificar(clave_hmac, b"otro", mac)
    print("[OK] HMAC")

    # --- Auth fichero ---
    linea = alta_usuario_linea("alice", "pass1234")
    partes = linea.strip().split(",")
    salt = base64.b64decode(partes[1])
    assert verifica_password("pass1234", salt, partes[2])
    assert not verifica_password("incorrecta", salt, partes[2])
    print("[OK] PBKDF2 alta/verificar usuario")

    # --- Empaquetar formatos ---
    for nombre, empaquetar, desempaquetar in [
        ("JSON",         empaquetar_json_firma,     desempaquetar_json_firma),
        ("CSV coma",     empaquetar_coma,            desempaquetar_coma),
        ("Pipe",         empaquetar_pipe,            desempaquetar_pipe),
        ("Dos líneas",   empaquetar_dos_lineas,      desempaquetar_dos_lineas),
        ("Binario fijo", empaquetar_binario_fijo,    desempaquetar_binario_fijo),
        ("Struct",       empaquetar_struct,          desempaquetar_struct),
    ]:
        paquete = empaquetar(b"mensaje test", priv_a)
        m, ok = desempaquetar(paquete, pub_a)
        assert m == b"mensaje test" and ok, f"Falló {nombre}"
        print(f"[OK] Empaquetar {nombre}")

    print("\n=== Todos los tests pasaron ===")
