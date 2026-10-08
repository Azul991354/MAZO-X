# 🚀 MAZOX 6.1

> **"YA NO GASTES DINERO EN EL MAZO"**

**MAZOX** es un lenguaje de programación interpretado, ligero y modular diseñado sobre Python para ejecutarse de forma nativa en entornos como **Termux** y Linux. Esta documentación refleja de forma exacta el comportamiento y los comandos reales del intérprete `mazox.py`.

---

## 🛠️ Instalación y Requisitos

* **Python:** 3.8 o superior
* **Librerías estándar requeridas:** sys, os, math, json, heapq, sqlite3, urllib, re, datetime, hashlib, base64, statistics, itertools, functools, csv, zipfile, threading, asyncio.

Para ejecutar el intérprete interactivo o un script `.mazoxpkg`:

```bash
python mazox.py
python mazox.py util.mazoxpkg
```
*(Nota: El intérprete interactivo acepta comandos en vivo, mientras que los scripts automatizados deben usar obligatoriamente la extensión `.mazoxpkg`)*

---

## 📚 Sintaxis General y Reglas

1. **Delimitación de Argumentos:**
   Todos los valores y argumentos de un comando deben ir estrictamente entre delimitadores angulares `<` y `>`. El parser no soporta comandos anidados en una sola asignación.
   `mazo:<variable=valor>`

2. **Resolución de Variables:**
   Para referenciar o concatenar el contenido de una variable, lista o diccionario en comandos de texto, antepón el símbolo `$`:
   `yanog:<El valor guardado es $variable>`

3. **Restricciones del Parser:**
   * **Una instrucción por línea:** No se pueden declarar estructuras multilínea tabuladas nativas de Python (como `if:` o `while:`).
   * **Macros en cadena:** Para ejecutar múltiples comandos en una sola línea (ideal para condicionales o bucles), se debe usar el comando del sistema `azomazo:` separando las órdenes con una tubería `|`.
   * **Operaciones Matemáticas:** Los comandos matemáticos nativos (`dinero:`, `menosmazo:`, etc.) **imprimen directamente en consola**; no devuelven un valor almacenable en memoria.

---

## 📋 Referencia de Comandos Reales (v5.0)

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

## 💡 Ejemplo de Código Corregido (100% Funcional)

Este script está adaptado a las capacidades exactas de tu parser lineal. Modifica el contador en una macro estática para controlar el flujo sin caer en ciclos infinitos y ejecuta operaciones de grafos válidas:

```mazoxpkg
# --- Inicialización de variables ---
mazo:<limite=3>
mazo:<contador=0>

# --- Bucle Mientras con avance controlado ---
# Nota: Como el parser es lineal y los comandos matemáticos imprimen en pantalla,
# usamos azomazo para simular las fases del contador de forma segura.
mientrasmazo:<$contador < $limite -> azomazo:<yanog:<&b[Iteración] Ejecutando paso número $contador...> | mazo:<contador=3> >>

# --- Demostración de Grafos y Caminos ---
mazografo:<red=A,B,C>
mazografoarista:<red, A->B>
mazografoarista:<red, B->C>
mazodijkstra:<red, A->C>
```

---

## ⚠️ Advertencia de Seguridad

El comando **`mazoejecuta:<comando>`** ejecuta instrucciones directas en la terminal del sistema operativo (`os.system`). Por razones de seguridad, **nunca ejecutes archivos `.mazoxpkg` de fuentes desconocidas** sin verificar primero que no contengan comandos maliciosos que puedan alterar tu sistema o acceder a tus archivos locales.
