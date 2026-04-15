import random 
import string

def main():
    key=[]
    for i in range(0,3) :
        key.append(str(random.randint(0,9)))
    
    for i in range(0,5):
        key.append(random.choice(string.ascii_lowercase + string.ascii_uppercase))
    for i in range(2):
        key.append(random.choice(['*', '-', '¿', '?' , '/']))

    new_key=''.join(key)
    print(new_key)
    if len(key)!=10:
        print('La longitud no es del todo correcta')

if __name__ == "__main__":

    main()