"""
Autenticacion contra medicos.txt.enc: descifra con clave maestra, verifica PBKDF2,
genera token de sesion si la contrasena es correcta.
"""

import base64
import hashlib
import os
import time

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from registro import descifrar_fichero_medicos, ITERACIONES


def verifica_password(contrasena_plano: str, salt: bytes, hash_almacenado: str) -> bool:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=ITERACIONES,
        backend=default_backend(),
    )
    try:
        kdf.verify(contrasena_plano.encode(), base64.b64decode(hash_almacenado))
        return True
    except Exception:
        return False


def generar_token_sesion(usuario: str) -> str:
    salt_sesion = os.urandom(16).hex()
    timestamp = str(int(time.time()))
    token = hashlib.sha256(f"{usuario}:{timestamp}:{salt_sesion}".encode()).hexdigest()
    return token


def autentica_usuario(usuario: str, contrasena: str, contrasena_admin: str) -> tuple[bool, str | None]:
    """
    Descifra el fichero de medicos, busca al usuario y verifica la contrasena.
    Retorna (exito, token_sesion_hex) o (False, None).
    """
    try:
        contenido = descifrar_fichero_medicos(contrasena_admin)
    except Exception as e:
        print(f"Error al descifrar fichero de medicos: {e}")
        return False, None

    for linea in contenido.splitlines():
        datos = linea.strip().split(",")
        if len(datos) != 3:
            continue
        nombre_almacenado, salt_almacenado, hash_almacenado = datos
        if nombre_almacenado != usuario:
            continue
        salt = base64.b64decode(salt_almacenado)
        if verifica_password(contrasena, salt, hash_almacenado):
            token = generar_token_sesion(usuario)
            print(f"El usuario {usuario} ha sido autenticado con exito")
            print(f"Token de sesion: {token[:16]}...")
            return True, token
        print(f"Contrasena incorrecta para el usuario {usuario}")
        return False, None

    print(f"Usuario {usuario} no encontrado")
    return False, None
