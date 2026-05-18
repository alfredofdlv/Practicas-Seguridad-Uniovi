# ENUNCIADOS DE PRÁCTICA — CRIPTOGRAFÍA

> Ejercicios que combinan varios conceptos del temario para simular condiciones de examen.
> Soluciones en `Criptografia/Examen-Enero/` para referencia.

---

## EJERCICIO 1 — Autenticación + Cifrado Híbrido RSA

**Dificultad:** Media-Alta | **Conceptos:** PBKDF2, Hash, RSA, Fernet, Firma

### Escenario

Un hospital tiene tres médicos (A, B, C) registrados en un sistema de autenticación seguro. Antes de poder enviar o recibir información, cada médico debe autenticarse con su usuario y contraseña. Solo una vez autenticado, puede participar en la comunicación cifrada.

### Tareas

**Parte 1 — Sistema de registro y autenticación**

Crea dos módulos:

- `registro.py`: permite dar de alta a un médico. Almacena en `medicos.txt` el nombre, un salt aleatorio (`os.urandom(16)`) y el hash de la contraseña derivado con `PBKDF2HMAC` (SHA256, 100000 iteraciones, 32 bytes). Las contraseñas **nunca se almacenan en texto plano**. El fichero usa `,` como separador.
- `autenticar.py`: dado un nombre y contraseña, lee `medicos.txt`, recupera el salt (decodificado desde base64) y verifica la contraseña usando `PBKDF2HMAC.verify()`. Imprime si la autenticación fue correcta, contraseña incorrecta, o usuario no encontrado.

**Parte 2 — Comunicación cifrada tras autenticación**

Una vez autenticado el médico A, este envía un informe confidencial a B. El médico B, tras recibirlo, lo reenvía a C.

Requisitos del cifrado:

- Cifrado **híbrido RSA + Fernet** (claves en `.pem`).
- El médico A **firma** el informe  antes de cifrar.
- El médico B **verifica** la firma de A tras descifrar.
- La firma debe viajar **dentro del cifrado Fernet** (embebida en el payload JSON, igual que `Ejercicio-Hibrido-FirmaInterna.py`).
- El programa solo llega al cifrado si la autenticación de A fue exitosa.

**Datos a usar:**

```
Informe A→B: b"Historia clinica paciente 42: diagnostico reservado."
Informe B→C: b"Validado por Dr. B. Derivar a oncologia."
```

**Estructura sugerida:**

```
main()
  └─ autenticar('medicoA', 'conA')  → si True, continuar
  └─ generar/cargar claves RSA para A, B, C
  └─ enviar(A→B): firma + cifra híbrido (firma interna)
  └─ recibir(B): descifra + verifica firma de A
  └─ enviar(B→C): firma + cifra híbrido
  └─ recibir(C): descifra + verifica firma de B
```

---

## EJERCICIO 2 — Integridad Hash + Cifrado Híbrido ECIES

**Dificultad:** Media | **Conceptos:** hashlib update(), SHA256, ECIES, Fernet, Firma ECDSA

### Escenario

Un servidor de actualizaciones distribuye un parche de seguridad crítico dividido en **3 segmentos** por limitaciones de red. El administrador A recibe los 3 segmentos y debe verificar la integridad del parche completo antes de reenviarlo cifrado a los administradores B y C.

### Tareas

**Parte 1 — Verificación de integridad**

Usando `hashlib` y el método `update()` (lectura incremental), calcula el SHA256 del parche completo concatenando los 3 segmentos y compara con el hash oficial. **Si el hash no coincide, el programa debe abortar** sin cifrar nada.

```python
segmento_1 = b"PARCHE_v2.1_INICIO_[kernel-patch-header]_"
segmento_2 = b"PARCHE_v2.1_CUERPO_[memory-allocator-fix]_"
segmento_3 = b"PARCHE_v2.1_FIN_[checksum-validation]"
hash_oficial = "CALCULA_Y_PON_AQUI_EL_HASH_CORRECTO"
```

**Parte 2 — Distribución cifrada (solo si el hash es válido)**

Si la integridad es correcta, A envía el parche completo (segmentos concatenados) a B y a C usando cifrado **híbrido ECIES + Fernet**. 

A firma el parche con ECDSA antes de enviarlo. 

B y C deben descifrar y verificar la firma de A.

No es necesaria transitividad (A envía directamente a ambos B y C, no B reenvía a C).

**Requisitos adicionales:**

- Claves ECIES en ficheros `.txt` hexadecimales.
- Modularización completa con prints descriptivos.
- La firma viaja como elemento separado (versión estándar, no interna).

---

## EJERCICIO 3 — Autenticación + Hash de Sesión + Híbrido ECIES (Nivel Alto)

**Dificultad:** Alta | **Conceptos:** PBKDF2, SHA256, ECIES, Fernet, ECDSA, JSON

### Escenario

Una empresa de auditoría tiene tres auditores (A, B, C). El sistema exige:

1. Que cada auditor se autentique antes de operar.
2. Que cada mensaje incluya un **hash SHA256 del mensaje** junto con la firma, ambos empaquetados dentro del cifrado Fernet (firma interna).
3. Que el receptor, además de verificar la firma ECDSA, verifique también que el hash del mensaje recibido coincide con el hash incluido en el payload.

### Tareas

**Parte 1 — Registro**

Crea `registro_auditores.py` que registre a los 3 auditores en `auditores.txt` con PBKDF2 + salt (igual que el ejercicio anterior). Contraseñas: `conA`, `conB`, `conC`.

**Parte 2 — Payload extendido**

El payload JSON que se cifra con Fernet debe incluir **tres campos**:

```json
{
  "mensaje":  "<base64 del mensaje>",
  "firma":    "<base64 de la firma ECDSA>",
  "hash_msg": "<hexdigest SHA256 del mensaje>"
}
```

**Parte 3 — Flujo de comunicación**

Solo los auditores autenticados pueden operar. Al recibir un mensaje, el receptor debe:

1. Descifrar el payload Fernet.
2. Verificar que `SHA256(mensaje_recuperado).hexdigest() == hash_msg` del payload.
3. Verificar la firma ECDSA con la pública del emisor.
4. Solo si ambas verificaciones pasan, imprimir el mensaje.

Comunicación: A → B → C (B reenvía a C con su propia firma y hash).

**Datos:**

```python
mensaje_AB = b"Auditoria Q3: se detectaron 3 anomalias en contabilidad."
mensaje_BC = b"Anomalias confirmadas por B. Escalado a direccion."
```

---

## EJERCICIO 4 — Cifrado Simétrico por Canales + Detección de Alteración

**Dificultad:** Media | **Conceptos:** Fernet, hashlib, integridad, manejo de excepciones

### Escenario

Un sistema de mensajería interna usa **cifrado simétrico por canal** (A-B y B-C usan claves distintas). Cada mensaje va acompañado de su hash SHA256 calculado **antes de cifrar**. El receptor, después de descifrar, recalcula el hash y lo compara para detectar posibles alteraciones o fallos de transmisión.

### Tareas

**Parte 1 — Comunicación normal**

Implementa el canal A→B y B→C con Fernet. Cada `enviar_mensaje()` debe:

- Calcular el hash SHA256 del mensaje en texto claro.
- Cifrar el mensaje con Fernet.
- Retornar `(mensaje_cifrado, hash_original)`.

Cada `recibir_mensaje()` debe:

- Descifrar el mensaje con Fernet.
- Recalcular el hash del mensaje descifrado.
- Comparar con `hash_original` e imprimir si la integridad es correcta o fue comprometida.

**Parte 2 — Simulación de ataque**

Crea una función `simular_alteracion(mensaje_cifrado)` que modifique un byte del mensaje cifrado y retorne el mensaje alterado. Llama a `recibir_mensaje()` con el mensaje alterado. El programa debe capturar la excepción `InvalidToken` de Fernet (que salta antes incluso de llegar al hash) e imprimirla como evidencia de la alteración.

**Datos:**

```python
mensaje_AB = b"Transferencia autorizada: 50000 EUR a cuenta ES12-0000."
mensaje_BC = b"Validado por B. Proceder con la transferencia."
```

> Este ejercicio ilustra por qué Fernet ya incluye un HMAC interno: detecta alteraciones antes incluso de descifrar.
>
>

