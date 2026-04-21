from cryptography.fernet import Fernet

# ==========================================
# 1. GESTION DE CLAVES SIMETRICAS (Fernet - AES)
# ==========================================

def generar_clave(canal):
    """Genera una clave simetrica para un canal de comunicacion (ej: A-B)."""
    print(f'Generando clave simetrica para el canal {canal}....')
    clave = Fernet.generate_key()
    return clave

def guardar_clave(clave, canal):
    """Guarda la clave compartida en un archivo local."""
    print(f'Guardando clave compartida del canal {canal} en local...')
    with open(f"simetrica_clave_{canal}.key", "wb") as f:
        f.write(clave)

def cargar_clave(canal):
    """Lee la clave simetrica de un canal."""
    print(f'Cargando clave del canal {canal} desde disco...')
    with open(f"simetrica_clave_{canal}.key", "rb") as f:
        clave = f.read()
    return clave


# ==========================================
# 2. CIFRADO Y DESCIFRADO SIMETRICO
# ==========================================

def cifrar_mensaje(mensaje, clave):
    """Cifra un mensaje usando la clave simetrica compartida."""
    print(' [Cifrado] Cifrando el mensaje con clave simetrica compartida...')
    f = Fernet(clave)
    return f.encrypt(mensaje)

def descifrar_mensaje(mensaje_cifrado, clave):
    """Descifra un mensaje usando la clave simetrica compartida."""
    print(' [Descifrado] Descifrando mensaje con clave simetrica...')
    f = Fernet(clave)
    return f.decrypt(mensaje_cifrado)


# ==========================================
# 3. FLUJO DE COMUNICACION
# ==========================================

def enviar_mensaje(origen, destino, clave_compartida, mensaje):
    print(f'\n=================[ {origen} ENVIA A {destino} ]=================')
    print(f'Mensaje original: "{mensaje.decode("utf-8")}"')
    
    mensaje_cifrado = cifrar_mensaje(mensaje, clave_compartida)
    
    print('>> Enviando mensaje por el canal cifrado... <<')
    return mensaje_cifrado

def recibir_mensaje(origen, destino, clave_compartida, mensaje_cifrado):
    print(f'\n=================[ {destino} RECIBE DE {origen} ]=================')
    
    try:
        mensaje_descifrado = descifrar_mensaje(mensaje_cifrado, clave_compartida)
        print(f'Mensaje descifrado resultante: "{mensaje_descifrado.decode("utf-8")}"')
        return mensaje_descifrado
    except Exception as e:
        print("❌ Error al descifrar. ¿La clave es correcta o el mensaje fue alterado?")


# ==========================================
# MAIN
# ==========================================
def main():
    print("--- PREPARACION DEL ENTORNO SIMETRICO ---")
    
    # IMPORTANTE: En el cifrado simétrico, A y B usan la MISMA clave. B y C usan OTRA clave.
    canales = ['AB', 'BC']
    
    for canal in canales:
        clave = generar_clave(canal)
        guardar_clave(clave, canal)

    # Cargar claves de ambos canales
    clave_AB = cargar_clave('AB')
    clave_BC = cargar_clave('BC')

    # --- COMUNICACION 1: A -> B ---
    mensaje_AB = b"Documento super secreto de A para B."
    
    # A cifra y envia usando la clave que comparte con B
    msg_cifrado_AB = enviar_mensaje('A', 'B', clave_AB, mensaje_AB)
    
    # B recibe y descifra usando la clave que comparte con A
    recibir_mensaje('A', 'B', clave_AB, msg_cifrado_AB)


    # --- COMUNICACION 2: B -> C ---
    # Nota: B descifra el paquete original, se asegura de que este bien, 
    # y ahora lo tiene que cifrar con la OTRA clave que comparte con C.
    mensaje_BC = b"Documento de A, validado por B y reenviado a C."
    
    # B cifra y envia usando la clave que comparte con C
    msg_cifrado_BC = enviar_mensaje('B', 'C', clave_BC, mensaje_BC)
    
    # C recibe y descifra usando la clave que comparte con B
    recibir_mensaje('B', 'C', clave_BC, msg_cifrado_BC)


if __name__ == "__main__":
    main()