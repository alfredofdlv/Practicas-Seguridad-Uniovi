from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Generar clave privado
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
#Generar publica desde la privada 
public_key = private_key.public_key()
#Creamos texto a cifrar
mensaje_cifrar = b'Mensaje a cifrar'

#Encriptar
texto_encriptado= public_key.encrypt(
    mensaje_cifrar,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None)
        )
print(mensaje_cifrar)
texto_encriptado

mensaje_firmar=b"Mensaje a firmar"
firma= private_key.sign(
    mensaje_firmar,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),      #funcion de la generación de la mascara 
        salt_length=padding.PSS.MAX_LENGTH      #tamaño del salt a utilizar 
    ),
    hashes.SHA256()
)
print(firma)

#Desencriptar
mensaje_descifrado= private_key.decrypt(
    texto_encriptado,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None)
        )

#Verificación 
if mensaje_cifrar==mensaje_descifrado:
    print('VERIFICACIÓN')
else:
    print('NO VERIFICACIÓN')
print(mensaje_descifrado)   