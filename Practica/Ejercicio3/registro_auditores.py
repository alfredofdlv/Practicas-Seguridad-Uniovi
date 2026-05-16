"""
Dar de alta a un medico en el medico.txt
Nombre, un salt aleatorio (os.urandom(16)) y el hash de la contraseña derivado con PBKDF2HMAC (SHA256, 100000 iteraciones, 32 bytes)
usa , como separador

"""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64

def genera_salt(tamaño=16):
    return os.urandom(tamaño)

def hasheo_password(contraseña,salt):
    der_clave=PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    hash_bytes=der_clave.derive(contraseña.encode())

    return base64.b64encode(hash_bytes).decode()

def alta_usuario(nombre,contraseña):
    salt=genera_salt()  
    hash_contraseña=hasheo_password(contraseña, salt)

    with open(r'D:\clase\Practicas-Seguridad-Uniovi\Practica\Ejercicio3\auditores.txt', mode='rb') as f_read:
        for linea in f_read:
            if nombre in linea.decode(): 
                print(f"El usuario {nombre} ya existe")
                return
    with open(r'D:\clase\Practicas-Seguridad-Uniovi\Practica\Ejercicio3\auditores.txt', mode='ab') as f_write:
                f_write.write(f"{nombre},{base64.b64encode(salt).decode()},{hash_contraseña}\n".encode())
                print(f"El usuario {nombre} ha sido añadido con éxito")
                f_write.close()
                return

def main():
    usuario=input('Nombre de usuario: ')
    contraseña=input("Contraseña:  ")
    alta_usuario(usuario,contraseña)


if __name__=="__main__":
    main()