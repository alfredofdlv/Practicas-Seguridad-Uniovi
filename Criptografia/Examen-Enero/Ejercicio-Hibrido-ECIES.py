from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
from cryptography.fernet import Fernet
import hashlib
from eth_keys import keys 

# ==========================================
# 0. GESTION DE CLAVES (Igual que el asimetrico, formato TXT Hex)
# ==========================================
def generar_claves(nombre_usuario):
    priv_key = generate_eth_key()
    return priv_key.to_hex(), priv_key.public_key.to_hex()

def guardar_claves(priv_hex, pub_hex, nombre_usuario):
    with open(f"ecies_hibrido_{nombre_usuario}.txt", "w") as f:
        f.write(f"{priv_hex}\n{pub_hex}\n")

def cargar_claves(nombre_usuario):
    with open(f"ecies_hibrido_{nombre_usuario}.txt", "r") as f:
        lineas = f.read().splitlines()
        return lineas[0], lineas[1]

# ==========================================
# 1. FIRMA Y VERIFICACION (ECDSA)
# ==========================================
def firmar_mensaje(mensaje, priv_hex):
    mensaje_hash = hashlib.sha256(mensaje).digest()
    priv_key = keys.PrivateKey(bytes.fromhex(priv_hex.replace('0x', '')))
    return priv_key.sign_msg_hash(mensaje_hash).to_bytes()

def verificar_firma(mensaje, firma_bytes, pub_hex):
    mensaje_hash = hashlib.sha256(mensaje).digest()
    pub_key = keys.PublicKey(bytes.fromhex(pub_hex.replace('0x', '')))
    firma = keys.Signature(firma_bytes)
    if pub_key.verify_msg_hash(mensaje_hash, firma):
        print('   ✅ Firma CORRECTA.')
    else:
        print('   ❌ ERROR de firma.')


# ==========================================
# 2. CIFRADO HÍBRIDO (Fernet + ECIESpy)
# ==========================================
def cifrar_hibrido(mensaje, pub_hex_destino):
    print(' [Cifrado] Iniciando cifrado hibrido (Fernet + ECIES)...')
    
    # 1. Crear clave simetrica Fernet
    clave_fernet = Fernet.generate_key()
    
    # 2. Cifrar el mensaje pesado con Fernet (Simetrico)
    f = Fernet(clave_fernet)
    mensaje_cifrado_fernet = f.encrypt(mensaje)
    
    # 3. Cifrar la clave Fernet usando la publica ECC (Asimetrico con ECIESpy)
    print('   -> Cifrando clave Fernet con ECIES (Hex publico)...')
    clave_fernet_cifrada = encrypt(pub_hex_destino, clave_fernet)
    
    return clave_fernet_cifrada, mensaje_cifrado_fernet

def descifrar_hibrido(clave_fernet_cifrada, mensaje_cifrado_fernet, priv_hex_destino):
    print(' [Descifrado] Iniciando descifrado hibrido (Fernet + ECIES)...')
    
    # 1. Recuperar la clave Fernet usando la privada ECC de eciespy
    clave_fernet = decrypt(priv_hex_destino, clave_fernet_cifrada)
    
    # 2. Descifrar el mensaje con Fernet
    f = Fernet(clave_fernet)
    mensaje = f.decrypt(mensaje_cifrado_fernet)
    
    return mensaje


# ==========================================
# 3. FLUJO MAESTRO
# ==========================================
def enviar_mensaje(origen, destino, priv_origen_hex, pub_destino_hex, mensaje):
    print(f'\n=================[ {origen} ENVIA A {destino} ]=================')
    firma = firmar_mensaje(mensaje, priv_origen_hex)
    clave_f_cifrada, msg_f = cifrar_hibrido(mensaje, pub_destino_hex)
    return clave_f_cifrada, msg_f, firma

def recibir_mensaje(origen, destino, priv_destino_hex, pub_origen_hex, clave_f_cifrada, msg_f, firma):
    print(f'\n=================[ {destino} RECIBE DE {origen} ]=================')
    mensaje_recuperado = descifrar_hibrido(clave_f_cifrada, msg_f, priv_destino_hex)
    print(f'Mensaje recuperado: "{mensaje_recuperado.decode("utf-8")}"')
    verificar_firma(mensaje_recuperado, firma, pub_origen_hex)


def main():
    print("--- PREPARACION ENTORNO (HIBRIDO ECIES + FERNET) ---")
    for usuario in ['A', 'B', 'C']:
        priv, pub = generar_claves(usuario)
        guardar_claves(priv, pub, usuario)

    priv_a, pub_a = cargar_claves('A')
    priv_b, pub_b = cargar_claves('B')
    priv_c, pub_c = cargar_claves('C')

    # A -> B 
    mensaje_AB = b"Archivo masivo de 10GB encriptado Hibrido con ECIES."
    paquete_AB = enviar_mensaje('A', 'B', priv_a, pub_b, mensaje_AB)
    recibir_mensaje('A', 'B', priv_b, pub_a, *paquete_AB)

    # B -> C 
    mensaje_BC = b"Aprobado por B. Reenviado a C."
    paquete_BC = enviar_mensaje('B', 'C', priv_b, pub_c, mensaje_BC)
    recibir_mensaje('B', 'C', priv_c, pub_b, *paquete_BC)

if __name__ == "__main__":
    main()