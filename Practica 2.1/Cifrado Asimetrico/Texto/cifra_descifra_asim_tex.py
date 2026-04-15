from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa



def main():
    
    # Generamos nuestra clave privada 
    priv_key=rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    # Clave pública 
    pub_key=priv_key.public_key()

    # Propiedades
    


















if __name__=="__main__":
    main()