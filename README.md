# 🚀 MAZOX 6.2

> **"YA NO GASTES DINERO EN EL MAZO"**

**MAZOX** es un lenguaje de programación interpretado, ligero y modular diseñado sobre Python para ejecutarse de forma nativa en entornos como **Termux** y Linux. Esta documentación refleja de forma exacta el comportamiento y los comandos reales del intérprete `mazox.py` y del compilador `mazoxc.py`.

---

## 🆕 Novedades en v6.2

* **Lector real de `.mazoxpkg`**: el intérprete ya no trata los paquetes como texto plano. Ahora los parsea byte a byte, ejecuta su `/main.mazox` y conserva los binarios intactos.
* **Compilador oficial `mazoxc.py`**: convierte una carpeta de proyecto en un `.mazoxpkg` con un REPL dedicado.
* **7 comandos nuevos de paquete**: `abremazo:`, `mazopkglista`, `mazopkginfo`, `mazopkgleer:`, `mazopkgbinario:`, `mazopkgejecuta:`, `mazopkgcerrar`.
* **Soporte para `.mazox` normales** (texto plano, estilo bash) además de `.mazoxpkg`.
* **Detección automática del marcador binario** (`0x0B EndFile` o `EndFile` plano, por si el byte no se renderiza).

---

## 🛠️ Instalación y Requisitos

* **Python:** 3.8 o superior
* **Librerías estándar requeridas:** sys, os, math, json, heapq, sqlite3, urllib, re, datetime, hashlib, base64, statistics, itertools, functools, csv, zipfile, threading, asyncio, struct, pickle.

Archivos del sistema:

```
mazox.py       → intérprete (REPL + ejecutor de scripts)
mazoxc.py      → compilador de proyectos a .mazoxpkg
```

Para ejecutar el intérprete interactivo o un script:

``` bash
python mazox.py                          # consola interactiva
python mazox.py script.mazox             # ejecuta un .mazox (texto plano)
python mazox.py paquete.mazoxpkg         # abre y ejecuta /main.mazox del paquete
```

---

## 📚 Sintaxis General y Reglas

1. **Delimitación de Argumentos:**
   Todos los valores y argumentos de un comando deben ir estrictamente entre delimitadores angulares `<` y `>`. El parser no soporta comandos anidados en una sola asignación.

   ``` mazox
   mazo:<variable=valor>
   ```

2. **Resolución de Variables:**
   Para referenciar o concatenar el contenido de una variable, lista o diccionario en comandos de texto, antepón el símbolo `$`:

   ``` mazox
   yanog:<El valor guardado es $variable>
   ```

3. **Restricciones del Parser:**
   * **Una instrucción por línea:** No se pueden declarar estructuras multilínea tabuladas nativas de Python (como `if:` o `while:`).
   * **Macros en cadena:** Para ejecutar múltiples comandos en una sola línea (ideal para condicionales o bucles), se debe usar el comando del sistema `azomazo:` separando las órdenes con una tubería `|`.
   * **Operaciones Matemáticas:** Los comandos matemáticos nativos (`dinero:`, `menosmazo:`, etc.) **imprimen directamente en consola**; no devuelven un valor almacenable en memoria.

---

## 📋 Referencia de Comandos Reales

### 1. Salida y Consola
* **`yanog:<texto>`** — Imprime un mensaje con salto de línea. Soporta colores tipo Minecraft (`&r` Rojo, `&v` Verde, `&a` Amarillo, `&z` Azul, `&m` Magenta, `&c` Cian, `&b` Blanco, `&n` Negrita, `&0` Reset).
* **`yanogsmazo:<texto>`** — Imprime texto en la consola sin salto de línea.
* **`yanogmazo:<texto>`** — Imprime el texto formateado dentro de un recuadro gráfico.

### 2. Gestión de Memoria y Variables
* **`mazo:<nombre=valor>`** — Asigna una variable. Detecta automáticamente listas si usas `[1,2]` o diccionarios si usas `{"k":"v"}`.
* **`nomazo:<nombre>`** — **Elimina** de forma global una variable, lista, diccionario, set, stack o cola de la memoria activa.

### 3. Operaciones Matemáticas (Salida Directa)
* **`dinero:<a+b>`** — Realiza exclusivamente **sumas** aritméticas e imprime el resultado.
* **`menosmazo:<a-b>`** — Realiza operaciones de **resta**.
* **`masmazo:<a*b>`** — Realiza operaciones de **multiplicación**.
* **`delmazo:<a/b>`** — Realiza operaciones de **división**.

### 4. Estructuras de Control y Flujo
* **`si:<condicion -> comando>`** — Evalúa una condición (ej. `$contador == 5`) y ejecuta la acción si es verdadera.
* **`mientrasmazo:<condicion -> comando>`** — Bucle iterativo. Ejecuta el comando en bucle continuo mientras la condición sea válida (Tope de seguridad: 100,000 iteraciones).
* **`repmazo:<n -> comando>`** — Repite una acción exactamente *n* veces, inyectando el índice en la variable de sistema `$_i`.

### 5. Grafos y Rutas
* **`mazografo:<nombre=nodoA,nodoB,nodoC>`** — Inicializa un grafo con sus vértices correspondientes.
* **`mazografoarista:<grafo, nodo1->nodo2>`** — Crea una arista bidireccional entre ambos nodos.
* **`mazodijkstra:<grafo, inicio->fin>`** — Calcula e imprime la distancia más corta (peso constante de 1 por arista) entre el nodo de inicio y fin.

### 6. Sistema Avanzado
* **`mazoejecuta:<comando>`** — Ejecuta instrucciones directas en la terminal del sistema operativo (`os.system`).

---

## 📦 Gestión de Paquetes `.mazoxpkg` (Nuevo en v6.2)

### 6.1 Comandos del intérprete

| Comando | Descripción |
|---------|-------------|
| **`abremazo:<archivo.mazoxpkg>`** | Abre un paquete y ejecuta automáticamente su `/main.mazox`. |
| **`mazopkglista`** | Lista los archivos del paquete abierto con su tipo (`TXT`/`BIN`) y tamaño. |
| **`mazopkginfo`** | Muestra info general del paquete actual (número de archivos, marcador detectado, etc.). |
| **`mazopkgleer:</ruta/interna>`** | Imprime el contenido de un archivo de texto del paquete. |
| **`mazopkgbinario:</ruta,destino>`** | Extrae un archivo binario del paquete a disco, preservando sus bytes exactos. |
| **`mazopkgejecuta:</ruta/interna>`** | Ejecuta un archivo `.mazox` interno del paquete. |
| **`mazopkgcerrar`** | Cierra el paquete actual y libera la referencia. |

**Ejemplo de sesión:**

``` mazox
>> abremazo:MiPaquete.mazoxpkg
📦 Paquete abierto: MiPaquete.mazoxpkg (3 archivos, marcador: b'\x0bEndFile')
... salida de /main.mazox ...

>> mazopkglista
📦 Paquete con 3 archivos (marcador: b'\x0bEndFile')
  [TXT] /main.mazox (86 bytes)
  [TXT] /notes/readme.txt (1024 bytes)
  [BIN] /assets/imagen.png (20480 bytes)

>> mazopkgbinario:/assets/imagen.png,imagen_extraida.png
📦 Extraído '/assets/imagen.png' → 'imagen_extraida.png' (20480 bytes)
```

### 6.2 Estructura del formato

``1
MAZOXPKG
filesPaths=/main.mazox,/notes/readme.txt;
files=/main.mazox-Bin0Contains=...contenido...\x0BEndFile\n
     /notes/readme.txt-Bin0Contains=...contenido...\x0BEndFile
```

* **`MAZOXPKG`** → cabecera mágica (magic value).
* **`filesPaths=...;`** → índice de rutas separadas por `,` y terminadas en `;`.
* **`files=`** → inicio de contenidos.
* **`<ruta>-Bin0Contains=`** → archivo de texto.
* **`<ruta>-Bin1Contains=`** → archivo binario (bytes intactos).
* **`\x0BEndFile`** → cierra el paquete (byte `0x0B`, no los caracteres `"0B"`).
* **`\x0BEndFile\n`** → cierra un archivo intermedio.

### 6.3 Delimitación binaria (importante)

El formato no incluye un campo de longitud ni escape para el marcador de fin. El lector v6.2 mitiga esto:

1. **Archivos intermedios:** el marcador de fin debe ir seguido de la **ruta exacta del siguiente archivo** (`/<next>-Bin`). Así se descartan coincidencias accidentales.
2. **Último archivo:** se usa `rfind` exigiendo que tras el marcador solo queden espacios/EOF.
3. **Fallback:** primero se busca `\x0BEndFile`; si no aparece, se busca `EndFile` plano.

Limitación teórica única: un binario que contenga **literalmente** `\x0BEndFile\n<ruta_siguiente>-Bin`. Para eliminar esta limitación habría que cambiar el formato (campo de longitud o escape), lo cual **no** se ha hecho para mantener compatibilidad.

---

## 🔨 Compilador `mazoxc.py` (Nuevo en v6.2)

### 7.1 Estructura de proyecto

```
mi_paquete/
├── main.mazox              ← OBLIGATORIO (punto de entrada)
├── scripts/
│   ├── util.mazox
│   └── config.mazox
├── notes/
│   └── readme.txt
├── assets/
│   ├── imagen.png
│   └── sonido.wav
└── data/
    └── config.json
```

Reglas:

* Debe existir `main.mazox` en la raíz.
* Todos los archivos (incluyendo subcarpetas) se incluyen **excepto**: archivos ocultos (`.`), `.git`, `__pycache__`, `node_modules`, `.venv`, `venv`, `.pyc`, `.mazoxpkg`.
* Cada archivo se marca como `Bin0` o `Bin1` según su extensión y contenido.
* Los nombres no pueden contener `,` ni `;` (rompen `filesPaths`).

### 7.2 Uso del compilador

``` bash
# Desde la carpeta del proyecto
cd mi_paquete
python3 mazoxc.py

# O indicando la ruta del proyecto
python3 mazoxc.py /storage/emulated/0/MiPaquete
python3 mazoxc.py --help
```

El prompt cambia al estilo Termux:

```
/storage/emulated/0/MiPaquete >>
```

### 7.3 Comandos del compilador

| Comando | Descripción |
|---------|-------------|
| **`mazoruta:<ruta>`** | Cambia la carpeta del proyecto actual. |
| **`mazocd:<ruta>`** | Alias de `mazoruta:`. |
| **`mazoerrores`** | Detecta errores de compilación y advertencias. |
| **`mazocompilar`** | Compila el proyecto a `<nombre>.mazoxpkg`. |
| **`mazovalidar:<arch>`** | Verifica un `.mazoxpkg` ya compilado. |
| **`mazopreview`** | Vista previa (400 bytes) del paquete que se generaría. |
| **`mazolista`** | Lista archivos que se incluirán con tipo y tamaño. |
| **`mazotree`** | Muestra el árbol de carpetas del proyecto. |
| **`mazoinfo`** | Info del proyecto actual (rutas, conteo, salida). |
| **`mazoname:<nombre>`** | Cambia el nombre del archivo de salida. |
| **`mazoclean`** | Borra el `.mazoxpkg` compilado. |
| **`mazofind:<patron>`** | Busca archivos por substring en la ruta interna. |
| **`mazohistorial`** | Muestra los últimos 30 comandos. |
| **`ayuda`** / **`help`** | Muestra la ayuda. |
| **`limpiar`** / **`clear`** | Limpia la pantalla. |
| **`salir`** / **`exit`** | Sale del compilador. |

### 7.4 Flujo típico de compilación

``` bash
# 1. Crear estructura
mkdir -p MiPaquete/{scripts,notes}
cd MiPaquete

cat > main.mazox << 'EOF'
yanog:<Hola desde mi paquete mazoxpkg>
llamamazo:saludo
EOF

cat > scripts/util.mazox << 'EOF'
mazofuncion:saludo=yanog:<Hola desde util.mazox>
EOF

echo "Este es mi primer paquete" > notes/readme.txt

# 2. Abrir el compilador
python3 mazoxc.py /storage/emulated/0/MiPaquete
```

Dentro del REPL:

``` mazocompiler
/storage/emulated/0/MiPaquete >> mazoerrores
✓ Sin errores ni advertencias.

/storage/emulated/0/MiPaquete >> mazolista
Archivos a compilar (3):
  [TXT] /main.mazox (45 B)
  [TXT] /notes/readme.txt (26 B)
  [TXT] /scripts/util.mazox (53 B)
  Total: 124 B

/storage/emulated/0/MiPaquete >> mazocompilar
✓ Compilación exitosa
  → /storage/emulated/0/MiPaquete/MiPaquete.mazoxpkg
  3 archivo(s), 195 B

/storage/emulated/0/MiPaquete >> mazovalidar:MiPaquete.mazoxpkg
✓ Paquete válido: /storage/emulated/0/MiPaquete/MiPaquete.mazoxpkg

/storage/emulated/0/MiPaquete >> salir
Adiós.
```

Y finalmente ejecutar con el intérprete:

``` bash
python3 mazox.py /storage/emulated/0/MiPaquete/MiPaquete.mazoxpkg
```

### 7.5 Qué detecta `mazoerrores`

**Errores (bloquean la compilación):**
* Falta de `main.mazox`.
* Nombres con `,` o `;`.
* Archivos `.mazox` que no son UTF-8 válido.
* Archivos ilegibles.

**Advertencias (no bloquean):**
* Contenido con bytes `0x0B EndFile` (puede romper el formato).
* Archivos mayores a 50 MB.

---

## 💡 Ejemplo de Código Corregido (100% Funcional)

``` mazox
# --- Inicialización de variables ---
mazo:<limite=3>
mazo:<contador=0>

# --- Bucle Mientras con avance controlado ---
mientrasmazo:<$contador < $limite -> azomazo:<yanog:<&b[Iteración] Ejecutando paso número $contador...> | mazo:<contador=3> >>

# --- Demostración de Grafos y Caminos ---
mazografo:<red=A,B,C>
mazografoarista:<red, A->B>
mazografoarista:<red, B->C>
mazodijkstra:<red, A->C>
```

---

## 🎯 Ejemplo completo con `.mazoxpkg` (v6.2)

Proyecto `saludador/`:

```
saludador/
├── main.mazox
├── scripts/
│   └── funcion.mazox
└── notas/
    └── LEEME.txt
```

`main.mazox`:

``` mazox
yanog:<&v=== Saludador MAZOX v6.2 ===>
llamamazo:bienvenida
mazofuncion:despedida=yanog:<&a¡Hasta pronto!>
llamamazo:despedida
```

`scripts/funcion.mazox`:

``` mazox
mazofuncion:bienvenida=yanog:<&b¡Hola desde el paquete compilado!>
```

`notas/LEEME.txt`:

```
Este es un paquete .mazoxpkg de ejemplo.
```

Compilar y ejecutar:

``` bash
python3 mazoxc.py saludador/
# En el REPL:
saludador/ >> mazocompilar
saludador/ >> salir

python3 mazox.py saludador/saludador.mazoxpkg
```

Salida esperada:

```
📦 Paquete abierto: saludador/saludador.mazoxpkg (3 archivos, marcador: b'\x0bEndFile')
=== Saludador MAZOX v6.2 ===
¡Hola desde el paquete compilado!
¡Hasta pronto!
```

---

## ⚠️ Advertencia de Seguridad

El comando **`mazoejecuta:<comando>`** ejecuta instrucciones directas en la terminal del sistema operativo (`os.system`). Por razones de seguridad, **nunca ejecutes archivos `.mazoxpkg` de fuentes desconocidas** sin verificar primero que no contengan comandos maliciosos que puedan alterar tu sistema o acceder a tus archivos locales.

Se recomienda:

1. Compilar siempre desde carpetas de tu confianza.
2. Ejecutar `mazovalidar:` antes de abrir un paquete externo.
3. Inspeccionar el `main.mazox` con `mazopkgleer:/main.mazox` si recibiste un paquete de terceros.
4. Nunca ejecutar paquetes que contengan `mazoejecuta:` con comandos de shell sin revisarlos.

---

## 📝 Historial de versiones

| Versión | Cambios principales |
|---------|---------------------|
| **v5.0** | Base del lenguaje: variables, listas, dicts, sets, grafos, árboles, hilos, patrones, SQL, ZIP, HTTP, CSV. |
| **v5.5** | Comandos mazónicos: bóveda, pociones, mobs, mazmorras, logros, clanes, trades, recetas, hechizos, apuestas, misiones. |
| **v6.0** | +150 comandos nuevos, mejoras internas del parser. |
| **v6.1** | Correcciones menores de estabilidad. |
| **v6.2** | **Lector real de `.mazoxpkg`** (parseo binario, ejecución de `/main.mazox`), **soporte para `.mazox` planos**, **7 comandos nuevos de paquete**, **compilador `mazoxc.py`** con REPL dedicado, preview, validación y detección de errores de compilación. |

---

> 💡 **Recuerda:** YA NO GASTES DINERO EN EL MAZO 🪓 — pero ahora sí puedes **compilar tus propios paquetes** y distribuirlos como `.mazoxpkg`.
