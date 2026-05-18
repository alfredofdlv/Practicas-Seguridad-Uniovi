"""
Ejercicio E — Auth + fichero cifrado + token de sesion en hash del mensaje.
"""

import registro
import autentica
import comunicacion
from pathlib import Path

CLAVE_MAESTRA = "clave_admin_secreta"

MEDICOS_TXT = Path(__file__).resolve().parent / "medicos.txt"
MEDICOS_ENC = Path(__file__).resolve().parent / "medicos.txt.enc"


def preparar_entorno():
    """Registro de medicos y cifrado del fichero de credenciales."""
    if MEDICOS_ENC.exists():
        MEDICOS_ENC.unlink()
    if MEDICOS_TXT.exists():
        MEDICOS_TXT.unlink()

    usuarios = {"medicoA": "contra1", "medicoB": "contra2"}
    print("--- Registro de medicos ---")
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

    print("\n--- Comunicacion clinica A -> B (con token de sesion de A) ---")
    clave_cifrada, payload_cifrado = comunicacion.enviar_mensaje(
        "medicoA", "medicoB", priv_a, pub_b, mensaje_AB, token_a
    )

    # B necesita el token de sesion del emisor A para validar hash_msg
    # (en produccion: servidor de sesiones compartiria el contexto)
    comunicacion.recibir_mensaje(
        "medicoA", "medicoB", priv_b, pub_a, clave_cifrada, payload_cifrado, token_a
    )

    print("\n--- Autenticacion medico B (sesion propia) ---")
    ok_b, token_b = autentica.autentica_usuario("medicoB", "contra2", CLAVE_MAESTRA)
    if ok_b:
        print(f"medicoB autenticado (token distinto al de A: {token_b[:16]}...)")


if __name__ == "__main__":
    main()