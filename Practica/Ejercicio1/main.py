import autentica, comunicacion, registro


def autenticar(usuario, contraseña):
    return autentica.autentica_usuario(usuario, contraseña)




def main():
    # Registramos a los usuarios mediante el modulo de registro 
    
    usuarios={"medicoA":"contra1","medicoB":"contra2","medicoC":"contra3"}
    print('Registrando usuarios........')
    for usuario in usuarios.keys():
        contra=usuarios[usuario]
        print(f"Usuario: {usuario} | Contraseña :")
        registro.alta_usuario(usuario,contra)


    # Flujo de comunicación A -> B 
    # 1- Auntenticar usuario A
    if autenticar("medicoA","contra1"):
        
        if autenticar("medicoB","contra2"):

            privA,pubA=comunicacion.generar_claves("medicoA")
            privB,pubB=comunicacion.generar_claves("medicoB")

            # Iniciamos la comunicacion:
            # A -> B
            mensaje_AB = b"Historia clinica paciente 42: diagnostico reservado."
            paquete_AB = comunicacion.enviar_mensaje('A', 'B', privA, pubB, mensaje_AB)
            comunicacion.recibir_mensaje('A', 'B', privB, pubA, *paquete_AB)


            # Antes de iniciar segunda parte verificamos usuario C:
            if autenticar("medicoC","contra3"):
                privC,pubC=comunicacion.generar_claves("medicoC")
                # B -> C
                mensaje_BC = b"Validado por Dr. B. Derivar a oncologia."
                paquete_BC = comunicacion.enviar_mensaje('B', 'C', privB, pubC, mensaje_BC)
                comunicacion.recibir_mensaje('B', 'C', privC, pubB, *paquete_BC)
    else: 
        print('Usuario no autenticado\nNo se puede realizar la comunicacion.')



if __name__=="__main__":
    main()