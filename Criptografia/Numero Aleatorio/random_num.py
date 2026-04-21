import random  

start=random.randint(0,1)

if start==0:
    print('Empieza Jugador 1')
else: 
    print('Empieza el jugador 2')

numero_dado=random.randint(1,6)
print('El numero dado es : ',numero_dado)