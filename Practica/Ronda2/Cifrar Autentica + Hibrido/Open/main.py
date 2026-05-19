"""
Ejercicio E — version with open() en directorio propio (EjercicioE_open).
Equivalente a ../EjercicioE/main.py
"""

import os

import registro
import autentica
import comunicacion

CLAVE_MAESTRA = "clave_admin_secreta"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDICOS_TXT = os.path.join(BASE_DIR, "medicos.txt")
MEDICOS_ENC = os.path.join(BASE_DIR, "medicos.txt.enc")


def preparar_entorno():
    if os.path.exists(MEDICOS_ENC):
        os.remove(MEDICOS_ENC)
    if os.path.exists(MEDICOS_TXT):
        os.remove(MEDICOS_TXT)

    usuarios = {"medicoA": "contra1", "medicoB": "contra2"}
    print("--- Registro de medicos (with open) ---")
    for usuario, contra in usuarios.items():
        registro.alta_usuario(usuario, contra, CLAVE_MAESTRA)


def main():
    preparar_entorno()

    mensaje_AB = b"Alta paciente: Juan Garcia, DOB 1980-03-15."

    print("\n--- Autenticacion medico A ---")
    ok_a, token_a = autentica.autentica_usuario("medicoA", "contra1", CLAVE_MAESTRA)
    if not ok_a:
        print("No se puede continuar sin autenticacion de A.")
        return

    print("\n--- Claves RSA A y B ---")
    for nombre in ("medicoA", "medicoB"):
        priv, pub = comunicacion.generar_claves(nombre)
        comunicacion.guardar_claves(priv, pub, nombre)

    priv_a, pub_a = comunicacion.cargar_claves("medicoA")
    priv_b, pub_b = comunicacion.cargar_claves("medicoB")

    print("\n--- Comunicacion clinica A -> B ---")
    clave_cifrada, payload_cifrado = comunicacion.enviar_mensaje(
        "medicoA", "medicoB", priv_a, pub_b, mensaje_AB, token_a
    )
    comunicacion.recibir_mensaje(
        "medicoA", "medicoB", priv_b, pub_a, clave_cifrada, payload_cifrado, token_a
    )

    print("\n--- Autenticacion medico B ---")
    ok_b, token_b = autentica.autentica_usuario("medicoB", "contra2", CLAVE_MAESTRA)
    if ok_b:
        print(f"medicoB autenticado (token: {token_b[:16]}...)")


if __name__ == "__main__":
    main()
