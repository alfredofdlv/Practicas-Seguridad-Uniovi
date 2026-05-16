"""

Modulo de comunicación principal

Un hospital tiene tres médicos (A, B, C) registrados en un sistema de autenticación seguro



"""

"""
EJERCICIO - HÍBRIDO RSA + FERNET CON FIRMA INTERNA
===================================================
Versión RSA de la firma interna (equivalente a Ejercicio-Hibrido-FirmaInterna.py).

Diferencias respecto a la versión ECIES:
  - Claves RSA en ficheros .pem  (no .txt hex)
  - Cifrado de clave Fernet: RSA OAEP  (no eciespy)
  - Firma: RSA PSS + SHA256  (no ECDSA eth_keys)
  - La firma NO necesita hashear manualmente: RSA lo hace internamente

Flujo (idéntico en lógica):
  Emisor:  firma(msg, priv_origen) + JSON{msg,firma} → Fernet.encrypt() → RSA.encrypt(clave_fernet)
  Receptor: RSA.decrypt() → Fernet.decrypt() → JSON → verificar firma(msg, pub_origen)
"""
import json
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import Fernet


# ==========================================
# 0. GESTIÓN DE CLAVES RSA (ficheros .pem)
# ==========================================
def generar_claves(nombre):
    print(f'Generando claves RSA para {nombre}...')
    priv = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return priv, priv.public_key()

def guardar_claves(priv, pub, nombre):
    print(f'Guardando claves de {nombre} en .pem...')
    with open(f"hibrido_rsa_interno_privada_{nombre}.pem", "wb") as f:
        f.write(priv.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        ))
    with open(f"hibrido_rsa_interno_publica_{nombre}.pem", "wb") as f:
        f.write(pub.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def cargar_claves(nombre):
    print(f'Cargando claves de {nombre} desde .pem...')
    with open(f"hibrido_rsa_interno_privada_{nombre}.pem", "rb") as f:
        priv = serialization.load_pem_private_key(f.read(), password=None)
    with open(f"hibrido_rsa_interno_publica_{nombre}.pem", "rb") as f:
        pub = serialization.load_pem_public_key(f.read())
    return priv, pub


# ==========================================
# 1. EMPAQUETADO: Mensaje + Firma RSA → Payload JSON
# ==========================================
def empaquetar_con_firma(mensaje, priv_origen):
    """
    Firma el mensaje con RSA PSS (SHA256) y serializa mensaje + firma en JSON bytes.
    RSA hashea el mensaje internamente: se pasa el mensaje en claro directamente a .sign().
    Este payload es lo que Fernet cifrará.
    """
    print('   -> Firmando mensaje (RSA PSS) y empaquetando en payload JSON...')
    firma_bytes = priv_origen.sign(
        mensaje,
        asym_padding.PSS(
            mgf=asym_padding.MGF1(hashes.SHA256()),
            salt_length=asym_padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    payload = {
        "mensaje": base64.b64encode(mensaje).decode(),
        "firma":   base64.b64encode(firma_bytes).decode()
    }
    return json.dumps(payload).encode()   # bytes listos para Fernet.encrypt()


def desempaquetar_y_verificar(payload_bytes, pub_emisor):
    """
    Extrae el mensaje y la firma del payload JSON.
    Verifica la firma RSA PSS con la clave pública del emisor.
    Retorna (mensaje: bytes, firma_valida: bool).
    RSA lanza InvalidSignature si falla: se captura y devuelve False.
    """
    print('   -> Desempaquetando payload y verificando firma interna (RSA PSS)...')
    payload     = json.loads(payload_bytes.decode())
    mensaje     = base64.b64decode(payload["mensaje"])
    firma_bytes = base64.b64decode(payload["firma"])

    try:
        pub_emisor.verify(
            firma_bytes,
            mensaje,
            asym_padding.PSS(
                mgf=asym_padding.MGF1(hashes.SHA256()),
                salt_length=asym_padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return mensaje, True
    except InvalidSignature:
        return mensaje, False


# ==========================================
# 2. CIFRADO HÍBRIDO (RSA cifra la clave Fernet)
# ==========================================
def cifrar_hibrido(mensaje, priv_origen, pub_destino):
    """
    1. Firma el mensaje con RSA privada del emisor.
    2. Empaqueta mensaje + firma en JSON (bytes).
    3. Cifra ese payload completo con Fernet.
    4. Cifra la clave Fernet con RSA pública del destino (OAEP).
    Retorna: (clave_fernet_cifrada, payload_cifrado)
    """
    print(' [Cifrado] Iniciando cifrado híbrido RSA con firma interna...')

    # Paso 1+2: mensaje → payload firmado (JSON bytes)
    payload = empaquetar_con_firma(mensaje, priv_origen)

    # Paso 3: cifrar payload completo con Fernet
    print('   -> Cifrando payload (mensaje+firma) con Fernet...')
    clave_fernet    = Fernet.generate_key()
    payload_cifrado = Fernet(clave_fernet).encrypt(payload)

    # Paso 4: cifrar clave Fernet con RSA OAEP (pública del destino)
    print('   -> Cifrando clave Fernet con RSA OAEP (pública del destino)...')
    clave_fernet_cifrada = pub_destino.encrypt(
        clave_fernet,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return clave_fernet_cifrada, payload_cifrado


def descifrar_hibrido(clave_fernet_cifrada, payload_cifrado, priv_destino, pub_emisor):
    """
    1. Recupera la clave Fernet con RSA privada del receptor (OAEP).
    2. Descifra el payload completo con Fernet.
    3. Extrae el mensaje y verifica la firma RSA desde el interior del payload.
    Retorna: (mensaje: bytes, firma_ok: bool)
    """
    print(' [Descifrado] Iniciando descifrado híbrido RSA con firma interna...')

    # Paso 1: recuperar clave Fernet con RSA privada
    print('   -> Recuperando clave Fernet con RSA OAEP (privada del receptor)...')
    clave_fernet = priv_destino.decrypt(
        clave_fernet_cifrada,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Paso 2: descifrar el payload
    print('   -> Descifrando payload completo con Fernet...')
    payload_bytes = Fernet(clave_fernet).decrypt(payload_cifrado)

    # Paso 3: extraer mensaje y verificar firma desde el interior del payload
    return desempaquetar_y_verificar(payload_bytes, pub_emisor)


# ==========================================
# 3. FLUJO MAESTRO
# ==========================================
def enviar_mensaje(origen, destino, priv_origen, pub_destino, mensaje):
    print(f'\n=================[ {origen} ENVIA A {destino} ]=================')
    print(f'Mensaje original: "{mensaje.decode()}"')
    clave_cifrada, payload_cifrado = cifrar_hibrido(mensaje, priv_origen, pub_destino)
    print('>> Paquete enviado: (clave_fernet_cifrada, payload_cifrado) <<')
    print('   NOTA: la firma RSA viaja dentro del payload, invisible desde fuera.')
    return clave_cifrada, payload_cifrado


def recibir_mensaje(origen, destino, priv_destino, pub_emisor, clave_cifrada, payload_cifrado):
    print(f'\n=================[ {destino} RECIBE DE {origen} ]=================')
    mensaje, firma_ok = descifrar_hibrido(clave_cifrada, payload_cifrado, priv_destino, pub_emisor)
    print(f'Mensaje recuperado: "{mensaje.decode()}"')
    if firma_ok:
        print('   Firma CORRECTA. El mensaje es autentico y no fue alterado.')
    else:
        print('   ERROR: La firma interna RSA no es valida.')


# ==========================================
# MAIN
# ==========================================
def main():
    print("=== PREPARACION ENTORNO (HIBRIDO RSA + FIRMA INTERNA) ===")
    for usuario in ['A', 'B', 'C']:
        priv, pub = generar_claves(usuario)
        guardar_claves(priv, pub, usuario)

    priv_a, pub_a = cargar_claves('A')
    priv_b, pub_b = cargar_claves('B')
    priv_c, pub_c = cargar_claves('C')

    # A -> B
    mensaje_AB = b"Informe confidencial de A para B. Firma RSA embebida en el cifrado."
    paquete_AB = enviar_mensaje('A', 'B', priv_a, pub_b, mensaje_AB)
    recibir_mensaje('A', 'B', priv_b, pub_a, *paquete_AB)

    # B -> C
    mensaje_BC = b"Revisado y aprobado por B. Reenviado a C con firma RSA interna."
    paquete_BC = enviar_mensaje('B', 'C', priv_b, pub_c, mensaje_BC)
    recibir_mensaje('B', 'C', priv_c, pub_b, *paquete_BC)


if __name__ == "__main__":
    main()



