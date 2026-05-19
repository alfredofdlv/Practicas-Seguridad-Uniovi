# ÍNDICE DE FUNCIONES — KIT EXAMEN CRIPTOGRAFÍA

> **Kit completo:** `Criptografia/FuncionesResumen/kit_examen_cripto.py`
> **Guía conceptual:** `Apuntes/Guia_Examen_Criptografia.md`
>
> Todas las funciones están en el mismo fichero; basta con copiarlo entero
> o importar lo que necesites: `from kit_examen_cripto import hibrido_rsa_cifrar`.

---

## Tabla maestra

| Función | Bloque | Entradas clave | Salida | Nota examen |
|---------|--------|----------------|--------|-------------|
| `fernet_generar_clave()` | 1 Simétrico | — | `bytes` (clave) | Generar antes de `fernet_cifrar` |
| `fernet_guardar_clave(clave, ruta)` | 1 | `bytes`, `str` | — | Modo `"wb"` |
| `fernet_cargar_clave(ruta)` | 1 | `str` | `bytes` | Modo `"rb"` |
| `fernet_cifrar(mensaje, clave)` | 1 | `bytes`, `bytes` | token `bytes` | |
| `fernet_descifrar(token, clave)` | 1 | `bytes`, `bytes` | `bytes` | Lanza `InvalidToken` si falla |
| `fernet_cifrar_fichero(entrada, salida, clave)` | 1 | `str`, `str`, `bytes` | — | Lee `rb`, escribe `wb` |
| `fernet_descifrar_fichero(ruta_enc, clave)` | 1 | `str`, `bytes` | `bytes` | |
| `rsa_generar()` | 2 Claves RSA | — | `(priv, pub)` | |
| `rsa_guardar_pem(priv, pub, nombre)` | 2 | obj, obj, `str` | — | `rsa_privada_{nombre}.pem` |
| `rsa_cargar_pem(nombre)` | 2 | `str` | `(priv, pub)` | |
| `rsa_guardar_pem_ruta(priv, pub, ruta_priv, ruta_pub)` | 2 | obj, obj, `str`, `str` | — | Rutas absolutas |
| `rsa_cargar_pem_ruta(ruta_priv, ruta_pub)` | 2 | `str`, `str` | `(priv, pub)` | |
| `ecies_generar()` | 3 Claves ECIES | — | `(priv_hex, pub_hex)` | |
| `ecies_guardar_txt(priv_hex, pub_hex, nombre)` | 3 | `str`, `str`, `str` | — | `ecies_claves_{nombre}.txt` |
| `ecies_cargar_txt(nombre)` | 3 | `str` | `(priv_hex, pub_hex)` | |
| `rsa_cifrar_oaep(mensaje, pub)` | 4 RSA ops | `bytes`, obj | `bytes` | Límite ~190 B |
| `rsa_descifrar_oaep(cifrado, priv)` | 4 | `bytes`, obj | `bytes` | |
| `rsa_firmar(mensaje, priv)` | 4 | `bytes`, obj | firma `bytes` | RSA hashea internamente |
| `rsa_verificar(firma, mensaje, pub)` | 4 | `bytes`, `bytes`, obj | `bool` | |
| `rsa_firmar_prehashed(msg_hash, priv)` | 4 | `bytes`(32), obj | firma `bytes` | `sha256(m).digest()` |
| `rsa_verificar_prehashed(firma, msg_hash, pub)` | 4 | `bytes`, `bytes`(32), obj | `bool` | |
| `ecies_cifrar(mensaje, pub_hex)` | 5 ECIES ops | `bytes`, `str` | `bytes` | |
| `ecies_descifrar(cifrado, priv_hex)` | 5 | `bytes`, `str` | `bytes` | |
| `ecies_firmar(mensaje, priv_hex)` | 5 | `bytes`, `str` | firma `bytes` | Hashea SHA256 internamente |
| `ecies_verificar(firma_bytes, mensaje, pub_hex)` | 5 | `bytes`, `bytes`, `str` | `bool` | |
| `hash_sha256_segmentos(*segs)` | 6 Hash | `bytes...` | hex `str` | Para JSON/comparar en texto |
| `hash_sha256_bytes(*segs)` | 6 | `bytes...` | `bytes` (32) | Para firmar / HMAC |
| `hash_sha256_cryptography(*segs)` | 6 | `bytes...` | hex `str` | Usa librería `cryptography` |
| `hash_cadena_siguiente(msg, hash_previo)` | 6 | `bytes`, `bytes` | `bytes` | SHA256(msg + hash_previo) |
| `hash_verificar_segmentos(hex_esp, *segs)` | 6 | `str`, `bytes...` | `bool` | |
| `hibrido_rsa_cifrar(mensaje, pub_destino)` | 7 Híbrido RSA | `bytes`, obj | `(clave_enc, msg_enc)` | Firma aparte |
| `hibrido_rsa_descifrar(clave_enc, msg_enc, priv)` | 7 | `bytes`, `bytes`, obj | `bytes` | |
| `hibrido_ecies_cifrar(mensaje, pub_hex)` | 8 Híbrido ECIES | `bytes`, `str` | `(clave_enc, msg_enc)` | Firma aparte |
| `hibrido_ecies_descifrar(clave_enc, msg_enc, priv_hex)` | 8 | `bytes`, `bytes`, `str` | `bytes` | |
| `empaquetar_json_firma(mensaje, priv)` | 9 Firma interna RSA | `bytes`, obj | `bytes` | **Más probable** en examen |
| `desempaquetar_json_firma(payload, pub)` | 9 | `bytes`, obj | `(msg, bool)` | |
| `hibrido_rsa_cifrar_firma_interna(msg, priv_orig, pub_dest)` | 9 | — | `(clave_enc, payload_enc)` | |
| `hibrido_rsa_descifrar_firma_interna(clave, payload, priv, pub)` | 9 | — | `(msg, bool)` | |
| `empaquetar_json_firma_ecies(mensaje, priv_hex)` | 9b Firma interna ECIES | `bytes`, `str` | `bytes` | |
| `desempaquetar_json_firma_ecies(payload, pub_hex)` | 9b | `bytes`, `str` | `(msg, bool)` | |
| `hibrido_ecies_cifrar_firma_interna(msg, priv_hex, pub_hex)` | 9b | — | `(clave_enc, payload_enc)` | |
| `hibrido_ecies_descifrar_firma_interna(clave, payload, priv_hex, pub_hex)` | 9b | — | `(msg, bool)` | |
| `hash_mensaje_sesion(token, mensaje)` | 9c Sesión Ronda2 | `str`, `bytes` | hex `str` | |
| `empaquetar_json_firma_sesion(msg, priv, token)` | 9c | — | `bytes` | JSON: mensaje+firma+hash_msg |
| `desempaquetar_json_firma_sesion(payload, pub, token)` | 9c | — | `(msg, hash_ok, firma_ok)` | |
| `hibrido_rsa_cifrar_sesion(msg, priv, pub, token)` | 9c | — | `(clave_enc, payload_enc)` | |
| `hibrido_rsa_descifrar_sesion(clave, payload, priv, pub, token)` | 9c | — | `(msg, hash_ok, firma_ok)` | |
| `empaquetar_coma(mensaje, priv)` | 10 Empaquetar | `bytes`, obj | `bytes` | msg_b64,firma_b64 |
| `desempaquetar_coma(payload, pub)` | 10 | `bytes`, obj | `(msg, bool)` | `split(",",1)` |
| `empaquetar_pipe(mensaje, priv)` | 10 | — | `bytes` | msg_b64\|firma_b64 |
| `desempaquetar_pipe(payload, pub)` | 10 | — | `(msg, bool)` | |
| `empaquetar_dos_lineas(mensaje, priv)` | 10 | — | `bytes` | msg_b64\nfirma_b64 |
| `desempaquetar_dos_lineas(payload, pub)` | 10 | — | `(msg, bool)` | |
| `empaquetar_binario_fijo(mensaje, priv)` | 10 | — | `bytes` | mensaje+firma(256B) |
| `desempaquetar_binario_fijo(paquete, pub)` | 10 | — | `(msg, bool)` | `paquete[-256:]` |
| `empaquetar_struct(mensaje, priv)` | 10 | — | `bytes` | 4B longitud+firma+msg |
| `desempaquetar_struct(paquete, pub)` | 10 | — | `(msg, bool)` | |
| `derivar_clave_maestra(contrasena_admin)` | 11 Auth | `str` | clave Fernet `bytes` | PBKDF2+urlsafe_b64encode |
| `cifrar_fichero(ruta_txt, ruta_enc, pwd_admin)` | 11 | `str`, `str`, `str` | — | Borra plano por defecto |
| `descifrar_fichero(ruta_enc, pwd_admin)` | 11 | `str`, `str` | `str` | UTF-8 |
| `hasheo_password(contrasena, salt)` | 11 | `str`, `bytes` | base64 `str` | Para guardar en CSV |
| `verifica_password(contrasena, salt, hash_alm)` | 11 | `str`, `bytes`, `str` | `bool` | PBKDF2.verify |
| `alta_usuario_linea(nombre, contrasena)` | 11 | `str`, `str` | línea CSV `str` | Añadir con `f.write(...)` |
| `generar_token_sesion(usuario)` | 11 | `str` | hex `str` | SHA256(user:ts:salt) |
| `autentica_usuario(usuario, pwd, ruta_enc, pwd_admin)` | 11 | — | `(bool, token\|None)` | Flujo completo |
| `hmac_generar(clave, mensaje)` | 12 HMAC | `bytes`, `bytes` | `bytes` | Canal simétrico |
| `hmac_verificar(clave, mensaje, mac)` | 12 | `bytes`, `bytes`, `bytes` | `bool` | compare_digest |
| `cadena_enviar_ab(mensaje, clave_ab)` | 13 Cadena | `bytes`, `bytes` | `(cifrado, hash1)` | |
| `cadena_recibir_ab(cifrado, hash1, clave_ab)` | 13 | — | `(msg, hash_ok)` | |
| `cadena_reenviar_bc(msg_bc, hash1, clave_bc)` | 13 | — | `(cifrado, hash1, hash2)` | |
| `cadena_recibir_bc(cifrado, hash1, hash2, clave_bc)` | 13 | — | `(msg, h1_ok, h2_ok)` | |

---

## Snippets de uso rápido

### Simétrico

```python
clave = fernet_generar_clave()
token = fernet_cifrar(b"mensaje", clave)
msg   = fernet_descifrar(token, clave)
```

### Claves RSA

```python
priv, pub = rsa_generar()
rsa_guardar_pem(priv, pub, "A")
priv, pub = rsa_cargar_pem("A")
```

### Claves ECIES

```python
priv_hex, pub_hex = ecies_generar()
ecies_guardar_txt(priv_hex, pub_hex, "A")
priv_hex, pub_hex = ecies_cargar_txt("A")
```

### Híbrido RSA (firma aparte)

```python
firma = rsa_firmar(mensaje, priv_a)
clave_enc, msg_enc = hibrido_rsa_cifrar(mensaje, pub_b)
# --- red ---
msg = hibrido_rsa_descifrar(clave_enc, msg_enc, priv_b)
ok  = rsa_verificar(firma, msg, pub_a)
```

### Híbrido RSA con firma interna (más probable en examen)

```python
clave_enc, payload_enc = hibrido_rsa_cifrar_firma_interna(mensaje, priv_a, pub_b)
# --- red ---
msg, firma_ok = hibrido_rsa_descifrar_firma_interna(clave_enc, payload_enc, priv_b, pub_a)
```

### Híbrido RSA Ronda2 (firma + hash de sesión)

```python
token = generar_token_sesion("alice")
clave_enc, payload_enc = hibrido_rsa_cifrar_sesion(mensaje, priv_a, pub_b, token)
# --- red ---
msg, hash_ok, firma_ok = hibrido_rsa_descifrar_sesion(clave_enc, payload_enc, priv_b, pub_a, token)
```

### Hash y verificar integridad

```python
hash_hex = hash_sha256_segmentos(seg1, seg2, seg3)
ok = hash_verificar_segmentos(hash_esperado, seg1, seg2, seg3)
```

### Cadena de hashes A→B→C

```python
cifrado_ab, hash1 = cadena_enviar_ab(mensaje_ab, clave_ab)
msg_ab, h1_ok     = cadena_recibir_ab(cifrado_ab, hash1, clave_ab)
cifrado_bc, h1, hash2 = cadena_reenviar_bc(mensaje_bc, hash1, clave_bc)
msg_bc, _, h2_ok  = cadena_recibir_bc(cifrado_bc, h1, hash2, clave_bc)
```

### Fichero cifrado con contraseña admin

```python
# Alta y cifrado
linea = alta_usuario_linea("alice", "pass1234")
with open("medicos.txt", "w") as f:
    f.write(linea)
cifrar_fichero("medicos.txt", "medicos.txt.enc", "clave_admin_secreta")

# Autenticación
ok, token = autentica_usuario("alice", "pass1234", "medicos.txt.enc", "clave_admin_secreta")
```

### HMAC (canal simétrico)

```python
mac = hmac_generar(clave_compartida, mensaje)
ok  = hmac_verificar(clave_compartida, mensaje, mac)
```

---

## Árbol de decisión — "si el enunciado pide X"

| Si pide… | Función(es) a usar |
|----------|--------------------|
| Cifrar fichero completo con contraseña | `derivar_clave_maestra` + `cifrar_fichero` / `descifrar_fichero` |
| Autenticar usuario contra fichero cifrado | `autentica_usuario` (o desglosar con `verifica_password`) |
| Firma dentro del cifrado Fernet (firma interna) | `hibrido_rsa_cifrar_firma_interna` / `..._descifrar_firma_interna` |
| Token de sesión ligado al mensaje | `generar_token_sesion` + `hibrido_rsa_cifrar_sesion` |
| Verificar integridad de segmentos con hash | `hash_verificar_segmentos` |
| Trazabilidad A→B→C con hashes encadenados | `cadena_enviar_ab` / `cadena_reenviar_bc` / `cadena_recibir_bc` |
| Autenticación simétrica sin RSA | `hmac_generar` + `hmac_verificar` |
| Unir mensaje y firma para enviar | `empaquetar_json_firma` (o variante `_coma`, `_pipe`, `_struct`…) |
