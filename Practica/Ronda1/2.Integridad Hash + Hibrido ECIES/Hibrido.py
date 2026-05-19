"""
EJERCICIO - HÍBRIDO ECIES + FERNET CON FIRMA INTERNA
=====================================================
Variante donde la firma digital se empaqueta DENTRO del cifrado Fernet.

Diferencia con la versión estándar:
  - Versión estándar:  envia (clave_cifrada, msg_cifrado, firma)  <- firma viaja en claro
  - Esta versión:      envia (clave_cifrada, payload_cifrado)     <- firma va DENTRO del payload Fernet

Ventaja: la firma queda protegida por el cifrado simétrico.
Nadie puede saber quién firmó ni leer la firma sin la clave privada ECIES del receptor.

Serialización: mensaje + firma → JSON (base64) → bytes → Fernet.encrypt()
"""
import json
import base64
import hashlib
from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
from cryptography.fernet import Fernet
from eth_keys import keys


# ==========================================
# 0. GESTIÓN DE CLAVES (igual que ECIES estándar)
# ==========================================
def generar_claves(nombre):
    priv = generate_eth_key()
    return priv.to_hex(), priv.public_key.to_hex()

def guardar_claves(priv_hex, pub_hex, nombre):
    with open(f"hibrido_interno_{nombre}.txt", "w") as f:
        f.write(f"{priv_hex}\n{pub_hex}\n")

def cargar_claves(nombre):
    with open(f"hibrido_interno_{nombre}.txt", "r") as f:
        lineas = f.read().splitlines()
    return lineas[0], lineas[1]


# ==========================================
# 1. EMPAQUETADO: Mensaje + Firma → Payload JSON
# ==========================================
def empaquetar_con_firma(mensaje, priv_hex):
    """
    Firma el mensaje (ECDSA) y serializa mensaje + firma en un JSON codificado en bytes.
    Este payload es lo que Fernet cifrará, ocultando también la firma.
    """
    print('   -> Firmando mensaje y empaquetando en payload JSON...')
    msg_hash    = hashlib.sha256(mensaje).digest()
    priv_obj    = keys.PrivateKey(bytes.fromhex(priv_hex.replace('0x', '')))
    firma_bytes = priv_obj.sign_msg_hash(msg_hash).to_bytes()

    payload = {
        "mensaje": base64.b64encode(mensaje).decode(),
        "firma":   base64.b64encode(firma_bytes).decode()
    }
    return json.dumps(payload).encode()   # bytes listos para Fernet.encrypt()


def desempaquetar_y_verificar(payload_bytes, pub_hex_emisor):
    """
    Extrae el mensaje y la firma del payload JSON.
    Verifica la firma con la clave pública del emisor.
    Retorna (mensaje: bytes, firma_valida: bool).
    """
    print('   -> Desempaquetando payload y verificando firma interna (ECDSA)...')
    payload     = json.loads(payload_bytes.decode())
    mensaje     = base64.b64decode(payload["mensaje"])
    firma_bytes = base64.b64decode(payload["firma"])

    msg_hash  = hashlib.sha256(mensaje).digest()
    pub_obj   = keys.PublicKey(bytes.fromhex(pub_hex_emisor.replace('0x', '')))
    firma_obj = keys.Signature(firma_bytes)

    es_valida = pub_obj.verify_msg_hash(msg_hash, firma_obj)
    return mensaje, es_valida


# ==========================================
# 2. CIFRADO HÍBRIDO (Fernet cifra el payload completo)
# ==========================================
def cifrar_hibrido(mensaje, priv_hex_origen, pub_hex_destino):
    """
    Flujo completo de cifrado:
    1. Firma el mensaje con la privada del emisor.
    2. Empaqueta mensaje + firma en un JSON (bytes).
    3. Cifra ese payload completo con Fernet (nadie ve la firma sin descifrar).
    4. Cifra la clave Fernet con la pública ECIES del destino.
    Retorna: (clave_fernet_cifrada, payload_cifrado)  <- solo 2 elementos
    """
    print(' [Cifrado] Iniciando cifrado híbrido con firma interna...')

    # Paso 1+2: mensaje → payload firmado (JSON bytes)
    payload = empaquetar_con_firma(mensaje, priv_hex_origen)

    # Paso 3: cifrar payload completo con Fernet
    print('   -> Cifrando payload (mensaje+firma) con Fernet...')
    clave_fernet    = Fernet.generate_key()
    payload_cifrado = Fernet(clave_fernet).encrypt(payload)

    # Paso 4: cifrar clave Fernet con ECIES pública del destino
    print('   -> Cifrando clave Fernet con ECIES (pública del destino)...')
    clave_fernet_cifrada = encrypt(pub_hex_destino, clave_fernet)

    return clave_fernet_cifrada, payload_cifrado


def descifrar_hibrido(clave_fernet_cifrada, payload_cifrado, priv_hex_destino, pub_hex_emisor):
    """
    Flujo completo de descifrado:
    1. Recupera la clave Fernet con la privada ECIES del receptor.
    2. Descifra el payload completo con Fernet.
    3. Extrae el mensaje y verifica la firma (todo dentro del payload).
    Retorna: (mensaje: bytes, firma_ok: bool)
    """
    print(' [Descifrado] Iniciando descifrado híbrido con firma interna...')

    # Paso 1: recuperar clave Fernet
    print('   -> Recuperando clave Fernet con ECIES (privada del receptor)...')
    clave_fernet = decrypt(priv_hex_destino, clave_fernet_cifrada)

    # Paso 2: descifrar el payload
    print('   -> Descifrando payload completo con Fernet...')
    payload_bytes = Fernet(clave_fernet).decrypt(payload_cifrado)

    # Paso 3: extraer mensaje y verificar firma desde el interior del payload
    return desempaquetar_y_verificar(payload_bytes, pub_hex_emisor)


# ==========================================
# 3. FLUJO MAESTRO
# ==========================================
def enviar_mensaje(origen, destino, priv_origen_hex, pub_destino_hex, mensaje):
    print(f'\n=================[ {origen} ENVIA A {destino} ]=================')
    print(f'Mensaje original: "{mensaje.decode()}"')
    clave_cifrada, payload_cifrado = cifrar_hibrido(mensaje, priv_origen_hex, pub_destino_hex)
    print('>> Paquete enviado: (clave_fernet_cifrada, payload_cifrado) <<')
    print('   NOTA: la firma viaja dentro del payload, invisible desde fuera.')
    return clave_cifrada, payload_cifrado


def recibir_mensaje(origen, destino, priv_destino_hex, pub_origen_hex, clave_cifrada, payload_cifrado):
    print(f'\n=================[ {destino} RECIBE DE {origen} ]=================')
    mensaje, firma_ok = descifrar_hibrido(clave_cifrada, payload_cifrado, priv_destino_hex, pub_origen_hex)
    print(f'Mensaje recuperado: "{mensaje.decode()}"')
    if firma_ok:
        print('   Firma CORRECTA. El mensaje es autentico y no fue alterado.')
    else:
        print('   ERROR: La firma interna no es valida.')


# ==========================================
# MAIN
# ==========================================
def main():
    print("=== PREPARACION ENTORNO (HIBRIDO ECIES + FIRMA INTERNA) ===")
    for usuario in ['A', 'B', 'C']:
        priv, pub = generar_claves(usuario)
        guardar_claves(priv, pub, usuario)

    priv_a, pub_a = cargar_claves('A')
    priv_b, pub_b = cargar_claves('B')
    priv_c, pub_c = cargar_claves('C')

    # A -> B
    mensaje_AB = b"Informe confidencial de A para B. Firma embebida en el cifrado."
    paquete_AB = enviar_mensaje('A', 'B', priv_a, pub_b, mensaje_AB)
    recibir_mensaje('A', 'B', priv_b, pub_a, *paquete_AB)

    # B -> C
    mensaje_BC = b"Revisado y aprobado por B. Reenviado a C con firma interna."
    paquete_BC = enviar_mensaje('B', 'C', priv_b, pub_c, mensaje_BC)
    recibir_mensaje('B', 'C', priv_c, pub_b, *paquete_BC)


if __name__ == "__main__":
    main()
