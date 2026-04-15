from cryptography.fernet import Fernet

def genera_key():
    key = Fernet.generate_key()
    with open("clave.key","wb") as archivo_clave:
        archivo_clave.write(key)

def carga_key():
    with open("clave.key","rb") as archivo_clave:
        f = archivo_clave.read()
    return f 
def guarda_msj_encriptado(mensaje_encriptado):
    with open('texto_cifrado.bin','wb') as archivo :
        archivo.write(mensaje_encriptado)
def guarda_msj_desencriptado(mensaje_desencriptado):
    with open('texto_descifrado.bin','wb') as archivo :
        archivo.write(mensaje_desencriptado)


def encriptar(text,key):
    key=carga_key()

    fernet=Fernet(key)  # Creamos objeto Fernet

    mensaje_cifrado=fernet.encrypt(text)  # Encriptamos 
    guarda_msj_encriptado(mensaje_cifrado)



def desencriptar(text,key):
    
    fernet=Fernet(key)  # Creamos objeto Fernet
    mensaje_descifrado=fernet.decrypt(text)
    # print('Texto desencriptado: ', mensaje_descifrado)
    guarda_msj_desencriptado(mensaje_descifrado)   # Guardamos en local dicha clave 


def main():
    genera_key()
    key=carga_key()
    with open('file.txt', 'rb') as f:
        archivo_info= f.read()
    # print(archivo_info)

    encriptar(archivo_info,key)

    with open('texto_cifrado.bin', 'rb') as f:
        texto_cipher= f.read()

    desencriptar(texto_cipher,key) 

if __name__ == "__main__":
    main()