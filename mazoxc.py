#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════════╗
║                   MAZOXPKG COMPILER v1.0                                           ║
║              Compilador de proyectos MAZO-X a .mazoxpkg                           ║
╚═══════════════════════════════════════════════════════════════════════╝

ESTRUCTURA DE UN PROYECTO MAZO-X
================================

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


REGLAS DEL COMPILADOR
=====================

1. La carpeta raíz del proyecto DEBE contener 'main.mazox'.
   Sin ese archivo, el compilador se niega a compilar.

2. TODOS los archivos dentro de la carpeta (en cualquier subcarpeta)
   se incluyen en el .mazoxpkg, EXCEPTO:
     - Archivos ocultos (empiezan con '.')
     - Carpetas ignoradas: .git, __pycache__, node_modules, .venv, venv
     - Archivos con extensión .pyc o .mazoxpkg (por seguridad)

3. Cada archivo se marca como texto (Bin0) o binario (Bin1):
     - Archivos .mazox → siempre Bin0
     - Otros que decodifiquen como UTF-8 → Bin0
     - Resto → Bin1
   Los bytes se preservan EXACTAMENTE, sin conversiones.

4. Las rutas internas son relativas a la raíz, con '/' al inicio:
       main.mazox          → /main.mazox
       notes/readme.txt    → /notes/readme.txt
       assets/imagen.png   → /assets/imagen.png

5. Los nombres NO pueden contener ',' ni ';' (rompen filesPaths).

6. Los archivos que contengan los bytes 0x0B 'EndFile' en su contenido
   generan advertencia porque pueden romper el formato al compilar.
   Se recomienda evitarlos o codificarlos (base64, etc.).


FORMATO GENERADO
================

    MAZOXPKG
    filesPaths=/main.mazox,/notes/readme.txt;
    files=/main.mazox-Bin0Contains=<contenido>\x0BEndFile\n
         /notes/readme.txt-Bin0Contains=<contenido>\x0BEndFile

Donde:
  - '\x0B' es el byte 0x0B (vertical tab), NO el texto "0B"
  - '\x0BEndFile\n' cierra archivos INTERMEDIOS (con salto de línea)
  - '\x0BEndFile'  cierra el ÚLTIMO archivo (sin salto de línea)


USO
===

    python3 mazoxc.py                        # abre en el cwd
    python3 mazoxc.py /ruta/a/mi/proyecto    # abre en esa ruta
    python3 mazoxc.py --help                 # muestra esta ayuda

COMANDOS DEL COMPILADOR
=======================

    mazoruta:<ruta>        Cambia la carpeta del proyecto
    mazocd:<ruta>          Alias de mazoruta
    mazoerrores            Detecta errores de compilación
    mazocompilar           Compila el proyecto a .mazoxpkg
    mazovalidar:<arch>     Verifica un .mazoxpkg ya compilado
    mazopreview            Vista previa del paquete compilado
    mazolista              Lista archivos que se incluirán
    mazotree               Muestra el árbol de carpetas
    mazoinfo               Información del proyecto actual
    mazoname:<nombre>      Cambia el nombre del archivo de salida
    mazoclean              Borra el .mazoxpkg compilado
    mazofind:<patron>      Busca archivos por patrón
    mazohistorial          Muestra el historial de comandos
    ayuda                  Muestra la ayuda
    limpiar                Limpia la pantalla
    salir                  Sale del compilador
"""

import os
import sys
import shutil

VERSION = "1.0"

# ─── Colores ANSI ──────────────────────────────────────────────
C = {
    "r": "\033[31m", "g": "\033[32m", "y": "\033[33m",
    "b": "\033[34m", "m": "\033[35m", "c": "\033[36m",
    "n": "\033[1m",  "0": "\033[0m",
}

def col(txt, *codes):
    return "".join(C.get(c, "") for c in codes) + str(txt) + C["0"]


# ─── Constantes del formato ────────────────────────────────────
MAGIC         = b"MAZOXPKG"
END_MARKER    = b"\x0bEndFile"      # cierra el paquete
END_MARKER_NL = b"\x0bEndFile\n"    # cierra un archivo intermedio

TEXT_EXTS = {
    ".mazox", ".txt", ".md", ".json", ".xml", ".html", ".htm",
    ".css", ".js", ".csv", ".yaml", ".yml", ".ini", ".cfg",
    ".log", ".py", ".sh", ".toml", ".svg",
}

IGNORE_DIRS  = {".git", "__pycache__", "node_modules",
                ".venv", "venv", ".idea", ".vscode"}
IGNORE_FILES = {".DS_Store", "Thumbs.db", "desktop.ini"}
IGNORE_EXTS  = {".mazoxpkg", ".pyc", ".pyo"}


# ─── Utilidades ────────────────────────────────────────────────
def is_text_content(path, data):
    """True si el archivo debe tratarse como texto (Bin0)."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".mazox":
        try:
            data.decode("utf-8")
            return True
        except UnicodeDecodeError:
            return False
    if ext in TEXT_EXTS:
        return True
    if b"\x00" in data:
        return False
    try:
        data.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def fmt_bytes(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


# ─── Verificación de un .mazoxpkg ──────────────────────────────
def verify_package_bytes(data):
    """Comprobación rápida de la estructura del paquete compilado."""
    if not data.startswith(MAGIC):
        return False, "no empieza con 'MAZOXPKG'"
    if not data.endswith(END_MARKER):
        return False, "no termina con 0x0B 'EndFile'"

    pos = len(MAGIC)
    while pos < len(data) and data[pos:pos+1] in (b" ", b"\n", b"\r", b"\t"):
        pos += 1
    if not data.startswith(b"filesPaths=", pos):
        return False, "falta 'filesPaths='"
    end = data.find(b";", pos)
    if end == -1:
        return False, "falta ';' tras filesPaths"
    pos = end + 1
    while pos < len(data) and data[pos:pos+1] in (b" ", b"\n", b"\r", b"\t"):
        pos += 1
    if not data.startswith(b"files=", pos):
        return False, "falta 'files='"
    return True, "OK"


def verify_package_file(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError as e:
        return False, f"No se pudo leer: {e}"
    return verify_package_bytes(data)


# ─── Proyecto ──────────────────────────────────────────────────
class Project:
    def __init__(self, root):
        self.root = os.path.abspath(root).rstrip("/") or "/"
        self._cache = None

    def has_main(self):
        return os.path.isfile(os.path.join(self.root, "main.mazox"))

    def is_valid(self):
        return os.path.isdir(self.root) and self.has_main()

    def scan(self, force=False):
        if self._cache is not None and not force:
            return self._cache

        result = []
        if not os.path.isdir(self.root):
            self._cache = result
            return result

        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = sorted(
                d for d in dirnames
                if d not in IGNORE_DIRS and not d.startswith(".")
            )
            for fname in sorted(filenames):
                if fname.startswith(".") or fname in IGNORE_FILES:
                    continue
                ext = os.path.splitext(fname)[1].lower()
                if ext in IGNORE_EXTS:
                    continue

                abs_path = os.path.join(dirpath, fname)
                rel = os.path.relpath(abs_path, self.root).replace(os.sep, "/")
                internal = "/" + rel

                entry = {
                    "internal": internal,
                    "abs": abs_path,
                    "size": 0,
                    "content": b"",
                    "is_bin": False,
                    "error": None,
                }
                try:
                    with open(abs_path, "rb") as f:
                        content = f.read()
                    entry["content"] = content
                    entry["size"] = len(content)
                    entry["is_bin"] = not is_text_content(abs_path, content)
                except OSError as e:
                    entry["error"] = str(e)

                result.append(entry)

        result.sort(key=lambda e: (e["internal"] != "/main.mazox", e["internal"]))
        self._cache = result
        return result

    def check(self):
        errors = []
        warns = []

        if not os.path.isdir(self.root):
            errors.append(f"La ruta no existe o no es una carpeta: {self.root}")
            return False, errors, warns

        if not self.has_main():
            errors.append("Falta el archivo OBLIGATORIO 'main.mazox' en la raíz")

        files = self.scan(force=True)

        if not files:
            errors.append("No se encontró ningún archivo para compilar")

        for f in files:
            if f["error"]:
                errors.append(f"{f['internal']}: {f['error']}")
                continue

            if "," in f["internal"] or ";" in f["internal"]:
                errors.append(
                    f"{f['internal']}: el nombre contiene ',' o ';' "
                    f"(rompe 'filesPaths')"
                )

            if f["internal"].endswith(".mazox") and f["is_bin"]:
                errors.append(
                    f"{f['internal']}: es .mazox pero no es UTF-8 válido"
                )

            if END_MARKER in f["content"]:
                warns.append(
                    f"{f['internal']}: contiene los bytes 0x0B 'EndFile' "
                    f"(puede romper el formato al compilar)"
                )

            if f["size"] > 50 * 1024 * 1024:
                warns.append(
                    f"{f['internal']}: archivo muy grande ({fmt_bytes(f['size'])})"
                )

        return len(errors) == 0, errors, warns

    def compile(self):
        ok, errors, warns = self.check()
        if not ok:
            return False, None, {"errors": errors, "warns": warns}

        files = self.scan(force=True)

        paths_str = ",".join(f["internal"] for f in files)
        out = bytearray()
        out += MAGIC + b"\n"
        out += b"filesPaths=" + paths_str.encode("utf-8") + b";\n"
        out += b"files="

        n = len(files)
        for i, f in enumerate(files):
            out += f["internal"].encode("utf-8")
            out += b"-Bin" + (b"1" if f["is_bin"] else b"0")
            out += b"Contains="
            out += f["content"]
            out += END_MARKER_NL if i < n - 1 else END_MARKER

        base = os.path.basename(self.root.rstrip("/")) or "paquete"
        out_name = base + ".mazoxpkg"
        out_path = os.path.join(self.root, out_name)

        try:
            with open(out_path, "wb") as fp:
                fp.write(out)
        except OSError as e:
            return False, None, {
                "errors": [f"No se pudo escribir: {e}"], "warns": warns
            }

        v_ok, v_msg = verify_package_bytes(bytes(out))
        if not v_ok:
            warns = warns + [f"Verificación interna falló: {v_msg}"]

        return True, out_path, {
            "files": n,
            "size": len(out),
            "warns": warns,
            "errors": [],
        }


# ─── Banner / ayuda ────────────────────────────────────────────
def banner():
    print(col(f"""
╔══════════════════════════════════════════════════╗
║        MAZOXPKG COMPILER v{VERSION}                  ║
║        'ayuda' para comandos                     ║
╚══════════════════════════════════════════════════╝
""", "c", "n"))


def print_help():
    print(f"""
{col('COMANDOS DEL COMPILADOR', 'c', 'n')}

  {col('mazoruta:<ruta>', 'y')}       Cambia la carpeta del proyecto
  {col('mazocd:<ruta>', 'y')}         Alias de mazoruta
  {col('mazoerrores', 'y')}           Detecta errores de compilación
  {col('mazocompilar', 'y')}          Compila el proyecto a .mazoxpkg
  {col('mazovalidar:<arch>', 'y')}    Verifica un .mazoxpkg ya compilado
  {col('mazopreview', 'y')}           Vista previa del paquete compilado
  {col('mazolista', 'y')}             Lista archivos que se incluirán
  {col('mazotree', 'y')}              Muestra el árbol de carpetas
  {col('mazoinfo', 'y')}              Información del proyecto actual
  {col('mazoname:<nombre>', 'y')}     Cambia el nombre del archivo de salida
  {col('mazoclean', 'y')}             Borra el .mazoxpkg compilado
  {col('mazofind:<patron>', 'y')}     Busca archivos por patrón
  {col('mazohistorial', 'y')}         Muestra el historial de comandos
  {col('ayuda', 'y')}                 Muestra esta ayuda
  {col('limpiar', 'y')}               Limpia la pantalla
  {col('salir', 'y')}                 Sale del compilador
""")


# ─── REPL ──────────────────────────────────────────────────────
class CompilerREPL:
    def __init__(self, start):
        self.project = Project(start)
        self.history = []
        self.custom_name = None

    def _prompt(self):
        return col(self.project.root, "g") + " " + col(">>", "m", "n") + " "

    def _status(self):
        if not os.path.isdir(self.project.root):
            print(col(f"✗ La ruta no existe: {self.project.root}", "r"))
            return
        if not self.project.has_main():
            print(col(f"⚠ Falta main.mazox en {self.project.root}", "y"))
            return
        n = len(self.project.scan())
        print(col(f"✓ Proyecto válido: {self.project.root}", "g"))
        print(f"  {n} archivo(s) detectado(s)")

    def run(self):
        banner()
        self._status()
        print()
        while True:
            try:
                line = input(self._prompt()).strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not line:
                continue
            self.history.append(line)
            if not self.dispatch(line):
                break

    def dispatch(self, line):
        if line in ("salir", "salirmazo", "exit", "quit"):
            print("Adiós.")
            return False
        if line in ("ayuda", "help"):
            print_help()
            return True
        if line in ("limpiar", "clear"):
            os.system("cls" if os.name == "nt" else "clear")
            return True

        if line.startswith("mazoruta:"):
            self._cambiar_ruta(line[len("mazoruta:"):].strip())
            return True
        if line.startswith("mazocd:"):
            self._cambiar_ruta(line[len("mazocd:"):].strip())
            return True
        if line == "mazoerrores":
            self._errores()
            return True
        if line == "mazocompilar":
            self._compilar()
            return True
        if line.startswith("mazovalidar:"):
            self._validar(line[len("mazovalidar:"):].strip())
            return True
        if line == "mazopreview":
            self._preview()
            return True
        if line == "mazolista":
            self._lista()
            return True
        if line == "mazotree":
            self._tree()
            return True
        if line == "mazoinfo":
            self._info()
            return True
        if line.startswith("mazoname:"):
            name = line[len("mazoname:"):].strip()
            if name:
                self.custom_name = name
                print(col(f"Nombre de salida: {name}.mazoxpkg", "g"))
            return True
        if line == "mazoclean":
            self._clean()
            return True
        if line.startswith("mazofind:"):
            self._find(line[len("mazofind:"):].strip())
            return True
        if line == "mazohistorial":
            self._historial()
            return True

        print(col(f"Comando no reconocido: '{line}'. Prueba 'ayuda'.", "r"))
        return True

    # ─── comandos ───
    def _cambiar_ruta(self, ruta):
        if not ruta:
            print(col("Uso: mazoruta:<ruta>", "r"))
            return
        ruta = os.path.expanduser(os.path.expandvars(ruta.rstrip("/") or "/"))
        if not os.path.isdir(ruta):
            print(col(f"✗ No es una carpeta válida: {ruta}", "r"))
            return
        self.project = Project(ruta)
        self.custom_name = None
        self._status()

    def _errores(self):
        print("Revisando proyecto...")
        ok, errors, warns = self.project.check()
        if errors:
            print(col(f"✗ {len(errors)} error(es):", "r"))
            for e in errors:
                print(f"   - {e}")
        if warns:
            print(col(f"⚠ {len(warns)} advertencia(s):", "y"))
            for w in warns:
                print(f"   - {w}")
        if ok and not warns:
            print(col("✓ Sin errores ni advertencias.", "g"))
        elif ok:
            print(col("✓ Compilable (con advertencias).", "g"))
        else:
            print(col("✗ Corrige los errores antes de compilar.", "r"))

    def _compilar(self):
        print("Compilando...")
        ok, out_path, info = self.project.compile()
        if not ok:
            print(col("✗ Compilación fallida:", "r"))
            for e in info.get("errors", []):
                print(f"   - {e}")
            return

        if self.custom_name:
            wanted = os.path.join(self.project.root, self.custom_name + ".mazoxpkg")
            if wanted != out_path:
                try:
                    if os.path.exists(wanted):
                        os.remove(wanted)
                    shutil.move(out_path, wanted)
                    out_path = wanted
                except OSError as e:
                    print(col(f"⚠ No se pudo renombrar: {e}", "y"))

        print(col("✓ Compilación exitosa", "g"))
        print(f"  → {out_path}")
        print(f"  {info['files']} archivo(s), {fmt_bytes(info['size'])}")
        if info.get("warns"):
            print(col(f"  ⚠ {len(info['warns'])} advertencia(s):", "y"))
            for w in info["warns"]:
                print(f"     - {w}")

    def _validar(self, ruta):
        if not ruta:
            print(col("Uso: mazovalidar:<archivo.mazoxpkg>", "r"))
            return
        if not os.path.isfile(ruta):
            alt = os.path.join(self.project.root, ruta)
            if os.path.isfile(alt):
                ruta = alt
            else:
                print(col(f"✗ No existe: {ruta}", "r"))
                return
        ok, msg = verify_package_file(ruta)
        if ok:
            print(col(f"✓ Paquete válido: {ruta}", "g"))
        else:
            print(col(f"✗ Paquete inválido: {msg}", "r"))

    def _preview(self):
        ok, errors, warns = self.project.check()
        if not ok:
            print(col("✗ No compilable:", "r"))
            for e in errors:
                print(f"   - {e}")
            return
        files = self.project.scan(force=True)
        n = len(files)
        out = bytearray()
        out += MAGIC + b"\n"
        out += b"filesPaths=" + ",".join(f["internal"] for f in files).encode() + b";\n"
        out += b"files="
        for i, f in enumerate(files):
            out += f["internal"].encode()
            out += b"-Bin" + (b"1" if f["is_bin"] else b"0")
            out += b"Contains="
            out += f["content"]
            out += END_MARKER_NL if i < n - 1 else END_MARKER

        preview = out[:400]
        print(col(f"Vista previa ({min(400, len(out))} de {len(out)} bytes):", "c"))
        print("─" * 60)
        try:
            print(preview.decode("utf-8", errors="replace"))
        except Exception:
            print(repr(preview))
        if len(out) > 400:
            print(col(f"... ({len(out) - 400} bytes más)", "y"))
        print("─" * 60)

    def _lista(self):
        files = self.project.scan(force=True)
        if not files:
            print("(sin archivos)")
            return
        print(col(f"Archivos a compilar ({len(files)}):", "c"))
        total = 0
        for f in files:
            if f["error"]:
                print(col(f"  ✗ {f['internal']} — {f['error']}", "r"))
                continue
            tipo = "BIN" if f["is_bin"] else "TXT"
            color = "y" if f["is_bin"] else "g"
            total += f["size"]
            print(f"  {col('[' + tipo + ']', color)} {f['internal']} "
                  f"({fmt_bytes(f['size'])})")
        print(f"  Total: {fmt_bytes(total)}")

    def _tree(self):
        if not os.path.isdir(self.project.root):
            print(col("Ruta inválida.", "r"))
            return
        print(col(self.project.root, "c", "n"))
        self._walk(self.project.root, "")

    def _walk(self, path, prefix):
        try:
            entries = sorted(os.listdir(path))
        except OSError:
            return
        entries = [e for e in entries
                   if not e.startswith(".") and e not in IGNORE_DIRS]
        for i, entry in enumerate(entries):
            full = os.path.join(path, entry)
            last = (i == len(entries) - 1)
            branch = "└── " if last else "├── "
            if os.path.isdir(full):
                print(f"{prefix}{branch}{col(entry + '/', 'b')}")
                self._walk(full, prefix + ("    " if last else "│   "))
            else:
                print(f"{prefix}{branch}{entry}")

    def _info(self):
        p = self.project
        print(col("Proyecto:", "c", "n"))
        print(f"  Ruta:      {p.root}")
        print(f"  Válido:    {'sí' if p.is_valid() else 'no'}")
        files = p.scan(force=True)
        txt  = sum(1 for f in files if not f["is_bin"] and not f["error"])
        bin_ = sum(1 for f in files if f["is_bin"] and not f["error"])
        print(f"  Archivos:  {len(files)} ({txt} texto, {bin_} binario(s))")
        print(f"  Tamaño:    {fmt_bytes(sum(f['size'] for f in files))}")
        base = os.path.basename(p.root.rstrip("/")) or "paquete"
        print(f"  Salida:    {self.custom_name or base}.mazoxpkg")

    def _clean(self):
        base = os.path.basename(self.project.root.rstrip("/")) or "paquete"
        name = self.custom_name or base
        path = os.path.join(self.project.root, name + ".mazoxpkg")
        if os.path.isfile(path):
            try:
                os.remove(path)
                print(col(f"✓ Borrado: {path}", "g"))
            except OSError as e:
                print(col(f"✗ No se pudo borrar: {e}", "r"))
        else:
            print(col(f"No existe: {path}", "y"))

    def _find(self, pat):
        if not pat:
            print(col("Uso: mazofind:<patron>", "r"))
            return
        files = self.project.scan(force=True)
        hits = [f for f in files if pat.lower() in f["internal"].lower()]
        if not hits:
            print(col(f"Sin coincidencias para '{pat}'.", "y"))
            return
        for f in hits:
            print(f"  {f['internal']}")

    def _historial(self):
        for i, h in enumerate(self.history[-30:], 1):
            print(f"  {i:3d}. {h}")


# ─── main ──────────────────────────────────────────────────────
def main():
    args = sys.argv[1:]
    if args and args[0] in ("-h", "--help", "help"):
        print(__doc__)
        return
    start = args[0] if args else os.getcwd()
    if not os.path.isdir(start):
        print(col(f"Ruta inválida: {start}", "r"))
        sys.exit(1)
    CompilerREPL(start).run()


if __name__ == "__main__":
    main()
