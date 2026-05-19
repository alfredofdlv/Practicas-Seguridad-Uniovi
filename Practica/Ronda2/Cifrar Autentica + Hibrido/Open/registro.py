"""
Registro de medicos y cifrado del fichero de credenciales (with open + os.path).
Version equivalente a ../EjercicioE/registro.py
"""

import os
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDICOS_TXT = os.path.join(BASE_DIR, "medicos.txt")
MEDICOS_ENC = os.path.join(BASE_DIR, "medicos.txt.enc")

ADMIN_SALT = b"hospital_admin_salt_v1"
ITERACIONES = 100_000


def derivar_clave_maestra(contrasena_admin: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=ADMIN_SALT,
        iterations=ITERACIONES,
        backend=default_backend(),
    )
    return base64.urlsafe_b64encode(kdf.derive(contrasena_admin.encode()))


def genera_salt(tamano: int = 16) -> bytes:
    return os.urandom(tamano)


def hasheo_password(contrasena: str, salt: bytes) -> str:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERACIONES,
        backend=default_backend(),
    )
    return base64.b64encode(kdf.derive(contrasena.encode())).decode()


def cifrar_fichero_medicos(contrasena_admin: str) -> None:
    if not os.path.exists(MEDICOS_TXT):
        print("No hay medicos.txt para cifrar.")
        return

    with open(MEDICOS_TXT, mode="rb") as f_read:
        contenido = f_read.read()

    clave = derivar_clave_maestra(contrasena_admin)
    token = Fernet(clave).encrypt(contenido)

    with open(MEDICOS_ENC, mode="wb") as f_write:
        f_write.write(token)

    os.remove(MEDICOS_TXT)
    print("Fichero cifrado guardado en medicos.txt.enc")


def descifrar_fichero_medicos(contrasena_admin: str) -> str:
    if not os.path.exists(MEDICOS_ENC):
        if os.path.exists(MEDICOS_TXT):
            with open(MEDICOS_TXT, mode="r", encoding="utf-8") as f:
                return f.read()
        return ""

    with open(MEDICOS_ENC, mode="rb") as f_read:
        datos_cifrados = f_read.read()

    clave = derivar_clave_maestra(contrasena_admin)
    contenido = Fernet(clave).decrypt(datos_cifrados)
    return contenido.decode("utf-8")


def _contenido_actual(contrasena_admin: str) -> str:
    if os.path.exists(MEDICOS_TXT):
        with open(MEDICOS_TXT, mode="r", encoding="utf-8") as f:
            return f.read()
    if os.path.exists(MEDICOS_ENC):
        return descifrar_fichero_medicos(contrasena_admin)
    return ""


def alta_usuario(nombre: str, contrasena: str, contrasena_admin: str) -> None:
    texto = _contenido_actual(contrasena_admin)

    for linea in texto.splitlines():
        if not linea.strip():
            continue
        if linea.split(",")[0] == nombre:
            print(f"El usuario {nombre} ya existe")
            return

    salt = genera_salt()
    hash_contrasena = hasheo_password(contrasena, salt)
    nueva_linea = f"{nombre},{base64.b64encode(salt).decode()},{hash_contrasena}\n"

    with open(MEDICOS_TXT, mode="w", encoding="utf-8") as f_write:
        f_write.write(texto + nueva_linea)

    print(f"El usuario {nombre} ha sido anadido con exito")
    cifrar_fichero_medicos(contrasena_admin)
