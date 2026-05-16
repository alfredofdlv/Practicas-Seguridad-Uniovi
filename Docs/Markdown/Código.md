```
Area de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD^1

# Confidencialidad: Cifrado Simétrico y

# Cifrado Asimétrico

# Práctica 2 .1 - Presencial

# 1. Objetivo

Se presenta un doble objetivo en esta parte de la práctica. En primer lugar, **desplegar el entorno de
desarrollo** que se utilizará atendiendo a **Visual Studio Code** y lenguaje **Python**. Por otro lado,
introduciremos los **conceptos básicos del cifrado simétrico** desde el punto de vista de la
**programación** para comprender mejor este tipo de cifrado.

# 2. Entorno de Desarrollo

Necesitamos un entorno de desarrollo para llevar a cabo las tareas requeridas en esta parte de la
práctica. Para ello, instalaremos en la Máquina Virtual Windows 11 el software Visual Studio Code
(VSC). Accede a https://code.visualstudio.com/download para poder descargarlo y proceder con la
instalación. Si utilizas el ordenador de clase para realizar esta parte, no necesitarás instalar VSC.

Descarga la versión para Windows 11 y procede a realizar la instalación en la Máquina Virtual
realizando una instalación típica dejando por defecto todas las opciones que nos muestra el
instalador. Una vez instalado, comprueba que se abre de forma correcta y tenemos el software
disponible para ser usado.

Realiza la configuración del entorno eligiendo el tema del entorno que más se adecúe a tu estilo de
programación, así como el idioma en el que lo quieres (en el caso de las prácticas siempre se usarán
elementos en español).


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 2

Si quieres poner en software en español, una vez abierto presiona la tecla F1 del sistema para abrir
la paleta de comandos y escribe “ _Configure display languaje”_

Al pinchar sobre la opción que nos muestra se mostrarán los idiomas instalados y disponibles. En mi
caso ya tengo instalado el español como idioma predeterminado por lo que me aparece en la parte
superior. En caso de que no lo tengas instalado deberás proceder a seleccionarlo (se descarga e
instala casi instantáneamente).

Con esto tendremos ya configurado en software para desarrollo atendiendo a las características
propias del mismo.

## 2.1 Instalación y Configuración de VSC para Python

Una vez que tenemos Visual Studio Code (VSC) instalado, tendremos que proceder a realizar la
instalación y configuración de VSC para poder utilizar en lenguaje Python.

En primer lugar realizaremos la validación de la versión e instalación de Python. En este caso, y como
el desarrollo de Python 2 se interrumpió en 2020, haremos uso de Python 3.

Nota: Algunos sistemas podrían tener preinstalado Python 2, por lo que, deberemos actualizar dicha
versión a Python 3.

Para saber si tengo Python 3 instalado en el sistema (no debería porque la instalación se ha realizado
desde 0 y no se ha instalado nada), podemos utilizar el símbolo de sistema. Para ello, desde la barra
de tareas de Windows pincha en el botón de _Inicio_ y posteriormente escribe _cmd._ Abre el símbolo
de sistema y teclea el siguiente comando: _python --version_ o _py –version._

Como podemos observar no tenemos instalado Python en el sistema por lo que, habrá que proceder
a su instalación.

Procederemos a la instalación de Python desde la Microsoft Store. Para ello, desde la barra de
tareas, busca la tienda de Microsoft y ábrela. A continuación, busca la palabra Python para poder
verificar las diferentes versiones disponibles en la tienda.


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 3

Selecciona la versión del lenguaje de programación Python 3.13 y pulsa sobre descargar para que
comience la descarga. Una vez finalizada verás que está instalada en el sistema como aparece en la
imagen superior.

Una vez instalado, puede que nos aparezca un menú emergente en la parte inferior derecha de la
pantalla proponiendo el Inicio de Python. Si pulsamos en _Iniciar_ se abrirá una pantalla modo consola
como la siguiente:

Si no aparece, puedes acceder desde el menú de inicio al software de Python para poder ejecutar la
consola de igual forma. En este consola vemos la versión instalada de Python (3.13.9) y en la que
podemos ejecutar comandos en Python. Para comprobar la funcionalidad incluye ejecuta la
siguiente sentencia, que imprimirá “Hola Mundo” por pantalla: print(“Hola Mundo”).


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 4

Aunque ya hemos comprobado la versión al iniciar Python, accede de nuevo al símbolo de sistema
del equipo y ejecuta la orden: python --version para comprobar que la versión se
corresponde con la que hemos visto anteriormente.

Una vez comprobado, ya tendremos instalado correctamente Python en el sistema operativo
Windows 11, lo que tendremos que realizar ahora es vincular VSC con Python para poder desarrollar
en desde el software instalado.

Para realizar esto, habrá que instalar la extensión de Python en VSC. Para ello, abre VSC y ve al menú

#### Ver → Extensiones

En la parte izquierda de la pantalla nos aparecerán todas las extensiones, ya instaladas y
recomendadas más populares en el _Marketplace_. En mi caso, tengo ya instalada la extensión de
paquete de idioma _Español_ que instalamos anteriormente.

En el buscador escribe _Python_ para poder realizar la búsqueda de las extensiones que contengan
Python para poder ser usado:


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 5

Selecciona la primera de ellas y pulsa sobre el botón instalar que se ve en la descripción de la misma
(parte derecha de la pantalla) para proceder a su instalación.

Una vez instalada podremos observar que las opciones de la extensión cambia y, al estar ya
instalada, aparecen las opciones de desinstalar y de cambiar a la presión preliminar de la misma.
Deja marcada la opción de _Actualización automática_ para que si entra una nueva versión nos la
instale de forma automática.

La otra pestaña que nos muestra VSC cuando realizamos la instalación los permitirá realizar algunas
acciones iniciales sobre la extensión instalada:

Como vemos, podemos abrir un proyecto en Python, crear uno nuevo o seleccionar un entorno de
desarrollo entre otros.

Con esto, ya tendríamos instalado y configurado VSC con la extensión de Python para poder ser
usada ya que, previamente, hemos realizado la instalación de Python en nuestro sistema local.


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 6

## 2.2 Primera Aplicación Python – Contraseña Segura

Para crear la primera aplicación, utilizaremos íntegramente VSC para realizarla, aunque hay pasos
que se podrían hacer desde fuera del software como la creación de la carpeta que contendrá la
aplicación en sí.

#### Para ello, abre una nueva terminal dentro de VSC desde el menú Terminal → Nuevo Terminal. Esto

abrirá una terminal en PowerShell que nos permitirá ejecutar comandos.

Desde la terminal crea una nueva carpeta en el Escritorio del equipo llamada **_numero-aleatorio_** para
almacenar el código de la aplicación que vamos a desarrollar.

#### Abre esta carpeta en VSC desde el menú Archivo → Abrir Carpeta y asegúrate que se abre de forma

correcta:

Como puedes ver, todavía no contiene nada, por lo que habrá que crear un nuevo fichero .py que
almacenará la lógica de nuestra aplicación.


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 7

Pulsa sobre el botón _Nuevo archivo..._ para crear un archivo cuyo nombre será: _random_num.py_ y
guarda dicho fichero.

Ahora estaremos en disposición de escribir el código necesario para llevar a cabo la aplicación que
genere números aleatorios en Python.

Llegados a este punto, vamos a comenzar a crear la aplicación para la generación de números
aleatorios.

En este caso, Python nos permite usar diferentes métodos para crear elementos aleatorios. Entre
ellos, encontramos los siguientes:

- randint(): devuelve un número entero comprendido entre los valores indicados. Los
    valores de los límites inferior y superior también pueden aparecer entre los valores
    devueltos. Para números decimales (float) se usa la función uniform().
- randrange(): devuelve números enteros comprendidos entre un valor inicial y otro final,
    separados por un valor "paso" determinado.
- choice() y choices(), permiten seleccionar valores de una lista de forma aleatoria.
    Toman una lista como argumento y seleccionan aleatoriamente un valor (o valores en el caso
    de choices()).
- shuffle(): "baraja" una lista. Esta función “mezcla” o cambia aleatoriamente el orden de
    los elementos de una lista antes de seleccionar uno de ellos.
- gauss(): genera un conjunto de números aleatorios cuya distribución de probabilidad es
    una distribución gaussiana o normal.

Como **ejemplo** de uso, vamos a crear una pequeña aplicación que determine de forma aleatoria
quien comienza a jugar una partida en la que se debe jugar con un dado. Dispondremos de 2
jugadores (Jugador 1 y Jugador 2) y de un dado con 6 caras (del 1 al 6). El programa deberá
determinar quién comienza a jugar y qué número saca en su tirada de dado.

Para llevar a cabo este ejemplo utilizaremos randint() 2 veces, una para determinar el jugador
y otro para determinar la jugada. Verifica el código siguiente para ver lo que se realiza en el ejemplo.


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 8

En primer lugar se importa la librería **random** de Python para poder hacer uso de los métodos que
contiene para poder generar números aleatorios. A continuación, declaramos una variable _start_ que
determinará quien empieza a jugar generando un valor entre 0 (Jugador 1) o 1 (Jugador 2).
Imprimiremos el resultado atendiendo a una estructura _if_. Por último volvemos a generar un
número aleatorio, en este caso entre 1 y 6 para ver la jugada del dado imprimiendo el resultado por
pantalla.

Para la ejecución del programa, accede a la terminal y desde ahí introduce el comando: python
nombre_del_ejecutable como se muestra en la figura:

Puedes observar que se ejecutó varias veces para verificar el funcionamiento del número aleatorio
en este caso. También puedes ejecutar el ejercicio pulsando el botón “Play” de la parte superior
derecha del entorno de desarrollo.

Como **ejercicio final,** y haciendo uso de los métodos explicados anteriormente, se propone la
creación de un programa ( _Contra_Segura.py_ ) que sea capaz de crear contraseñas seguras de forma
aleatoria. En este caso las contraseñas deben cumplir lo siguiente:

- Tener al inicio 3 números
- A continuación, contener letras (un total de 5 letras mayúsculas y minúsculas)
- Para finalizar, debe contener algún carácter especial de entre los siguientes: *, -, ¿,? o /
- La longitud final de la contraseña debe ser de 10 caracteres.

Se recomienda incorporar el módulo **string** en la solución para poder hacer uso de los métodos
string.ascii_uppercase y string.ascii_lowercase que nos permitirán abarcar
todas las posibilidades existentes en relación a las letras del abecedario tanto en mayúscula como
en minúscula.

Puedes ayudarte de una variable llamada _password_ para ir almacenando los caracteres creados de
forma aleatoria en cada caso con el objetivo de poder concatenarlos y tener la contraseña segura
creada. Se recomienda utilizar diferentes métodos de generación de caracteres aleatorios para cada
uno de los puntos mencionados anteriormente (números, letras y caracteres especiales).

A modo de ejemplo, se muestra una posible ejecución del programa para verificar que las
contraseñas se crean atendiendo a lo especificado en el enunciado del ejercicio:

Merece la pena mencionar que este tipo de contraseña puede ser más robusta si intercambiamos
las posiciones de los elementos, pero este ejercicio se propone de esta forma para poder utilizar
diferentes métodos del módulo **random** en el desarrollo del mismo.


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 9

Una vez que ya tenemos nuestra primera aplicación funcionando, y hemos obtenido los
conocimientos básicos de Python y conocemos también el entorno de desarrollo que usaremos, nos
adentraremos en puntos posteriores en las librerías o módulos que otorgan funcionalidad relativa
a la seguridad informática para, por ejemplo, poder hacer cifrados de datos.

## 2.3 Introducción a Python en Seguridad

Para añadir funcionalidad de elementos relacionados con la Seguridad, usaremos la librería
**cryptography**. Esta librería nos va a ofrecer funcionalidad relacionada con criptografía empleados
en esta práctica. Accede a https://pypi.org/project/cryptography/ y echa un vistazo a la
introducción que se nos da de este proyecto.

También puedes acceder a la documentación sobre la librería en: https://cryptography.io/en/latest/
Aquí encontrarás la última versión disponible y documentación relacionada con el uso de la misma.

Como puedes observar, lo primero que debemos hacer es instalar la librería **cryptography** en el
equipo para poder hacer uso de la misma. Para ello, introduce el siguiente comando: pip
install cryptography en el _Símbolo de Sistema_ del equipo.

Verifica que la instalación se realiza de forma correcta en la última versión disponible (en el caso de
la creación de este guión de práctica la versión de la librería es la 43.0.1, que se puede observar al
final de la ejecución del comando propuesto) que debe coincidir con la que muestra la web del
proyecto (visible más arriba).


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 10

Una vez instalada, ya tendremos preparado el entorno para comenzar a crear pequeños programas
que hagan uso de elementos criptográficos (encriptación y desencriptación) de información
atendiendo a los métodos que la librería nos ofrece.

Una vez concluida esta parte y puesta en marcha nuestra primera aplicación en Python puedes
refrescar contenidos asociados con la programación en este lenguaje en la siguiente página web:
https://www.w3schools.com/python/. Ten en cuenta que trabajaremos en este lenguaje a través
de diferentes funcionalidades que ofrece en el mismo, por ejemplo: importando librerías/módulos,
creando funciones, manejando ficheros, etc., materia que se da por supuesta para continuar las
prácticas.

# 3. Cifrado Simétrico

Ahora estamos en disposición de comenzar con la creación de dos pequeños programas que utilice
Cifrado Simétrico (cifrado y descifrado) para realizar la encriptación y desencriptación de
información. Para ello, utilizaremos un **algoritmo de tipo AES** ( _Advanced Encryption Standard_ ) que
generará una clave (en un archivo) a través de la cual podremos encriptar nuestra información. Al
ser un algoritmo simétrico, utilizaremos la misma clave para desencriptar dicha información.

Importa **Fernet** desde la librería de criptografía que incorporamos anteriormente. Fernet es una
herramienta muy útil para desarrollar aspectos de ciberseguridad en Python. Es un pequeño script
de Python que se utiliza para resolver problemas comunes y que nos **proporciona cifrado simétrico
y autenticación de datos**. Usa AES en modo de operación CBC ( _Cipher-Block Chainning_ ) con una
clave de 128 bits. Forma parte de la biblioteca de criptografía para Python, desarrollada por la
Autoridad Criptográfica de Python (PYCA). Fernet garantiza que un mensaje cifrado no pueda ser
manipulado o leído sin clave.

## 3.1 Cifrado/Descifrado de mensaje de texto

Crea un directorio llamado _cifra_descifra_simetrico_texto_ que albergará todo el desarrollo realizado
en este punto de la práctica. En su interior, creo la solución llamada **_cifra_descifra_sim_tex.py_**. No
olvides añadir los **comentarios** que estimes oportunos en el desarrollo del código para una mejor
comprensión del mismo.

Para iniciar el desarrollo, incorpora la siguiente sentencia al inicio de la solución. Esta sentencia
usará lo explicado anteriormente haciendo uso de Fernet:


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 11

from cryptography.fernet import Fernet

A continuación, **crea una función** llamada **genera_key()** , que sea capaz de **generar la clave** que
utilizaremos y almacenarla en un fichero llamado _clave.key_. Para realizarlo utiliza una variable
llamada _key_ a la que pasarás el método de Fernet **generate_key().** Y escribe esta contraseña
en el fichero creado. Otorga al fichero el modo de escritura (w) y determina que es un fichero binario
(b).

Como ejemplo, al ser el primer tratamiento de ficheros que hacemos, se muestra la solución del
mismo:

**def genera_key():
key = Fernet.generate_key()
with open("clave.key","wb") as archivo_clave:
archivo_clave.write(key)**

Crea ahora la **función para cargar dicha clave**. En este caso, el nombre de la función será
**carga_key()** y lo único que hará será devolver la lectura del fichero de clave a través del método
**open()** , ten en cuenta que el método para el acceso será de lectura (r) y habrá que determinar
que es un fichero binario (b) porque así lo definimos previamente.

Ahora estaremos en disposición de realizar las tareas principales desde la **función principal** del
programa para proceder a encriptar el mensaje y mostrarlo por pantalla. Para ello habrá que:

1. Llamar a la función que genera la clave
2. Crear una variable a la que le pasamos la llamada de la función para cargar la clave
3. Declarar una variable que contendrá un _string_ con el mensaje a encriptar (hay que pasarle
    el método **encode()** para codificar dicho mensaje y que pueda ser tratado por el
    encriptador). El mensaje será “MENSAJE SECRETO”.
4. Iniciar Fernet para que pueda funcionar de forma correcta. Para ello crea una variable
    llamada _fernet_ a la que le pasarás un objeto Fernet con la variable donde has cargado la
    clave.
5. Realizar, en una nueva variable, el encriptado almacenando el resultado de usar la variable
    fernet creada anteriormente con el método **encrypt()** del mensaje a encriptar.

Ahora, **muestra por pantalla la clave que se ha usado y el mensaje encriptado**.

Abre el fichero _clave.key_ para verificar el formato en el que se almacena la clave en el fichero.

Como puedes verificar antes de la clave o del mensaje aparece **b’** esto se debe a que se identifica
que es un mensaje definido en binario, como habíamos establecido previamente.

**Almacena el mensaje encriptado en un fichero** llamado _texto_cifrado.bin_ para poder verificar que
el texto se guarda en el formato correcto. Para ello, deberás crear una nueva función llamada
**guarda_msj_encriptado(mensaje_encriptado)** a la que le pasarás como parámetro el
mensaje encriptado teniendo en cuenta que será un fichero binario (b). Realiza una llamada a dicha
función para verificar el funcionamiento.

Como último paso, comprueba que se corresponde la salida observada en la terminal de VSC con lo
que se almacena tanto en el fichero de clave como en el fichero del mensaje encriptado.


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 12

En este punto estaremos en disposición de desencriptar el mensaje que hemos encriptado haciendo
uso de la variable que tenía almacenada dicho mensaje y de la clave simétrica que usamos para su
encriptación.

Sigue completando la solución que tenías hasta ahora para ahora hacer uso del método
**decrypt()** del objeto Fernet para poder **desencriptar** el **mensaje cifrado**. Almacena el resultado
en una variable.

**Muestra por la terminal** el **mensaje** inicial desencriptado.

Por último, crea una función **guarda_msj_desencriptado(msg_desencriptado)** , que
sea capaz de almacenar en un fichero binario el mensaje en texto plano para que sea legible.

Como conclusión, **verifica el procedimiento** y los pasos que has ido realizando para tener claro cómo
funciona este tipo de cifrado y su programación en Python. Verifica que se han creado todos los
ficheros de clave y de mensajes que se requieren.

## 3.2 Cifrado/Descifrado simétrico de archivo

Una vez que hemos cifrado un mensaje haciendo uso de una clave almacenada en un fichero y
hemos guardado su contenido en un fichero externo para verificar su funcionalidad, en esta sección
realizaremos el cifrado simétrico de un archivo completo para verificar el funcionamiento de este
tipio de cifrado atendiendo a archivos completos.

En primer lugar, crea un nuevo directorio raíz llamado _cifra_descifra_simetrico_archivo_ en el que
almacenarás la solución y todos los ficheros necesarios para la realización de esta parte de la
práctica.

Crea una **nueva solución** (con un nuevo directorio llamado _cifra_simetrico_archivo_ ) en la que crees
de nuevo un fichero llamado **_cifra_descifra_sim_file.py_** , que manejará lo necesario para llevar a
cabo la encriptación de un fichero completo.

En primer lugar, debemos crear nuestro fichero de texto ( _file.txt_ ) que será el que encriptemos.
Créalo en el directorio raíz de la solución. Accede a https://es.lipsum.com/, una web para crear texto
de relleno y crea 5 párrafos de texto que deberás copiar y pegar en el fichero _file.txt_ añadiendo al
inicio la cabecera (MENSAJE SECRETO:)

Este será el fichero que debemos encriptar en nuestra solución.

A continuación, y por no volver a generar la clave, copia de la solución anterior (“Cifrado/Descifrado
de mensaje de texto”) el fichero _clave.key_ que será el que utilicemos como clave simétrica en esta
nueva solución y pégalo en el directorio raíz en el que estes.


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 13

En primer lugar, crea una función igual que en la solución anterior para cargar la clave llamada
**carga_key()** , ten en cuenta que deberá ser un fichero de lectura y en formato binario.

A continuación, habrá que crear dos funciones para encriptar y desencriptar el fichero.
Comenzaremos por la de encriptación haciendo referencia a los siguientes pasos:

1. Crea una función llamada **encriptar()** a la que se le pasará el archivo en texto plano y la
    clave para poder encriptarlo.
2. Crea un objeto Fernet al que le pases la clave que será el que utilicemos para encriptar el
    archivo.
3. Lee el fichero _file.txt_ que hemos generado anteriormente y almacénalo en una variable
    (puedes llamarla _archivo_info_ ya que almacenará la información del fichero)
4. Crea una variable para guardar la llamada al método **encrypt(archivo_info)**.
5. Crea un nuevo fichero en el que almacenarás la información encriptada que has creado
    anteriormente. Deberás crearlo como un fichero binario con permisos de escritura. Llama al
    método **write()** para escribir en él.

Para abordar la función para desencriptar, deberemos seguir estos pasos:

1. Crea una función llamada **desencriptar()** a la que se le pasará el archivo encriptado y
    la clave para poder desencriptarlo (será la misma al estar en cifrado simétrico).
2. Crea un objeto Fernet al que le pases la clave a utilizar en la desencriptación del fichero.
3. Lee el fichero encriptado y almacena la información leída en una variable.
4. Crea una nueva variable que almacenará la información desencriptada a través del método
    **decrypt(info_encriptada).**
5. Crea un nuevo fichero en el que almacenarás la información del fichero desencriptada. Ten
    en cuenta que deberá ser un fichero con permiso de escritura y formato binario. Al igual que
    anteriormente, utiliza el método **write()** para escribir en él.

Ahora estaremos en disposición de abordar la función principal del programa, así como las llamadas
a las funciones creadas.

En primer lugar, crea una variable en la que almacenes lo que devuelve la llamada a
**carga_key()** que nos permitirá tener la clave para poder usar en dicha variable.

Asigna el nombre del fichero en texto plano que tenemos inicialmente ( _file.txt_ ) a una variable, que
será la que utilicemos a la hora de realizar llamadas a las funciones correspondientes.

Llama a la función **encriptar()** a la que le pasarás la variable creada anteriormente (nombre del
fichero) y la clave cargada.

Crea una variable para almacenar el nombre del fichero encriptado que se pasará a la función
**desencriptar()**.

Llama a la función **desencriptar()** pasándole la variable creada (nombre del fichero) y la clave
para desencriptar.

**Verifica que se crean de forma correcta los ficheros** encriptados/desencriptados para comprobar
la funcionalidad.

Con esto finalizamos la parte del cifrado simétrico de esta práctica, teniendo a nuestra disposición
dos soluciones para cifrar/descifrar de forma simétrica por un lado texto plano en un programa, y
por otro ficheros completos.


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 14

# Confidencialidad: Cifrado Simétrico y

# Cifrado Asimétrico

# Práctica 2 .1 - Online

# 1. Objetivo

El objetivo de esta parte de la práctica será el de asimilar los **conceptos asociados al cifrado
asimétrico** ya vistos en la parte de teoría. Para ello, se hará uso del algoritmo de cifrado asimétrico
RSA, que nos permitirá, no únicamente encriptar/desencriptar información, sino también poder
firmar mensajes, lo que garantizará la autenticidad y confidencialidad de los datos. Se hará uso del
software instalado y configurado anteriormente.

# 2. Cifrado Asimétrico

A diferencia del Cifrado Simétrico estudiado anteriormente, en este caso utilizaremos un Cifrado de
tipo Asimétrico a través del **algoritmo RSA** , que como ya sabéis, es un algoritmo criptográfico de
clave pública que utiliza factorización de números enteros.

En este caso, tendremos que utilizar una **clave privada y una clave pública** para trabajar. La clave
pública podrá ser compartida con quien queramos (agente de confianza o no), miembros que la
clave privada deberá ser secreta.

No utilizaremos este algoritmo para cifrar/descifrar información únicamente, sino también para
firmar un mensaje con clave privada. Esto nos proporcionará dos casos de uso principales:
**autenticación y confidencialidad**. En esta parte de la práctica únicamente atenderemos al
cifrado/descifrado (confidencialidad), dejando la parte de la firma para la siguiente práctica.

Seguiremos usando la librería **_cryptography_** instalada previamente, pero en este caso haremos uso
del paquete _Hazmat_ (en lugar de Fernet) para llevar a cabo las tareas asociadas al cifrado asimétrico.
https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/.

## 2.1 Cifrado/Descifrado asimétrico de texto

Crea un nuevo directorio en el que almacenaras todo lo necesario para crear la solución de esta
parte de la práctica. Llama al directorio _cifra_descifra_asimetrico_texto._

Crea una nueva solución ( **_cifra_descifra_asim_tex.py_** ) en la que resolveremos el cifrado/descifrado
de información atendiendo al algoritmo RSA (asimétrico).

En primer lugar, importa los objetos **_default_backend_** y **_rsa_** del paquete _Hazmat_ que nos permitirá
usar los métodos necesarios en el desarrollo de la práctica. El primero de ellos, hace referencia a los
diferentes tipos de respaldo que ofrece la librería (CipherBackend, RSABackend, etc.), pero siempre
usaremos el que viene por defecto. El segundo importará lo necesario para usar el algoritmo RSA
en nuestro desarrollo. Para añadirlos a la solución utiliza las siguiente sentencias:

from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives.asymmetric import rsa


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 15

A continuación, utilizaremos el método **generate_private_key** para crear nuestra clave
asignándole los parámetros que consideremos oportunos. Para ello, crea una variable ( _private_key_ )
a la que, haciendo uso del objeto **_rsa_** llames al método **generate_private_key()** pasándole
los siguientes valores:

- Exponente público (public_exponent) = 216 +1 = 65537 (por defecto siempre usaremos este)
- Tamaño de clave (key_size) = 2048
- Backend = default_backend()

Con esto tendremos configurada la clave privada que usaremos. En este caso, se atiende a una clave
RSA que utiliza un tamaño de 2048 bits.

Para seguir, deberemos crear la **clave pública**. En este caso, crea una variable ( _public_key_ ) a la que
asignes la llamada al método **public_key()** haciendo uso de la clave privada generada
anteriormente. Con esto, generamos una clave pública a partir de nuestra clave privada.

Podríamos manejar las dos claves guardándolas en un fichero o serializándolas para poder
recuperarlas en Hexadecimal, pero no lo haremos para no dilatar la ejecución de la práctica y
supondremos que se almacenan de forma correcta si se hace el cifrado y el descifrado
correctamente.

Para verificar la existencia de la clave **muestra algunas propiedades** de las claves (privada y pública),
como por ejemplo el tamaño (debe ser 2048) o la clase ( ___class___ )que devolverá el tipo de objeto
que esta almacenado _RSAPrivateKey_ o _RSAPublicKey_. Algunas propiedades serán objetos dentro de
la definición de la clave y no nos permitirá verlos en texto plano, pero entendemos que son
correctos.

Ahora estaremos en disposición de encriptar/desencriptar un mensaje. Para ello, crea una nueva
variable que contenga el mensaje a cifrar que deberá ser definido como cadena de bytes (añadiendo
“b” al mensaje) para que pueda ser tratado de forma correcta desde los métodos de
cifrado/descifrado:

Ejemplo: **mensaje_cifrar = b”Mensaje a cifrar”**

Este será el mensaje que queremos cifrar.

A continuación, crea una nueva variable que contendrá el texto encriptado que será definido
haciendo uso del método **encrypt()** de la clave pública (ciframos con clave pública y desciframos
con clave privada). Consulta la documentación del método para comprobar que se le pasan 2
parámetros: el mensaje a cifrar (variable creada previamente) y el relleno ( _padding_ ).

En el caso del relleno, habrá que definir el tipo que queremos utilizar pudiendo utilizar OAEP
( _Optimal Asymetric Encryption Padding_ ), PSS ( _Probabilistic Signature Scheme_ ) o PKCS1v
( _PublicKey Cryptography Standards_ ) entre otros. En este caso, haremos uso de OAEP al que habrá
que pasarle 3 parámetros: **_mgf_** que determinará la función de generación de máscara (solo se
soporta MGF1), **_algorithm_** , que será la instancia del algoritmo de hash utilizado y por último, **_label_**
(etiqueta) que determinará la etiqueta a aplicar. Por defecto se establece a valor **_None._**

Para facilitar el tratamiento del relleno se propone una posible solución:

**padding.OAEP(
mgf=padding.MGF1(algorithm=hashes.SHA256()),
algorithm=hashes.SHA256(),
label=None
)**


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 16

Como vemos, se utiliza un relleno de tipo OAEP en el que atendemos a un algoritmo hash SHA
( _Secure Hash Algorithm_ de 256 bits).

**Muestra por pantalla el mensaje cifrado** para comprobar que efectivamente se ha producido el
cifrado del mismo.

Nos quedará ahora realizar el **descifrado del mensaje cifrado** anteriormente. Para ello crea una
nueva vabiable ( _mensaje_descifrado_ ) a la que le pases el método **decrypt()** usando como objeto
la clave privada (usada para descifrar el mensaje en cifrado asimétrico). Al método **decrypt()**
se le deben pasar los mismos parámetros que al **encrypt()** en este caso, el mensaje cifrado (ya
lo tenemos calculado anteriormente) y el relleno ( _padding_ ) que tendrá los mismos valores que para
el caso del cifrado.

**Muestra por pantalla el mensaje descifrado** para comprobar que coincide con el mensaje inicial
que teníamos guardado. Para realizar la verificación, usa una sentencia **_if_** que sea capaz de comparar
ambos mensajes. En caso de que sean iguales se deberá mostrar por pantalla _VERIFICACIÓN
CORRECTA_ en caso contrario, _VERIFICACIÓN INCORRECTA_.

**Incluye** en la solución mediante impresiones por pantalla lo que va haciendo la solución para ver los
**pasos** que se van dando a la hora de realizar un **cifrado/descifrado asimétrico**.

Un posible ejemplo de ejecución puede ser el siguiente:

## 2.2 Cifrado/Descifrado asimétrico con eciespy

Existen otras librerías que nos pueden permitir realizar tareas de cifrado/descifrado de información
haciendo uso de algoritmos asimétricos. En este caso, utilizaremos **_eciespy_** para llevar a cabo el
cifrado/descifrado de un mensaje de texto de forma **muy rápida e intuitiva** ya que nos permite
tener funciones directas para poder ver claves, y encriptar/desencriptar información.

Antes de comenzar a desarrollar el desarrollo de esta parte, tendremos que instalar la librería. Para
ello utiliza el siguiente comando: pip install eciespy. Puedes hacerlo desde la propia
terminal de PowerShell que ofrece _Visual Studio Code_.

Una vez finalizada la instalación, crea una nueva solución llamada **_cifra_descifra_eciespy.py_**. En ella
será donde realicemos lo necesario para llevar a cabo el cifrado/descifrado de información.

En primer lugar, importa la librería necesaria para trabajar con **_eciespy_** para realizar
cifrado/descifrado de información.


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 17

from ecies import encrypt, decrypt

from ecies.utils import generate_eth_key, generate_key

Una vez incorporadas, estaremos en disposición de crear lo necesario para poder cifrar/descifrar
información.

En primer lugar, crea una **variable** a la que le pases una llamada al **método importado
generate_eth_key()** esto nos creará directamente las dos claves (privada y pública). Puedes
llamar a la variable _claves._

A continuación, crea dos variables llamadas _clave_privada_ y _clave_publica_. Para almacenar el
hexadecimal la clave y poder verla bastará con llamar al método **to_hex()** desde la variable que
creaste anteriormente para almacenar las claves.

En el caso de la clave pública, deberás hacer uso de esa misma variable, pero accediendo a la clase
**public_key** para llamar de nuevo al método **to_hex()** para almacenar dicha variable.

A continuación, **muestra con un** **_print_** **las claves privada y pública generadas** para comprobar que
son visibles por pantalla en formato hexadecimal.

Una vez que ya tenemos las claves, crea una **variable** que contenga el mensaje que queremos
encriptar. En este caso, puedes incluir el texto: “ **Mensaje a encriptar** ”. Recuerda que sea una cadena
de bytes (añade “b” al inicio de la cadena).

Crea una nueva variable que almacenará el mensaje encriptado. Para ello, asigna a dicha variable la
llamada al método **encrypt()** al que pasarás la clave pública y el mensaje a encriptar.

**Muestra por pantalla el mensaje encriptado**. No olvides usar la notación hexadecimal para que se
vea de forma correcta (método **hex()** ).

Para proceder desencriptar el mensaje. Crea una nueva variable que almacenará el mensaje
desencriptado y utiliza el método **decrypt()** al que pasarás la clave privada y el mensaje
encriptado como parámetros.

**Muestra por pantalla el mensaje desencriptado**. En este caso, no hace falta que se pase a
hexadecimal ya que tendremos un texto plano y se podrá mostrar sin realizar ninguna conversión.

Al igual que hicimos en la solución anterior, verifica el funcionamiento usando una sentencia **_if_** que
sea capaz de comparar ambos mensajes. En caso de que sean iguales se deberá mostrar por pantalla
_VERIFICACIÓN CORRECTA_ en caso contrario, _VERIFICACIÓN INCORRECTA_.

Para comprobar si la verificación funciona, **introduciremos un “error”** en la validación y será la
creación de otra nueva clave privada para hacer el desencriptado de información. Para ello, crea
una nueva variable a la que asignarás la llamada al método **generate_key().to_hex()**.
Prueba ahora a realizar el desencriptado ( **decrypt()** ) de información atendiendo a esta nueva
clave y al mensaje cifrado anteriormente. Almacénalo en una nueva variable. ¿Qué sucede?. Al no
estar vinculadas las claves (pública y privada) el mensaje no puede ser desencriptado de forma
correcta y nos debería saltar el error: ValueError: MAC check failed.

**Verifica paso a paso** lo que va haciendo la solución para comprobar cómo trabaja el
cifrado/descifrado simétrico atendiendo a esta librería.

Pese a que hayamos visto dos librerías que nos permiten realizar cifrado/descifrado asimétrico, se
recomienda usar la librería de referencia **_cryptography_** , ya que es la más extendida, la que mayor
variedad de opciones nos ofrece y la mayormente soportada por la comunidad.


```
Area de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 1

# Integridad y Autenticidad: Funciones

# Resumen y Certificados

# Práctica 2 .2 - Presencial

# 1. Objetivo

El objetivo de esta práctica será el de familiarizarse con los conceptos de **integridad y autenticidad**
a través del uso de **funciones resumen y de certificados**. En este parte se abordarán los conceptos
relacionados con las Funciones Resumen (Hash), vinculándola con la práctica anterior a través de la
firma de mensajes a encriptar/desencriptar.

# 2. Firma Mensajes

Además de conseguir confidencialidad (ya vista en la práctica anterior), a través de la firma de
mensajes podemos conseguir **autenticación** , entendiendo que el usuario que envía ese mensaje es
el que debe ser y no otro. Para ello, lo que se realizará, será la firma del mensaje a encriptar (no lo
encriptaremos en esta práctica ya que lo hicimos en la anterior) a través de funciones hash.

Para ello, copia la solución en la que utilizaste cifrado asimétrico a través de la librería _cryptography_
para hacer uso de la misma y proceder con la firma del mensaje creado. En este caso llama a la
nueva solución **_firma_mensaje.py_** para diferenciarla de la anterior.

Verifica que la solución es funcional y que se crea el mensaje inicial (a cifrar) de forma correcta. Este
será el mensaje a firmar.

Procede a realizar la **firma del mensaje con clave privada**. Esto permitirá a cualquier usuario que
tenga la clave pública verificar que el mensaje fue creado por alguien que tiene la clave privada. Las
firmas en RSA requieren de una función hash específica (función para transformar cualquier bloque
arbitrario de datos en una nueva serie de caracteres de longitud fija) y un relleno ( _padding_ ) para
poder ser utilizado. También se utilizará un _salt_ que consistirá en un conjunto de bits aleatorios que
se usa como entrada en una función.

Para hacer uso de las funciones resumen ( _hash_ ) y del relleno ( _padding_ ), añade los siguientes
módulos a la solución:

from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.asymmetric import padding

Ahora atiende a la variable que tenía el texto a cifrar, ya que será el mensaje que firmemos. Por
simplicidad, se recomienda crear una nueva variable ( _mensaje_firmar_ ) para evitar confusión. A esta
variable será a la que le pases un _string_ que determine el texto que se firmará, por ejemplo:
“Mensaje a firmar”.

Crea una variable llamada _firma_ que llame al método **sing()** de la clave privada, que será con la
que firmemos el mensaje. A este método, habrá que pasarle 3 parámetros, el mensaje a firmar, el
relleno a utilizar ( _padding_ ) y la función hash.


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 2

El mensaje se pasará sin definir propiedades ya que es un _string_ creado en la variable
_mensaje_firmar_. No olvides definirlo como cadena de bytes (añadiendo “b” al mensaje) para que
pueda ser tratado correctamente desde los métodos de cifrado/descifrado.

Ejemplo: **mensaje_firmar = b”Mensaje a firmar”**

Utilizaremos el método PSS ( _Probabilistic Signature Scheme_ ) para el _padding_ ya que es más complejo
y seguro que PKCS1. A este método hay que pasarle 2 parámetros: **_mgf_** que será un objeto de
función para la generación de máscara (únicamente soporta MGF1) y **_salt_length_** que determinará
el tamaño del _salt_ a utilizar (se suele emplear el tamaño máximo _PSS.MAX_LENGTH_ ).

Como ayuda, se ofrece la definición del _padding_ a utilizar:

**padding.PSS(
mgf=padding.MGF1(hashes.SHA256()),
salt_length=padding.PSS.MAX_LENGTH
),**

Como podemos ver, se crea el relleno mediante PSS atendiendo a los dos parámetros mencionados
anteriormente. Usaremos MGF1 para definir _mgf_ pasándole una función hash, en este caso que use
SHA ( _Secure Hash Algorithm_ ) de 256 bits empleado en seguridad criptográfica.

El último parámetro vendrá definido como la función hash a utilizar que deberá ser la misma que en
la definición del relleno. Por tanto estableceremos como método SHA256() quedando de la
siguiente forma:

**hashes.SHA256()**

Con esto conseguimos tener en la variable _firma_ la firma generada con la clave privada que teníamos
disponible anteriormente y el mensaje ( _string_ ) firmado.

Para verificarlo, **imprime por pantalla la firma**.

Para verificar que la firma cambia, crea otra nueva variable llamada _mensaje_firma2_ con un nuevo
mensaje (por ejemplo, “Mensaje a Firmar 2”) y ahora crea una nueva firma (variable _firma2_ ) para
este mensaje. Imprime por pantalla esta nueva firma para ver si se corresponde a la anterior o por
el contrario ha cambiado.

Con esto conseguiremos tener mensajes firmados que pueden ser cifrados (atendiendo a la anterior
práctica) para poder enviarlos a un destinatario. A través de esto, conseguimos autenticación de
datos y a través del cifrado confidencialidad.

# 3. Funciones Resumen

Como ya sabemos, las funciones resumen, también llamadas funciones hash o simplemente hash,
son algoritmos que consiguen crear una salida alfanumérica de longitud normalmente fija que
representa un resumen de la información, a partir de una entrada de datos.

Principalmente, esto se traduce en un proceso criptográfico generado por un algoritmo, pero se
diferencia con el resto de métodos criptográficos en que este no puede descifrarse, es decir, con
este método no es posible devolver el valor original del dato de entrada.

Por tanto, tendremos algo parecido a esto:


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 3

A la vista de la figura superior, no podemos a partir del “Valor Hash” deducir la entrada de datos.

En esta parte de la práctica, realizaremos varios cifrados de datos usando funciones hash que
devolverán un valor hash determinado, así como diferentes pruebas para verificar el
funcionamiento de este tipo de algoritmo.

## 3.1 Módulo hashlib

La librería estándar de Python ya nos propone el uso del módulo **hashlib** , cuya documentación está
disponible en: (https://docs.python.org/3/library/hashlib.html). Este módulo consigue implementar
una interfaz común para el uso de múltiples algoritmos seguros de hash. Entre ellos se incluyen los
siguientes: FIPS, SHA1, SHA224, SHA256 (ya usado), SHA384 y SHA512 (definidos en FIPS 180 - 2) y
también el algoritmo MD5 de RSA (definido en Internet RFC 1321).

Pese a que los términos más usados hoy en día son “Hash Seguro” y “Resumen del mensaje” (son lo
mismo), los algoritmos más antiguos se solían llamar algoritmos de “Digestión de Mensajes” (o
“Funciones de Digestión”), de ahí usar el método **digest()** en algunos casos.

En este módulo existe un método constructor para cada tipo de hash. Todos los métodos devolverá
un objeto hash con la misma interfaz independientemente del método que se use. En cualquier
instante se puede pedir el resumen de la concatenación de los datos introducidos hasta ese
momento atendiendo al método mencionado anteriormente **digest()** y al método
**hexdigest()** que devolverá realizará la misma función pero en hexadecimal.

Para probar todo lo explicado hasta el momento, vamos a utilizar el hash **SHA2 56** para cifrar un
mensaje e imprimirlo por pantalla.

En primer lugar, crea una nueva solución llamada, **_prueba_hash.py_** e importa el módulo **hashlib** que
hemos explicado anteriormente haciendo uso de la sentencia:

import hashlib

A continuación crea una nueva variable llamada _mensaje_ que contendrá un _string_ , por ejemplo,
“Mensaje a hashear”. Recuerda declararlo con la “b” inicial para tratarla como cadena de bytes.

Crea otra nueva variable llamada _mensaje_hash_ a la que, haciendo uso del objeto **_hashlib_** se llame
al método **sha256()** al que se le pasará el mensaje inicial.

A continuación, imprime dicha variable pasándole los métodos descritos anteriormente
( **digets()** y **hexdigets()** ) para verificar cómo se puede ver la información del hash que
obtenemos en ambos casos:

**Ejecuta el programa varias veces** (con 2 o 3 es suficiente) para verificar que el valor del hash es
siempre el mismo ya que el mensaje no cambia.

##### DATO

##### ENTRADA

##### FUNCION

##### HASH

##### VALOR

##### HASH


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 4

Ahora, realizaremos algunas **pruebas de concepto** sobre el cálculo de valores hash, modificando
algunos parámetros y verificando los hash encontrados.

1. Como primera prueba, **cambia el mensaje inicial** de la variable _mensaje_ para que ahora
    tenga el valor “Texto a hashear” (cambiamos la palabra _Mensaje_ por _Texto_ ) y vuelve a
    ejecutar el programa. (Puedes utilizar una nueva variable para ir apilando las diferentes
    pruebas). ¿Qué valor ofrecen ahora los métodos **digets()** y **hexdigets()**? ¿Varía con
    respecto a la ejecución inicial de la solución?. Al cambiar el mensaje, el resultado será
    totalmente diferente. Con esto podemos evitar que, si un atacante “captura” nuestro
    mensaje (por ejemplo en un ataque MitM ( _Man-In-The-Middle_ ), pueda modificar el valor
    inicial del mismo ya que no se podría obtener a partir del hash y si se modifica el emisor
    sabría que se ha modificado.
2. Prueba a **modificar el algoritmo SHA** por otro de la misma familia, por ejemplo por **SHA**
    y vuelve a ejecutarlo. ¿Qué obtenemos ahora?¿Cambia el Hash?¿Es más pequeño o más
    grande?
3. Además de la familia de algoritmos SHA, el módulo _hashlib_ puede usar otros como ya
    explicamos antes. Prueba ahora a modificar el **algoritmo por MD5** y compara el resultado
    que obtienes con el caso anterior. ¿Qué se obtiene?¿Cuál consideras que, a priori, es más
    seguro?¿Por qué?
4. La función **new()** devuelve un nuevo objeto de la clase hash que implementa la función
    hash que se le especifique. En este caso, el primer parámetro deberá ser una cadena con el
    nombre de la función hash que se quiera utilizar (“sha1”, “md5”, “sha256”, etc.) y el segundo
    parámetro cualquier tipo de cadena que queramos cifrar. Añade el uso de esta función a las
    pruebas realizadas anteriormente. Para ello, crea una variable a la que asignes una llamada
    a la función new pasándole el algoritmo _“sha256”_ y el mensaje _b”texto”_. Imprime esta
    variable utilizando el método **digets()** y **hexdigets()**. Cambia el algoritmo a otro de
    los conocidos y comprueba de nuevo la salida.
5. La función **update()** actualizará el objeto hash añadiendo nueva información
    (normalmente otra cadena). Pese a que se realice más de una llamada al método, será lo
    equivalente a realizar una única llamada. Utiliza este método para realizar el hash de un
    mensaje que actualizarás posteriormente. Para ello, crea una variable ( _mensaje_ ) y asigna
    directamente la llamada al objeto _hashlib_ usando el método **sha256()**. Posteriormente
    utiliza la función **uptate()** 3 veces (ya no hace falta usar el objeto _hashlib_ ) para actualizar
    el valor de la variable mensaje creada anteriormente. Puedes introducir el texto que quieras,
    por ejemplo, “ _mensaje_ ” en la primera actualización, “ _super” en la segunda_ y “ _secreto_ ” en la
    tercera. Posteriormente, muestra por pantalla el mensaje.

```
Hacer esto, equivaldría a realizar lo siguiente:
```
```
mensaje = hashlib.sha256(b”mensaje” + b”super” + b”secreto”)
```
6. Por último, **verifica la longitud de todos los hash generados** en las pruebas realizadas con
    anterioridad. Para ello, utiliza el atributo **digest_size** en las variables de mensajes
    encriptados mediante hash que has utilizado anteriormente.


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 5

## 3.2 Funciones resumen desde librería cryptography

En esta ocasión, atenderemos a las opciones que nos ofrece la librería cryptography para el uso de
funciones resumen (hash). Veremos casos muy similares a los expuestos anteriormente con el
módulo _hashlib_. Para acceder a toda la documentación relativa a este tipo de funciones resumen,
puedes acceder a: https://cryptography.io/en/latest/hazmat/primitives/cryptographic-hashes/.

En primer lugar, y por no aculumar muchas líneas de código y mezclar conceptos, crea una nueva
solución llamada _hash_cryptography.py_ para resolver esta parte de la práctica.

Para hacer uso de resúmenes de mensaje (Hashing), tendremos que importar la función
_default_backend()_ y el módulo _hashes_ para poder hacer uso de funciones resumen en este sentido.
Para ello, incorpora lo siguiente:

from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives import hashes

Una importados, ya podremos utilizar unas operaciones parecidas a lo que utilizamos en el apartado
anterior para llevar a cabo tareas de hash.

Para comprobar el funcionamiento básico de este tipo de operaciones utilizando la librería
_cryptography_ en primer lugar, crea un objeto llamado _digest_ que será a la que le pasemos el hash a
utilizar. Asigna a ese objeto una llamada al método **Hash()** haciendo uso del módulo _hashes,_ al
que le tendremos que pasar 2 parámetros: el algoritmo de hash a utilizar y el _backend_.

Pasa como algoritmo **SHA256()** y por como el segundo parámetro pasa el _backend_ por defento
( **default_backend()** ). Actualiza a través de **update()** el contenido de digest, puedes añadir
un par de mensajes como “ _Mensaje_ ” + “ _Secreto_ ”. Recuerda añadir la “b” inicial a los mensajes.

Por último, utiliza el método **finalize()** sobre el objeto digest. Este método finaliza el trabajo
en el contexto actual y devuelve el mensaje _digest_ como bytes.

**Imprime por pantalla las características del objeto** **_digest_** creado. En este caso, deberás imprimir la
cadena de bytes que devuelve el objeto, el propio objeto para verificar lo que devuelve, y el
algoritmo que está usando dicho objeto. Deberás obtener algo parecido a esto:

Ahora como **prueba final** , _cambia el mensaje anterior_ (puedes usar el mismo programa y cambiar la
cadenas a “ _Secret”_ + _“Message”_ para verificar si el hash calculado desde la librería _cryptography_
también cambia al igual que pasaba con la librería _hashlib_. ¿Cambia? ¿Se modifica el valor del objeto
creado cuando mostramos el algoritmo del mismo en cada ejecución?. Intenta razonar el porqué de
estos posibles cambios/no cambios.

Realiza alguna **prueba extra** sobre el programa realizado haciendo uso de la librería _cryptography_
para verificar su funcionamiento. Por ejemplo, **cambia el algoritmo** elegido para ver cómo se
comporta el uso de funciones hash en este tipo de aplicaciones.

# 3. Autenticación de Usuarios

Como ya sabemos, la autenticación de usuarios es una acción imprescindible hoy en día para poder
acceder a sistemas, edificios y otras entidades. Por ese motivo, esta parte de la práctica, aborda la
creación de un sistema de autenticación basándose en varios formatos de almacenamiento de
credenciales.

## 3.1 Creación de Fichero de Usuarios

Pese a que los registros de usuario se suelen almacenar en una Base de Datos dedicada que contiene
también seguridad de acceso, para abordar esta práctica, crearemos ficheros que harán las veces
de repositorio de datos que contendrán los datos de los usuarios. En este caso, utilizaremos **un
fichero de texto** que almacenará información codificada en bytes.

En dicho fichero, guardaremos la siguiente información relativa a los usuarios: **Nombre, Salt** y
**Resumen de Contraseña.** Esto nos permitirá almacenar el **nombre** (en texto plano), un **salt** que será
un conjunto de bits aleatorios que se usan como una de las entradas en una función derivadora de
clases y el **Resumen de la Contraseña** que será calculado con una función de resumen (hash) que
sea capaz de encriptar esta contraseña ya que **NUNCA SE DEBEN ALMACENAR CONTRASEÑAS EN
TEXTO PLANO**.

Para comenzar, crea una solución Python llamada **_CreaTxt.py_** que contendrá el código necesario
para generar un fichero de texto con la información necesaria para el registro de usuarios
atendiendo a los datos ofrecidos anteriormente (nombre y resumen de contraseña).

Utilizaremos la librería **_cryptography_** para poder abordar la solución por lo que importa lo necesario
para hacer uso de ella:

from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

Como puedes comprobar, además del módulo _hashes_ y la función _default_backend_ que ya fueron
incluidos en anteriores prácticas, añadimos la clase _PBKDF2HMAC_ ,que serán funciones de
derivación de claves con un gasto computacional variable y que se utilizan para reducir la
vulnerabilidad de los ataques por fuerza bruta.


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 32

Además de esto, importa también los módulos **_os_** que me permitirá realizar operaciones
dependientes del Sistema Operativo y el módulo **_Base64_** que me permitirá codificar datos binarios
en caracteres ASCII imprimibles y decodificar dichas codificaciones en datos binarios:

import os

import base64

La solución completa se basará en la petición de un nombre y una contraseña (en texto plano) al
usuario que lo ejecuta para posteriormente almacenar los datos mencionados anteriormente en un
fichero de texto. Se deberá ejecutar la solución tantas veces como usuarios necesitemos crear. Se
recomienda usar como contraseña para la autenticación del usuario **_conX_** , siendo _X_ la inicial del
nombre del usuario en mayúscula para no olvidarla. El formato del fichero será este: _nombre, salt,
resumen_contraseña_ :

Define una función principal en la que pidas un usuario y contraseña almacenándolos cada uno en
una variable. Utiliza le método **input()** para ello. A continuación, llama a una función con nombre
**alta_usuario(nombre, contraseña)** , esta será la función que nos permita añadir un
usuario al archivo de texto mencionado.

Como ya conocemos, para dar de alta al usuario en el fichero necesitamos obtener un _salt_ y un
resumen de contraseña (o hash de la contraseña), por lo que, antes de completar esta función, crea
una función llamada **genera_salt()** que nos permita generar un _salt_ aleatorio de tamaño= 16
bytes. Para llevar a cabo esto, esta función únicamente devolverá el resultado de la llamada a la
función **urandom(tamaño)** desde el módulo _os_.

Una vez que tenemos calculado el hash, habrá que obtener el resumen de la contraseña a partir del
_salt_ calculado anteriormente. Para esto, crea una función llamada **hasheo_password** a la que
se le pasará la **_contraseña_** **en texto plano** y el **_salt_** calculado de la función anterior. En esta función
es donde utilizaremos la derivación de clave (PBKDF2HMAC) para generar confusión y que la clave
no sea accesible por ataques externos al propio sistema de autenticación. Crea una variable llamada
_der_clave_ a la que se le pasa un objeto de la clase PBKDF2HMAC que vendrá definido con las
siguientes características:

- Algoritmo: SHA256
- Longitud: 32 bytes
- Salt=Salt (ya fue generado anteriormente)
- Iteraciones: 100000
- Backend: default_backend()

Además de este objeto, en esta función deberemos crear una variable que nos permita derivar este
objeto. Para ello, crea una variable llamada _hash_bytes_ que almacenará la derivación de claves
siguiente:


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 33

**hash_bytes = der_clave.derive(contraseña.encode())**

Esta función devolverá (return) la decodificación de esa variable ( _hash_bytes_ ) en base 64 de la
siguiente forma:

**return base64.b64encode(hash_bytes).decode()**

Con esto, ya tendríamos “hasheada” la contraseña haciendo uso del salt inicial usando un algoritmo
SHA256.

Volviendo a la función **alta_usuario** , ya tendríamos definido por tanto el _salt_ y el _hash de la
contraseña_ por lo que, lo único que nos faltaría realizar sería almacenarlo en un fichero para su
posterior tratamiento.

Crea un fichero llamado _usuarios.txt_ en el que se almacenarán los valores obtenidos separados por
comas (,), esto nos servirá como delimitador para poder autenticar usuarios sin problema. No
olvides utilizar la base64 para realizar las operaciones de decodificación del salt y pasar nombre de
usuario y hash de contraseña. La llamada de escritura en el archivo puede ser la siguiente:

```
f.write(f"{nombre},{base64.b64encode(salt).decode()},{hash_contraseña}\n")
```
Por último imprime por pantalla si el usuario ha sido añadido (o no) con éxito en el fichero de texto.

Como posible **mejora opcional** , puedes evitar que un usuario repita su nombre de usuario dentro
del fichero de registro de usuarios, es decir, que no puedan existir dos usuarios con el mismo
nombre. Realiza lo necesario para que esto se lleve a cabo.

## 3.2 Autenticación de Usuarios desde Fichero

Una vez creado el fichero que almacenan a los usuarios atendiendo al nombre, el salt y contraseña
(encriptada) – _usuarios.txt_ , procederemos a la creación del sistema de autenticación de usuarios.
Para ello, crea una nueva solución llamada **_Autentica.py_** que contendrá el código necesario para
realizar este tipo de sistemas.

Este sistema en su función principal, el programa deberá solicitar al usuario un nombre de usuario
y una contraseña (para poder autenticarlo). A continuación, llamará a la función
**autentica_usuario** a la que se le pasará dichos parámetros para poder autenticarlo.

Antes de comenzar a definir la función para autenticar usuarios, debemos crear una función que sea
capaz de verificar la contraseña que tenemos almacenada ya que la hemos creado a partir de
funciones hash. Crea una función **verifica_password** a la que se le pase la contraseña (en
texto plano), el salt (que ya tenemos almacenado en el fichero) y el resumen de la contraseña (hash)
que también tenemos almacenado.

Esta función volverá a crear un nuevo objeto llamado _der_clave_ para el derivador de clave al que se
asignará la clase PBKDF2HMAC con los mismos parámetros que en la anterior solución, es decir:

- Algoritmo: SHA256
- Longitud: 32 bytes
- Salt=Salt (será el que recuperemos del fichero más adelante)
- Iteraciones: 100000
- Backend: default_backend()

Para hacer el programa más robusto crea una construcción _try..._ para manejar posibles errores de
tiempo de ejecución en la verificación de la contraseña.


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 34

Dentro del bloque _try_ utiliza el objeto creado anteriormente ( _der_clave_ ) para verificar si la
contraseña (codificada) coincide con el resumen de contraseña almacenado. Si es así, devuelve
**True**. Se puede verificar de la siguiente forma:

**der_clave.verify(contraseña.encode(), base64.b64decode(hash_almacenado))**

Como puedes ver, se usa el método **verify()** para verificar la contraseña codificada y el
_hash_almacenado_ en base64.

En el bloque _except Exception:_ únicamente se deberá devolver _False_ en caso de que no se pueda
verificar esa contraseña.

Una vez completada esta función, estaremos en disposición de abordar la función previa llamada
**autentica_usuario** , para poder autenticar usuarios. Esta será la función raíz de la presente
solución ya que será capaz de autenticar a los usuarios almacenados en el sistema devolviendo el
resultado de la autenticación que podrá ser:

- Autenticación correcta (usuario y contraseña son correctos y autenticados)
- Contraseña incorrecta (el usuario existe pero la contraseña no es correcta)
- Usuario no encontrado (el usuario no existe)

Añadiremos también funcionalidad extendida que verifique si no existe fichero de usuarios (o no se
encuentra) o si existe cualquier otro error al autenticar no especificado anteriormente.

Para llevar a cabo esta solución crea de nuevo una construcción _try..._ que nos permita verificar si el
código ejecutado se lleva a cabo correctamente o genera algún tiempo de excepción en tiempo de
ejecución.

Dentro del bloque _try_ abre el fichero de usuarios en modo lectura y a continuación lee los datos que
contiene con una estructura for. Esto nos permitirá ir avanzando línea a línea por el mismo. Utiliza
una variable llamada _datos_ para almacenar lo que se va leyendo en cada línea. Ten en cuenta que
los datos están separados por comas (,) por lo que habrá que usar este separador para almacenar
estos datos. Utiliza el método **strip()** para eliminar los espacios en blanco y **split(,)** para
determinar el carácter separador (coma).

A continuación, comprueba si la longitud de la variable _datos_ es 3 y determina cada uno de los
campos guardados en la variable _datos_ para almacenarlos en 3 variables independientes. Es decir,
realiza lo siguiente:

**nombre_almacenado, salt_almacenado, hash_almacenado = datos**

Con esto conseguimos tener 3 variables con los valores adecuados extraídos del fichero de usuarios.

Ahora tendremos que pasar a verificar si las variables coinciden con lo que tenemos en función del
nombre, por tanto, si el nombre que se le pasa al sistema es el mismo que nombre_almacenado,
deberemos recuperar el salt teniendo en cuenta la decodificación del mismo en base64. Puedes
usar algo parecido a esto:

salt = base64.b64decode(salt_almacenado)

A continuación, habrá que llamar a la función para verificar la contraseña ( **verifica_password** )
a la que se le pasará la contraseña, el salt recuperado y el hash almacenado. Por lo tanto, si la
verificación es correcta, el programa imprimirá “Autenticación Correcta” y devolverá _True_. Sino,
imprimirá “Contraseña Incorrecta”, ya que verificó que existía un usuario con ese nombre pero la
contraseña no se verificó.

Si el programa recorre el _for_ inicial y no encuentra al usuario, devolverá el mensaje “Usuario no
encontrado” y devolverá _False_.


```
Área de Arquitectura y Tecnología de Computadores
ASIGNATURA DE:
```
### SLGD 35

Para finalizar, ten en cuenta la captura de dos excepciones:

- _FileNotFoundError_ por si no encuentra el fichero de usuarios
- _Exception_ por si se produce cualquier otro error al autenticar

Con todo esto conseguimos autenticar a un usuario de forma segura atendiendo a un fichero de
texto en el que se almacenan los datos necesarios para proceder con la autenticación.
