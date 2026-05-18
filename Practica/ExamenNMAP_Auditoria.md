---

# Posibles Ejercicios de Examen: Nmap y Auditoría Windows — **SOLUCIONES**

## Base: Estructura del examen de enero

El examen de enero sigue un patrón claro: APARTADOS temáticos con sub-preguntas (a, b, c, d) que van de lo más simple a lo más interpretativo/analítico.

---

## BLOQUE A — Solo Nmap

### APARTADO: Descubrimiento y escaneo básico

- **a)** Escribe el comando para descubrir hosts activos en la red `192.168.0.0/24` sin escanear puertos. ¿Qué perfil de Zenmap equivale a este comando?

**Comando:**

```bash
nmap -v -sn 192.168.0.0/24
```

**Perfil Zenmap:** `Ping scan` (equivale a la opción `-sn`).

- **b)** Del descubrimiento anterior encuentras el host `192.168.0.196`. Escribe el comando equivalente al perfil "Intense scan" de Zenmap para analizarlo en profundidad.

```bash
nmap -T4 -A -v 192.168.0.196
```

(`-A` = `-O -sV -sC --traceroute`: detección de SO, versiones de servicios, scripts por defecto y traceroute.)

- **c)** En la pestaña `Ports/Hosts` de Zenmap aparecen semáforos de colores. ¿Qué significa cada color (verde, rojo, naranja) respecto al estado de un puerto?

| Color   | Estado   | Significado                                      |
|---------|----------|--------------------------------------------------|
| Verde   | `open`   | Puerto abierto, hay un servicio activo           |
| Rojo    | `closed` | Puerto cerrado, no hay servicio escuchando       |
| Naranja | `filtered` | Cortafuegos/filtro bloquea o no responde la sonda |

- **d)** El cortafuegos del objetivo bloquea los paquetes de descubrimiento y no aparece en el `ping scan`. ¿Qué opción de Nmap usarías? ¿Qué riesgo tiene usarla sobre toda la subred `/24`?

**Opción:** `-Pn` (no ping — trata todos los hosts como activos y escanea directamente).

```bash
nmap -v -Pn 192.168.0.196
```

Sobre una `/24` completa, Nmap intentará escanear los 256 hosts aunque no respondan al descubrimiento, lo que puede tardar **horas** (en la práctica se mencionan más de 3 h). En el examen conviene usar `-Pn` solo sobre **IPs concretas**, no sobre subredes grandes.

---

### APARTADO: Scripts NSE para SSL/TLS

- **a)** Escribe el comando para auditar los cifrados TLS del servidor `192.168.0.196` en el puerto 443 y ver la calificación de robustez.

```bash
nmap -sV -p 443 --script ssl-enum-ciphers 192.168.0.196
```

(También válido sin `-sV`: `nmap -p 443 --script ssl-enum-ciphers 192.168.0.196`.)

- **b)** El output del script muestra `least strength: C`. ¿Qué significa esa letra y qué implica sobre la seguridad del servidor?

La letra **C** indica calificación **suficiente pero débil**: el conjunto de cifrado más débil que acepta el servidor está en un nivel mejorable. No es lo peor (D/E/F), pero **no es recomendable** para entornos que exijan seguridad alta; conviene deshabilitar cifrados débiles y reforzar la configuración TLS.

Escala de referencia: **A** (fuerte) → **B** (bueno) → **C** (suficiente/débil) → **D/E** (débil) → **F** (inseguro).

- **c)** Escribe el comando para comprobar si el servidor acepta SSL 2.0. Si el script no devuelve ningún resultado, ¿cómo se interpreta?

```bash
nmap -p 443 --script sslv2 192.168.0.196
```

Si el script **no devuelve nada** = el servidor **no acepta SSLv2** (no hay esa vulnerabilidad). Si devuelve resultados = **sí es vulnerable** a SSL 2.0.

- **d)** Escribe el comando para obtener información del certificado digital del servidor (emisor, validez, CN).

```bash
nmap -p 443 --script ssl-cert 192.168.0.196
```

---

### APARTADO: Evasión de cortafuegos

- **a)** ¿Qué hace la opción `-f`? ¿En cuántos bytes fragmenta los paquetes?

La opción **`-f`** indica a Nmap que **fragmente** los paquetes de sondeo en trozos de **8 bytes** para intentar evadir cortafuegos que no reensamblan correctamente. Los IDS/IPS modernos bien configurados suelen detectarlo igualmente.

- **b)** Escribe un comando para hacer ping scan de `192.168.0.0/24` usando 10 señuelos aleatorios.

```bash
nmap -sn -D RND:10 192.168.0.0/24
```

(O con verbose: `nmap -v -sn -D RND:10 192.168.0.0/24`.)

- **c)** El uso de señuelos (`-D`) con tu IP real incluida, ¿oculta completamente el origen del escaneo? Justifica.

**No.** Nmap **sigue enviando paquetes con la IP real del atacante además** de las IPs señuelo. El objetivo ve tráfico desde varias direcciones, lo que **dificulta identificar** cuál es el origen real, pero **no oculta** al escáner por completo ni impide el rastreo si se analiza el tráfico con detalle.

- **d)** ¿Qué opción imita que el tráfico proviene del puerto 53 (DNS)? Escribe el comando. ¿Por qué puede engañar a ciertos cortafuegos?

**Opción:** `-g 53` o `--source-port 53`.

```bash
nmap -sn -g 53 192.168.0.0/24
```

Algunos cortafuegos **confían en tráfico que parece salir de puertos “legítimos”** (20 FTP, 53 DNS, 67 DHCP) y lo dejan pasar sin inspeccionar tanto. Simular origen en el puerto 53 puede hacer que el escaneo no se bloquee, aunque no es infalible.

---

## BLOQUE B — Solo Auditoría Windows

### APARTADO: Visor de eventos y navegación

- **a)** ¿Cuál es el comando de consola para abrir el Visor de eventos? ¿En qué rama del árbol de la izquierda están los eventos de auditoría de seguridad?

**Comando:** `eventvwr`

**Rama:** `Registros de Windows` → **`Seguridad`**

- **b)** Explica los pasos para filtrar el registro de Seguridad mostrando solo los eventos del día de ayer (00:00:00 a 23:59:00).

1. Abrir `eventvwr`.
2. Panel izquierdo → `Registros de Windows` → `Seguridad`.
3. Panel derecho → **“Filtrar registro actual...”**.
4. En **“Registrado”**, cambiar “En cualquier momento” por **“Intervalo personalizado...”**.
5. Indicar fecha de ayer: desde **00:00:00** hasta **23:59:00**.
6. Aceptar. El panel central muestra solo los eventos de ese día.

- **c)** Tras el filtrado, guarda los eventos en un fichero llamado `EventosSegDia`. ¿Qué extensión tiene el fichero? Si luego borras el elemento de "Registros guardados" en el visor, ¿se borra el fichero del disco?

**Extensión:** `.evtx` (fichero de registro de eventos de Windows).

**Al borrar en “Registros guardados”:** **No** se borra el fichero del disco. Solo se elimina el acceso rápido en el visor; el `.evtx` sigue en la carpeta donde se guardó.

- **d)** ¿Qué ruta del panel izquierdo del Visor de eventos contiene los eventos relacionados con cambios en las reglas del Firewall de Windows?

`Registros de aplicaciones y servicios` → `Microsoft` → `Windows` → **`Windows Firewall With Advanced Security`** → **`Firewall`**

---

### APARTADO: secpol y configuración de auditoría

- **a)** Antes de usar la "Configuración de directiva de auditoría avanzada" hay un paso previo obligatorio en `secpol`. ¿Cuál es y dónde se activa?

En **`secpol`** → `Directivas locales` → **`Opciones de seguridad`** → directiva **“Auditoría: forzar la configuración de subcategorías de directiva de auditoría para invalidar la configuración de la directiva de auditoría heredada”** → doble clic → **Habilitada** → Aceptar.

Sin esto, rige la directiva de auditoría básica (9 categorías) y no la avanzada con subcategorías.

- **b)** Quieres detectar intentos de acceso con contraseña incorrecta. Indica la categoría, subcategoría y opción (Correcto/Erróneo/Ambas) que debes configurar en la auditoría avanzada.

- **Categoría:** `Inicio y cierre de sesión`
- **Subcategoría:** **`Auditar inicio de sesión`**
- **Opción:** **`Erróneo`** (solo fallos) o **`Ambas`** (correctos y fallidos; útil si también quieres ver logins exitosos).

Para contraseña incorrecta basta con **Erróneo**; si el enunciado pide ver todo el intento de acceso, usar **Ambas**.

- **c)** Activas "Auditar sistema de archivos" en `secpol` para auditar accesos al fichero `C:\secreto.txt`. ¿Es suficiente? ¿Qué paso adicional hay que realizar sobre el propio fichero?

**No es suficiente.** Además hay que configurar la **SACL** (auditoría) en el objeto:

1. Clic derecho en `C:\secreto.txt` → **Propiedades** → pestaña **Seguridad** → **Opciones avanzadas**.
2. Pestaña **Auditoría** → **Agregar** → elegir usuario/grupo, operaciones a auditar (lectura, escritura, etc.) y **Correcto/Erróneo**.
3. Aceptar.

Sin SACL en el fichero, no se generan eventos **4663** (acceso a objeto) aunque la directiva global esté activa.

- **d)** ¿Qué ID de evento aparece cuando el login falla? ¿Y cuando es correcto? ¿Y cuando la cuenta queda bloqueada por demasiados intentos?

| Situación              | ID de evento |
|------------------------|--------------|
| Login **fallido**      | **4625**     |
| Login **correcto**     | **4624**     |
| Cuenta **bloqueada**   | **4740**     |

---

### APARTADO: Análisis forense de eventos

- **a)** En el Visor de eventos ves esta secuencia para el mismo usuario: `4625 → 4625 → 4625 → 4624`. ¿Qué ha ocurrido? ¿Qué indica si después del cuarto aparece un `4740`?

**4625 × 3 + 4624:** Tres intentos de inicio de sesión **fallidos** (contraseña incorrecta u otro error) seguidos de un inicio **correcto** — patrón típico de **fuerza bruta** o prueba de credenciales antes de acertar.

Si después aparece **4740:** la cuenta quedó **bloqueada** por superar el umbral de intentos fallidos configurado en la directiva de bloqueo de cuenta (el mecanismo de protección actuó).

- **b)** ¿Qué ID de evento del registro Firewall indica que se ha añadido una nueva regla? ¿Y que se ha eliminado? ¿Y que se han borrado TODAS las reglas a la vez?

| Operación                         | ID     |
|-----------------------------------|--------|
| Regla **añadida**                 | **2097** |
| Regla **eliminada**               | **2006** |
| **Todas** las reglas eliminadas   | **2033** |

(Modificación de regla existente: **2099**.)

- **c)** Describe brevemente qué información clave aporta el detalle de un evento `4625` (al hacer doble clic sobre él).

En la pestaña **General** y **Detalles** suele aparecer:

- **Cuenta** que intentó iniciar sesión (nombre de usuario).
- **Dominio** / tipo de inicio (local, red, etc.).
- **Motivo del fallo** (código de error: contraseña incorrecta, cuenta deshabilitada, etc.).
- **Origen:** dirección IP de origen, puerto de trabajo, ID de proceso si aplica.
- **Fecha y hora** del intento.
- **Equipo** de destino y registro de auditoría.

Sirve para correlacionar ataques y saber **quién**, **desde dónde** y **por qué** falló el login.

- **d)** Un técnico afirma que el Firewall está correctamente configurado y no ha cambiado. ¿Cómo verificarías esto usando solo el Visor de eventos, sin tocar `secpol` ni el Firewall directamente?

1. Abrir `eventvwr` y navegar a: `Registros de aplicaciones y servicios` → `Microsoft` → `Windows` → `Windows Firewall With Advanced Security` → **`Firewall`**.
2. Revisar el historial buscando eventos **2097** (regla añadida), **2099** (modificada), **2006** (eliminada), **2033** (borrado total), **2003** (cambio de configuración/perfil).
3. Filtrar por **intervalo de fechas** o por **ID de evento** (panel derecho → “Filtrar registro actual” → campo IDs).
4. Si **no hay** eventos de cambio en el periodo auditado, es coherente con que no se modificó; si **sí hay**, el técnico está equivocado y hay que documentar fecha, ID y descripción de cada evento.

---

## BLOQUE C — Mezclando Nmap + Auditoría

### APARTADO: Flujo completo de auditoría con Nmap como generador de eventos

- **a)** Usando `secpol`, activa la auditoría para capturar inicios de sesión correctos y fallidos. Indica la ruta exacta dentro de `secpol` y la opción de auditoría elegida.

1. `secpol` → `Directivas locales` → `Opciones de seguridad` → habilitar **“Auditoría: forzar la configuración de subcategorías...”**.
2. `secpol` → **`Configuración de directiva de auditoría avanzada`** → **`Inicio y cierre de sesión`** → **`Auditar inicio de sesión`** → marcar **Correcto** y **Erróneo** (**Ambas**).

- **b)** Para generar eventos de prueba, cierra sesión, haz 2 intentos con contraseña incorrecta y uno correcto. Después lanza `nmap -T4 -A -v 192.168.0.196` desde otra máquina. ¿Qué tipo de eventos esperas encontrar en el Visor?

En **Registros de Windows → Seguridad:**

- **4625** (×2): intentos de login fallidos.
- **4624**: login correcto.
- Posiblemente **4634** / **4647** si hubo cierre de sesión previo.
- **4672** si el usuario tiene privilegios elevados (admin).

El escaneo **Nmap desde otra máquina** no siempre genera eventos en el registro de **Seguridad** del host escaneado (depende de auditoría de red/firewall). Si el firewall del objetivo registra conexiones, podrían verse eventos en el registro **Firewall** del equipo atacado o del escaneado si hay reglas de registro habilitadas; lo habitual en la práctica es centrarse en los **4624/4625** del apartado de logon.

- **c)** Abre `eventvwr` y filtra el registro de Seguridad. Localiza los eventos 4624 y 4625. ¿Qué información concreta (usuario, timestamp, origen) aparece en cada uno?

| Campo        | Evento 4625 (fallo)                    | Evento 4624 (éxito)                    |
|--------------|----------------------------------------|----------------------------------------|
| **Usuario**  | Nombre de cuenta intentada             | Cuenta que inició sesión correctamente |
| **Timestamp**| Fecha/hora del intento fallido         | Fecha/hora del login exitoso           |
| **Origen**   | IP de origen, estación de trabajo      | IP de origen, tipo de inicio (2/3/10…) |
| **Extra**    | Código de motivo del fallo             | Nivel de privilegios, dominio          |

(Valores concretos dependen de la MV; en el examen se documentan con captura del detalle del evento.)

- **d)** Busca en el registro del Firewall (`Windows Firewall With Advanced Security > Firewall`) los eventos generados. Identifica el ID y la operación que describen.

Si durante la práctica se **añadió, modificó o eliminó** una regla del firewall:

| ID     | Operación típica                                      |
|--------|-------------------------------------------------------|
| **2097** | Se agregó una regla a la lista de excepciones        |
| **2099** | Se modificó una regla existente                      |
| **2006** | Se eliminó una regla                                 |
| **2003** | Cambió configuración del firewall (perfil, etc.)     |

Si solo se lanzó Nmap **sin tocar el firewall**, puede que **no aparezcan** eventos nuevos en ese registro; en ese caso indicarlo en la respuesta.

---

## BLOQUE D — Mezclando Nmap + Wireshark

### APARTADO: Nmap visto desde Wireshark

- **a)** Tienes Wireshark capturando tráfico y ejecutas `nmap -v -sn 192.168.0.0/24`. ¿Qué tipos de paquetes verías en la captura durante la fase de descubrimiento?

Durante **host discovery** (`-sn`), Nmap envía por defecto (entre otros):

- **ICMP Echo Request** (ping clásico, opción `-PE`).
- **ICMP Timestamp Request** (`-PP`).
- **TCP SYN** hacia puerto **443** (`-PS`).
- **TCP ACK** hacia puerto **80** (`-PA`).

No se hace escaneo completo de puertos en esta fase; solo sondas de “¿está vivo el host?”.

- **b)** Escribe un filtro de Wireshark para ver solo los paquetes con destino a `192.168.0.196` durante el escaneo.

```
ip.dst == 192.168.0.196
```

(Para ver tráfico en ambos sentidos: `ip.addr == 192.168.0.196`.)

- **c)** ¿Por qué al hacer `nmap -p 443 --script ssl-enum-ciphers 192.168.0.196` sí ves el handshake TLS en Wireshark pero no puedes leer el contenido del tráfico HTTPS?

Porque **TLS cifra** el contenido de la aplicación tras el handshake. Wireshark muestra **ClientHello, ServerHello, certificados, intercambio de claves**, etc., pero los datos de aplicación van **cifrados**; sin la clave privada del servidor o el registro de claves de sesión (SSLKEYLOG), no se puede descifrar el tráfico HTTPS en la práctica 4.

- **d)** Mientras Nmap hace `nmap -sS 192.168.0.196`, ¿verías el three-way handshake TCP completo en Wireshark? Justifica (recordar que -sS es half-open).

**No** (en el host escaneado no se completa el handshake habitual de conexión).

Con **`-sS` (SYN scan / half-open)**, Nmap envía **SYN**, si el puerto está abierto recibe **SYN-ACK** y responde con **RST** para **no completar** el three-way handshake (no envía el ACK final). Por tanto verás **SYN** y posiblemente **SYN-ACK + RST**, pero **no** la secuencia completa **SYN → SYN-ACK → ACK** de una conexión TCP establecida.

---

## Resumen de repaso

- **Examen corto:** comandos Nmap + IDs de eventos (4624, 4625, 4740, 2097, 2006).
- **Examen largo:** flujo Bloque C (secpol → pruebas → eventvwr).
- **Sorpresa posible:** Bloque D (Nmap + Wireshark).
- **Justificar siempre:** `-sn` vs `-Pn`, limitaciones de `-D`, `least strength`, borrado en “Registros guardados” ≠ borrar `.evtx`.
