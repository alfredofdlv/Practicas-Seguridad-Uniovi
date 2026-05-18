import registro_auditores, autentica, comunicacion






def main():
    usuarios={"usuarioA":"conA","usuarioB":"conB","usuarioC":"conC"}
    print('Registrando usuarios........')
    for usuario in usuarios.keys():
        contra=usuarios[usuario]
        print(f"Usuario: {usuario} | Contraseña :")
        registro_auditores.alta_usuario(usuario,contra)

    if autentica.autentica_usuario("usuarioA","conA"):
        privA,pubA=comunicacion.generar_claves("usuarioA")
        if autentica.autentica_usuario("usuarioB","conB"):
            privA,pubA=comunicacion.generar_claves("usuarioA")
            privB,pubB=comunicacion.generar_claves("usuarioB")


            # Iniciamos la comunicacion:
            # A -> B
            mensaje_AB = b"Auditoria Q3: se detectaron 3 anomalias en contabilidad."
            paquete_AB = comunicacion.enviar_mensaje('A', 'B', privA, pubB, mensaje_AB)

            comunicacion.recibir_mensaje('A', 'B', privB, pubA, *paquete_AB)
            


            # Antes de iniciar segunda parte verificamos usuario C:
            if autentica.autentica_usuario("usuarioC","conC"):
                privC,pubC=comunicacion.generar_claves("usuarioC")
                # B -> C
                mensaje_BC = b"Anomalias confirmadas por B. Escalado a direccion."            
                paquete_BC = comunicacion.enviar_mensaje('B', 'C', privB, pubC, mensaje_BC)
                comunicacion.recibir_mensaje('B', 'C', privC, pubB, *paquete_BC)
        
        

    


if __name__=="__main__":
    main()