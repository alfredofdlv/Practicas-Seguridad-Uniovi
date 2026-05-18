from registro import hasheo_password
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

"""
Dado un nombre y contraseña, lee medicos.txt, recupera el salt (decodificado desde base64) 
Verifica la contraseña usando PBKDF2HMAC.verify(). 
Imprime si la autenticación fue correcta, contraseña incorrecta, o usuario no encontrado

"""

def verifica_password(contraseña_plano,salt,hash_almacenado):
    der_clave=PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    try: 
        der_clave.verify(contraseña_plano.encode(), base64.b64decode(hash_almacenado))
        return True
    except Exception as e:
        print(f"Error al verificar la contraseña: {e}")
        return False
def autentica_usuario(usuario,contraseña):
    try:
        with open(r"D:\clase\Practicas-Seguridad-Uniovi\Practica\Ejercicio1\medico.txt", mode="r") as f:
            for linea in f:
                datos=linea.strip().split(",")
                # print(f.read())
                # print(datos)
                if len(datos) == 3:
                    nombre_almacenado, salt_almacenado, hash_almacenado = datos
                    if nombre_almacenado == usuario:
                        salt = base64.b64decode(salt_almacenado)
                        if verifica_password(contraseña, salt, hash_almacenado):
                            print(f"El usuario {usuario} ha sido autenticado con éxito")
                            return True
                        print(f"Contraseña incorrecta para el usuario {usuario}")
                        return False
            print(f"Usuario {usuario} no encontrado")
            return False

    except Exception as e:
        print(f"Error al autenticar el usuario: {e}")
        return False