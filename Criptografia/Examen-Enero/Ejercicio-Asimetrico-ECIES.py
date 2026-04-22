import hashlib
from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
from eth_keys import keys # eciespy usa esto por debajo para las claves
from eth_keys.exceptions import ValidationError

# ==========================================
# 1. GESTIÓN DE CLAVES (Formato TXT / HEX)
# ==========================================

def generar_claves(nombre_usuario):
    """
    Genera claves de Curva Elíptica (secp256k1) usando eciespy.
    Retorna strings en hexadecimal en lugar de bytes complejos.
    """
    print(f'Generando claves ECC para {nombre_usuario}....')
    priv_key = generate_eth_key()
    
    # Convertimos a formato hexadecimal (string plano)
    priv_hex = priv_key.to_hex()
    pub_hex = priv_key.public_key.to_hex()
    
    return priv_hex, pub_hex

def guardar_claves(priv_hex, pub_hex, nombre_usuario):
    """Guarda las claves en un .txt normal como cadenas Hexadecimales (Sin PEM)."""
    print(f'Guardando claves de {nombre_usuario} en archivos txt (Hexadecimales)...')
    with open(f"ecies_claves_{nombre_usuario}.txt", "w") as f:
        f.write(f"{priv_hex}\n")
        f.write(f"{pub_hex}\n")

def cargar_claves(nombre_usuario):
    """Lee las cadenas Hexadecimales desde el .txt"""
    print(f'Cargando claves de {nombre_usuario} desde disco...')
    with open(f"ecies_claves_{nombre_usuario}.txt", "r") as f:
        lineas = f.read().splitlines()
        priv_hex = lineas[0]
        pub_hex = lineas[1]
    return priv_hex, pub_hex


# ==========================================
# 2. FIRMA Y VERIFICACIÓN (ECDSA sobre secp256k1)
# ==========================================
def firmar_mensaje(mensaje, priv_hex):
    """
    Firma usando la clave privada. eciespy usa eth_keys por debajo.
    La firma requiere que firmemos un hash de 32 bytes del mensaje.
    """
    print(' [Firma] Firmando el mensaje (ECDSA)...')
    # 1. Hashear el mensaje (Sha256) a 32 bytes exactos
    mensaje_hash = hashlib.sha256(mensaje).digest()
    
    # 2. Reconstruir la clave privada desde el hex
    priv_key = keys.PrivateKey(bytes.fromhex(priv_hex.replace('0x', '')))
    
    # 3. Firmar el hash
    firma = priv_key.sign_msg_hash(mensaje_hash)
    return firma.to_bytes() # Retorna los bytes de la firma

def verificar_firma(mensaje, firma_bytes, pub_hex):
    """Verifica que la firma corresponda al mensaje y a la clave pública."""
    print(' [Firma] Verificando la firma del remitente (ECDSA)...')
    mensaje_hash = hashlib.sha256(mensaje).digest()
    
    pub_key = keys.PublicKey(bytes.fromhex(pub_hex.replace('0x', '')))
    firma = keys.Signature(firma_bytes)
    
    try:
        es_valida = pub_key.verify_msg_hash(mensaje_hash, firma)
        if es_valida:
            print('   ✅ Firma CORRECTA. El mensaje es auténtico.')
            return True
        else:
            raise ValidationError("Firma invalida")
    except Exception:
        print('   ❌ ERROR: La firma no coincide.')
        return False


# ==========================================
# 3. CIFRADO Y DESCIFRADO ASIMÉTRICO (ECIES)
# ==========================================
def cifrar_mensaje(mensaje, pub_hex):
    """Cifra el mensaje usando eciespy directamente con el Hex de la pública."""
    print(' [Cifrado] Cifrando mensaje con ECIES...')
    return encrypt(pub_hex, mensaje)

def descifrar_mensaje(mensaje_cifrado, priv_hex):
    """Descifra el mensaje usando eciespy con el Hex de la privada."""
    print(' [Descifrado] Descifrando mensaje con ECIES...')
    return decrypt(priv_hex, mensaje_cifrado)


# ==========================================
# 4. FLUJO DE COMUNICACIÓN MAESTRO
# ==========================================
def flujo_comunicacion(origen, destino, priv_origen_hex, pub_destino_hex, mensaje):
    print(f'\n--- Iniciando operacion {origen} -> {destino} ---')
    print(f'Mensaje original: "{mensaje.decode("utf-8")}"')
    
    firma = firmar_mensaje(mensaje, priv_origen_hex)
    mensaje_cifrado = cifrar_mensaje(mensaje, pub_destino_hex)
    
    print('>> Enviando paquete por la red... <<')
    return mensaje_cifrado, firma

def recepcion_comunicacion(origen, destino, priv_destino_hex, pub_origen_hex, mensaje_cifrado, firma):
    print(f'\n--- {destino} procesando datos recibidos de {origen} ---')
    
    mensaje_descifrado = descifrar_mensaje(mensaje_cifrado, priv_destino_hex)
    print(f'Mensaje descifrado resultante: "{mensaje_descifrado.decode("utf-8")}"')
    
    verificar_firma(mensaje_descifrado, firma, pub_origen_hex)


# ==========================================
# MAIN
# ==========================================
def main():
    print("--- PREPARACION DEL ENTORNO (ASIMÉTRICO ECIESPY) ---")
    
    for usuario in ['A', 'B', 'C']:
        priv, pub = generar_claves(usuario)
        guardar_claves(priv, pub, usuario)

    priv_a, pub_a = cargar_claves('A')
    priv_b, pub_b = cargar_claves('B')
    priv_c, pub_c = cargar_claves('C')

    # A -> B 
    mensaje_AB = b"Mensaje confidencial de A para B usando ECIES."
    msg_cifrado_AB, firma_AB = flujo_comunicacion('A', 'B', priv_a, pub_b, mensaje_AB)
    recepcion_comunicacion('A', 'B', priv_b, pub_a, msg_cifrado_AB, firma_AB)

    # B -> C 
    mensaje_BC = b"B confirma y reenvia la informacion a C."
    msg_cifrado_BC, firma_BC = flujo_comunicacion('B', 'C', priv_b, pub_c, mensaje_BC)
    recepcion_comunicacion('B', 'C', priv_c, pub_b, msg_cifrado_BC, firma_BC)

if __name__ == "__main__":
    main()