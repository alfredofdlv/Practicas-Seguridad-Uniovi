import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# ====================================================================
# EJERCICIO DE EXAMEN PROPUESTO SOBRE FUNCIONES RESUMEN (HASH)
# ====================================================================
"""
ENUNCIADO:
Eres administrador de sistemas y has descargado un parche crítico 
(dividido en 3 segmentos por motivos de red). 
El servidor te proporciona un valor HASH en hexadecimal (SHA256) del 
parche completo para verificar su integridad.

Tareas a realizar:
1. Usar 'hashlib' y su metodología 'update()' para reconstruir el hash 
   ingresando los 3 segmentos secuencialmente y comprobar si el hash 
   resultante coincide con el hash original proporcionado.
2. Hacer exactamente la misma comprobación pero utilizando la librería 
   'cryptography'.
"""

def main():
    # DATOS PROPORCIONADOS POR EL PROBLEMA
    segmento_1 = b"PARCHE_SISTEMA_PARTE_1_INICIO_"
    segmento_2 = b"PARCHE_SISTEMA_PARTE_2_MEDIO_"
    segmento_3 = b"PARCHE_SISTEMA_PARTE_3_FIN"
    
    # El hash esperado que nos da el fabricante en su web oficial
    hash_oficial_esperado = "55d78a834e7cb8a35606dafa1723f1fd3ff67bb2d3b259160fe968db7f8bfbf1"
    
    print("=================== PARTE 1: HASHLIB ===================")
    # Inicializamos el objeto hash con sha256
    hash_obj = hashlib.sha256()
    
    # Actualizamos el hash secuencialmente (simulando lectura de archivo/red)
    hash_obj.update(segmento_1)
    hash_obj.update(segmento_2)
    hash_obj.update(segmento_3)
    
    # Obtenemos el digest hexadecimal
    hash_calculado = hash_obj.hexdigest()
    
    print(f"Hash Oficial : {hash_oficial_esperado}")
    print(f"Hash Obtenido: {hash_calculado}")
    
    if hash_calculado == hash_oficial_esperado:
        print("✅ [HASHLIB] El parche es INTEGRO y no ha sido modificado.")
    else:
        print("❌ [HASHLIB] ALERTA: El archivo esta corrupto o modificado.")
        

    print("\n=================== PARTE 2: CRYPTOGRAPHY ==============")
    # Inicializamos el objeto usando la API de cryptography hazmat
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    
    # Actualizamos el hash paso a paso
    digest.update(segmento_1)
    digest.update(segmento_2)
    digest.update(segmento_3)
    
    # Finalizamos la operación y obtenemos bytes raw
    resultado_bytes = digest.finalize()
    
    # Hay que pasarlo a hexadecimal para compararlo con el 'hash_oficial_esperado'
    hash_crypto_calculado = resultado_bytes.hex()
    
    print(f"Hash Oficial : {hash_oficial_esperado}")
    print(f"Hash Obtenido: {hash_crypto_calculado}")
    
    if hash_crypto_calculado == hash_oficial_esperado:
        print("✅ [CRYPTOGRAPHY] El parche es INTEGRO y no ha sido modificado.")
    else:
        print("❌ [CRYPTOGRAPHY] ALERTA: El archivo esta corrupto o modificado.")


if __name__ == '__main__':
    main()