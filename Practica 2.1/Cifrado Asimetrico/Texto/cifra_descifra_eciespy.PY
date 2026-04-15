from ecies import encrypt, decrypt
from ecies.utils import generate_eth_key, generate_key

# Paso 1: Generar las claves (privada y pública) usando generate_eth_key()
claves = generate_eth_key()

# Paso 2: Extraer la clave privada en formato hexadecimal
clave_privada = claves.to_hex()

# Paso 3: Extraer la clave pública en formato hexadecimal
clave_publica = claves.public_key.to_hex()

print(f"Clave Privada: {clave_privada}")
print(f"Clave Pública: {clave_publica}")

# Paso 5: Crear el mensaje a encriptar (cadena de bytes)
mensaje = b"Mensaje a encriptar"

mensaje_encriptado = encrypt(clave_publica, mensaje)

print(f"Mensaje Encriptado (hex): {mensaje_encriptado.hex()}")


mensaje_desencriptado = decrypt(clave_privada, mensaje_encriptado)
print(f"Mensaje Desencriptado: {mensaje_desencriptado}")


if mensaje == mensaje_desencriptado:
    print("✓ VERIFICACIÓN CORRECTA")
else:
    print("✗ VERIFICACIÓN INCORRECTA")


clave_privada_incorrecta = generate_key().to_hex()
print(f"Clave Privada Incorrecta: {clave_privada_incorrecta}")

# Paso 12: Intentar desencriptar con la clave privada incorrecta
try:
    mensaje_desencriptado_error = decrypt(clave_privada_incorrecta, mensaje_encriptado)
    print(f"Mensaje Desencriptado con clave incorrecta: {mensaje_desencriptado_error}")
except ValueError as e:
    print(f"✗ ERROR CAPTURADO: {e}")