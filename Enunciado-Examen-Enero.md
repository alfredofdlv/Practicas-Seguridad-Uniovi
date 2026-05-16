
Dado un pcap 
1-a Obtener numero de paquetes mediante wireshark
1-b % de paquetes con tcp
1-c Identifica la IP creando filtro para visualizar paquetes emitidos por esta IO 
1-d Sí, hay picos de tráfico. -> Gráfica de E/S

APARTADO 2. Conexiones remotas
a) Conexión FTP
a. Se establece alguna conexión queutilice protocolo FTP???? FILTROS POR PROTOCOLO Y POR PUERTO
_ws.col.protocol == "FTP" para el filtro como protocolo
tcp.port == 21 filtro con puerto (ftp.port no deja)
b. Cuantos paquetes se emiten desde el equipo que esta capturando del trafico de este tipo
c. Que usuario se utiliza para la conexión FTP
d. Se finaliza la conexión FTP de alguna forma?? Quien informa sobre el cierre de esta seion?? Haz el
filto, para ver i se lleva a cabo, quien y informacion ofrece para el cierre de la conexion
b) Verificación DNS
a. Cual es la IP correspondiente al servidor DNS utilizado desde el equipo que captura el trafico?
b. Se utiliza DNS hacia algún sitio de Google?? Verifica si el equipo hace consulta dns.qry hacia esa
ubicación. Determina el numero de paquetes totales que se visualizan y utiliza un filtro adecuado
para verificarlo


APARTADO 3. Intercambio de pings entre dispositivos
a) Crea un filtro que permita ver todos los intentos de pings realizados. Permite que se ven peticiones resquest
y reply. Cuantas veces se lanza el comando suponiendo que se realiza desde un equipo Windows y que en
cada ejecución se realizan 4 intentos de conexión?? Todos los pines reciben respuesta?? Captura pantalla
con filtro y solución
b) Limita filtro anterior para que únicamente se muestren por pantalla los paquetes de tipo reply. Estos tienen
un tipo de paquete = 0. cuantos paquetes hay??


APARTADO 4.
Se ha detectado varios intentos de acceso a la config del router que da acceso a internet, se ha determinado
conexión se realiza a ip 192.168.1.1 o 192.168.0.1. piden que determinemos nombre del usuario con el que se ha
intentado, y contraseña en texto plano con la que esta intentando acceder. Para ello crea un filtro en el que se
delimiten los paquetes que intentan acceder al dispositivo (ip de destino = la del router localizado) y el protocolo y
método por el que se tiene acceso a esta información. Realiza captura de pantalla de todos los intentos de login en
el que aparezcan nombres de usuarios utilizados y a contraseña en texto plano (se debe ver el filtro usado)