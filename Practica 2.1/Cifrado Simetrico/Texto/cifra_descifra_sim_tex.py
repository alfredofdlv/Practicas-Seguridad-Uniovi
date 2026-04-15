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



def main():

    # Generamos la clave y guardamos dicha clave en local para su posterior uso 
    genera_key()
    key=carga_key()

    # Generamos el mensaje secreto 
    mensaje="MENSAJE SECRETO"
    mensaje=mensaje.encode()

    # Creamos la variable fernet para poder encriptar el mensaje 
    fernet=Fernet(key)  # Creamos objeto Fernet
    mensaje_cifrado=fernet.encrypt(mensaje)  # Encriptamos 
    guarda_msj_encriptado(mensaje_cifrado)   # Guardamos en local dicha clave 


    # Des encripatmos el mensaje 
    mensaje_descifrado=fernet.decrypt(mensaje_cifrado)
    guarda_msj_desencriptado(mensaje_descifrado)   # Guardamos en local dicha clave 






if __name__ == "__main__":

    main()