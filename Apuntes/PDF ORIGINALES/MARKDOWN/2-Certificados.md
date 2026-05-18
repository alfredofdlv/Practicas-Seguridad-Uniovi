https://gemini.google.com/share/6eb494fafe4d

# Tipos de certificados:

```
Windows almacena certificados en 2 almacenes diferentes:
```
- Certificados de Usuario
- Certificados de Equipo (se necesita ser administrador para poder
    administrarlos)

# Buscar Certificados:

```
Poner en la barra de búsqueda: certificados
```
```
Administrar Certificados de usuario
```
## Anatomía de un Certificado (Las 3 Pestañas Clave)

- **General (Información Básica)** : Aquí encontrarás los propósitos del certificado, para
    quién fue emitido ("Emitido para"), quién lo emite ("Emitido por") y su periodo de
    validez.
- **Detalles (Datos Técnicos)** : Muestra el contenido del certificado campo por campo;
    al seleccionar un campo en la lista superior, su contenido exacto se muestra en la
    ventana inferior.

```
o Campos Críticos en "Detalles" : En esta pestaña es donde el profesor te
pedirá buscar la "Clave pública", la "Huella digital" (Thumbprint) o el
"Identificador de clave del titular".
```
- **Ruta de Certificación** : Muestra la jerarquía (la ruta) desde tu certificado hasta la
    entidad raíz, además de indicar el estado actual del certificado (por ejemplo,
    "Certificado válido").

```
o Ruta en Certificados Raíz : Recuerda que en el caso de abrir un certificado
raíz, esta pestaña no mostrará ninguna ruta hacia arriba, ya que él es el
inicio de la cadena
```
**Truco de Examen (Certificados Raíz)** : Si te preguntan **cómo saber a simple vista si un
certificado es un "Certificado Raíz" mirando la pestaña General** , la respuesta es que en estos
certificados el campo "Emitido para" es exactamente igual al campo "Emitido por".

## Resolución de Problemas de Confianza (¡Pregunta típica de examen!)

Un escenario clásico de examen es que te den un certificado instalado que muestra un error y
te pidan arreglarlo.

- **Identificar el Error** : Si al abrir el certificado ves un mensaje en la parte superior
    indicando que "Windows no tiene la suficiente información para comprobar este
    certificado", tienes un problema con la cadena de certificación.
- **Comprobación del Estado** : Si vas a la pestaña "Ruta de certificación", verás que no hay
    ruta disponible y el estado indicará que no se puede encontrar al emisor del
    certificado.


- **La Solución** : Para arreglar esto, debes instalar el certificado de la Autoridad
    Certificadora (el archivo .cer de quien emitió tu certificado) en el sistema.
- **Almacén Correcto** : Durante el asistente de importación de este certificado raíz, es vital
    que selecciones manualmente el almacén llamado "Entidades de certificación raíz de
    confianza".
- **Anclaje de Confianza** : Al aceptar esta instalación, creas un nuevo anclaje de confianza,
    haciendo que el computador confíe en todos los certificados emitidos por esa
    autoridad, arreglando el error del certificado original.

## Almacenamiento Físico de los Certificados (Nivel Avanzado)

A veces, los profesores quieren comprobar si entiendes qué hace el sistema operativo "por
debajo" de la interfaz gráfica.

- **Ubicación Oculta** : Los certificados se guardan como archivos físicos en directorios
    ocultos del sistema, generalmente en la ruta
    C:\Users\Usuario\AppData\Roaming\Microsoft\SystemCertificates\My\Certificates
- **Relación Nombre-Huella** : Si te piden buscar el archivo físico de un certificado concreto,
    el nombre de ese archivo coincidirá exactamente con la "Huella digital" que aparece en
    la pestaña Detalles del certificado.
- **Ubicación de la Clave Privada** : Las claves privadas asociadas se guardan en un
    directorio diferente llamado Keys (dentro de la misma ruta).

```
C:\Users\Usuario\AppData\Roaming\Microsoft\SystemCertificates\My\Keys
```
- **Relación Nombre-Clave** : El nombre del archivo físico de la clave privada coincide con el
    valor del campo "Identificador de clave del titular" del certificado.
- **Peligro al Borrar** : Si eliminas un certificado desde la interfaz visual (certmgr), su archivo
    se borra, pero la clave privada RSA asociada no se elimina automáticamente del
    directorio Keys.

```
Certificados de Equipo / Local Machine (certlm.msc
```
**1. Los Certificados (La parte pública)**

```
A diferencia de los tuyos, los certificados de equipo no se guardan como archivos
convencionales en una carpeta. Se guardan como bloques de datos binarios (BLOBs)
directamente dentro del Registro de Windows.
```
```
Puedes encontrarlos abriendo el Editor del Registro (regedit) en las siguientes rutas:
```
- **Ruta principal:**
    HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SystemCertificates
- **Certificados instalados por Políticas de Grupo (GPO):**
    HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\SystemCertificates

```
Si entras ahí, verás carpetas con nombres como My (Personal) o Root (Entidades de
confianza), y dentro verás claves de registro con nombres larguísimos: esa es la Huella
Digital (Thumbprint) del certificado.
```

**2. Las Claves Privadas (La parte secreta)**

```
Esta es la parte física. Las claves privadas asociadas a los certificados del equipo sí se
guardan en el disco duro, pero en una ubicación oculta a la que ni siquiera un
administrador tiene acceso fácil por defecto.
```
```
Se guardan en las siguientes rutas físicas:
```
- **Para claves RSA tradicionales:**
    C:\ProgramData\Microsoft\Crypto\RSA\MachineKeys
- **Para claves CNG (Cryptography Next Generation, más modernas):**
    C:\ProgramData\Microsoft\Crypto\SystemKeys o
    C:\ProgramData\Microsoft\Crypto\Keys

```
Los archivos dentro de estas carpetas no tienen la extensión .pfx ni .cer; tienen
nombres que son cadenas alfanuméricas ininteligibles generadas por el sistema
criptográfico de Windows.
```
# Creación Certificados

Formas de crear certificados:

```
1 - Utilizando una autoridad de certificación pública a la que se puede acceder vía
web
2 - Instalando una autoridad certificadora propia que emita certificados
("Certificate Server" de Windows Serve)
3 - Sencillo programa que permita crear certificados
4 - cmdlet en PowerShell usando el comando New-SelfSignedCertificat
```
**Abrir el PowerShell ISE**

Comprobar que la ejecución Scripts está restringida :

**Get-ExecutionPolicy**

Activar la ejecución

**Set-ExecutionPolicy –Scope CurrentUser Unrestricted**

**Si a todo**

**Generar Certificado raíz**

$cert = New-SelfSignedCertificate -Type Custom ` -Subject "CN=zpac.as" ` -KeyAlgorithm RSA -
KeyLength 2048 -KeySpec Signature -KeyExportPolicy Exportable ` -KeyUsageProperty All -
KeyUsage None ` -Provider "Microsoft Enhanced RSA and AES Cryptographic Provider" ` -
NotBefore (Get-Date) ` -NotAfter (Get-Date).AddYears(10) ` -HashAlgorithm sha256 ` -
TextExtension @("2.5.29.19={critical}{text}ca=1") ` -CertStoreLocation "Cert:\CurrentUser\My"


**La Trampa del Examen (TextExtension)** : Para que un navegador como Firefox acepte tu
certificado como una Autoridad Certificadora real, debes incluir **obligatoriamente** el parámetro

- TextExtension @("2.5.29.19={critical}{text}ca=1"). Si no lo pones, el certificado se crea, pero
no funcionará como CA.

**Recuperar la variable** $cert

Puedes buscar su Huella Digital (Thumbprint) usando

Get-ChildItem -Path "Cert:\CurrentUser\My"

y luego cargarlo de nuevo en la variable con:

Get-ChildItem -Path "Cert:\CurrentUser\My\AQUÍ_LA_HUELLA_DIGITAL"

## Explicacion Parámetros:

**- Type:** Especifica el tipo de certificado creado. Aquí se utiliza el tipo Custom. Otros tipos son
CodeSigningCert, DocumentEncryptionCert y SSLServerAuthentication (defecto).
**- KeyAlgorithm:** Especifica el algoritmo para el que se crean las claves asimétricas asociadas al
certificado. Los valores posibles son RSA y ECDSA.
**- KeyLength:** Especifica la longitud en bits de la clave que es asociada con el nuevo certificado.
No existe un valor por defecto.
**- KeySpec:** Especifica si la clave privada asociada con el nuevo certificado se puede usar para
firmar, cifrar o ambas cosas. Los valores aceptables son KeyExchange, Signature y None
(defecto). El valor None indica que se usa el valor por defecto que utiliza el proveedor de
servicios criptográficos.
**- KeyExportPolicy:** Especifica la política que gobierna la exportación de la clave privada asociada
con el certificado. Los valores aceptables son: Exportable, ExportableEncrypted (defecto) y
NonExportable. Exportable: **Vital**. Si no pones esto, luego no podrás exportar el certificado con
su clave privada en formato .pfx
**- keyUsageProperty:** Especifica los usos de la clave para la propiedad “Usos de clave” de la clave
privada. Los valores aceptables para este parámetro son: All, Decrypt, KeyAgreement, None
(defecto) y Sign. El valor None indica que el comando usa el valor por defecto que utilice el
proveedor de servicios de claves.
**- KeyUsage:** Especifica los usos de clave establecidos en la extensión de uso de clave del
certificado. Los valores aceptables para este parámetro son: CertSign, CRLSign,
DataEncipherment, DecipherOnly, DigitalSignature, EncipherOnly, KeyAgreement,
KeyEncipherment, None (defecto) y NonRepudiation. El valor predeterminado, None, indica
que este cmdlet no incluye la extensión KeyUsage en el nuevo certificado. El uso de la clave se
restringe a los valores especificados en este parámetro. Por ello es mejor no restringir el uso
indicando None.


**- Provider:** Especifica el nombre del proveedor de servicios criptográficos (CSP) o del proveedor
de almacenamiento de claves (KSP). Consultar la ayuda para determinar los proveedores
disponibles. Si no se indica nada se determina un proveedor en función del parámetro –
KeySpec. Por defecto: “Microsoft Base Cryptographic Provider v1.0”. Es esencial usar
“Microsoft Enhanced RSA and AES Cryptographic Provider” para evitar limitaciones en el uso
de las claves privadas.
**- NotBefore:** Indica la fecha de inicio del período de validez del certificado.
**- NotAfter:** Indica la fecha de finalización del período de validez del certificado.
**- HashAlgorithm:** Especifica el nombre del algoritmo de hash usado en la firma del nuevo
certificado. El algoritmo por defecto depende del proveedor que almacena la clave privada
usada para firmar el nuevo certificado.
**- TextExtension:** En este caso se utiliza para indicar que el certificado es de una Autoridad
Certificadora. Es necesario para que el navegador Firefox permita cargarlo en el almacén de
raíces de confianza.
**- CertStoreLocation:** Especifica el almacén en que se almacena el nuevo certificado. Solo se
puede especificar dos almacenes de certificados: Cert:\CurrentUser\My o
Cert:\LocalMachine\My. NO se pueden usar otros almacenes de certificados.

**Creación de Certificados de Servidor y Usuario**

Una vez tienes tu CA (en $cert), vas a crear certificados "hijos" para servidores o usuarios. Los
parámetros cambian un poco respecto al certificado Raíz:

- **El parámetro de Firma (-Signer)** : Esta es la diferencia más importante. A los certificados
    de servidor y usuario debes añadirles el parámetro -Signer $cert. Esto le dice a
    PowerShell: _"Usa la clave privada de mi CA para firmar este nuevo certificado"_.
- **Nombres DNS (-DnsName)** : Muy útil para servidores. Te permite añadir la extensión
    "nombre alternativo del sujeto" para que un mismo certificado sirva para varios
    dominios (ej. "zpser.as", "www.zpser.es", "[www.zpser.com](https://www.zpser.com)"). Si usas
    esto, no es estrictamente necesario usar el parámetro -Subject.
- **Tipo de Clave (-KeySpec)** : A diferencia de la CA (que usa Signature para firmar), en los
    certificados de servidor/usuario este parámetro suele cambiar a KeyExchange.
- **NotBefore / -NotAfter** : Controlan la validez. Normalmente usarás (Get-Date) para el
    inicio y (Get-Date).AddYears(X) para la caducidad.

**Servidor**

New-SelfSignedCertificate -Type Custom ` -Subject "CN=zpser.as" -DnsName "zpser.as",
"www.zpser.es", "www.zpser.com" ` -KeyAlgorithm RSA -KeyLength 2048 -KeySpec
KeyExchange -KeyExportPolicy Exportable ` -KeyUsageProperty All -KeyUsage None ` -Provider
"Microsoft Enhanced RSA and AES Cryptographic Provider" ` -NotBefore (Get-Date) ` -NotAfter
(Get-Date).AddYears(5) ` -HashAlgorithm sha256 ` -Signer $cert ` -CertStoreLocation
"Cert:\CurrentUser\My"

En - **TextExtension**

oid=2.5.29.37 "Enhanced Key Usage"


oid=1.3.6.1.5.5.7.3.1 "Server Authentication"

**Usuario**

New-SelfSignedCertificate -Type Custom ` -Subject "CN=zpusu.as" -DnsName "zpusu.as” ` -
KeyAlgorithm RSA -KeyLength 2048 -KeySpec KeyExchange -KeyExportPolicy Exportable ` -
KeyUsageProperty All -KeyUsage None ` -Provider "Microsoft Enhanced Cryptographic Provider
v1.0" ` -NotBefore (Get-Date) ` -NotAfter (Get-Date).AddYears(5) ` -HashAlgorithm sha256 ` -
Signer $cert ` -CertStoreLocation "Cert:\CurrentUser\My"

# Exportación Certificados

Hay 2 posibilidades:

1.-Exportar solamente el certificado

```
2.-Exportar el certificado juntamente con su clave privada asociada.
```
Clic derecho + Todas las Tareas + Exportar

### EXPORTACIÓN PARA LA AUTORIDAD CERTIFICADORA

Sin Clave Privada

- **DER** Es el más común (Usar este si no dice nada)
- **Base 64:** A diferencia del DER, este sí se puede abrir y leer en texto plano con el
    Bloc de notas. Útil si necesitas copiar y pegar el certificado en un formulario we
- **PKCS#**
    o Doble clic al generado -> se abre para visualizar el contenido del fichero.
    o El resto te lleva a la ventana Certificado que te permite instalarlo en el
       almacén.
    o Útil cuando hay que almacenar una cadena de certificados, pero en el caso de
       una autoridad certificadora, solo se almacena un fichero, por lo que no es útil.
       Porque permite incluir toda la " **ruta de certificación** " (la cadena de
       certificados)

Con Clave Privada

Una Autoridad Certificadora **solo** debe exportar la clave privada para disponer de un backup

En las practicas se usa PKCS#12. Se recomienda seleccionar TODAS las opciones, EXCEPTO
Eliminar la clave privada si la exportación es correcta.

```
Contraseña : conacpfx zpACas.pfx
```
En el apartado de cifrado dejar TripleDES-SHA

### EXPORTACIÓN PARA EL SERVIDOR

SIN clave privada solamente en formato DER binario. _zpSERas.cer_


CON clave privada, usando como contraseña **conserpfx** _zpSERas.pfx_

### EXPORTACIÓN PARA EL USUARIO

SIN clave privada solamente en formato DER binario. zpUSUas.cer.

CON clave privada, contraseña conusupfx zpUSUas.pfx.

### RESUMEN

**.pfx -> Con clave privada**

**.cer -> Sin clave privada SOLO LA PUBLICA**

**Solo el certificado (Sin Clave Privada):** Lo usas cuando quieres que otros confíen en ti o te
envíen cosas cifradas. Es público.

## Certificado + Clave Privada: Lo usas para hacer una copia de seguridad (backup) o para

## llevarte tu identidad a otro ordenador.

# Carga Certificados

**Ubicación del Almacén:** Selecciona **"Usuario actual"** (a menos que el examen te pida
explícitamente instalarlo para todo el equipo local, lo cual requiere ser administrador)

**Cargar el Certificado de Usuario (El archivo .pfx)** Este es el archivo que contiene tu identidad
completa (pública y privada).

- **Inicio:** Haz doble clic sobre el archivo zpUSUas.pfx. Esto abrirá el Asistente para
    importación.
- **Ubicación del Almacén:** Selecciona **"Usuario actual"** (a menos que el examen te pida
    explícitamente instalarlo para todo el equipo local, lo cual requiere ser administrador).
- **La Contraseña:** El asistente te pedirá la clave con la que protegiste el archivo en la
    sección anterior (según el guion, conusupfx).
- **Opciones de Importación (¡Pregunta de examen!):**

```
o NO habilites la protección segura de clave privada.
```
```
o SÍ marca la clave privada como exportable
```
```
o SÍ incluye todas las propiedades extendidas.
```
- **El Almacén Destino: No dejes que Windows elija automáticamente.** Selecciona
    "Colocar todos los certificados en el siguiente almacén", pulsa Examinar, marca
    "Mostrar los almacenes físicos" y selecciona el almacén **Personal/Registro**.


- En la mayoría de las ocasiones en las que se carga un certificado se usará la que tenga
    clave privada .pfx para poder firmar a menos que se quiera cargar la Autoridad
    Certificadora (tu CA), entonces es el .cer.
**3. La Trampa del Examen (El Error de Confianza)** Una vez importado el .pfx, si abres la
herramienta certmgr.msc y haces doble clic en tu certificado de usuario recién importado,
verás algo alarmante:
- **El Mensaje:** En la pestaña General dirá: _"Windows no tiene suficiente información para
comprobar este certificado"_.
- **La Ruta Rota:** Si vas a la pestaña "Ruta de certificación", verás que no hay ruta y dice
que no encuentra al emisor.
- **¿Por qué pasa esto?** Porque tu sistema no conoce a la Autoridad Certificadora (tu CA)
que emitió este certificado. ¡Es completamente normal en este punto! (A veces, al
importar el PFX, Windows cuela el certificado de la CA en la carpeta Personal; si lo ves
ahí, bórralo, porque ese no es su sitio).
**4. Arreglar la Cadena: Importar la Raíz (El archivo .cer)** Para solucionar el error anterior, debes
decirle a tu ordenador: _"Oye, confía en esta Autoridad Certificadora que he creado"_.
- **Inicio:** Haz doble clic sobre el archivo zpACas.cer (tu certificado Raíz sin clave privada).
- **Instalar:** Pulsa el botón "Instalar certificado...".
- **El Almacén Crítico (¡Ojo aquí!):** Selecciona "Usuario actual", pero esta vez, al elegir el
almacén manualmente, debes seleccionar **"Entidades de certificación raíz de
confianza"**. _Deja que el asistente elija el almacén físico._
- **La Advertencia de Seguridad:** Windows te lanzará una alerta roja preguntando si estás
seguro de instalar un certificado de una CA que dice representar a zmAC.as. Esto es el
sistema protegiéndote de crear "anclajes de confianza" falsos. Dile que **SÍ**.
**5. La Verificación Final (El Momento de la Verdad)** Para demostrar al profesor que todo está
perfecto:
- Abre certmgr.msc.
- Ve a la carpeta **Personal > Certificados** y haz doble clic en tu certificado de usuario
(zpusu.as).
- Ve a la pestaña **Ruta de certificación**.
- **El Resultado:** Ahora deberías ver una jerarquía clara (tu CA arriba y tu usuario colgando
de ella) y en el estado del certificado pondrá: **"Este certificado es válido"**.

**Puntos extra para nota:** Si el profesor te pregunta "¿dónde guarda Windows realmente estos
certificados que acabamos de importar?", recuerda que no están "dentro" del certmgr, sino
como archivos físicos en:
C:\Users\TuUsuario\AppData\Roaming\Microsoft\SystemCertificates\My\Certificates (y las
claves privadas en la carpeta \Keys de esa misma ruta).

Para saber que archivo hay que mirar :

- Certificates – Huella Digital


- Keys - Identificador de clave del titular

# Firma

## 1. Preparación de la Herramienta

- **Software Requerido** : Se presupone el uso de **Adobe Acrobat Reader**. Si el

## examen se realiza en una máquina virtual y no está instalado, deberás

## descargarlo desde su web oficial e instalarlo.

- **Acceso a la Herramienta de Firma** : Abre el documento PDF en Adobe Reader.

## Debes localizar y acceder a la pestaña de "Herramientas".

- **Seleccionar la Acción** : Dentro de las herramientas disponibles, debes buscar y

## hacer clic en la opción "Utilizar un certificado".

## 2. El Proceso de Firma (Paso a Paso)

- **Iniciar la Firma** : Al seleccionar la herramienta anterior, se abrirá un submenú

## superior. Haz clic en el botón "Firmar Digitalmente".

- **Área de Firma** : Verás que el cursor del ratón cambia y se convierte en una cruz.

## Tu tarea es pinchar y arrastrar para dibujar un rectángulo en el documento;

## este será el espacio físico donde aparecerá el sello visual de tu firma.

- **Selección del Certificado** : Inmediatamente aparecerá un cuadro de diálogo

## mostrando todos los certificados válidos para firma que tienes en tu almacén

## personal de Windows (por ejemplo, el de la FNMT). Selecciona el que te

## indique el profesor y pulsa "Continuar".

## 3. Auditoría y Configuración antes de Firmar (¡Atención al examen!) Esta es la

## pantalla crítica donde los profesores suelen pedir comprobaciones.

- **Verificación de Detalles** : Antes de darle al botón final, acostúmbrate a pinchar

## en "Ver detalles del certificado".

- **Revisión de la Cadena** : El panel izquierdo te mostrará la jerarquía. Te pueden

## pedir que verifiques las propiedades del certificado del usuario y también las

## propiedades de la entidad emisora (ej. "FNMT Usuarios").

- **Pestañas de Información** : Debes navegar por las diferentes pestañas (Detalles,

## Revocación, Confianza, Normativas y Aviso Legal) para comprobar que todo

## está en orden, tal como hacías en certmgr.

- **La Trampa del Bloqueo** : Cuando vuelvas a la ventana de firma principal,

## verifica cuidadosamente que la casilla "Bloquear el documento tras la firma"

## NO esté marcada. Si la marcas, el documento quedará cerrado y nadie más (ni

## el profesor ni un tercer compañero) podrá añadir su firma.

- **Guardar el Archivo** : Al pulsar "Firmar", el programa te pedirá que guardes el

## documento. Es recomendable guardarlo con un nombre nuevo (ej.

## documento_firmado.pdf) para no sobrescribir el original y finalizar el proceso

## criptográfico.


## 4. Validación de la Firma Para que la pregunta esté perfecta, debes demostrar que la

## firma es correcta.

- **Mensaje Visual** : Al guardar, el PDF mostrará tu firma en el recuadro que

## dibujaste, y debería aparecer una banda azul en la parte superior del

## documento indicando que "las firmas son válidas".

- **El Panel de Firma** : Haz clic en el botón superior derecho llamado **"Panel de**

## Firma". Aquí se despliega la información técnica de la firma y es el lugar ideal

## para revisar de nuevo que la cadena de confianza y los certificados empleados

## no presentan errores.

## 5. Ejercicio de Examen: Certificados Autofirmados y Confianza Una práctica típica es

## pedirte que firmes usando un "ID Digital Nuevo" generado desde el propio Adobe, o

## con el certificado de usuario que creaste con PowerShell.

- **El Error de Confianza** : Si firmas con un certificado autofirmado o generado en

## prácticas (y no instalaste la raíz correctamente), al ir a "Ver detalles" y revisar

## las propiedades, el sistema te advertirá que el certificado no es de confianza.

- **Por qué ocurre** : Esto ilustra el problema de los certificados autofirmados: al no

## estar emitidos por una Entidad Certificadora Real y reconocida mundialmente

## (como la FNMT), no sirven para trámites oficiales a menos que la persona que

## recibe el documento instale manualmente tu certificado raíz para confiar en ti.

## 1. "Una AC es un certificado que sirve para crear otros certificados e indicar que son

## reales y válidos."

- **Veredicto: Correcto.** * **La explicación técnica:** Una Autoridad Certificadora (AC

## o CA en inglés) actúa como el "padre" o el notario de la red. Su función

## principal es emitir certificados para "hijos" (usuarios, servidores) y dar fe de

## que son quienes dicen ser. Por eso, al crear la AC en la consola, se le indica

## explícitamente mediante una extensión que es una autoridad certificadora

## (ca=1).

## 2. "Si vas a crear un certificado de usuario o servidor necesitas tener la AC con clave

## privada (.pfx) para poder firmar dichos certificados."


- **Veredicto: Correcto, con un pequeño matiz técnico.**
- **La explicación técnica:** Efectivamente, para que la AC "dé a luz" a un certificado

## hijo, necesita firmarlo usando su clave privada.

- **Matiz de Examen:** El formato .pfx (PKCS#12) es simplemente el "archivo de

## transporte" o copia de seguridad que contiene tanto el certificado público

## como esa clave privada. En la práctica con PowerShell, cuando firmas un

## certificado nuevo usando -Signer $cert, el sistema no está leyendo un archivo

## .pfx, sino que está usando la clave privada que tiene cargada en ese momento

## en el almacén de Windows (al que hace referencia la variable $cert). Pero el

## concepto fundamental lo tienes perfecto: Sin la clave privada de la AC, es

## imposible emitir/firmar nuevos certificados.

## 3. "Si vas a firmar con uno de los certificados creados por la AC necesitas tener el .cer

## de esta para poder indicar que con el que firmas es de confianza."

- **Veredicto: Totalmente Correcto.**
- **La explicación técnica:** Cuando tú firmas un PDF con tu certificado de usuario,

## Adobe Reader mira quién te emitió ese certificado. Como te lo emitió tu propia

## AC (que te acabas de inventar), el programa desconfía.

- **La Solución:** Para que tu PC confíe en esa firma, tienes que coger la clave

## pública de tu AC (el archivo .cer sin clave privada) e instalarlo en el almacén de

## "Entidades de certificación raíz de confianza". Al hacer esto, creas un "anclaje

## de confianza". Le estás diciendo a Windows: "A partir de ahora, confía a ciegas

## en cualquier cosa que haya sido firmada por esta AC".


