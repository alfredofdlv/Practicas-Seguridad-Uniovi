# Resolución — Examen posible SSL/TLS e IIS + Firewall de Windows

> Respuestas basadas en la Práctica 3 y en [Guia_SSL_Firewall.md](../Apuntes/Guia_SSL_Firewall.md).  
> Las capturas de pantalla las debes adjuntar tú al realizar los pasos en la máquina virtual.

---

## APARTADO 1 — Servidor Web Seguro con IIS

### a) Certificados en IIS y almacenes

**¿Qué opción del panel central del servidor muestra los certificados?**

En `inetmgr`, selecciona el **nombre del servidor** (nodo raíz, p. ej. `DESKTOP-...`) en el panel izquierdo. En el panel central aparece **Certificados de servidor**.

**¿En qué almacén se guarda el certificado al importarlo desde IIS?**

En el almacén de certificados del **equipo local**, carpeta lógica **Personal** → subalmacén **Hospedaje de sitios web** (Web Hosting). No va al almacén del usuario.

**Verificación con `certlm.msc`**

1. Ejecutar `certlm.msc` (requiere permisos de administrador para gestionar certs de equipo).
2. Navegar: **Personal** → **Certificados**.
3. Debe aparecer el certificado con CN `zpser.as` (o el nombre emitido en la práctica).

**Diferencia `certmgr.msc` vs `certlm.msc`**


| Herramienta   | Ámbito              | Uso típico en la práctica                         |
| ------------- | ------------------- | ------------------------------------------------- |
| `certmgr.msc` | Usuario actual      | AC en raíces de confianza del usuario, certs FNMT |
| `certlm.msc`  | Equipo local (todo) | Certificados de IIS / servidor web (HTTPS)        |


IIS usa certificados del **equipo**; por eso el cert del sitio se comprueba en `certlm.msc`, no en `certmgr.msc`.

---

### b) Crear sitio web HTTPS

**Parámetros del asistente "Agregar sitio web..."**


| Parámetro        | Valor                     |
| ---------------- | ------------------------- |
| Nombre del sitio | `zpser.as`                |
| Ruta física      | `C:\inetpub\wwwroot\seg\` |
| Tipo de enlace   | `https`                   |
| Puerto           | `443`                     |
| Certificado SSL  | `zpser.as` (de la lista)  |


**¿Por qué el nombre del sitio debe coincidir con el CN del certificado?**

Durante el handshake TLS, el navegador comprueba que el **nombre al que accede** (SNI / nombre en la URL) coincida con los nombres del certificado (**CN** y **SAN** en *Nombre alternativo del titular*). Si accedes por IP o por otro nombre distinto al del certificado, aparece error del tipo *"El certificado no es válido para esta dirección"* aunque la cadena de confianza sea correcta.

*(Adjuntar captura del asistente con todos los campos rellenos.)*

---

### c) Configuración de SSL — certificados de cliente

En IIS: sitio `zpser.as` → panel central → **Configuración de SSL**.

**Las tres opciones para certificados de cliente**


| Opción       | Comportamiento                                                                                               |
| ------------ | ------------------------------------------------------------------------------------------------------------ |
| **Omitir**   | El servidor no pide ni usa certificado de cliente (predeterminado).                                          |
| **Aceptar**  | Si el cliente envía certificado, el servidor lo valida; si no, puede seguir el acceso (según configuración). |
| **Requerir** | El cliente **debe** presentar un certificado válido; sin él no hay acceso HTTPS al sitio.                    |


**Para exigir certificado de cliente:** seleccionar **Requerir** → activar también **Requerir SSL** si se indica en el guion → **Aplicar**.

**Si el sitio es público sin autenticación de cliente:** **Omitir**.

La decisión la toma el **servidor** (IIS), no el navegador del usuario.

*(Adjuntar captura de Configuración de SSL con "Requerir" seleccionado.)*

---

### d) Examen de directorios

En IIS: sitio `zpser.as` → **Examen de directorios** → panel derecho **Habilitar** → marcar opciones → **Aplicar**.

**Fichero creado:** `web.config` en `C:\inetpub\wwwroot\seg\`.

**Para qué sirve:** Define la configuración del sitio/aplicación para IIS (directorios, permisos de listado, etc.) sin tener que repetir la configuración solo en la consola; IIS lee ese XML al servir el sitio.

---

## APARTADO 2 — Resolución de nombres y confianza

### a) Fichero hosts

**Ubicación:**

```
C:\Windows\System32\drivers\etc\hosts
```

**Línea a añadir** (sustituir `A.B.C.D` por la IP real de la VM):

```
A.B.C.D    zpser.as
```

**¿Por qué hace falta Administrador?**

El fichero está en una ruta del sistema y suele tener permisos que impiden escritura a usuarios normales; sin elevación, el Bloc de notas no puede guardar cambios.

**¿Afecta a otros equipos?**

**No.** `hosts` solo resuelve nombres en el **equipo donde se edita**. En el cliente (máquina física) hay que editar su propio `hosts` con la misma línea si también accede por nombre.

**Cómo editar (ejemplo):**

```cmd
cd C:\Windows\System32\drivers\etc
notepad hosts
```

(Ejecutar CMD o Notepad **como administrador**.)

---

### b) Acceso con EDGE antes de instalar la AC

**Error típico:** advertencia de seguridad / certificado no de confianza; mensaje del estilo *"La conexión no es privada"* o *"NET::ERR_CERT_AUTHORITY_INVALID"*.

**Causa principal (sin AC instalada):** el certificado del servidor (`zpser.as`) está firmado por una **AC propia** (`zpac.as`) que **no** está en el almacén de raíces de confianza de Windows. EDGE no puede construir una cadena hasta una raíz de confianza.

**Qué instalar para el candado sin advertencias (cadena):**

- Fichero `**zpACas.cer`** (solo clave pública de la AC).
- Almacén: **Entidades de certificación raíz de confianza** (en `certmgr.msc` para el usuario que usa EDGE).

*(Si además no resolviste `zpser.as` en `hosts`, puede aparecer también error de nombre no coincidente.)*

---

### c) Instalar `zpACas.cer` y volver a probar en EDGE

**Pasos:**

1. Doble clic en `zpACas.cer` → **Instalar certificado...** → **Usuario actual**.
2. Almacén: **Entidades de certificación raíz de confianza** (elegir manualmente si hace falta).
3. Aceptar la advertencia de seguridad.
4. Borrar estado SSL: Panel de control → Opciones de Internet → **Borrar estado SSL** (recomendado entre pruebas).
5. Acceder de nuevo a `https://zpser.as`.

**Diferencia observada:** la cadena se valida; el certificado del servidor aparece como emitido por `zpac.as` y el estado suele ser **válido** / conexión segura (candado), si el nombre en la URL coincide con el certificado.

**Implicación de seguridad:** al instalar una raíz propia, Windows **confía en todos los certificados** que esa AC emita. Es un **anclaje de confianza** fuerte: solo debe hacerse con ACs que controlas y en entornos de laboratorio.

---

### d) Firefox vs almacén de Windows

**¿Por qué Firefox sigue fallando si la AC está en Windows?**

Firefox usa su **propio almacén de certificados**, independiente de `certmgr.msc` / CryptoAPI de Windows.

**Dónde importar en Firefox:**

**Configuración** → **Privacidad y seguridad** → **Certificados** → **Ver certificados...** → pestaña **Autoridades** → **Importar** → seleccionar `zpACas.cer` → marcar confianza para identificar sitios web.

**Navegadores y almacén:**


| Navegador       | ¿Usa almacén de Windows? |
| --------------- | ------------------------ |
| Microsoft EDGE  | Sí                       |
| Google Chrome   | Sí                       |
| Mozilla Firefox | **No** (almacén propio)  |


---

## APARTADO 3 — Firewall: perfiles y reglas ICMP

### a) Perfiles y política por defecto

**Tres perfiles de Firewall (seguridad avanzada):**


| Perfil      | Tipo de red típica                                | Restricción relativa        |
| ----------- | ------------------------------------------------- | --------------------------- |
| **Dominio** | Red con controlador de dominio (Active Directory) | Menor (corporativa)         |
| **Privado** | Casa, oficina pequeña, detrás de router/NAT       | Media                       |
| **Público** | WiFi pública, aeropuerto, redes no confiables     | **Mayor** (más restrictivo) |


**Política predeterminada:**

- Tráfico **entrante:** **bloqueado** (salvo reglas que permitan).
- Tráfico **saliente:** **permitido** (salvo reglas que bloqueen).

**Si también se bloqueara todo lo saliente por defecto:** muchas aplicaciones dejarían de funcionar (navegador, actualizaciones, DNS saliente, etc.) hasta crear reglas de salida explícitas para cada servicio; el equipo quedaría muy aislado.

---

### b) Reglas ICMP en Reglas de entrada (perfil Público)

En `wf.msc` → **Reglas de entrada** → filtrar por perfil **Público** → buscar *eco ICMP* / *ICMPv4*.

**Reglas "Archivos e impresoras compartidos (petición eco ICMPv4 de entrada)":** suelen aparecer **dos** entradas en la lista (una asociada al perfil **Dominio** y otra a **Privado/Público** — según versión de Windows los nombres pueden variar ligeramente).

**¿Habilitadas por defecto?** En instalación típica, **no** (deshabilitadas) para perfiles no corporativos; el ping entrante queda bloqueado salvo que se habiliten.

**Símbolos en la lista:**


| Aspecto               | Símbolo / aspecto visual          |
| --------------------- | --------------------------------- |
| Habilitada + Permitir | Círculo verde con marca (OK)      |
| Habilitada + Bloquear | Círculo rojo (stop)               |
| **Deshabilitada**     | **Sin icono** (espacio en blanco) |


---

### c) Habilitar ICMP y probar ping

1. `wf.msc` → Reglas de entrada → habilitar la regla **petición eco ICMPv4 de entrada** para **Privado/Público** (la que aplique a tu red).
2. Desde la máquina física: `ping <IP_maquina_virtual>`.

**¿Responde?** Sí, si la VM está en la misma red y no hay otro firewall intermedio bloqueando ICMP.

**Ping por defecto en Windows:** se envían **4** peticiones ICMP (4 paquetes request) y se esperan **4** respuestas (reply), salvo que uses `ping -n N` para cambiar el número.

**¿Por qué ICMP no usa puertos?**

ICMP es un protocolo de la **capa de red** (capa 3), no de transporte. TCP y UDP usan puertos en la capa 4; ICMP usa tipos y códigos (p. ej. echo request = tipo 8, echo reply = tipo 0), no números de puerto.

*(Adjuntar captura: `ping` con 4 respuestas + regla habilitada en wf.msc.)*

---

### d) Deshabilitar ICMP de nuevo

Tras **deshabilitar** la regla ICMP, `ping` desde la máquina física suele mostrar **"Tiempo de espera agotado"** para todos los paquetes o **"Host de destino inaccesible"** según el caso.

**Deshabilitar vs eliminar:**


| Acción           | Efecto                                                                                 |
| ---------------- | -------------------------------------------------------------------------------------- |
| **Deshabilitar** | La regla sigue en la lista pero no se aplica; se puede volver a activar sin recrearla. |
| **Eliminar**     | La regla se borra del sistema; hay que crearla de nuevo si se necesita otra vez.       |


*(Adjuntar captura: ping fallido + regla deshabilitada sin icono verde.)*

---

## APARTADO 4 — Regla de salida personalizada

### a) Bloquear todo saliente excepto `192.168.1.200`

**Asistente:** Reglas de salida → **Nueva regla...** → **Personalizada** → Todos los programas → Protocolo: **Cualquiera** → Ámbito:

- Dirección local: **Cualquier IP**
- Dirección remota: **Estas direcciones IP** → **Agregar** dos **intervalos**:

```
0.0.0.0          →  192.168.1.199
192.168.1.201    →  255.255.255.255
```

**Acción:** **Bloquear la conexión**  
**Perfil:** Todos  
**Nombre:** p. ej. `Bloquear salida excepto 192.168.1.200`

**¿Por qué dos rangos?**

Una regla de **bloqueo** solo afecta al tráfico que **coincide** con el ámbito. Si bloqueas un solo rango grande, la IP permitida podría quedar dentro del rango bloqueado. Con **dos intervalos** que dejan un "hueco" en `192.168.1.200`, esa IP **no coincide** con ninguna regla de bloqueo y el tráfico hacia ella sigue permitido por la política por defecto (saliente permitido).

*(Adjuntar captura del paso Ámbito con los dos intervalos.)*

---

### b) Comprobar con ping

Con la regla **habilitada**:


| Comando              | Resultado esperado                                           |
| -------------------- | ------------------------------------------------------------ |
| `ping www.google.es` | **Falla** (bloqueado o sin respuesta por la regla de salida) |
| `ping 192.168.1.200` | **Puede funcionar** si ese host existe y responde ICMP       |


En `wf.msc`, columna **Acción** de la regla creada: **Bloquear**.

*(Nota: si `192.168.1.200` no existe en tu red, el ping puede fallar por timeout de red, no por el firewall; en el examen se valora la lógica de la regla.)*

---

### c) Unilateral vs IPsec

**Reglas de firewall unilaterales:** se configuran y actúan **solo en un equipo**. Bloquear o permitir tráfico en la VM no cambia automáticamente el firewall del otro PC.

**Reglas de seguridad de conexión (IPsec):** son **bilaterales** — hace falta una política compatible en **ambos** extremos para negociar autenticación/cifrado.

**Para autenticación en ambos extremos:** crear **reglas de seguridad de conexión** (no solo reglas de firewall) en **los dos equipos** que participan en la comunicación.

---

### d) Deshabilitar regla y exportar lista

1. Deshabilitar la regla de salida → comprobar que `ping www.google.es` vuelve a funcionar (conectividad general restaurada).
2. En `wf.msc` → **Reglas de salida** → panel derecho → **Exportar lista...** → guardar fichero.

**Contenido del export:** listado de reglas visibles (según filtros activos) con datos como nombre, grupo, perfiles, habilitada, acción, programa, protocolo, puertos, direcciones, etc.

**Formato:** fichero de **texto plano** (`.txt`), legible con Bloc de notas.

---

## Resumen rápido para repaso


| Tema                       | Respuesta clave                                                     |
| -------------------------- | ------------------------------------------------------------------- |
| Cert IIS                   | Panel **Certificados de servidor**; almacén equipo → **certlm.msc** |
| CN del sitio               | Debe coincidir con URL/certificado (CN/SAN)                         |
| SSL cliente                | Omitir / Aceptar / **Requerir**                                     |
| hosts                      | Solo local; ruta `drivers\etc\hosts`                                |
| EDGE + AC                  | `zpACas.cer` en **Raíces de confianza**                             |
| Firefox                    | Importar AC en **Autoridades** del propio Firefox                   |
| Firewall entrante/saliente | Bloqueado / Permitido por defecto                                   |
| ICMP                       | Sin puertos; regla eco ICMPv4; 4 pings en Windows                   |
| Regla salida 1 IP          | Dos rangos de bloqueo dejando hueco en `.200`                       |
| IPsec                      | Bilateral; firewall normal = unilateral                             |


---

## Checklist de capturas (entrega examen)

- Apartado 1b: asistente sitio HTTPS
- Apartado 1c: Configuración SSL (Requerir)
- Apartado 2b/c: EDGE antes/después de instalar AC (opcional)
- Apartado 3c: ping OK + regla ICMP habilitada
- Apartado 3d: ping fallido + regla deshabilitada
- Apartado 4a: Ámbito con dos rangos IP
- Apartado 4b: salida de ambos pings

## **Ejercicios prácticos propuestos**

### **APARTADO 5 — Reglas de seguridad de conexión (IPsec)**

> *Usando el Firewall con seguridad avanzada y el Visor de eventos.*

**a) Localización en** `wf.msc`  
Abre `wf.msc`. Indica en el panel izquierdo los **tres** tipos de reglas que aparecen. ¿En cuál crearías una regla para exigir que el tráfico entre la VM y la máquina física vaya protegido con IPsec? Captura del árbol con **Reglas de seguridad de conexión** visible.

**b) Comparación unilateral / bilateral**  
En el PC de la VM creas una regla de **entrada** que permite ICMP desde la IP de la máquina física. En la física **no** creas ninguna regla. ¿Funciona el ping si solo existe la regla en la VM?  
Repite el razonamiento: si solo en la VM creas una **regla de seguridad de conexión** que exige IPsec hacia la física, pero en la física no hay política compatible, ¿se establece IPsec? Justifica.

**c) Visor de eventos**  
Abre `eventvwr` y navega a:  
`Registros de aplicaciones y servicios` → `Microsoft` → `Windows` → `Windows Firewall With Advanced Security`.  
¿Qué diferencia hay entre los registros **Seguridad de conexión** y **Seguridad de conexión detallada**?  
Habilita (si está deshabilitado) el registro detallado, crea o modifica una regla de firewall cualquiera y otra acción que genere evento IPsec si la práctica lo permite; ¿qué tipo de información esperarías en cada registro?

**d) Escenario de diseño (sin implementar IPsec completo)**  
Se quiere que **solo** los equipos `192.168.0.10` (servidor) y `192.168.0.20` (cliente) se comuniquen por TCP **sin** IPsec, pero que **cualquier otro** tráfico entre esas dos IPs deba ir con autenticación IPsec.  
¿Bastaría con una regla de **salida** en el cliente? ¿Qué tipo de regla adicional necesitarías? ¿En cuántos equipos?