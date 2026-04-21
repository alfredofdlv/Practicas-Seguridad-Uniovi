import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.exceptions import InvalidSignature

# ==========================================
# 1. GESTION DE CLAVES ASIMETRICAS (RSA)
# ==========================================

def generar_claves(nombre_usuario):
    """Genera un par de claves RSA para un usuario."""
    print(f'Generando claves asimetricas RSA para {nombre_usuario}....')
    priv_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    pub_key = priv_key.public_key()
    return priv_key, pub_key

def guardar_claves(priv_key, pub_key, nombre_usuario):
    """Guarda las claves en disco en formato PEM."""
    print(f'Guardando claves de {nombre_usuario} en archivos .pem locales...')
    with open(f"hibrido_privada_{nombre_usuario}.pem", "wb") as f:
        f.write(priv_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    with open(f"hibrido_publica_{nombre_usuario}.pem", "wb") as f:
        f.write(pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def cargar_claves(nombre_usuario):
    """Lee las claves RSA desde los .pem."""
    print(f'Cargando claves de {nombre_usuario} desde disco...')
    with open(f"hibrido_privada_{nombre_usuario}.pem", "rb") as f:
        priv_key = serialization.load_pem_private_key(f.read(), password=None)
    with open(f"hibrido_publica_{nombre_usuario}.pem", "rb") as f:
        pub_key = serialization.load_pem_public_key(f.read())
    return priv_key, pub_key


# ==========================================
# 2. FIRMA Y VERIFICACION (RSA)
# ==========================================

def firmar_mensaje(mensaje, priv_key):
    """Firma el mensaje original usando la clave privada del emisor (RSA)."""
    print(' [Firma] Firmando el mensaje original (RSA)...')
    return priv_key.sign(
        mensaje,
        asym_padding.PSS(mgf=asym_padding.MGF1(hashes.SHA256()), salt_length=asym_padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

def verificar_firma(mensaje, firma, pub_key):
    """Verifica que la firma coincida con el mensaje (RSA)."""
    print(' [Firma] Verificando la firma del remitente (RSA)...')
    try:
        pub_key.verify(
            firma,
            mensaje,
            asym_padding.PSS(mgf=asym_padding.MGF1(hashes.SHA256()), salt_length=asym_padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        print(' Firma CORRECTA. El mensaje es verdaderamente del origen.')
        return True
    except InvalidSignature:
        print('  ERROR: La firma no coincide. Mensaje alterado o remitente falso.')
        return False


# ==========================================
# 3. CIFRADO Y DESCIFRADO HÍBRIDO (AES + RSA)
# ==========================================

def cifrar_hibrido(mensaje, pub_key_destino):
    
    """
    Cifra un mensaje de forma hibrida:
    1. Genera una clave simetrica de un solo uso (AES).
    2. Cifra el mensaje con AES (muy rapido, sin limites de tamano).
    3. Cifra la clave AES usando la publica RSA del destino.
    """
    print(' [Cifrado] Iniciando cifrado hibrido...')
    
    # 1. Crear clave simetrica y vector de inicializacion (IV)
    clave_aes = os.urandom(32) # AES-256
    iv = os.urandom(16)        # IV de 16 bytes para AES-CBC
    
    # 2. Cifrar el mensaje con AES (Simétrico)
    print('   -> Cifrando el mensaje con AES-256-CBC...')
    padder = sym_padding.PKCS7(128).padder() # AES bloque es 128 bits
    mensaje_padded = padder.update(mensaje) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(clave_aes), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    mensaje_cifrado_aes = encryptor.update(mensaje_padded) + encryptor.finalize()
    
    # 3. Cifrar la clave AES con RSA (Asimétrico)
    print('   -> Cifrando la clave AES con la publica RSA del destino...')
    clave_aes_cifrada_rsa = pub_key_destino.encrypt(
        clave_aes,
        asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    
    # Retornamos el paquete con todo lo necesario para descifrar: 
    # la clave AES cifrada, el IV (no pasa nada si viaja en claro) y el mensaje cifrado
    return clave_aes_cifrada_rsa, iv, mensaje_cifrado_aes

def descifrar_hibrido(clave_aes_cifrada_rsa, iv, mensaje_cifrado_aes, priv_key_destino):
    """
    Descifra un mensaje híbrido:
    1. Descifra la clave AES usando la clave privada RSA.
    2. Descifra el mensaje con AES usando la clave recuperada.
    """
    print(' [Descifrado] Iniciando descifrado hibrido...')
    
    # 1. Recuperar la clave AES usando RSA privada
    print('   -> Recuperando clave AES usando RSA privada...')
    clave_aes = priv_key_destino.decrypt(
        clave_aes_cifrada_rsa,
        asym_padding.OAEP(mgf=asym_padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    
    # 2. Descifrar el mensaje con AES
    print('   -> Descifrando el mensaje con AES-256-CBC...')
    cipher = Cipher(algorithms.AES(clave_aes), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    mensaje_padded = decryptor.update(mensaje_cifrado_aes) + decryptor.finalize()
    
    # Quitar el padding
    unpadder = sym_padding.PKCS7(128).unpadder()
    mensaje = unpadder.update(mensaje_padded) + unpadder.finalize()
    
    return mensaje


# ==========================================
# 4. FLUJO DE COMUNICACIÓN MAESTRO
# ==========================================

def enviar_mensaje(origen, destino, priv_origen, pub_destino, mensaje):
    print(f'\n=================[ {origen} ENVIA A {destino} ]=================')
    print(f'Mensaje en claro: "{mensaje.decode("utf-8")}"')
    
    # 1. Origen firma el mensaje en claro para demostrar autoria
    firma = firmar_mensaje(mensaje, priv_origen)
    
    # 2. Origen empaqueta todo cifrandolo de forma hibrida
    # Nota: para este ejercicio, enviare la firma a parte del texto cifrado,
    # aunque en hibrido puro podriamos concatenar [mensaje + firma] y cifrarlo con AES!
    # Lo dejamos separado para ver claramente la verificacion vs descifrado.
    clave_aes_rsa, iv, msg_aes = cifrar_hibrido(mensaje, pub_destino)
    
    print('>> Enviando paquete de datos por la red... <<')
    return clave_aes_rsa, iv, msg_aes, firma

def recibir_mensaje(origen, destino, priv_destino, pub_origen, clave_aes_rsa, iv, msg_aes, firma):
    print(f'\n=================[ {destino} RECIBE DE {origen} ]=================')
    
    # 1. El destino abre el "candado hibrido" para obtener el mensaje en claro
    mensaje_recuperado = descifrar_hibrido(clave_aes_rsa, iv, msg_aes, priv_destino)
    print(f'Mensaje recuperado: "{mensaje_recuperado.decode("utf-8")}"')
    
    # 2. Verifica que realmente fue el origen quien lo envio
    verificar_firma(mensaje_recuperado, firma, pub_origen)


# ==========================================
# MAIN
# ==========================================
def main():
    print("--- PREPARACION DEL ENTORNO ---")
    # Generar y guardar claves para todos los empleados de la empresa
    for usuario in ['A', 'B', 'C']:
        priv, pub = generar_claves(usuario)
        guardar_claves(priv, pub, usuario)

    # Cargar las claves guardadas para garantizar que usamos los ficheros locales
    priv_a, pub_a = cargar_claves('A')
    priv_b, pub_b = cargar_claves('B')
    priv_c, pub_c = cargar_claves('C')

    # --- COMUNICACION 1: A -> B ---
    mensaje_AB = b"Archivo financiero gigante de 10GB (Simulado). Saludos A."
    
    # A procesa y envia
    paquete_AB = enviar_mensaje('A', 'B', priv_a, pub_b, mensaje_AB)
    # B recibe y procesa
    recibir_mensaje('A', 'B', priv_b, pub_a, *paquete_AB)

    # --- COMUNICACION 2: B -> C ---
    mensaje_BC = b"He revisado el documento de A, todo aprobado. Te lo paso, C."
    
    # B procesa y envia
    paquete_BC = enviar_mensaje('B', 'C', priv_b, pub_c, mensaje_BC)
    # C recibe y procesa
    recibir_mensaje('B', 'C', priv_c, pub_b, *paquete_BC)

if __name__ == "__main__":
    main()
