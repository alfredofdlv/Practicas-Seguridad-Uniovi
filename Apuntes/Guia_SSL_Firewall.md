# GUÍA COMPLETA DE SSL/TLS Y FIREWALL DE WINDOWS

### Para el examen de Seguridad de Datos

```
IIS, servidor web seguro, certificados SSL/TLS, reglas de Firewall y protección de comunicaciones
```
```
Contenido basado en la Práctica 3 — Protección de Comunicaciones y Acceso
```

## HERRAMIENTAS CLAVE

#### Acceso rápido

```
Herramienta                    Comando         Ruta de menú
Administrador de IIS           inetmgr         Panel de control > Herramientas de Windows > Administrador de IIS
Firewall avanzado              wf.msc          Buscar "Firewall de Windows Defender" > Configuración avanzada
Gestión certs equipo           certlm.msc      Ejecutar > certlm.msc
Gestión certs usuario          certmgr.msc     Ejecutar > certmgr.msc
```

```
CONSEJO: En el examen usa siempre los comandos de consola (inetmgr, wf.msc, certlm.msc).
Son mucho más rápidos que navegar por el Panel de control.
```


## APARTADO 1: Servidor Web Seguro con IIS

#### Activar IIS en Windows 11

1. Inicio > Panel de control > Programas > Programas y características
2. "Activar o desactivar las características de Windows"
3. Seleccionar casilla **Internet Information Services** con opciones por defecto → Aceptar

Verificar en Firewall: "Permitir una aplicación..." → marcar **Privado y Público**:
- Servicios World Wide Web (HTTP)
- Servicios seguros World Wide Web (HTTPS)

```
IMPORTANTE (trampa de examen): Si HTTP funciona pero HTTPS no, suele faltar marcar
"Servicios seguros World Wide Web (HTTPS)" en el firewall. Sin puerto 443 abierto el
certificado SSL no sirve de nada.
```

#### Cargar un certificado en IIS

1. Abrir `inetmgr`
2. En panel izquierdo seleccionar el nombre del servidor (DESKTOP-...)
3. Panel central → "Certificados de servidor"
4. Panel derecho → "Importar..."
5. Seleccionar `zpSERas.pfx` → contraseña: `conserpfx`
6. Almacén: **Hospedaje de sitios web**

```
IMPORTANTE: El certificado del servidor se carga en el almacén "Hospedaje de sitios web"
del EQUIPO LOCAL (no del usuario). Usar certlm.msc para verificarlo.
```

Importar también la AC (`zpACas.cer`, **nunca** el `.pfx`) en **Entidades de certificación raíz de confianza** del **equipo local** (`certlm.msc`).

```
IMPORTANTE (pregunta de oro): Distribuir el .pfx de la AC a los clientes compromete
toda la PKI: les das la clave privada y podrían emitir certificados falsos de confianza.
Solo se distribuye el .cer (público).
```

#### Crear el servidor web seguro

Preparar directorio para el nuevo sitio:

```
%SystemDrive%\inetpub\wwwroot\seg\
```

En IIS: clic derecho sobre "Sitios" → "Agregar sitio web..."

```
Parámetro             Valor
Nombre del sitio      zpser.as   (debe coincidir con el CN del certificado)
Ruta física           C:\inetpub\wwwroot\seg\
Tipo de enlace        https
Puerto                443
Certificado SSL       zpser.as   (elegir de la lista)
```

Página de inicio del sitio: `Default.htm` en `C:\inetpub\wwwroot\seg\`

#### Configuración SSL (opciones de certificados de cliente)

En IIS → seleccionar zpser.as → panel central → "Configuración de SSL":

```
Opción      Comportamiento
Omitir      El servidor NO acepta ni pide certificado de cliente (PREDETERMINADO)
Aceptar     El servidor acepta certificado si se proporciona y verifica la identidad
Requerir    El servidor EXIGE certificado de cliente para permitir el acceso
```

```
IMPORTANTE: La opción de certificados de cliente la decide el SERVIDOR, no el cliente.
En el examen la pregunta típica es "¿qué opción usar para autenticar a los clientes?"
→ Requerir. Para acceso público sin autenticación → Omitir.
```

Activar "Requerir SSL" para habilitar cifrado de 40 bits mínimo. Hacer clic en **Aplicar**.

#### Examinar el directorio del sitio

En IIS → zpser.as → "Examen de directorios" → panel derecho "Habilitar" → seleccionar todas las opciones → Aplicar.

Esto crea `web.config` en el directorio del sitio.


## APARTADO 2: Resolver el Nombre del Servidor

#### El problema del nombre del certificado

El certificado fue emitido para `zpser.as`, NO para una IP. El navegador mostrará error si se
accede por IP en lugar de nombre.

```
Error típico: "El certificado no es válido para esta dirección"
Causa: el certificado dice "zpser.as" pero el usuario accede a https://192.168.0.196
Solución: editar el fichero hosts para que el nombre resuelva a la IP correcta
```

#### Editar el fichero hosts

Ruta del fichero:

```
C:\Windows\system32\drivers\etc\hosts
```

Añadir la línea:

```
A.B.C.D    zpser.as
```

Donde `A.B.C.D` es la IP del servidor web (máquina virtual).

**Cómo editar como Administrador:**

```
Método 1: Buscar "Símbolo del sistema" → clic derecho → "Ejecutar como administrador"
          → cd C:\Windows\system32\drivers\etc → notepad hosts

Método 2: Guardar en otra ubicación y luego copiar con permisos de administrador
```

```
IMPORTANTE: El fichero hosts resuelve nombres SOLO en el equipo local donde se edita.
Para que el cliente externo (máquina física) también resuelva, hay que editar el hosts
en ESE equipo también.
```

#### Prueba progresiva desde el cliente externo (máquina física)

1. **Por IP:** `https://TU_IP_VIRTUAL` → advertencia *"Su conexión no es privada"*; en Avanzado: **NET::ERR_CERT_COMMON_NAME_INVALID** (el cert es para `zpser.as`, no para la IP).
2. **Por nombre sin hosts:** `https://zpser.as` → *"no se puede obtener acceso"* (DNS no resuelve).
3. **Editar hosts** en la máquina física (Bloc de notas **como administrador**): `C:\Windows\System32\drivers\etc\hosts`, filtro "Todos los archivos", línea `192.168.0.192 zpser.as` (tu IP real).
4. **Prueba final:** Borrar estado SSL → cerrar y reabrir navegador → `https://zpser.as` → debe verse la web con **candado** si la AC está en raíces de confianza.

```
CONSEJO: En el cliente usa certmgr.msc (usuario que navega), no certlm.msc. certlm es
para el servidor/IIS.
```

#### Borrar el estado SSL del navegador

Antes de cada prueba, borrar el estado SSL para evitar que el navegador use resultados
cacheados:

Panel de Control → Opciones de Internet → pestaña Contenido → botón "Borrar estado SSL"

O en EDGE: Configuración → Borrar datos de exploración → seleccionar todo → "Elegir qué
borrar cada vez que se cierra el explorador".


## APARTADO 3: Configurar Navegadores para Confiar en la AC

Para que el navegador muestre el candado verde sin errores, debe tener instalado el certificado
de la Autoridad Certificadora (AC) en el almacén de raíces de confianza.

#### Microsoft EDGE

1. Instalar `zpACas.cer` en `certmgr.msc` → "Entidades de certificación raíz de confianza"
2. EDGE usa el almacén de certificados de Windows automáticamente

Verificar en EDGE: Configuración → Privacidad, búsqueda y servicios → sección Seguridad →
"Administrar certificados"

#### Mozilla Firefox

```
IMPORTANTE: Firefox usa su PROPIO almacén de certificados, independiente de Windows.
Hay que importar zpACas.cer directamente en Firefox:
Configuración → Privacidad y seguridad → Ver certificados → Autoridades → Importar
```

#### Google Chrome

Chrome usa el almacén de Windows igual que EDGE. Basta con tener instalado el cert
de AC en `certmgr.msc`.


## APARTADO 4: Firewall de Windows

#### Conceptos: Ubicaciones de red

```
Ubicación       Descripción                                    Detección de red
Doméstica       Red de confianza en casa                       Activada
Trabajo         Pequeña oficina o subred corporativa           Activada
Pública         Cafeterías, aeropuertos, redes no confiables   DESACTIVADA
Dominio         Red controlada por controlador de dominio      Activada
```

Doméstica y Trabajo se tratan igual = **Red Privada**.

#### Perfiles de Firewall

```
Perfil     Cuándo se aplica                                           Restricción
Dominio    Adaptador conectado a red con controlador de dominio       Menos restrictivo
Privado    Red detrás de router NAT o firewall hardware               Nivel medio
Público    Conectado directamente a Internet                          MÁS restrictivo
```

```
CONSEJO: En la práctica se trabaja con perfil Público. Un computador puede tener varios
adaptadores de red, cada uno con su propio perfil asignado según la red detectada.
```

#### Comportamiento predeterminado

```
Tráfico            Política por defecto
Entrante           BLOQUEADO (salvo que haya regla que lo permita)
Saliente           PERMITIDO (salvo que haya regla que lo bloquee)
```

#### Tipos de reglas

```
Tipo                     Descripción
Reglas de entrada        Controlan quién puede conectarse AL equipo
Reglas de salida         Controlan qué puede salir DEL equipo
Reglas de seg. conexión  Autenticación IPsec entre dos equipos (bilateral)
```

```
IMPORTANTE: Las reglas de firewall son UNILATERALES (solo actúan en un equipo).
Las reglas de seguridad de conexión (IPsec) son BILATERALES (deben existir en ambos equipos).
```


## APARTADO 5: Ver y Gestionar Reglas del Firewall

#### Acceder al Firewall avanzado

```
wf.msc
```

O: Firewall de Windows Defender → panel izquierdo → "Configuración avanzada"

#### Columnas de cada regla

```
Columna              Descripción
Nombre               Identificador de la regla
Grupo                Grupo al que pertenece
Perfil               Dominio / Privado / Público / Todos
Habilitado           Sí / No
Acción               Permitir / Bloquear
Programa             Ejecutable al que aplica (o todos)
Protocolo            TCP / UDP / ICMP / Cualquiera
Puerto local         Puerto del equipo local
Puerto remoto        Puerto del equipo remoto
Dirección local/remota IPs afectadas
```

#### Símbolos de estado en la lista de reglas

```
Símbolo              Significado
Círculo verde OK     Regla habilitada, acción = Permitir
Círculo rojo (stop)  Regla habilitada, acción = Bloquear
Espacio en blanco    Regla DESHABILITADA
```

#### Filtrar reglas en el panel derecho

- Por perfil (Dominio / Privado / Público)
- Por estado (Habilitadas / Deshabilitadas)
- Por grupo

Usar "Exportar lista..." para guardar las reglas visibles en un fichero de texto.


## APARTADO 6: Habilitar Eco ICMP (Ping)

Por defecto Windows bloquea los pings entrantes. Para habilitarlos:

1. Abrir `wf.msc` → Reglas de entrada
2. Buscar: **Archivos e impresoras compartidos (petición eco ICMPv4 de entrada)**
3. Hay DOS reglas: una para perfil Dominio y otra para Privado/Público
4. Clic derecho sobre la regla → "Habilitar regla" o entrar en Propiedades → marcar "Habilitado"

```
IMPORTANTE: El Ping NO usa puertos TCP ni UDP. ICMP trabaja directamente en la capa IP.
No hay que abrir ningún puerto, solo habilitar la regla ICMP específica.
```

Verificar desde la máquina física:

```
ping IP_maquina_virtual
```


## APARTADO 7: Crear una Regla de Salida Personalizada

#### Objetivo: bloquear toda salida EXCEPTO hacia una IP concreta

Ejemplo: permitir solo comunicación con `192.168.1.200` y bloquear todo lo demás.

**Pasos en el asistente "Nueva regla de salida":**

```
Paso 1 — Tipo de regla:   Personalizada
Paso 2 — Programa:        Todos los programas
Paso 3 — Protocolo:       Cualquiera (sin especificar puertos)
Paso 4 — Ámbito:
          Local:  Cualquier dirección IP
          Remota: "Estas direcciones IP" → pulsar Agregar
          → Intervalo: 0.0.0.0 a 192.168.1.199     (bloquea todo antes de la IP)
          → Intervalo: 192.168.1.201 a 255.255.255.255  (bloquea todo después)
Paso 5 — Acción:          Bloquear la conexión
Paso 6 — Perfil:          Todos
Paso 7 — Nombre:          Nombre descriptivo + descripción
```

```
CONSEJO: Para permitir SOLO la IP X.X.X.X hay que bloquear DOS rangos:
- Desde 0.0.0.0 hasta X.X.X.X - 1
- Desde X.X.X.X + 1 hasta 255.255.255.255
La IP X.X.X.X queda fuera de ambos rangos y por tanto NO es bloqueada.
```

Verificar que funciona:
- Ping a `www.google.es` → debe fallar (bloqueado)
- Ping a la IP permitida → debe funcionar
- Deshabilitar regla → vuelve la conectividad


## CHULETA DE REFERENCIA RÁPIDA

#### Comandos de acceso rápido

```
Herramienta         Comando     Para qué sirve
IIS                 inetmgr     Administrar servidor web, certs IIS, sitios
Firewall avanzado   wf.msc      Reglas de entrada/salida, perfiles
Certs usuario       certmgr.msc Gestionar certificados del usuario actual
Certs equipo        certlm.msc  Gestionar certificados del equipo local (admin)
```

#### SSL — Opciones de certificados de cliente (IIS)

```
Opción    Descripción                          Cuándo usar
Omitir    No autentica al cliente              Acceso público sin autenticación
Aceptar   Autentica si el cliente tiene cert   Opcional/mixto
Requerir  Exige cert de cliente                Acceso restringido con autenticación
```

#### Perfiles de Firewall

```
Perfil    Red típica                           Restricción
Dominio   Empresa con Active Directory         Baja
Privado   Casa/oficina tras router             Media
Público   WiFi pública, café, aeropuerto       Alta (predeterminada)
```

#### Flujo de trabajo para el servidor web seguro

```
1. Activar IIS en "Características de Windows"
2. Importar zpSERas.pfx en IIS → "Certificados de servidor"
3. Crear sitio web: Agregar sitio web → https:443 → seleccionar cert
4. Crear directorio %SystemDrive%\inetpub\wwwroot\seg\
5. Colocar Default.htm en ese directorio
6. IIS → zpser.as → "Configuración de SSL" → Requerir SSL → Aplicar
7. Editar hosts: añadir "IP    zpser.as" en C:\Windows\system32\drivers\etc\hosts
8. Instalar zpACas.cer en certmgr → "Entidades raíz de confianza"
9. Probar: https://zpser.as → debe mostrar candado verde
```

#### Fichero hosts

```
Ruta:   C:\Windows\system32\drivers\etc\hosts
Editar: Abrir Bloc de notas como Administrador → notepad hosts
Línea a añadir:   A.B.C.D    zpser.as
```

#### Reglas de Firewall — Resumen

```
Acción    Descripción
Permitir  Deja pasar el tráfico que coincide con la regla
Bloquear  Bloquea el tráfico que coincide con la regla
Tráfico entrante por defecto:   BLOQUEADO
Tráfico saliente por defecto:   PERMITIDO
```

## PREGUNTAS TIPO EXAMEN

> Basado en [Resolucion_Examen_SSL_Firewall.md](../Practica/Resolucion_Examen_SSL_Firewall.md).

### Apartado 1 — IIS y certificados

- Panel central del servidor en `inetmgr`: **Certificados de servidor**; importar `zpSERas.pfx` (contraseña `conserpfx`) en almacén **Hospedaje de sitios web** → verificar en `certlm.msc` → Personal.
- Sitio HTTPS: nombre = CN del cert (`zpser.as`), puerto 443, enlace https.
- **Configuración de SSL:** Omitir / Aceptar / **Requerir** certificado de cliente (lo decide el servidor).
- **Examen de directorios** crea `web.config` en la ruta del sitio.

### Apartado 2 — Nombres y confianza

- `hosts` solo afecta al equipo donde se edita; ruta `C:\Windows\System32\drivers\etc\hosts`.
- Sin AC en raíces: error de autoridad no confiable; instalar `zpACas.cer` en **Entidades de certificación raíz de confianza** (`certmgr` en el cliente).
- **Firefox** no usa el almacén de Windows → importar la AC en Firefox (Autoridades).

### Apartado 3 — Firewall e ICMP

- Perfiles: Dominio, Privado, Público. Entrante bloqueado / saliente permitido por defecto.
- **Ping no usa puertos** → habilitar regla predefinida **petición eco ICMPv4 de entrada** (no crear regla de puerto).
- Windows envía **4** pings por defecto.

### Apartado 4 — Regla de salida (solo una IP)

- Regla personalizada de **salida**, protocolo cualquiera, acción **Bloquear**, ámbito remoto en dos rangos:
  - `0.0.0.0` → `192.168.1.199`
  - `192.168.1.201` → `255.255.255.255`
- La IP `192.168.1.200` queda en el hueco y sigue permitida por la política por defecto.

### Apartado 5 — IPsec (ejercicios propuestos)

- En `wf.msc`: **Reglas de seguridad de conexión** (no solo firewall) para exigir IPsec.
- Reglas de firewall = **unilaterales**; IPsec = **bilaterales** (política compatible en ambos extremos).
- Registros en `eventvwr`: `Windows Firewall With Advanced Security` → **Seguridad de conexión** vs **detallada**.

#### Resumen rápido

```
Cert IIS          → Certificados de servidor; certlm.msc
CN del sitio      → Debe coincidir con URL (CN/SAN)
SSL cliente       → Omitir / Aceptar / Requerir
EDGE + AC         → zpACas.cer en Raíces de confianza
Firefox           → Importar AC en su propio almacén
ICMP              → Sin puertos; regla eco ICMPv4
Salida 1 IP       → Dos rangos de bloqueo dejando hueco en .200
IPsec             → Bilateral; firewall normal = unilateral
```
