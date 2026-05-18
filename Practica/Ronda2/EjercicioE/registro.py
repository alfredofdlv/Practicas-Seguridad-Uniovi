"""
Registro de medicos y cifrado del fichero de credenciales.
Escribe medicos.txt en claro y genera medicos.txt.enc con Fernet + clave maestra (PBKDF2).
"""

from pathlib import Path
import os
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

BASE_DIR = Path(__file__).resolve().parent
MEDICOS_TXT = BASE_DIR / "medicos.txt"
MEDICOS_ENC = BASE_DIR / "medicos.txt.enc"

# Salt fijo para derivar la clave maestra de la contrasena admin (reproducible en examen)
ADMIN_SALT = b"hospital_admin_salt_v1"
ITERACIONES = 100_000


def derivar_clave_maestra(contrasena_admin: str) -> bytes:
    """PBKDF2 -> 32 bytes -> clave Fernet (url-safe base64)."""
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
    """Cifra todo medicos.txt y guarda medicos.txt.enc."""
    if not MEDICOS_TXT.exists():
        print("No hay medicos.txt para cifrar.")
        return
    contenido = MEDICOS_TXT.read_bytes()
    clave = derivar_clave_maestra(contrasena_admin)
    token = Fernet(clave).encrypt(contenido)
    MEDICOS_ENC.write_bytes(token)
    MEDICOS_TXT.unlink()
    print(f"Fichero cifrado guardado en {MEDICOS_ENC.name}")


def descifrar_fichero_medicos(contrasena_admin: str) -> str:
    """Descifra medicos.txt.enc y devuelve el contenido en texto."""
    if not MEDICOS_ENC.exists():
        if MEDICOS_TXT.exists():
            return MEDICOS_TXT.read_text(encoding="utf-8")
        return ""
    clave = derivar_clave_maestra(contrasena_admin)
    contenido = Fernet(clave).decrypt(MEDICOS_ENC.read_bytes())
    return contenido.decode("utf-8")


def _contenido_actual(contrasena_admin: str) -> str:
    if MEDICOS_TXT.exists():
        return MEDICOS_TXT.read_text(encoding="utf-8")
    if MEDICOS_ENC.exists():
        return descifrar_fichero_medicos(contrasena_admin)
    return ""


def alta_usuario(nombre: str, contrasena: str, contrasena_admin: str) -> None:
    """Alta en medicos.txt y vuelve a cifrar el fichero completo."""
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

    MEDICOS_TXT.write_text(texto + nueva_linea, encoding="utf-8")
    print(f"El usuario {nombre} ha sido anadido con exito")
    cifrar_fichero_medicos(contrasena_admin)
