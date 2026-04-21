from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes



def main():
    
    # Generamos nuestra clave privada 
    priv_key=rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    # Clave pública 
    pub_key=priv_key.public_key()

    # TODO Propiedades de las claves privadas y publicas 
    priv_numbers = priv_key.private_numbers()
    pub_numbers = pub_key.public_numbers()

    print("=== Propiedades de la clave privada ===")
    print("Tamaño de clave:", priv_key.key_size, "bits")
    print("Exponente privado d (bits):", priv_numbers.d.bit_length())

    print("\n=== Propiedades de la clave pública ===")
    print("Tamaño de clave:", pub_key.key_size, "bits")
    print("Exponente público e:", pub_numbers.e)
    print("Módulo n (bits):", pub_numbers.n.bit_length())

    # Creamos mensaje a cifrar 
    mensaje_cifrar=b"Mensaje a cifrar"

    # Ciframos mensaje mediante clave pública
    mensaje_cifrado= pub_key.encrypt(
        mensaje_cifrar,
        padding= padding.OAEP(
                mgf=padding.MGF1(
                    algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                    )

    )

    print('Mensaje cifrado :', mensaje_cifrado)

    # Descifrado mediante clave privada
    mensaje_descifrado= priv_key.decrypt(
        mensaje_cifrado,
        padding=padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                    )

    )
    if mensaje_descifrado != mensaje_cifrar:
        print('VERIFICACIÓN INCORRECTA')
    else: 
        print('VERIFICACIÓN CORRECTA')
    


if __name__=="__main__":
    main()