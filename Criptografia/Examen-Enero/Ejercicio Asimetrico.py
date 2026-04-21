# Hay 3 empleados A,B,C los cuales tienen sus claves  de forma asimetrica . 
# Se necesitan: 
# Firmar cifrar, descifrar y verificar los mensajes  
# Orden de operaciones es el siguiente :

# A -> B
# B-> C

# No es necesario transitividad, 
# Si es necesario guardar las claves de forma local.

# Debe estar modularizado y con debidos prints

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature


def generar_claves(nombre_usuario):
    print(f'Generando claves para {nombre_usuario}....')
    priv_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    pub_key = priv_key.public_key()


    return priv_key, pub_key

def guardar_claves(priv_key, pub_key, nombre_usuario):
    print(f'Guardando claves de {nombre_usuario} de forma local...')
    
    with open(f"privada_{nombre_usuario}.pem", "wb") as f:
        f.write(priv_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(f"publica_{nombre_usuario}.pem", "wb") as f:
        f.write(pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def cargar_claves(nombre_usuario):
    print(f'Cargando claves de {nombre_usuario} desde almacenamiento local...')

    with open(f"privada_{nombre_usuario}.pem", "rb") as f:
        priv_key = serialization.load_pem_private_key(f.read(), password=None)
    
    with open(f"publica_{nombre_usuario}.pem", "rb") as f:
        pub_key = serialization.load_pem_public_key(f.read())
    
    return priv_key, pub_key

def firmar_mensaje(mensaje, priv_key):
    print('Firmando mensaje...')
    return priv_key.sign(
        mensaje,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), 
                    salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

def verificar_firma(mensaje, firma, pub_key):
    print('Verificando firma del remitente...')
    try:
        pub_key.verify(
            firma,
            mensaje,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), 
                        salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        print('Firma verificada con éxito. El mensaje es auténtico.')
        return True
    except InvalidSignature:
        print('Error: La firma NO es válida o el mensaje fue alterado.')
        return False

def cifrar_mensaje(mensaje, pub_key):
    print('Cifrando mensaje para que solo el destino pueda leerlo...')
    return pub_key.encrypt(
        mensaje,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

def descifrar_mensaje(mensaje_cifrado, priv_key):
    print('Descifrando mensaje recibido...')
    return priv_key.decrypt(
        mensaje_cifrado,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), 
                     algorithm=hashes.SHA256(), label=None)
    )

def flujo_comunicacion(origen, destino, priv_origen, pub_destino, mensaje):
    print(f'\n--- Iniciando operacion {origen} -> {destino} ---')
    print(f'Mensaje original : {mensaje}')
    
    # 1. Origen firma el mensaje 
    firma = firmar_mensaje(mensaje, priv_origen)
    
    # 2. Origen cifra el mensaje con la clave pública del destino
    mensaje_cifrado = cifrar_mensaje(mensaje, pub_destino)
    
    print('....'*10)
    print(f'Mensaje cifrado y firma viajando por la red hacia {destino}....')
    print('....'*10)
    
    return mensaje_cifrado, firma

def recepcion_comunicacion(origen, destino, priv_destino, pub_origen, mensaje_cifrado, firma):
    print(f'\n--- {destino} procesando datos recibidos de {origen} ---')
    
    # 1. Destino descifra el mensaje con su clave privada
    mensaje_descifrado = descifrar_mensaje(mensaje_cifrado, priv_destino)
    print(f'Mensaje descifrado resultante: {mensaje_descifrado}')
    
    # 2. Destino verifica la firma usando la clave pública del origen y el mensaje que acaba de descifrar
    verificar_firma(mensaje_descifrado, firma, pub_origen)


def main(): 
    # 1. Generar y guardar claves locales para A, B y C
    for usuario in ['A', 'B', 'C']:
        priv, pub = generar_claves(usuario)
        guardar_claves(priv, pub, usuario)

    # 2. Cargar las claves guardadas para hacer el procedimiento
    priv_a, pub_a = cargar_claves('A')
    priv_b, pub_b = cargar_claves('B')
    priv_c, pub_c = cargar_claves('C')

    # A -> B ---------------------------------------
    mensaje_AB = b"Hola B, soy A."
    # A envia y B recibe
    msg_cifrado_AB, firma_AB = flujo_comunicacion('A', 'B', priv_a, pub_b, mensaje_AB)
    recepcion_comunicacion('A', 'B', priv_b, pub_a, msg_cifrado_AB, firma_AB)

    # B -> C ---------------------------------------
    mensaje_BC = b"Hola C, Soy B "
    # B envia y C recibe
    msg_cifrado_BC, firma_BC = flujo_comunicacion('B', 'C', priv_b, pub_c, mensaje_BC)
    recepcion_comunicacion('B', 'C', priv_c, pub_b, msg_cifrado_BC, firma_BC)


if __name__=="__main__":
    main()