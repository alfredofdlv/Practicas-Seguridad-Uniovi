import hashlib
from cryptography.fernet import Fernet


# ==========================================
# 1. GESTIÓN DE CLAVES SIMÉTRICAS (Fernet)
# ==========================================
def generar_clave(canal):
    print(f"Generando clave simétrica para el canal {canal}...")
    return Fernet.generate_key()


def guardar_clave(clave, canal):
    with open(f"simetrica_clave_{canal}.key", "wb") as f:
        f.write(clave)


def cargar_clave(canal):
    with open(f"simetrica_clave_{canal}.key", "rb") as f:
        return f.read()


# ==========================================
# 2. CIFRADO Y DESCIFRADO SIMÉTRICO
# ==========================================
def cifrar_mensaje(mensaje, clave):
    return Fernet(clave).encrypt(mensaje)


def descifrar_mensaje(mensaje_cifrado, clave):
    return Fernet(clave).decrypt(mensaje_cifrado)


# ==========================================
# 3. EJERCICIO D — CADENA DE HASHES
# ==========================================
def enviar_AB(mensaje, clave_AB):
    hash1 = hashlib.sha256(mensaje).digest()
    cifrado = cifrar_mensaje(mensaje, clave_AB)
    return cifrado, hash1


def recibir_AB(cifrado, hash1, clave_AB):
    mensaje = descifrar_mensaje(cifrado, clave_AB)
    if hashlib.sha256(mensaje).digest() != hash1:
        raise ValueError("Hash1 no coincide: mensaje alterado o clave incorrecta")
    print(f"[B] Mensaje AB verificado: {mensaje.decode('utf-8')}")
    return mensaje


def reenviar_BC(mensaje_BC, hash1, clave_BC):
    hash2 = hashlib.sha256(mensaje_BC + hash1).digest()
    cifrado_BC = cifrar_mensaje(mensaje_BC, clave_BC)
    return cifrado_BC, hash1, hash2


def recibir_BC(cifrado_BC, hash1, hash2, clave_BC):
    mensaje_BC = descifrar_mensaje(cifrado_BC, clave_BC)
    hash2_calculado = hashlib.sha256(mensaje_BC + hash1).digest()
    if hash2_calculado != hash2:
        raise ValueError(
            "Hash2 no coincide: B alteró el mensaje reenviado o la cadena de hashes"
        )
    print(f"[C] Mensaje BC verificado: {mensaje_BC.decode('utf-8')}")
    return mensaje_BC


def simular_ataque_B(mensaje_BC, hash1, hash2, clave_BC):
    mensaje_tocado = bytearray(mensaje_BC)
    mensaje_tocado[0] ^= 1
    mensaje_tocado = bytes(mensaje_tocado)
    print("[*] Ataque B: un byte del mensaje BC alterado; hash1 y hash2 sin recalcular")
    cifrado_BC = cifrar_mensaje(mensaje_tocado, clave_BC)
    return cifrado_BC, hash1, hash2


# ==========================================
# MAIN
# ==========================================
def main():
    print("--- Ejercicio D: Cadena de hashes (solo Fernet) ---\n")

    clave_AB = generar_clave("AB")
    clave_BC = generar_clave("BC")

    mensaje_AB = b"Factura 2024-INV-001: importe 12.500 EUR."
    mensaje_BC = b"Factura validada por B. Autorizar pago."

    print("\n=== A -> B ===")
    cifrado_AB, hash1 = enviar_AB(mensaje_AB, clave_AB)
    recibir_AB(cifrado_AB, hash1, clave_AB)

    print("\n=== B -> C (flujo honesto) ===")
    cifrado_BC, hash1_fwd, hash2 = reenviar_BC(mensaje_BC, hash1, clave_BC)
    recibir_BC(cifrado_BC, hash1_fwd, hash2, clave_BC)

    print("\n=== B -> C (ataque: B altera mensaje, reutiliza hash1/hash2) ===")
    cifrado_malo, h1, h2 = simular_ataque_B(mensaje_BC, hash1, hash2, clave_BC)
    try:
        recibir_BC(cifrado_malo, h1, h2, clave_BC)
    except ValueError as e:
        print(f"[C] Detección correcta del ataque: {e}")


if __name__ == "__main__":
    main()
