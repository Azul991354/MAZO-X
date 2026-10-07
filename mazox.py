# ======================= #
# MAZOX SYSTEM 6.0        #
# ––––––––––––––––––––––– #
#  v6.0 YA esta HECHO!!!  #
#  + 150 COMANDOS NUEVOS  #
#  NO SE QUE MAS DECIR    #
#  YA NO GASTES DINERO    #
#  EN EL MAZO!!!          #
# ======================= #

import sys
import time
import random
import os
import math
import json
import re
import datetime
import hashlib
import base64
import statistics
import itertools
import functools
import threading
import csv
import pickle
import sqlite3
import zipfile
import gzip
import bz2
import tarfile
import shutil
import subprocess
import platform
import urllib.request
import urllib.parse
import urllib.error
import smtplib
import socket
import uuid
import secrets
import textwrap
import string
import unicodedata
import difflib
import colorsys
import calendar
import decimal
import fractions
import copy
import struct
import binascii
import hmac
import zlib
import getpass
import glob
import heapq
import queue
from collections import deque, Counter, defaultdict, OrderedDict, namedtuple
from email.mime.text import MIMEText
from functools import lru_cache, reduce
from itertools import combinations, permutations, product, chain, groupby

# =========================
# ESTADO GLOBAL
# =========================
variables = {}
listas = {}
diccionarios = {}
sets_mazo = {}
stacks_mazo = {}
queues_mazo = {}
clases_mazo = {}
instancias_mazo = {}
funciones = {}
store = {}
aliases = {}
historial = []
pila_retorno = []
modulos_mazo = {}
estados_mazo = {}
eventos_mazo = {}
try_stack = []

# v5.0
grafos_mazo = {}
arboles_mazo = {}
prioridades_mazo = {}
caches_mazo = {}
memos_mazo = {}
pipelines_mazo = {}
currys_mazo = {}
composiciones_mazo = {}
observadores_mazo = {}
singletons_mazo = {}
hilos_mazo = {}
async_mazo = {}
promesas_mazo = {}
factories_mazo = {}
strategies_mazo = {}
builders_mazo = {}
decoradores_mazo = {}
generadores_mazo = {}
iteradores_mazo = {}
lambdas_mazo = {}
enums_mazo = {}
dataclasses_mazo = {}

# v5.5 — ESTADO NUEVO
boveda_mazo = {}          # bóveda secreta mazónica
pociones_mazo = {}        # pociones con efectos
encantamientos_mazo = {}  # encantamientos para funciones
mobs_mazo = {}            # mobs del mazo
mazmorras_mazo = {}       # mazmorras
logros_mazo = set()       # logros desbloqueados
inventario_mazo = {}      # inventario por jugador
trades_mazo = {}          # trades con aldeanos
recetas_mazo = {}         # recetas de crafteo
encantamientos_items = {}
hechizos_mazo = {}
clanes_mazo = {}
rankings_mazo = {}
torneos_mazo = {}
apuestas_mazo = {}
contratos_mazo = {}
misiones_mazo = {}
logros_secretos = {}
chismes_mazo = []
rumores_mazo = []
burlas_mazo = [
    "¿Otra vez con el mazo? Ya no gastes dinero en el mazo 🪓",
    "El mazo de Minecraft quedó inservible desde la lanza... ni lo intentes",
    "Ese mazo ya no sirve, mejor gasta el dinero en pociones 🧪",
    "Un mazo sin filo es como un día sin creeper explotando",
    "Ese mazo era legendario... hasta que llegó la lanza 🪓→🗡️",
]
packs_mazo = {}
logros_def = {
    "primermazo": "Creaste tu primer mazo",
    "cazador": "Mataste 10 mobs mazónicos",
    "minero": "Excavaste 100 bloques de la bóveda",
    "encantador": "Encantaste un mazo",
    "trader": "Hiciste 5 trades con aldeanos",
    "explorador": "Exploraste una mazmorra",
    "jefe_final": "Derrotaste al jefe del mazo (la lanza)",
    "sin_dinero": "Ya no gastaste dinero en el mazo",
}

# =========================
# COLORES
# =========================
COLORES = {
    "&r": "\033[31m", "&v": "\033[32m", "&a": "\033[33m",
    "&z": "\033[34m", "&m": "\033[35m", "&c": "\033[36m",
    "&b": "\033[37m", "&n": "\033[1m",  "&0": "\033[0m",
}

def color(txt):
    for k, v in COLORES.items():
        txt = txt.replace(k, v)
    return txt

# =========================
# HELPERS
# =========================
def extraer(linea, cmd):
    try:
        data = linea.split(cmd, 1)[1].strip()
        if data.startswith("<") and data.endswith(">"):
            return data[1:-1]
    except:
        pass
    return None

def resolver_variables(texto):
    if not isinstance(texto, str):
        return texto
    for nombre, lst in listas.items():
        texto = texto.replace(f"${nombre}", str(lst))
    for nombre, d in diccionarios.items():
        texto = texto.replace(f"${nombre}", str(d))
    for k, v in variables.items():
        texto = texto.replace(f"${k}", str(v))
    return texto

def _es_num(x):
    try: float(x); return True
    except: return False

def _menor(a, b):
    try: return float(a) < float(b)
    except: return str(a) < str(b)

def _mayor(a, b):
    try: return float(a) > float(b)
    except: return str(a) > str(b)

def _igual(a, b):
    try: return float(a) == float(b)
    except: return str(a) == str(b)

def _merge(a, b):
    resultado = []
    i = j = 0
    while i < len(a) and j < len(b):
        if _menor(a[i], b[j]):
            resultado.append(a[i]); i += 1
        else:
            resultado.append(b[j]); j += 1
    resultado.extend(a[i:]); resultado.extend(b[j:])
    return resultado

def _nums(texto):
    return [float(x) for x in resolver_variables(texto).split(",")]

def cond(c):
    try:
        c = resolver_variables(c).strip()
        if " yesmazo " in c or c.startswith("yesmazo "):
            partes = c.replace("yesmazo", "").strip()
            return all(cond(p) for p in partes.split(" yesmazo "))
        if " omazo " in c:
            partes = c.split(" omazo ")
            return any(cond(p) for p in partes)
        if c.startswith("nomazo2 "):
            return not cond(c[8:].strip())
        if c.startswith("estamazo "):
            return c[9:].strip() in variables or c[9:].strip() in listas
        if c.startswith("vaciomazo "):
            v = c[10:].strip()
            return v == "" or v == "[]" or v == "{}"
        if c.startswith("contienemazo "):
            try:
                resto = c[13:].strip()
                lst, val = resto.split("->", 1)
                lst = lst.strip(); val = val.strip()
                if lst in listas:
                    return val in listas[lst]
                return val in lst
            except: return False
        if c.startswith("esnumeromazo "):
            try:
                float(c[13:].strip()); return True
            except: return False
        c2 = c.replace(" ", "")
        op = None
        for oper in ["==", "!=", ">=", "<=", ">", "<"]:
            if oper in c2:
                op = oper; break
        if not op:
            return False
        a, b = c2.split(op, 1)
        try:
            na, nb = float(a), float(b)
            return {"==": na==nb, "!=": na!=nb, ">": na>nb,
                    "<": na<nb, ">=": na>=nb, "<=": na<=nb}[op]
        except ValueError:
            return {"==": a==b, "!=": a!=b}.get(op, False)
    except Exception:
        return False

# =========================
# EJECUTAR
# =========================
def ejecutar(linea):
    linea = linea.strip()
    if not linea or linea.startswith("#") or linea.startswith("//"):
        return
    historial.append(linea)

    # =========================
    # IMPRIMIR
    # =========================
    if linea.startswith("yanog:"):
        t = extraer(linea, "yanog:")
        if t is not None:
            print(color(resolver_variables(t)) + "\033[0m")

    elif linea.startswith("yanogsmazo:"):
        t = extraer(linea, "yanogsmazo:")
        if t is not None:
            print(color(resolver_variables(t)) + "\033[0m", end="")

    elif linea.startswith("yanogmazo:"):
        t = extraer(linea, "yanogmazo:")
        if t is not None:
            print("\033[1;36m╔══════════════════════════════╗\033[0m")
            print("\033[1;36m║\033[0m", color(resolver_variables(t)))
            print("\033[1;36m╚══════════════════════════════╝\033[0m")

    # =========================
    # VARIABLES
    # =========================
    elif linea.startswith("mazo:"):
        t = extraer(linea, "mazo:")
        if t:
            try:
                n, v = t.split("=", 1)
                n = n.strip()
                if v.strip().startswith("[") and v.strip().endswith("]"):
                    contenido = v.strip()[1:-1]
                    listas[n] = [resolver_variables(x.strip())
                                 for x in contenido.split(",") if x.strip()]
                elif v.strip().startswith("{") and v.strip().endswith("}"):
                    contenido = v.strip()[1:-1]
                    diccionarios[n] = {}
                    for par in contenido.split(","):
                        if ":" in par:
                            k, val = par.split(":", 1)
                            diccionarios[n][k.strip()] = resolver_variables(val.strip())
                else:
                    variables[n] = resolver_variables(v.strip())
                print(f"✔ mazo guardado: {n}")
            except:
                print("ERROR")

    elif linea.startswith("nomazo:"):
        t = extraer(linea, "nomazo:")
        if t:
            t = t.strip()
            eliminado = False
            for d in [variables, listas, diccionarios, sets_mazo, stacks_mazo, queues_mazo]:
                if t in d:
                    del d[t]; eliminado = True
            if eliminado:
                print(f"🗑 mazo '{t}' eliminado")
            else:
                print(f"el mazo '{t}' no existe")

    elif linea.startswith("cambiamazo:"):
        t = extraer(linea, "cambiamazo:")
        try:
            n, tipo = t.split("->", 1)
            n = n.strip(); tipo = tipo.strip()
            if n in variables:
                v = variables[n]
                if tipo == "numero": variables[n] = float(v)
                elif tipo == "texto": variables[n] = str(v)
                elif tipo == "booleano": variables[n] = str(v).lower() in ("yesmazo", "true", "1")
                print(f"🔄 '{n}' convertido a {tipo}")
        except: print("ERROR cambiamazo")

    elif linea.startswith("dinerazo:"):
        t = extraer(linea, "dinerazo:")
        if t:
            res = input("\033[1;33m[Mazo Input]: \033[0m")
            variables[t.strip()] = res

    elif linea.startswith("dinerazonumazo:"):
        t = extraer(linea, "dinerazonumazo:")
        if t:
            try:
                res = input("\033[1;33m[Mazo Número]: \033[0m")
                variables[t.strip()] = float(res)
            except:
                print("ERROR no es número")

    # =========================
    # MATEMÁTICAS
    # =========================
    elif linea.startswith("dinero:"):
        t = extraer(linea, "dinero:")
        try:
            a, b = resolver_variables(t).split("+")
            print("Suma mazo:", float(a)+float(b))
        except: print("ERROR")

    elif linea.startswith("menosmazo:"):
        t = extraer(linea, "menosmazo:")
        try:
            a, b = resolver_variables(t).split("-")
            print("Resta mazo:", float(a)-float(b))
        except: print("ERROR")

    elif linea.startswith("masmazo:"):
        t = extraer(linea, "masmazo:")
        try:
            a, b = resolver_variables(t).split("*")
            print("Multi mazo:", float(a)*float(b))
        except: print("ERROR")

    elif linea.startswith("delmazo:"):
        t = extraer(linea, "delmazo:")
        try:
            a, b = resolver_variables(t).split("/")
            print("Div mazo:", float(a)/float(b))
        except: print("ERROR")

    elif linea.startswith("raizmazo:"):
        t = extraer(linea, "raizmazo:")
        try:
            print("Raíz mazo:", math.sqrt(float(resolver_variables(t))))
        except: print("ERROR")

    elif linea.startswith("modmazo:"):
        t = extraer(linea, "modmazo:")
        try:
            a, b = resolver_variables(t).split("%")
            print("Módulo mazo:", float(a)%float(b))
        except: print("ERROR")

    elif linea.startswith("potenciamazo:"):
        t = extraer(linea, "potenciamazo:")
        try:
            a, b = resolver_variables(t).split("^")
            print("Potencia mazo:", float(a)**float(b))
        except: print("ERROR")

    elif linea.startswith("mazopromedio:"):
        t = extraer(linea, "mazopromedio:")
        try: print("📊 Promedio mazo:", statistics.mean(_nums(t)))
        except: print("ERROR promedio")

    elif linea.startswith("mazomediana:"):
        t = extraer(linea, "mazomediana:")
        try: print("📊 Mediana mazo:", statistics.median(_nums(t)))
        except: print("ERROR mediana")

    elif linea.startswith("mazomoda:"):
        t = extraer(linea, "mazomoda:")
        try: print("📊 Moda mazo:", statistics.mode(_nums(t)))
        except: print("ERROR moda")

    elif linea.startswith("mazodesviacion:"):
        t = extraer(linea, "mazodesviacion:")
        try: print("📊 Desviación mazo:", statistics.stdev(_nums(t)))
        except: print("ERROR desviación")

    elif linea.startswith("mazogcd:"):
        t = extraer(linea, "mazogcd:")
        try:
            a, b = resolver_variables(t).split(",")
            print("🔢 GCD mazo:", math.gcd(int(a), int(b)))
        except: print("ERROR gcd")

    elif linea.startswith("mazolcm:"):
        t = extraer(linea, "mazolcm:")
        try:
            a, b = resolver_variables(t).split(",")
            print("🔢 LCM mazo:", math.lcm(int(a), int(b)))
        except: print("ERROR lcm")

    elif linea.startswith("mazofactorial:"):
        t = extraer(linea, "mazofactorial:")
        try: print("🔢 Factorial mazo:", math.factorial(int(resolver_variables(t))))
        except: print("ERROR factorial")

    elif linea.startswith("mazoseno:"):
        t = extraer(linea, "mazoseno:")
        try: print("sin:", math.sin(float(resolver_variables(t))))
        except: print("ERROR")

    elif linea.startswith("mazocoseno:"):
        t = extraer(linea, "mazocoseno:")
        try: print("cos:", math.cos(float(resolver_variables(t))))
        except: print("ERROR")

    elif linea.startswith("mazotangente:"):
        t = extraer(linea, "mazotangente:")
        try: print("tan:", math.tan(float(resolver_variables(t))))
        except: print("ERROR")

    elif linea.startswith("mazolog:"):
        t = extraer(linea, "mazolog:")
        try: print("log:", math.log(float(resolver_variables(t))))
        except: print("ERROR")

    elif linea.startswith("mazopi:"):
        print("π mazo:", math.pi)

    elif linea.startswith("mazoe:"):
        print("e mazo:", math.e)

    elif linea.startswith("mazoredondea:"):
        t = extraer(linea, "mazoredondea:")
        try:
            n, dec = resolver_variables(t).split(",")
            print("🔢 Redondeo mazo:", round(float(n), int(dec)))
        except: print("ERROR redondea")

    elif linea.startswith("mazoabs:"):
        t = extraer(linea, "mazoabs:")
        try: print("|x| mazo:", abs(float(resolver_variables(t))))
        except: print("ERROR abs")

    # =========================
    # AZAR
    # =========================
    elif linea.startswith("nogastes:"):
        t = extraer(linea, "nogastes:")
        try:
            a, b = resolver_variables(t).split("-")
            print("Mazo azar:", random.randint(int(a), int(b)))
        except: print("ERROR")

    elif linea.startswith("tirael:"):
        t = extraer(linea, "tirael:")
        caras = int(resolver_variables(t)) if t else 6
        print("🎲 Mazo dado:", random.randint(1, caras))

    elif linea.startswith("mezclamazo:"):
        t = extraer(linea, "mezclamazo:")
        t = t.strip()
        if t in listas:
            random.shuffle(listas[t])
            print("🔀 Mezclado:", listas[t])
        else: print("no existe esa lista")

    elif linea.startswith("mazoelegir:"):
        t = extraer(linea, "mazoelegir:")
        t = t.strip()
        if t in listas:
            print("🎯 Elegido mazo:", random.choice(listas[t]))
        else: print("no existe")

    elif linea.startswith("mazomuestra:"):
        t = extraer(linea, "mazomuestra:")
        try:
            n, k = t.split(",")
            n = n.strip()
            if n in listas:
                print("🎯 Muestra mazo:", random.sample(listas[n], int(k)))
        except: print("ERROR muestra")

    # =========================
    # TIEMPO / FECHAS
    # =========================
    elif linea.startswith("yadinero:"):
        t = extraer(linea, "yadinero:")
        try: time.sleep(float(resolver_variables(t)))
        except: print("error yadinero")

    elif linea.startswith("mazoespera:"):
        t = extraer(linea, "mazoespera:")
        try: time.sleep(float(resolver_variables(t))/1000.0)
        except: print("ERROR")

    elif linea.startswith("mazohoy:"):
        print("📅 Mazo hoy:", datetime.datetime.now().strftime("%Y-%m-%d"))

    elif linea.startswith("mazohora:"):
        print("🕐 Mazo hora:", datetime.datetime.now().strftime("%H:%M:%S"))

    elif linea.startswith("mazofecha:"):
        print("📅 Mazo fecha completa:", datetime.datetime.now())

    elif linea.startswith("mazotiempo:"):
        print("⏱️ Timestamp mazo:", time.time())

    elif linea.startswith("mazocronometro:"):
        variables["_crono"] = time.time()
        print("⏱️ Cronómetro iniciado")

    elif linea.startswith("mazoparacrono:"):
        if "_crono" in variables:
            print("⏱️ Tiempo mazo:", time.time() - variables["_crono"], "seg")

    # =========================
    # MULTICOMANDO / MACROS
    # =========================
    elif linea.startswith("azomazo:"):
        t = extraer(linea, "azomazo:")
        if t:
            for x in t.split("|"):
                ejecutar(x.strip())

    elif linea.startswith("aliasmazo:"):
        t = extraer(linea, "aliasmazo:")
        try:
            nombre, cmd = t.split("=", 1)
            aliases[nombre.strip()] = cmd.strip()
            print(f"🔗 alias '{nombre.strip()}' creado")
        except: print("ERROR")

    # =========================
    # LISTAS
    # =========================
    elif linea.startswith("mazolista:"):
        t = extraer(linea, "mazolista:")
        try:
            n, vals = t.split("=", 1)
            n = n.strip()
            listas[n] = [resolver_variables(v.strip()) for v in vals.split(",")]
            print(f"📋 lista '{n}' creada con {len(listas[n])} items")
        except: print("ERROR")

    elif linea.startswith("agregamazo:"):
        t = extraer(linea, "agregamazo:")
        try:
            n, v = t.split("=", 1)
            listas[n.strip()].append(resolver_variables(v.strip()))
            print(f"➕ item agregado a '{n.strip()}'")
        except: print("ERROR")

    elif linea.startswith("quitamazo:"):
        t = extraer(linea, "quitamazo:")
        try:
            n, v = t.split("=", 1)
            listas[n.strip()].remove(resolver_variables(v.strip()))
            print(f"➖ item quitado de '{n.strip()}'")
        except: print("ERROR")

    elif linea.startswith("cuentamazo:"):
        t = extraer(linea, "cuentamazo:")
        t = t.strip()
        if t in listas:
            print(f"🔢 '{t}' tiene {len(listas[t])} items")
        elif t in diccionarios:
            print(f"🔢 '{t}' tiene {len(diccionarios[t])} claves")
        elif t in sets_mazo:
            print(f"🔢 '{t}' tiene {len(sets_mazo[t])} elementos")
        else:
            print(f"🔢 longitud:", len(resolver_variables(t)))

    elif linea.startswith("tomael:"):
        t = extraer(linea, "tomael:")
        try:
            n, i = t.split(",")
            n = n.strip()
            i = int(resolver_variables(i.strip()))
            print(listas[n][i])
        except: print("ERROR tomael")

    elif linea.startswith("mostrarmazo:"):
        t = extraer(linea, "mostrarmazo:")
        t = t.strip()
        if t in listas:
            for i, v in enumerate(listas[t]):
                print(f"  [{i}] {v}")
        else: print("no existe")

    elif linea.startswith("mazordena:"):
        t = extraer(linea, "mazordena:")
        t = t.strip()
        if t in listas:
            try: listas[t] = sorted(listas[t], key=lambda x: float(x))
            except: listas[t] = sorted(listas[t])
            print("🔤 Ordenado mazo:", listas[t])

    elif linea.startswith("mazordenaa:"):
        t = extraer(linea, "mazordenaa:")
        t = t.strip()
        if t in listas:
            try: listas[t] = sorted(listas[t], key=lambda x: float(x), reverse=True)
            except: listas[t] = sorted(listas[t], reverse=True)
            print("🔤 Ordenado desc mazo:", listas[t])

    elif linea.startswith("mazoinvierte:"):
        t = extraer(linea, "mazoinvierte:")
        t = t.strip()
        if t in listas:
            listas[t].reverse()
            print("🔄 Invertido mazo:", listas[t])

    elif linea.startswith("mazobusca:"):
        t = extraer(linea, "mazobusca:")
        try:
            n, v = t.split(",")
            n = n.strip(); v = v.strip()
            if n in listas:
                if v in listas[n]:
                    print(f"🔍 Encontrado en índice {listas[n].index(v)}")
                else:
                    print("🔍 No encontrado mazo")
        except: print("ERROR busca")

    elif linea.startswith("mazocuenta:"):
        t = extraer(linea, "mazocuenta:")
        try:
            n, v = t.split(",")
            n = n.strip(); v = v.strip()
            if n in listas:
                print(f"🔢 Aparece {listas[n].count(v)} veces")
        except: print("ERROR cuenta")

    elif linea.startswith("mazosuma:"):
        t = extraer(linea, "mazosuma:")
        t = t.strip()
        if t in listas:
            try: print("∑ mazo:", sum(float(x) for x in listas[t]))
            except: print("ERROR suma")

    elif linea.startswith("mazomin:"):
        t = extraer(linea, "mazomin:")
        t = t.strip()
        if t in listas:
            try: print("🔻 Mínimo mazo:", min(float(x) for x in listas[t]))
            except: print("ERROR min")

    elif linea.startswith("mazomax:"):
        t = extraer(linea, "mazomax:")
        t = t.strip()
        if t in listas:
            try: print("🔺 Máximo mazo:", max(float(x) for x in listas[t]))
            except: print("ERROR max")

    elif linea.startswith("mazofiltra:"):
        t = extraer(linea, "mazofiltra:")
        try:
            n, c = t.split("->", 1)
            n = n.strip(); c = c.strip()
            if n in listas:
                resultado = []
                for item in listas[n]:
                    variables["_item"] = item
                    if cond(c):
                        resultado.append(item)
                listas[n+"_filtrada"] = resultado
                print(f"🔍 Filtrado mazo: {resultado}")
        except: print("ERROR filtra")

    elif linea.startswith("mazomapea:"):
        t = extraer(linea, "mazomapea:")
        try:
            n, cmd = t.split("->", 1)
            n = n.strip(); cmd = cmd.strip()
            if n in listas:
                resultado = []
                for item in listas[n]:
                    variables["_item"] = item
                    try:
                        resultado.append(eval(resolver_variables(cmd.replace("_item", str(item)))))
                    except:
                        resultado.append(item)
                listas[n+"_mapeada"] = resultado
                print(f"🗺️ Mapeado mazo: {resultado}")
        except: print("ERROR mapea")

    elif linea.startswith("mazorango:"):
        t = extraer(linea, "mazorango:")
        try:
            n, r = t.split("=", 1)
            ini, fin = r.split("-")
            listas[n.strip()] = list(range(int(ini), int(fin)+1))
            print(f"📋 Rango mazo creado: {listas[n.strip()]}")
        except: print("ERROR rango")

    elif linea.startswith("mazocombina:"):
        t = extraer(linea, "mazocombina:")
        try:
            a, b = t.split(",")
            a = a.strip(); b = b.strip()
            if a in listas and b in listas:
                listas[a+"_combinada"] = listas[a] + listas[b]
                print("🔗 Combinada mazo:", listas[a+"_combinada"])
        except: print("ERROR combina")

    # =========================
    # DICCIONARIOS
    # =========================
    elif linea.startswith("mazodicc:"):
        t = extraer(linea, "mazodicc:")
        try:
            n, contenido = t.split("=", 1)
            n = n.strip()
            diccionarios[n] = {}
            contenido = contenido.strip()
            if contenido.startswith("{") and contenido.endswith("}"):
                contenido = contenido[1:-1]
            for par in contenido.split(","):
                if ":" in par:
                    k, v = par.split(":", 1)
                    diccionarios[n][k.strip()] = resolver_variables(v.strip())
            print(f"📖 Diccionario '{n}' creado con {len(diccionarios[n])} claves")
        except: print("ERROR dicc")

    elif linea.startswith("mazodiccpon:"):
        t = extraer(linea, "mazodiccpon:")
        try:
            n, kv = t.split(",", 1)
            n = n.strip()
            k, v = kv.split("=", 1)
            diccionarios[n][k.strip()] = resolver_variables(v.strip())
            print(f"➕ Añadido '{k.strip()}' a '{n}'")
        except: print("ERROR diccpon")

    elif linea.startswith("mazodicctoma:"):
        t = extraer(linea, "mazodicctoma:")
        try:
            n, k = t.split(",")
            n = n.strip(); k = k.strip()
            print(f"📖 {n}[{k}] =", diccionarios[n][k])
        except: print("ERROR dicctoma")

    elif linea.startswith("mazodiccquita:"):
        t = extraer(linea, "mazodiccquita:")
        try:
            n, k = t.split(",")
            n = n.strip(); k = k.strip()
            del diccionarios[n][k]
            print(f"➖ Quitado '{k}' de '{n}'")
        except: print("ERROR diccquita")

    elif linea.startswith("mazodiccclaves:"):
        t = extraer(linea, "mazodiccclaves:")
        t = t.strip()
        if t in diccionarios:
            print("🔑 Claves mazo:", list(diccionarios[t].keys()))

    elif linea.startswith("mazodiccvalores:"):
        t = extraer(linea, "mazodiccvalores:")
        t = t.strip()
        if t in diccionarios:
            print("💎 Valores mazo:", list(diccionarios[t].values()))

    # =========================
    # SETS
    # =========================
    elif linea.startswith("mazoset:"):
        t = extraer(linea, "mazoset:")
        try:
            n, vals = t.split("=", 1)
            sets_mazo[n.strip()] = set(v.strip() for v in vals.split(","))
            print(f"🎯 Set '{n.strip()}' creado: {sets_mazo[n.strip()]}")
        except: print("ERROR set")

    elif linea.startswith("mazosetpon:"):
        t = extraer(linea, "mazosetpon:")
        try:
            n, v = t.split("=", 1)
            sets_mazo[n.strip()].add(v.strip())
            print(f"➕ Añadido a set '{n.strip()}'")
        except: print("ERROR setpon")

    elif linea.startswith("mazosetune:"):
        t = extraer(linea, "mazosetune:")
        try:
            a, b = t.split(",")
            a = a.strip(); b = b.strip()
            print("🔗 Unión mazo:", sets_mazo[a] | sets_mazo[b])
        except: print("ERROR setune")

    elif linea.startswith("mazosetinterseca:"):
        t = extraer(linea, "mazosetinterseca:")
        try:
            a, b = t.split(",")
            a = a.strip(); b = b.strip()
            print("🎯 Intersección mazo:", sets_mazo[a] & sets_mazo[b])
        except: print("ERROR setinterseca")

    # =========================
    # STACKS / QUEUES
    # =========================
    elif linea.startswith("mazostack:"):
        t = extraer(linea, "mazostack:")
        try:
            n, vals = t.split("=", 1)
            stacks_mazo[n.strip()] = [v.strip() for v in vals.split(",")]
            print(f"📚 Stack '{n.strip()}' creado")
        except:
            stacks_mazo[t.strip()] = []
            print(f"📚 Stack '{t.strip()}' creado vacío")

    elif linea.startswith("mazopush:"):
        t = extraer(linea, "mazopush:")
        try:
            n, v = t.split("=", 1)
            stacks_mazo[n.strip()].append(v.strip())
            print(f"⬆️ Push a '{n.strip()}'")
        except: print("ERROR push")

    elif linea.startswith("mazopop:"):
        t = extraer(linea, "mazopop:")
        t = t.strip()
        if t in stacks_mazo and stacks_mazo[t]:
            print("⬇️ Pop mazo:", stacks_mazo[t].pop())
        else:
            print("stack vacío o no existe")

    elif linea.startswith("mazocola:"):
        t = extraer(linea, "mazocola:")
        t = t.strip()
        queues_mazo[t] = []
        print(f"🚶 Cola '{t}' creada")

    elif linea.startswith("mazoencola:"):
        t = extraer(linea, "mazoencola:")
        try:
            n, v = t.split("=", 1)
            queues_mazo[n.strip()].append(v.strip())
            print(f"➡️ Encolado en '{n.strip()}'")
        except: print("ERROR encola")

    elif linea.startswith("mazodesencola:"):
        t = extraer(linea, "mazodesencola:")
        t = t.strip()
        if t in queues_mazo and queues_mazo[t]:
            print("⬅️ Desencolado mazo:", queues_mazo[t].pop(0))
        else:
            print("cola vacía o no existe")

    # =========================
    # STRINGS
    # =========================
    elif linea.startswith("mayusmazo:"):
        t = extraer(linea, "mayusmazo:")
        print(resolver_variables(t).upper())

    elif linea.startswith("minusmazo:"):
        t = extraer(linea, "minusmazo:")
        print(resolver_variables(t).lower())

    elif linea.startswith("largomazo:"):
        t = extraer(linea, "largomazo:")
        print("Longitud mazo:", len(resolver_variables(t)))

    elif linea.startswith("juntamazo:"):
        t = extraer(linea, "juntamazo:")
        try:
            a, b = t.split("+")
            print(resolver_variables(a.strip()) + resolver_variables(b.strip()))
        except: print("ERROR")

    elif linea.startswith("reemplazamazo:"):
        t = extraer(linea, "reemplazamazo:")
        try:
            orig, resto = t.split(",", 1)
            viejo, nuevo = resto.split("->", 1)
            print(resolver_variables(orig).replace(viejo.strip(), nuevo.strip()))
        except: print("ERROR")

    elif linea.startswith("mazocorta:"):
        t = extraer(linea, "mazocorta:")
        try:
            txt, r = t.split(",", 1)
            ini, fin = r.split("-")
            print("✂️ Cortado mazo:", resolver_variables(txt)[int(ini):int(fin)])
        except: print("ERROR corta")

    elif linea.startswith("mazosplit:"):
        t = extraer(linea, "mazosplit:")
        try:
            txt, sep = t.split(",", 1)
            print("🔪 Split mazo:", resolver_variables(txt).split(sep.strip()))
        except: print("ERROR split")

    elif linea.startswith("mazotrim:"):
        t = extraer(linea, "mazotrim:")
        print("🧹 Trim mazo:", resolver_variables(t).strip())

    elif linea.startswith("mazocontiene:"):
        t = extraer(linea, "mazocontiene:")
        try:
            txt, sub = t.split(",", 1)
            print("🔍 Contiene mazo:", sub.strip() in resolver_variables(txt))
        except: print("ERROR contiene")

    elif linea.startswith("mazorepite:"):
        t = extraer(linea, "mazorepite:")
        try:
            txt, n = t.split(",")
            print("🔁 Repetido mazo:", resolver_variables(txt) * int(n))
        except: print("ERROR repite")

    elif linea.startswith("mazoreversa:"):
        t = extraer(linea, "mazoreversa:")
        print("🔄 Reversa mazo:", resolver_variables(t)[::-1])

    elif linea.startswith("mazoprimermazo:"):
        t = extraer(linea, "mazoprimermazo:")
        print("1️⃣ Primero mazo:", resolver_variables(t)[0])

    elif linea.startswith("mazoultimo:"):
        t = extraer(linea, "mazoultimo:")
        print("🔚 Último mazo:", resolver_variables(t)[-1])

    elif linea.startswith("mazocapitaliza:"):
        t = extraer(linea, "mazocapitaliza:")
        print("🅰️ Capitalizado mazo:", resolver_variables(t).capitalize())

    elif linea.startswith("mazotitulo:"):
        t = extraer(linea, "mazotitulo:")
        print("📰 Título mazo:", resolver_variables(t).title())

    # =========================
    # REGEX
    # =========================
    elif linea.startswith("mazoregex:"):
        t = extraer(linea, "mazoregex:")
        try:
            patron, txt = t.split(",", 1)
            matches = re.findall(patron.strip(), resolver_variables(txt.strip()))
            print("🔍 Regex mazo:", matches)
        except Exception as e: print("ERROR regex:", e)

    elif linea.startswith("mazoregexreemplaza:"):
        t = extraer(linea, "mazoregexreemplaza:")
        try:
            patron, resto = t.split(",", 1)
            txt, nuevo = resto.split("->", 1)
            print("🔄 Regex reemplazo:", re.sub(patron.strip(), nuevo.strip(), resolver_variables(txt.strip())))
        except Exception as e: print("ERROR regex:", e)

    # =========================
    # JSON
    # =========================
    elif linea.startswith("mazojson:"):
        t = extraer(linea, "mazojson:")
        t = t.strip()
        try:
            if t in diccionarios:
                print("📦 JSON mazo:", json.dumps(diccionarios[t], ensure_ascii=False))
            elif t in listas:
                print("📦 JSON mazo:", json.dumps(listas[t], ensure_ascii=False))
            else:
                print("📦 JSON mazo:", json.dumps(resolver_variables(t), ensure_ascii=False))
        except Exception as e: print("ERROR json:", e)

    elif linea.startswith("mazojsonleer:"):
        t = extraer(linea, "mazojsonleer:")
        try:
            n, txt = t.split("=", 1)
            diccionarios[n.strip()] = json.loads(resolver_variables(txt.strip()))
            print(f"📦 JSON leído en '{n.strip()}'")
        except Exception as e: print("ERROR jsonleer:", e)

    # =========================
    # ENCRIPTACIÓN
    # =========================
    elif linea.startswith("mazohash:"):
        t = extraer(linea, "mazohash:")
        print("🔐 Hash mazo:", hashlib.sha256(resolver_variables(t).encode()).hexdigest())

    elif linea.startswith("mazohashmd5:"):
        t = extraer(linea, "mazohashmd5:")
        print("🔐 MD5 mazo:", hashlib.md5(resolver_variables(t).encode()).hexdigest())

    elif linea.startswith("mazobase64:"):
        t = extraer(linea, "mazobase64:")
        print("🔐 Base64 mazo:", base64.b64encode(resolver_variables(t).encode()).decode())

    elif linea.startswith("mazodesbase64:"):
        t = extraer(linea, "mazodesbase64:")
        try:
            print("🔓 Base64 decodificado:", base64.b64decode(resolver_variables(t).encode()).decode())
        except: print("ERROR base64")

    # =========================
    # CONDICIONALES
    # =========================
    elif linea.startswith("si:"):
        t = extraer(linea, "si:")
        try:
            c, act = t.split("->", 1)
            if cond(c):
                ejecutar(act)
        except: print("ERROR si")

    elif linea.startswith("sino:"):
        t = extraer(linea, "sino:")
        if t: ejecutar(t)

    elif linea.startswith("siza:"):
        t = extraer(linea, "siza:")
        try:
            cond_str, resto = t.split("->", 1)
            si_cmd, sino_cmd = resto.split("|sino|", 1)
            if cond(cond_str):
                ejecutar(si_cmd.strip())
            else:
                ejecutar(sino_cmd.strip())
        except: print("ERROR siza")

    elif linea.startswith("mazoswitch:"):
        t = extraer(linea, "mazoswitch:")
        try:
            valor, casos = t.split("->", 1)
            valor = resolver_variables(valor.strip())
            for caso in casos.split("|"):
                if ":" in caso:
                    k, cmd = caso.split(":", 1)
                    if k.strip() == "defecto" or k.strip() == valor:
                        ejecutar(cmd.strip())
                        break
        except: print("ERROR switch")

    # =========================
    # BUCLES
    # =========================
    elif linea.startswith("repmazo:"):
        t = extraer(linea, "repmazo:")
        try:
            n, cmd = t.split("->", 1)
            n = int(resolver_variables(n.strip()))
            for i in range(n):
                variables["_i"] = i
                ejecutar(cmd.strip())
        except Exception as e:
            print("ERROR rep:", e)

    elif linea.startswith("mientrasmazo:"):
        t = extraer(linea, "mientrasmazo:")
        try:
            c, cmd = t.split("->", 1)
            vueltas = 0
            while cond(c) and vueltas < 100000:
                ejecutar(cmd.strip())
                vueltas += 1
        except Exception as e:
            print("ERROR mientras:", e)

    elif linea.startswith("paradineros:"):
        t = extraer(linea, "paradineros:")
        try:
            ini, fin, cmd = t.split("->", 2)
            for i in range(int(ini), int(fin)+1):
                variables["_i"] = i
                ejecutar(cmd.strip())
        except Exception as e:
            print("ERROR para:", e)

    elif linea.startswith("mazoporelmazo:"):
        t = extraer(linea, "mazoporelmazo:")
        try:
            n, cmd = t.split("->", 1)
            n = n.strip()
            if n in listas:
                for item in listas[n]:
                    variables["_item"] = item
                    ejecutar(cmd.strip())
        except Exception as e:
            print("ERROR porel:", e)

    elif linea.startswith("mazorompe:"):
        raise StopIteration("mazorompe")

    elif linea.startswith("mazocontinua:"):
        return

    # =========================
    # FUNCIONES
    # =========================
    elif linea.startswith("mazofuncion:"):
        t = extraer(linea, "mazofuncion:")
        try:
            nombre, cuerpo = t.split("=", 1)
            funciones[nombre.strip()] = cuerpo.strip()
            print(f"⚙️ función '{nombre.strip()}' definida")
        except: print("ERROR")

    elif linea.startswith("llamamazo:"):
        t = extraer(linea, "llamamazo:")
        t = t.strip()
        if t in funciones:
            try:
                ejecutar(funciones[t])
            except StopIteration:
                pass
        else:
            print("función no existe")

    elif linea.startswith("regresamazo:"):
        t = extraer(linea, "regresamazo:")
        if t:
            print("↩", resolver_variables(t.strip()))

    # =========================
    # TRY / CATCH
    # =========================
    elif linea.startswith("mazoexcepcion:"):
        t = extraer(linea, "mazoexcepcion:")
        try:
            ejecutar(t)
        except Exception as e:
            variables["_error"] = str(e)
            print(f"⚠️ Excepción mazo capturada: {e}")

    elif linea.startswith("mazocaptura:"):
        t = extraer(linea, "mazocaptura:")
        if "_error" in variables:
            ejecutar(t)
            del variables["_error"]

    elif linea.startswith("mazogarantiza:"):
        t = extraer(linea, "mazogarantiza:")
        ejecutar(t)

    # =========================
    # MÓDULOS
    # =========================
    elif linea.startswith("mazomodulo:"):
        t = extraer(linea, "mazomodulo:")
        try:
            n, contenido = t.split("=", 1)
            modulos_mazo[n.strip()] = contenido.strip()
            print(f"📦 Módulo '{n.strip()}' definido")
        except: print("ERROR modulo")

    elif linea.startswith("mazomodulollama:"):
        t = extraer(linea, "mazomodulollama:")
        t = t.strip()
        if t in modulos_mazo:
            ejecutar(modulos_mazo[t])
        else:
            print("módulo no existe")

    # =========================
    # ESTADOS
    # =========================
    elif linea.startswith("mazoestado:"):
        t = extraer(linea, "mazoestado:")
        try:
            n, v = t.split("=", 1)
            estados_mazo[n.strip()] = resolver_variables(v.strip())
            print(f"🚦 Estado '{n.strip()}' = {estados_mazo[n.strip()]}")
        except: print("ERROR estado")

    elif linea.startswith("mazoestadocambia:"):
        t = extraer(linea, "mazoestadocambia:")
        try:
            n, v = t.split("=", 1)
            if n.strip() in estados_mazo:
                estados_mazo[n.strip()] = resolver_variables(v.strip())
                print(f"🔄 Estado '{n.strip()}' → {estados_mazo[n.strip()]}")
        except: print("ERROR estadocambia")

    elif linea.startswith("mazoestadotoma:"):
        t = extraer(linea, "mazoestadotoma:")
        t = t.strip()
        if t in estados_mazo:
            print(f"🚦 Estado '{t}' = {estados_mazo[t]}")

    # =========================
    # EVENTOS
    # =========================
    elif linea.startswith("mazoevento:"):
        t = extraer(linea, "mazoevento:")
        try:
            n, cmd = t.split("=", 1)
            eventos_mazo[n.strip()] = cmd.strip()
            print(f"🎪 Evento '{n.strip()}' registrado")
        except: print("ERROR evento")

    elif linea.startswith("mazodispara:"):
        t = extraer(linea, "mazodispara:")
        t = t.strip()
        if t in eventos_mazo:
            ejecutar(eventos_mazo[t])
        else:
            print("evento no existe")

    # =========================
    # CLASES / OBJETOS
    # =========================
    elif linea.startswith("mazoclase:"):
        t = extraer(linea, "mazoclase:")
        try:
            nombre, metodos = t.split("=", 1)
            clases_mazo[nombre.strip()] = metodos.strip()
            print(f"🏗️ Clase '{nombre.strip()}' definida")
        except: print("ERROR clase")

    elif linea.startswith("mazoinstancia:"):
        t = extraer(linea, "mazoinstancia:")
        try:
            nombre, clase = t.split("=", 1)
            instancias_mazo[nombre.strip()] = {"clase": clase.strip(), "atributos": {}}
            print(f"🏗️ Instancia '{nombre.strip()}' creada de '{clase.strip()}'")
        except: print("ERROR instancia")

    elif linea.startswith("mazoatributo:"):
        t = extraer(linea, "mazoatributo:")
        try:
            inst, kv = t.split(",", 1)
            k, v = kv.split("=", 1)
            instancias_mazo[inst.strip()]["atributos"][k.strip()] = resolver_variables(v.strip())
            print(f"🏗️ Atributo '{k.strip()}' puesto en '{inst.strip()}'")
        except: print("ERROR atributo")

    elif linea.startswith("mazometodo:"):
        t = extraer(linea, "mazometodo:")
        try:
            inst, metodo = t.split(",", 1)
            inst = inst.strip()
            if inst in instancias_mazo:
                clase = instancias_mazo[inst]["clase"]
                if clase in clases_mazo:
                    for m in clases_mazo[clase].split("|"):
                        if ":" in m:
                            k, cmd = m.split(":", 1)
                            if k.strip() == metodo.strip():
                                for ak, av in instancias_mazo[inst]["atributos"].items():
                                    variables["_" + ak] = av
                                ejecutar(cmd.strip())
                                for ak in instancias_mazo[inst]["atributos"]:
                                    if "_" + ak in variables:
                                        instancias_mazo[inst]["atributos"][ak] = variables["_" + ak]
                                break
        except Exception as e: print("ERROR metodo:", e)

    # =========================
    # ASSERT / DEBUG
    # =========================
    elif linea.startswith("mazoverifica:"):
        t = extraer(linea, "mazoverifica:")
        try:
            c, msg = t.split("->", 1)
            if not cond(c):
                print(f"❌ Verificación fallida mazo: {msg}")
            else:
                print("✅ Verificación mazo OK")
        except: print("ERROR verifica")

    elif linea.startswith("mazodepura:"):
        t = extraer(linea, "mazodepura:")
        t = t.strip()
        if t in variables:
            print(f"🐛 {t} = {variables[t]} ({type(variables[t]).__name__})")
        elif t in listas:
            print(f"🐛 {t} = lista {listas[t]} ({len(listas[t])} items)")
        elif t in diccionarios:
            print(f"🐛 {t} = dict {diccionarios[t]}")
        else:
            print(f"🐛 '{t}' no existe")

    # =========================
    # SISTEMA AVANZADO
    # =========================
    elif linea.startswith("mazoejecuta:"):
        t = extraer(linea, "mazoejecuta:")
        try: os.system(resolver_variables(t))
        except Exception as e: print("ERROR ejecuta:", e)

    elif linea.startswith("mazoentorno:"):
        t = extraer(linea, "mazoentorno:")
        t = t.strip()
        if t in os.environ:
            print(f"🌍 {t} = {os.environ[t]}")
        else:
            print(f"🌍 '{t}' no está en el entorno")

    elif linea.startswith("mazoruta:"):
        print("📂 Ruta mazo actual:", os.getcwd())

    elif linea.startswith("mazodir:"):
        t = extraer(linea, "mazodir:")
        try:
            ruta = resolver_variables(t.strip()) if t else "."
            print("📂 Contenido mazo:", os.listdir(ruta))
        except Exception as e: print("ERROR dir:", e)

    elif linea.startswith("mazoarchivolee:"):
        t = extraer(linea, "mazoarchivolee:")
        try:
            with open(resolver_variables(t.strip()), "r", encoding="utf-8") as f:
                print(f.read())
        except Exception as e: print("ERROR archivo:", e)

    elif linea.startswith("mazoarchivoescribe:"):
        t = extraer(linea, "mazoarchivoescribe:")
        try:
            ruta, contenido = t.split(",", 1)
            with open(resolver_variables(ruta.strip()), "w", encoding="utf-8") as f:
                f.write(resolver_variables(contenido.strip()))
            print("💾 Archivo mazo escrito")
        except Exception as e: print("ERROR archivo:", e)

    elif linea.startswith("mazoarchivoagrega:"):
        t = extraer(linea, "mazoarchivoagrega:")
        try:
            ruta, contenido = t.split(",", 1)
            with open(resolver_variables(ruta.strip()), "a", encoding="utf-8") as f:
                f.write(resolver_variables(contenido.strip()) + "\n")
            print("💾 Añadido a archivo mazo")
        except Exception as e: print("ERROR archivo:", e)

    elif linea.startswith("mazoarchivoborra:"):
        t = extraer(linea, "mazoarchivoborra:")
        try:
            os.remove(resolver_variables(t.strip()))
            print("🗑️ Archivo mazo borrado")
        except Exception as e: print("ERROR borra:", e)

    # =========================
    # TIENDA
    # =========================
    elif linea.startswith("mazoel:"):
        t = extraer(linea, "mazoel:")
        try:
            name, code = t.split("=", 1)
            store[name.strip()] = {"code": code.strip(), "version": "5.5"}
            print("📦 app guardada:", name.strip())
        except: print("ERROR")

    elif linea.startswith("mazogastes:"):
        t = extraer(linea, "mazogastes:")
        t = resolver_variables(t).strip()
        if t in store:
            ejecutar(store[t]["code"])
        else:
            print("APP NO EXISTE")

    elif linea == "dineroel":
        print("📦 APPS EN EL MAZO:")
        if not store: print("  (Sin apps)")
        for k in store: print("-", k)

    # =========================
    # ARCHIVOS MAZO
    # =========================
    elif linea.startswith("guardarmazo:"):
        t = extraer(linea, "guardarmazo:")
        if t:
            try:
                if not t.endswith(".mazoxpkg"): t += ".mazoxpkg"
                with open(t, "w", encoding="utf-8") as f:
                    for app, data in store.items():
                        f.write(f"mazoel:<{app}={data['code']}>\n")
                print(f"💾 Guardado en '{t}'")
            except Exception as e: print("ERROR:", e)

    elif linea.startswith("leermazo:"):
        t = extraer(linea, "leermazo:")
        if t:
            try:
                with open(resolver_variables(t.strip()), "r", encoding="utf-8") as f:
                    for l in f:
                        ejecutar(l)
            except Exception as e: print("ERROR:", e)

    elif linea.startswith("sirvemazo:"):
        t = extraer(linea, "sirvemazo:")
        if t:
            try:
                with open(resolver_variables(t.strip()), "w", encoding="utf-8") as f:
                    f.write("")
                print("📄 archivo escrito (vacío)")
            except Exception as e: print("ERROR:", e)

    # =========================
    # v5.0 — GRAFOS
    # =========================
    elif linea.startswith("mazografo:"):
        t = extraer(linea, "mazografo:")
        try:
            n, vertices = t.split("=", 1)
            n = n.strip()
            grafos_mazo[n] = {v.strip(): [] for v in vertices.split(",")}
            print(f"🌐 Grafo '{n}' creado con {len(grafos_mazo[n])} vértices")
        except: print("ERROR grafo")

    elif linea.startswith("mazografoarista:"):
        t = extraer(linea, "mazografoarista:")
        try:
            n, resto = t.split(",", 1)
            a, b = resto.split("->")
            n = n.strip(); a = a.strip(); b = b.strip()
            grafos_mazo[n][a].append(b)
            grafos_mazo[n][b].append(a)
            print(f"🔗 Arista {a} <-> {b} añadida")
        except: print("ERROR arista")

    elif linea.startswith("mazografobfs:"):
        t = extraer(linea, "mazografobfs:")
        try:
            n, inicio = t.split(",")
            n = n.strip(); inicio = inicio.strip()
            visitados = set(); cola = [inicio]; orden = []
            while cola:
                v = cola.pop(0)
                if v not in visitados:
                    visitados.add(v); orden.append(v)
                    cola.extend(grafos_mazo[n].get(v, []))
            print(f"🔍 BFS mazo: {orden}")
        except: print("ERROR bfs")

    elif linea.startswith("mazografodfs:"):
        t = extraer(linea, "mazografodfs:")
        try:
            n, inicio = t.split(",")
            n = n.strip(); inicio = inicio.strip()
            visitados = set(); orden = []
            def dfs(v):
                if v in visitados: return
                visitados.add(v); orden.append(v)
                for vecino in grafos_mazo[n].get(v, []):
                    dfs(vecino)
            dfs(inicio)
            print(f"🔍 DFS mazo: {orden}")
        except: print("ERROR dfs")

    elif linea.startswith("mazodijkstra:"):
        t = extraer(linea, "mazodijkstra:")
        try:
            n, resto = t.split(",")
            inicio, fin = resto.split("->")
            n = n.strip(); inicio = inicio.strip(); fin = fin.strip()
            dist = {v: float('inf') for v in grafos_mazo[n]}
            dist[inicio] = 0
            pq = [(0, inicio)]
            while pq:
                d, v = heapq.heappop(pq)
                if v == fin: break
                if d > dist[v]: continue
                for vecino in grafos_mazo[n].get(v, []):
                    nd = d + 1
                    if nd < dist[vecino]:
                        dist[vecino] = nd
                        heapq.heappush(pq, (nd, vecino))
            print(f"🛣️ Distancia {inicio} → {fin}: {dist[fin]}")
        except Exception as e: print("ERROR dijkstra:", e)

    # =========================
    # v5.0 — ÁRBOLES
    # =========================
    elif linea.startswith("mazoarbol:"):
        t = extraer(linea, "mazoarbol:")
        try:
            n, raiz = t.split("=", 1)
            arboles_mazo[n.strip()] = {"raiz": raiz.strip(), "izq": None, "der": None}
            print(f"🌳 Árbol '{n.strip()}' creado con raíz {raiz.strip()}")
        except: print("ERROR arbol")

    elif linea.startswith("mazoarbolinserta:"):
        t = extraer(linea, "mazoarbolinserta:")
        try:
            n, v = t.split("=", 1)
            n = n.strip(); v = v.strip()
            def insertar(nodo, val):
                if nodo is None:
                    return {"raiz": val, "izq": None, "der": None}
                try:
                    if float(val) < float(nodo["raiz"]):
                        nodo["izq"] = insertar(nodo["izq"], val)
                    else:
                        nodo["der"] = insertar(nodo["der"], val)
                except:
                    if val < nodo["raiz"]:
                        nodo["izq"] = insertar(nodo["izq"], val)
                    else:
                        nodo["der"] = insertar(nodo["der"], val)
                return nodo
            arboles_mazo[n] = insertar(arboles_mazo[n], v)
            print(f"🌳 Insertado {v} en árbol '{n}'")
        except: print("ERROR inserta")

    elif linea.startswith("mazoarbolinorden:"):
        t = extraer(linea, "mazoarbolinorden:")
        n = t.strip()
        resultado = []
        def inorden(nodo):
            if nodo:
                inorden(nodo["izq"]); resultado.append(nodo["raiz"]); inorden(nodo["der"])
        inorden(arboles_mazo.get(n))
        print(f"🌳 Inorden mazo: {resultado}")

    # =========================
    # v5.0 — COLA PRIORIDAD
    # =========================
    elif linea.startswith("mazoprioridad:"):
        t = extraer(linea, "mazoprioridad:")
        t = t.strip()
        prioridades_mazo[t] = []
        print(f"⚡ Cola prioridad '{t}' creada")

    elif linea.startswith("mazoprioridadpon:"):
        t = extraer(linea, "mazoprioridadpon:")
        try:
            n, resto = t.split(",", 1)
            v, p = resto.split("->")
            n = n.strip()
            prioridades_mazo[n].append((float(p.strip()), v.strip()))
            prioridades_mazo[n].sort()
            print(f"⚡ Añadido {v.strip()} con prioridad {p.strip()}")
        except: print("ERROR prioridad")

    elif linea.startswith("mazoprioridadtoma:"):
        t = extraer(linea, "mazoprioridadtoma:")
        n = t.strip()
        if prioridades_mazo[n]:
            p, v = prioridades_mazo[n].pop(0)
            print(f"⚡ Tomado mazo: {v} (prioridad {p})")

    # =========================
    # v5.0 — CACHÉ LRU
    # =========================
    elif linea.startswith("mazocache:"):
        t = extraer(linea, "mazocache:")
        try:
            n, cap = t.split("=", 1)
            caches_mazo[n.strip()] = {"capacidad": int(cap), "items": {}}
            print(f"💾 Caché LRU '{n.strip()}' creada (cap {cap})")
        except: print("ERROR cache")

    elif linea.startswith("mazocachepon:"):
        t = extraer(linea, "mazocachepon:")
        try:
            n, resto = t.split(",", 1)
            k, v = resto.split("->")
            n = n.strip(); k = k.strip(); v = v.strip()
            cache = caches_mazo[n]
            if len(cache["items"]) >= cache["capacidad"]:
                cache["items"].pop(next(iter(cache["items"])))
            cache["items"][k] = v
            print(f"💾 Cacheado {k} = {v}")
        except: print("ERROR cachepon")

    elif linea.startswith("mazocachetoma:"):
        t = extraer(linea, "mazocachetoma:")
        try:
            n, k = t.split(",")
            n = n.strip(); k = k.strip()
            cache = caches_mazo[n]
            if k in cache["items"]:
                v = cache["items"].pop(k); cache["items"][k] = v
                print(f"💾 Cache hit: {v}")
            else:
                print("💾 Cache miss mazo")
        except: print("ERROR cachetoma")

    # =========================
    # v5.0 — MEMOIZACIÓN
    # =========================
    elif linea.startswith("mazomemo:"):
        t = extraer(linea, "mazomemo:")
        try:
            nombre, cmd = t.split("=", 1)
            memos_mazo[nombre.strip()] = {"cmd": cmd.strip(), "cache": {}}
            print(f"🧠 Función '{nombre.strip()}' memoizada")
        except: print("ERROR memo")

    elif linea.startswith("mazomemollama:"):
        t = extraer(linea, "mazomemollama:")
        try:
            n, args = t.split(",", 1)
            n = n.strip(); args = args.strip()
            memo = memos_mazo[n]
            if args in memo["cache"]:
                print(f"🧠 Memo hit: {memo['cache'][args]}")
            else:
                for par in args.split("|"):
                    if "=" in par:
                        k, v = par.split("=", 1)
                        variables[k.strip()] = v.strip()
                ejecutar(memo["cmd"])
                memo["cache"][args] = "calculado"
        except: print("ERROR memollama")

    # =========================
    # v5.0 — PIPELINE
    # =========================
    elif linea.startswith("mazopipeline:"):
        t = extraer(linea, "mazopipeline:")
        try:
            n, pasos = t.split("=", 1)
            pipelines_mazo[n.strip()] = [p.strip() for p in pasos.split("->")]
            print(f"🔧 Pipeline '{n.strip()}' creado")
        except: print("ERROR pipeline")

    elif linea.startswith("mazopipelinerun:"):
        t = extraer(linea, "mazopipelinerun:")
        try:
            n, valor = t.split(",", 1)
            n = n.strip()
            variables["_valor"] = valor.strip()
            for paso in pipelines_mazo[n]:
                if paso in funciones:
                    ejecutar(funciones[paso])
            print(f"🔧 Pipeline mazo terminado")
        except: print("ERROR pipelinerun")

    # =========================
    # v5.0 — CURRY
    # =========================
    elif linea.startswith("mazocurry:"):
        t = extraer(linea, "mazocurry:")
        try:
            nombre, params = t.split("=", 1)
            currys_mazo[nombre.strip()] = {"params": [p.strip() for p in params.split(",")], "valores": {}}
            print(f"🍛 Función currificada '{nombre.strip()}'")
        except: print("ERROR curry")

    elif linea.startswith("mazocurryaplica:"):
        t = extraer(linea, "mazocurryaplica:")
        try:
            n, kv = t.split(",", 1)
            k, v = kv.split("=", 1)
            currys_mazo[n.strip()]["valores"][k.strip()] = v.strip()
            print(f"🍛 Aplicado {k.strip()}={v.strip()}")
        except: print("ERROR curryaplica")

    # =========================
    # v5.0 — COMPOSICIÓN
    # =========================
    elif linea.startswith("mazocompone:"):
        t = extraer(linea, "mazocompone:")
        try:
            n, fs = t.split("=", 1)
            composiciones_mazo[n.strip()] = [f.strip() for f in fs.split("->")]
            print(f"🔗 Composición '{n.strip()}' creada")
        except: print("ERROR compone")

    # =========================
    # v5.0 — OBSERVADOR
    # =========================
    elif linea.startswith("mazoobserva:"):
        t = extraer(linea, "mazoobserva:")
        try:
            n, cmd = t.split("=", 1)
            observadores_mazo[n.strip()] = cmd.strip()
            print(f"👁️ Observando '{n.strip()}'")
        except: print("ERROR observa")

    elif linea.startswith("mazonotifica:"):
        t = extraer(linea, "mazonotifica:")
        try:
            n, v = t.split("=", 1)
            variables[n.strip()] = v.strip()
            if n.strip() in observadores_mazo:
                ejecutar(observadores_mazo[n.strip()])
        except: print("ERROR notifica")

    # =========================
    # v5.0 — SINGLETON
    # =========================
    elif linea.startswith("mazosingleton:"):
        t = extraer(linea, "mazosingleton:")
        try:
            n, cmd = t.split("=", 1)
            if n.strip() not in singletons_mazo:
                singletons_mazo[n.strip()] = {"cmd": cmd.strip(), "creado": False}
            print(f"🔒 Singleton '{n.strip()}' registrado")
        except: print("ERROR singleton")

    elif linea.startswith("mazosingletontoma:"):
        t = extraer(linea, "mazosingletontoma:")
        n = t.strip()
        if n in singletons_mazo:
            if not singletons_mazo[n]["creado"]:
                ejecutar(singletons_mazo[n]["cmd"])
                singletons_mazo[n]["creado"] = True
            print(f"🔒 Instancia singleton '{n}'")
        else: print("singleton no existe")

    # =========================
    # v5.0 — BÚSQUEDA BINARIA
    # =========================
    elif linea.startswith("mazobinaria:"):
        t = extraer(linea, "mazobinaria:")
        try:
            n, v = t.split(",")
            n = n.strip(); v = v.strip()
            arr = sorted(listas[n], key=lambda x: float(x) if _es_num(x) else x)
            lo, hi = 0, len(arr) - 1
            encontrado = -1
            while lo <= hi:
                mid = (lo + hi) // 2
                if str(arr[mid]) == v:
                    encontrado = mid; break
                try:
                    if float(arr[mid]) < float(v): lo = mid + 1
                    else: hi = mid - 1
                except:
                    if arr[mid] < v: lo = mid + 1
                    else: hi = mid - 1
            print(f"🔍 Búsqueda binaria: índice {encontrado}")
        except Exception as e: print("ERROR binaria:", e)

    # =========================
    # v5.0 — QUICKSORT
    # =========================
    elif linea.startswith("mazoquisort:"):
        t = extraer(linea, "mazoquisort:")
        n = t.strip()
        if n in listas:
            def quicksort(arr):
                if len(arr) <= 1: return arr
                pivote = arr[len(arr)//2]
                izq = [x for x in arr if _menor(x, pivote)]
                mid = [x for x in arr if _igual(x, pivote)]
                der = [x for x in arr if _mayor(x, pivote)]
                return quicksort(izq) + mid + quicksort(der)
            listas[n] = quicksort(listas[n])
            print(f"⚡ Quicksort mazo: {listas[n]}")

    # =========================
    # v5.0 — MERGESORT
    # =========================
    elif linea.startswith("mazomergesort:"):
        t = extraer(linea, "mazomergesort:")
        n = t.strip()
        if n in listas:
            def mergesort(arr):
                if len(arr) <= 1: return arr
                mid = len(arr) // 2
                izq = mergesort(arr[:mid])
                der = mergesort(arr[mid:])
                return _merge(izq, der)
            listas[n] = mergesort(listas[n])
            print(f"⚡ Mergesort mazo: {listas[n]}")

    # =========================
    # v5.0 — MATEMÁTICAS EXTRA
    # =========================
    elif linea.startswith("mazofibonacci:"):
        t = extraer(linea, "mazofibonacci:")
        try:
            n = int(resolver_variables(t))
            a, b = 0, 1; seq = []
            for _ in range(n):
                seq.append(a); a, b = b, a + b
            print(f"🌀 Fibonacci mazo: {seq}")
        except: print("ERROR fibonacci")

    elif linea.startswith("mazoprimos:"):
        t = extraer(linea, "mazoprimos:")
        try:
            n = int(resolver_variables(t))
            primos = [x for x in range(2, n+1) if all(x % d != 0 for d in range(2, int(x**0.5)+1))]
            print(f"🔢 Primos mazo hasta {n}: {primos}")
        except: print("ERROR primos")

    elif linea.startswith("mazopalindromo:"):
        t = extraer(linea, "mazopalindromo:")
        txt = resolver_variables(t).lower().replace(" ", "")
        print(f"🔄 ¿Palíndromo mazo?: {txt == txt[::-1]}")

    elif linea.startswith("mazoanagrama:"):
        t = extraer(linea, "mazoanagrama:")
        try:
            a, b = t.split(",")
            a = resolver_variables(a.strip()).lower().replace(" ", "")
            b = resolver_variables(b.strip()).lower().replace(" ", "")
            print(f"🔤 ¿Anagrama mazo?: {sorted(a) == sorted(b)}")
        except: print("ERROR anagrama")

    elif linea.startswith("mazolevenshtein:"):
        t = extraer(linea, "mazolevenshtein:")
        try:
            a, b = t.split(",")
            a = resolver_variables(a.strip()); b = resolver_variables(b.strip())
            m, n = len(a), len(b)
            dp = [[0]*(n+1) for _ in range(m+1)]
            for i in range(m+1): dp[i][0] = i
            for j in range(n+1): dp[0][j] = j
            for i in range(1, m+1):
                for j in range(1, n+1):
                    costo = 0 if a[i-1] == b[j-1] else 1
                    dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+costo)
            print(f"📏 Distancia Levenshtein mazo: {dp[m][n]}")
        except: print("ERROR levenshtein")

    # =========================
    # v5.0 — HILOS
    # =========================
    elif linea.startswith("mazohilo:"):
        t = extraer(linea, "mazohilo:")
        try:
            n, cmd = t.split("=", 1)
            n = n.strip()
            def worker(): ejecutar(cmd.strip())
            hilos_mazo[n] = threading.Thread(target=worker)
            hilos_mazo[n].start()
            print(f"🧵 Hilo '{n}' iniciado")
        except Exception as e: print("ERROR hilo:", e)

    elif linea.startswith("mazohiloespera:"):
        t = extraer(linea, "mazohiloespera:")
        n = t.strip()
        if n in hilos_mazo:
            hilos_mazo[n].join()
            print(f"🧵 Hilo '{n}' terminado")

    # =========================
    # v5.0 — ASYNC / AWAIT
    # =========================
    elif linea.startswith("mazoasync:"):
        t = extraer(linea, "mazoasync:")
        try:
            n, cmd = t.split("=", 1)
            async_mazo[n.strip()] = cmd.strip()
            print(f"⚡ Tarea async '{n.strip()}' definida")
        except: print("ERROR async")

    elif linea.startswith("mazoawait:"):
        import asyncio
        t = extraer(linea, "mazoawait:")
        n = t.strip()
        if n in async_mazo:
            async def correr(): ejecutar(async_mazo[n])
            asyncio.run(correr())
            print(f"⚡ Async '{n}' completado")

    # =========================
    # v5.0 — PROMESAS
    # =========================
    elif linea.startswith("mazopromesa:"):
        t = extraer(linea, "mazopromesa:")
        try:
            n, cmd = t.split("=", 1)
            promesas_mazo[n.strip()] = {"cmd": cmd.strip(), "resuelta": False}
            print(f"🤝 Promesa '{n.strip()}' creada")
        except: print("ERROR promesa")

    elif linea.startswith("mazoresuelve:"):
        t = extraer(linea, "mazoresuelve:")
        n = t.strip()
        if n in promesas_mazo:
            ejecutar(promesas_mazo[n]["cmd"])
            promesas_mazo[n]["resuelta"] = True
            print(f"🤝 Promesa '{n}' resuelta")

    # =========================
    # v5.0 — FACTORY
    # =========================
    elif linea.startswith("mazofactory:"):
        t = extraer(linea, "mazofactory:")
        try:
            n, tipos = t.split("=", 1)
            factories_mazo[n.strip()] = {}
            for tipo in tipos.split("|"):
                k, cmd = tipo.split(":")
                factories_mazo[n.strip()][k.strip()] = cmd.strip()
            print(f"🏭 Factory '{n.strip()}' creada")
        except: print("ERROR factory")

    elif linea.startswith("mazofactorycrea:"):
        t = extraer(linea, "mazofactorycrea:")
        try:
            n, tipo = t.split(",")
            n = n.strip(); tipo = tipo.strip()
            if tipo in factories_mazo[n]:
                ejecutar(factories_mazo[n][tipo])
                print(f"🏭 Creado {tipo} desde factory '{n}'")
        except: print("ERROR factorycrea")

    # =========================
    # v5.0 — STRATEGY
    # =========================
    elif linea.startswith("mazostrategy:"):
        t = extraer(linea, "mazostrategy:")
        try:
            n, estrategias = t.split("=", 1)
            strategies_mazo[n.strip()] = {}
            for e in estrategias.split("|"):
                k, cmd = e.split(":")
                strategies_mazo[n.strip()][k.strip()] = cmd.strip()
            print(f"🎯 Strategy '{n.strip()}' creada")
        except: print("ERROR strategy")

    elif linea.startswith("mazostrategyusa:"):
        t = extraer(linea, "mazostrategyusa:")
        try:
            n, resto = t.split(",", 1)
            est, cmd = resto.split("->", 1)
            n = n.strip(); est = est.strip()
            if est in strategies_mazo[n]:
                ejecutar(strategies_mazo[n][est])
        except: print("ERROR strategyusa")

    # =========================
    # v5.0 — BUILDER
    # =========================
    elif linea.startswith("mazobuilder:"):
        t = extraer(linea, "mazobuilder:")
        try:
            n, pasos = t.split("=", 1)
            builders_mazo[n.strip()] = {"pasos": [p.strip() for p in pasos.split("->")], "construido": []}
            print(f"🔨 Builder '{n.strip()}' creado")
        except: print("ERROR builder")

    elif linea.startswith("mazobuilderpaso:"):
        t = extraer(linea, "mazobuilderpaso:")
        try:
            n, cmd = t.split(",", 1)
            builders_mazo[n.strip()]["construido"].append(cmd.strip())
            print(f"🔨 Paso añadido a '{n.strip()}'")
        except: print("ERROR builderpaso")

    elif linea.startswith("mazobuilderfin:"):
        t = extraer(linea, "mazobuilderfin:")
        n = t.strip()
        if n in builders_mazo:
            for cmd in builders_mazo[n]["construido"]:
                ejecutar(cmd)
            print(f"🔨 Builder '{n}' finalizado")

    # =========================
    # v5.0 — DECORADOR
    # =========================
    elif linea.startswith("mazodecorador:"):
        t = extraer(linea, "mazodecorador:")
        try:
            n, cmd = t.split("=", 1)
            decoradores_mazo[n.strip()] = cmd.strip()
            print(f"🎀 Decorador '{n.strip()}' definido")
        except: print("ERROR decorador")

    elif linea.startswith("mazodecora:"):
        t = extraer(linea, "mazodecora:")
        try:
            dec, fn = t.split(",", 1)
            dec = dec.strip(); fn = fn.strip()
            if dec in decoradores_mazo: ejecutar(decoradores_mazo[dec])
            if fn in funciones: ejecutar(funciones[fn])
            print(f"🎀 Función '{fn}' decorada con '{dec}'")
        except: print("ERROR decora")

    # =========================
    # v5.0 — SQL
    # =========================
    elif linea.startswith("mazosql:"):
        t = extraer(linea, "mazosql:")
        try:
            db, query = t.split(",", 1)
            db = resolver_variables(db.strip())
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            cur.execute(resolver_variables(query.strip()))
            if query.strip().lower().startswith("select"):
                for fila in cur.fetchall():
                    print("📊 SQL mazo:", fila)
            else:
                conn.commit()
                print("📊 SQL mazo ejecutado")
            conn.close()
        except Exception as e: print("ERROR sql:", e)

    # =========================
    # v5.0 — PICKLE
    # =========================
    elif linea.startswith("mazopickle:"):
        t = extraer(linea, "mazopickle:")
        try:
            n, archivo = t.split(",")
            n = n.strip(); archivo = archivo.strip()
            datos = listas.get(n) or diccionarios.get(n) or variables.get(n)
            with open(archivo, "wb") as f: pickle.dump(datos, f)
            print(f"📦 Pickle guardado en {archivo}")
        except Exception as e: print("ERROR pickle:", e)

    elif linea.startswith("mazounpickle:"):
        t = extraer(linea, "mazounpickle:")
        try:
            n, archivo = t.split(",")
            n = n.strip(); archivo = archivo.strip()
            with open(archivo, "rb") as f: datos = pickle.load(f)
            if isinstance(datos, list): listas[n] = datos
            elif isinstance(datos, dict): diccionarios[n] = datos
            else: variables[n] = datos
            print(f"📦 Pickle cargado en {n}")
        except Exception as e: print("ERROR unpickle:", e)

    # =========================
    # v5.0 — ZIP
    # =========================
    elif linea.startswith("mazozip:"):
        t = extraer(linea, "mazozip:")
        try:
            zip_name, archivos = t.split(",", 1)
            with zipfile.ZipFile(zip_name.strip(), "w") as z:
                for a in archivos.split("|"): z.write(a.strip())
            print(f"🗜️ ZIP mazo creado: {zip_name.strip()}")
        except Exception as e: print("ERROR zip:", e)

    elif linea.startswith("mazounzip:"):
        t = extraer(linea, "mazounzip:")
        try:
            zip_name, destino = t.split(",")
            with zipfile.ZipFile(zip_name.strip(), "r") as z: z.extractall(destino.strip())
            print(f"🗜️ ZIP mazo extraído en {destino.strip()}")
        except Exception as e: print("ERROR unzip:", e)

    # =========================
    # v5.0 — CSV
    # =========================
    elif linea.startswith("mazocsvlee:"):
        t = extraer(linea, "mazocsvlee:")
        try:
            n, archivo = t.split(",")
            with open(archivo.strip(), "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                listas[n.strip()] = [fila for fila in reader]
            print(f"📊 CSV leído en '{n.strip()}'")
        except Exception as e: print("ERROR csv:", e)

    elif linea.startswith("mazocsvescribe:"):
        t = extraer(linea, "mazocsvescribe:")
        try:
            n, archivo = t.split(",")
            n = n.strip()
            with open(archivo.strip(), "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f); writer.writerows(listas[n])
            print(f"📊 CSV escrito: {archivo.strip()}")
        except Exception as e: print("ERROR csv:", e)

    # =========================
    # v5.0 — HTTP
    # =========================
    elif linea.startswith("mazohttp:"):
        try:
            t = extraer(linea, "mazohttp:")
            url = resolver_variables(t.strip())
            with urllib.request.urlopen(url, timeout=10) as r:
                contenido = r.read().decode("utf-8", errors="ignore")
            variables["_http"] = contenido
            print(f"🌐 HTTP mazo: {len(contenido)} bytes")
        except Exception as e: print("ERROR http:", e)

    elif linea.startswith("mazohttppost:"):
        try:
            t = extraer(linea, "mazohttppost:")
            url, data = t.split(",", 1)
            data_enc = urllib.parse.urlencode({"data": data.strip()}).encode()
            req = urllib.request.Request(url.strip(), data=data_enc)
            with urllib.request.urlopen(req, timeout=10) as r:
                contenido = r.read().decode("utf-8", errors="ignore")
            print(f"🌐 POST mazo: {len(contenido)} bytes")
            variables["_http"] = contenido
        except Exception as e: print("ERROR httppost:", e)

    elif linea.startswith("mazohttpguarda:"):
        t = extraer(linea, "mazohttpguarda:")
        try:
            if "_http" in variables:
                with open(t.strip(), "w", encoding="utf-8") as f: f.write(variables["_http"])
                print(f"💾 HTTP guardado en {t.strip()}")
        except Exception as e: print("ERROR httpguarda:", e)

    # =========================
    # v5.0 — SCRAPING
    # =========================
    elif linea.startswith("mazoscrap:"):
        try:
            t = extraer(linea, "mazoscrap:")
            url, patron = t.split(",", 1)
            with urllib.request.urlopen(url.strip(), timeout=10) as r:
                html = r.read().decode("utf-8", errors="ignore")
            matches = re.findall(patron.strip(), html)
            print(f"🕷️ Scraping mazo: {matches[:10]}")
        except Exception as e: print("ERROR scrap:", e)

    # =========================
    # v5.0 — CORREO
    # =========================
    elif linea.startswith("mazocorreo:"):
        t = extraer(linea, "mazocorreo:")
        try:
            smtp, resto = t.split(",", 1)
            origen, resto = resto.split(",", 1)
            destino, resto = resto.split(",", 1)
            asunto, cuerpo = resto.split(",", 1)
            msg = MIMEText(cuerpo.strip())
            msg["Subject"] = asunto.strip()
            msg["From"] = origen.strip()
            msg["To"] = destino.strip()
            with smtplib.SMTP(smtp.strip(), 587) as s:
                s.starttls(); s.send_message(msg)
            print(f"📧 Correo mazo enviado a {destino.strip()}")
        except Exception as e: print("ERROR correo:", e)

    # =========================
    # v5.0 — AES / FIRMA
    # =========================
    elif linea.startswith("mazoaes:"):
        t = extraer(linea, "mazoaes:")
        try:
            txt, clave = t.split(",", 1)
            txt = resolver_variables(txt.strip()); clave = clave.strip()
            key_bytes = hashlib.sha256(clave.encode()).digest()
            cifrado = bytes([ord(c) ^ key_bytes[i % len(key_bytes)] for i, c in enumerate(txt)])
            print("🔐 AES mazo:", base64.b64encode(cifrado).decode())
        except Exception as e: print("ERROR aes:", e)

    elif linea.startswith("mazodesaes:"):
        t = extraer(linea, "mazodesaes:")
        try:
            b64, clave = t.split(",", 1)
            b64 = resolver_variables(b64.strip()); clave = clave.strip()
            key_bytes = hashlib.sha256(clave.encode()).digest()
            cifrado = base64.b64decode(b64)
            descifrado = bytes([c ^ key_bytes[i % len(key_bytes)] for i, c in enumerate(cifrado)])
            print("🔓 DesAES mazo:", descifrado.decode("utf-8"))
        except Exception as e: print("ERROR desaes:", e)

    elif linea.startswith("mazofirma:"):
        t = extraer(linea, "mazofirma:")
        try:
            txt, clave = t.split(",", 1)
            txt = resolver_variables(txt.strip())
            firma = hashlib.sha256((txt + clave.strip()).encode()).hexdigest()
            print("🖊️ Firma mazo:", firma)
        except: print("ERROR firma")

    elif linea.startswith("mazoverificafirma:"):
        t = extraer(linea, "mazoverificafirma:")
        try:
            txt, resto = t.split(",", 1)
            clave, firma = resto.split(",", 1)
            esperada = hashlib.sha256((resolver_variables(txt.strip()) + clave.strip()).encode()).hexdigest()
            print("✅ Firma válida mazo:", esperada == firma.strip())
        except: print("ERROR verificafirma")

    # =========================
    # v5.0 — GENERADORES
    # =========================
    elif linea.startswith("mazogenerador:"):
        t = extraer(linea, "mazogenerador:")
        try:
            n, cmd = t.split("=", 1)
            generadores_mazo[n.strip()] = cmd.strip()
            print(f"🔄 Generador '{n.strip()}' definido")
        except: print("ERROR generador")

    elif linea.startswith("mazogeneranext:"):
        t = extraer(linea, "mazogeneranext:")
        n = t.strip()
        if n in generadores_mazo:
            if "_gen_" + n not in variables:
                variables["_gen_" + n] = 0
            variables["_i"] = variables["_gen_" + n]
            ejecutar(generadores_mazo[n])
            variables["_gen_" + n] += 1
            print(f"🔄 Generado mazo #{variables['_gen_' + n]}")

    # =========================
    # v5.0 — ITERADORES
    # =========================
    elif linea.startswith("mazoiter:"):
        t = extraer(linea, "mazoiter:")
        try:
            n, vals = t.split("=", 1)
            iteradores_mazo[n.strip()] = iter(vals.split(","))
            print(f"🔄 Iterador '{n.strip()}' creado")
        except: print("ERROR iter")

    elif linea.startswith("mazoiternext:"):
        t = extraer(linea, "mazoiternext:")
        n = t.strip()
        if n in iteradores_mazo:
            try: print(f"🔄 Iter next mazo: {next(iteradores_mazo[n])}")
            except StopIteration: print("🔄 Iterador agotado mazo")

    # =========================
    # v5.0 — LAMBDAS
    # =========================
    elif linea.startswith("mazolambda:"):
        t = extraer(linea, "mazolambda:")
        try:
            n, expr = t.split("=", 1)
            lambdas_mazo[n.strip()] = expr.strip()
            print(f"λ Lambda '{n.strip()}' definida")
        except: print("ERROR lambda")

    elif linea.startswith("mazolambdacalcula:"):
        t = extraer(linea, "mazolambdacalcula:")
        try:
            n, args = t.split(",", 1)
            n = n.strip()
            for par in args.split("|"):
                if "=" in par:
                    k, v = par.split("=", 1)
                    variables[k.strip()] = v.strip()
            expr = resolver_variables(lambdas_mazo[n])
            print(f"λ Resultado mazo: {eval(expr)}")
        except Exception as e: print("ERROR lambdacalcula:", e)

    # =========================
    # v5.0 — PATTERN MATCHING
    # =========================
    elif linea.startswith("mazomatch:"):
        t = extraer(linea, "mazomatch:")
        try:
            valor, casos = t.split("->", 1)
            valor = resolver_variables(valor.strip())
            for caso in casos.split("|"):
                if ":" in caso:
                    patron, cmd = caso.split(":", 1)
                    patron = patron.strip()
                    if patron == "_" or patron == valor:
                        ejecutar(cmd.strip()); break
        except: print("ERROR match")

    # =========================
    # v5.0 — CONTEXT MANAGER
    # =========================
    elif linea.startswith("mazocontexto:"):
        t = extraer(linea, "mazocontexto:")
        try:
            setup, cuerpo, teardown = t.split("|", 2)
            ejecutar(setup.strip())
            try: ejecutar(cuerpo.strip())
            finally: ejecutar(teardown.strip())
        except Exception as e: print("ERROR contexto:", e)

    # =========================
    # v5.0 — ENUM
    # =========================
    elif linea.startswith("mazoenum:"):
        t = extraer(linea, "mazoenum:")
        try:
            n, valores = t.split("=", 1)
            enums_mazo[n.strip()] = {v.strip(): i for i, v in enumerate(valores.split(","))}
            print(f"📋 Enum '{n.strip()}' creado: {list(enums_mazo[n.strip()].keys())}")
        except: print("ERROR enum")

    elif linea.startswith("mazoenumtoma:"):
        t = extraer(linea, "mazoenumtoma:")
        try:
            n, v = t.split(",")
            n = n.strip(); v = v.strip()
            if v in enums_mazo[n]:
                print(f"📋 {n}.{v} = {enums_mazo[n][v]}")
            else:
                print("valor no existe en enum")
        except: print("ERROR enumtoma")

    # =========================
    # v5.0 — DATACLASS
    # =========================
    elif linea.startswith("mazodataclass:"):
        t = extraer(linea, "mazodataclass:")
        try:
            n, campos = t.split("=", 1)
            dataclasses_mazo[n.strip()] = [c.strip() for c in campos.split(",")]
            print(f"📦 DataClass '{n.strip()}' con campos: {dataclasses_mazo[n.strip()]}")
        except: print("ERROR dataclass")

    elif linea.startswith("mazodatacrea:"):
        t = extraer(linea, "mazodatacrea:")
        try:
            n, resto = t.split(",", 1)
            inst_name, valores = resto.split("->", 1)
            n = n.strip()
            vals = [v.strip() for v in valores.split("|")]
            if len(vals) != len(dataclasses_mazo[n]):
                print("ERROR: número de valores no coincide")
            else:
                diccionarios[inst_name.strip()] = dict(zip(dataclasses_mazo[n], vals))
                print(f"📦 DataClass creada: {inst_name.strip()} = {diccionarios[inst_name.strip()]}")
        except: print("ERROR datacrea")

    # ============================================================
    # ============================================================
    #       v5.5 — COMANDOS NUEVOS MAZÓNICOS 🪓
    #       YA NO GASTES DINERO EN EL MAZO
    #       (el mazo quedó inservible por la lanza)
    # ============================================================
    # ============================================================

    # ---------- BURLA DEL MAZO ----------
    elif linea.startswith("mazoburla:"):
        t = extraer(linea, "mazoburla:")
        if t:
            variables["_last_burla"] = resolver_variables(t)
        print(color("&a🪓 " + random.choice(burlas_mazo) + " &0"))

    elif linea == "mazoburla":
        print(color("&a🪓 " + random.choice(burlas_mazo) + " &0"))

    elif linea.startswith("mazolanzo:"):
        # La lanza que arruinó el mazo
        t = extraer(linea, "mazolanzo:")
        objetivo = resolver_variables(t).strip() if t else "el mazo"
        daño = random.randint(50, 100)
        print(color(f"&r🗡️ ¡La lanza ataca a {objetivo}! Daño: {daño} &0"))
        if daño >= 90:
            print(color("&r💥 El mazo quedó INSERVIBLE. YA NO GASTES DINERO EN EL MAZO. &0"))
            logros_mazo.add("sin_dinero")

    # ---------- BÓVEDA MAZÓNICA ----------
    elif linea.startswith("mazoboveda:"):
        t = extraer(linea, "mazoboveda:")
        try:
            n, v = t.split("=", 1)
            boveda_mazo[n.strip()] = {"valor": resolver_variables(v.strip()), "tipo": "secreto"}
            print(f"🏦 Guardado en bóveda: {n.strip()}")
        except: print("ERROR boveda")

    elif linea.startswith("mazobovedatoma:"):
        t = extraer(linea, "mazobovedatoma:")
        n = t.strip()
        if n in boveda_mazo:
            print(f"🏦 Bóveda[{n}] = {boveda_mazo[n]['valor']}")
        else:
            print("🔒 La bóveda está vacía o no existe esa llave mazo")

    elif linea.startswith("mazobovedaborra:"):
        t = extraer(linea, "mazobovedaborra:")
        n = t.strip()
        if n in boveda_mazo:
            del boveda_mazo[n]
            print(f"🗑️ Bóveda mazo: {n} eliminado")

    elif linea == "mazoboveda":
        print(f"🏦 Bóveda mazónica: {list(boveda_mazo.keys()) or '(vacía)'}")

    # ---------- POCIONES ----------
    elif linea.startswith("mazopocion:"):
        t = extraer(linea, "mazopocion:")
        try:
            n, efecto = t.split("=", 1)
            pociones_mazo[n.strip()] = {"efecto": efecto.strip(), "usada": False}
            print(f"🧪 Poción '{n.strip()}' creada con efecto '{efecto.strip()}'")
        except: print("ERROR pocion")

    elif linea.startswith("mazotomapocion:"):
        t = extraer(linea, "mazotoma pocion:".replace(" ", ""))
        if t is None:
            t = extraer(linea, "mazotomapocion:")
        n = t.strip() if t else ""
        if n in pociones_mazo:
            p = pociones_mazo[n]
            if p["usada"]:
                print(f"🧪 Poción '{n}' ya fue usada, no gastes dinero en pociones usadas")
            else:
                p["usada"] = True
                print(f"🧪 ¡Glup! Efecto '{p['efecto']}' activado")
                # Aplica efecto si es una variable
                if p["efecto"] in variables:
                    print(f"✨ ${p['efecto']} se siente más fuerte")
                else:
                    variables["_" + n + "_efecto"] = p["efecto"]

    elif linea == "mazopociones":
        print(f"🧪 Pociones en el mazo: {list(pociones_mazo.keys()) or '(ninguna)'}")

    # ---------- ENCANTAMIENTOS ----------
    elif linea.startswith("mazoencanta:"):
        t = extraer(linea, "mazoencanta:")
        try:
            item, enc = t.split(",", 1)
            item = item.strip(); enc = enc.strip()
            encantamientos_items.setdefault(item, []).append(enc)
            print(f"✨ '{item}' encantado con '{enc}' (nivel mazónico)")
        except: print("ERROR encanta")

    elif linea.startswith("mazoverencantamiento:"):
        t = extraer(linea, "mazoverencantamiento:")
        item = t.strip()
        if item in encantamientos_items:
            print(f"✨ '{item}' tiene encantamientos: {encantamientos_items[item]}")
        else:
            print("✨ ese item no tiene encantamientos mazo")

    elif linea == "mazoencantamientos":
        print(f"✨ Items encantados: {encantamientos_items or '(ninguno)'}")

    # ---------- MOBS ----------
    elif linea.startswith("mazomob:"):
        t = extraer(linea, "mazomob:")
        try:
            n, stats = t.split("=", 1)
            mobs_mazo[n.strip()] = {
                "vida": random.randint(10, 50),
                "ataque": random.randint(1, 10),
                "tipo": stats.strip() or "genérico"
            }
            print(f"👾 Mob '{n.strip()}' apareció ({mobs_mazo[n.strip()]['tipo']})")
        except: print("ERROR mob")

    elif linea.startswith("mazoatacamob:"):
        t = extraer(linea, "mazoatacamob:")
        try:
            mob, daño = t.split(",")
            mob = mob.strip(); daño = int(daño.strip())
            if mob in mobs_mazo:
                mobs_mazo[mob]["vida"] -= daño
                if mobs_mazo[mob]["vida"] <= 0:
                    print(f"💀 '{mob}' ha sido derrotado. Suelta 1 esmeralda mazo")
                    del mobs_mazo[mob]
                else:
                    print(f"⚔️ '{mob}' recibió {daño}. Vida restante: {mobs_mazo[mob]['vida']}")
        except: print("ERROR atacamob")

    elif linea == "mazomobs":
        if mobs_mazo:
            for n, m in mobs_mazo.items():
                print(f"👾 {n}: vida={m['vida']} ataque={m['ataque']} tipo={m['tipo']}")
        else:
            print("👾 No hay mobs en el mazo (todos se fueron por la lanza)")

    # ---------- MAZMORRAS ----------
    elif linea.startswith("mazmazmorra:"):
        t = extraer(linea, "mazmazmorra:")
        try:
            n, dificultad = t.split("=", 1)
            mazmorras_mazo[n.strip()] = {
                "dificultad": dificultad.strip(),
                "salas": random.randint(3, 10),
                "tesoro": random.choice(["mazo", "lanza", "esmeralda", "poción", "nada"]),
                "explorada": False
            }
            print(f"🏰 Mazmorra '{n.strip()}' generada (dificultad {dificultad.strip()})")
        except: print("ERROR mazmorra")

    elif linea.startswith("mazoexplora:"):
        t = extraer(linea, "mazoexplora:")
        n = t.strip()
        if n in mazmorras_mazo:
            m = mazmorras_mazo[n]
            m["explorada"] = True
            print(f"🗺️ Explorando '{n}' ({m['salas']} salas, dificultad {m['dificultad']})")
            if m["tesoro"] == "lanza":
                print(color("&r🗡️ ¡Encontraste la LANZA! El mazo ya no sirve. YA NO GASTES DINERO EN EL MAZO. &0"))
                logros_mazo.add("explorador")
                logros_mazo.add("sin_dinero")
            else:
                print(f"💰 Encontraste: {m['tesoro']}")
                logros_mazo.add("explorador")

    elif linea == "mazmazmorras" or linea == "mazmazmorras:":
        print(f"🏰 Mazmorras: {list(mazmorras_mazo.keys()) or '(ninguna)'}")

    # ---------- LOGROS ----------
    elif linea.startswith("mazologro:"):
        t = extraer(linea, "mazologro:")
        n = t.strip()
        if n in logros_def:
            logros_mazo.add(n)
            print(f"🏆 ¡LOGRO DESBLOQUEADO! {logros_def[n]}")
        else:
            logros_mazo.add(n)
            print(f"🏆 Logro '{n}' desbloqueado (misterioso)")

    elif linea == "mazologros":
        if logros_mazo:
            print(f"🏆 Logros ({len(logros_mazo)}):")
            for l in logros_mazo:
                desc = logros_def.get(l, "logro secreto del mazo")
                print(f"  ✅ {l}: {desc}")
        else:
            print("🏆 Sin logros todavía. Sigue mazando")

    elif linea == "mazologrosdef":
        for k, v in logros_def.items():
            estado = "✅" if k in logros_mazo else "🔒"
            print(f"  {estado} {k}: {v}")

    # ---------- INVENTARIO ----------
    elif linea.startswith("mazoinv:"):
        t = extraer(linea, "mazoinv:")
        jugador = t.strip()
        inventario_mazo.setdefault(jugador, {})
        print(f"🎒 Inventario de '{jugador}' creado")

    elif linea.startswith("mazoinvpon:"):
        t = extraer(linea, "mazoinvpon:")
        try:
            jug, resto = t.split(",", 1)
            item, cant = resto.split("->")
            jug = jug.strip(); item = item.strip(); cant = int(cant.strip())
            inventario_mazo.setdefault(jug, {})
            inventario_mazo[jug][item] = inventario_mazo[jug].get(item, 0) + cant
            print(f"🎒 +{cant} {item} a {jug}")
        except: print("ERROR invpon")

    elif linea.startswith("mazoinvtoma:"):
        t = extraer(linea, "mazoinvtoma:")
        try:
            jug, resto = t.split(",", 1)
            item, cant = resto.split("->")
            jug = jug.strip(); item = item.strip(); cant = int(cant.strip())
            if inventario_mazo.get(jug, {}).get(item, 0) >= cant:
                inventario_mazo[jug][item] -= cant
                if inventario_mazo[jug][item] <= 0:
                    del inventario_mazo[jug][item]
                print(f"🎒 -{cant} {item} de {jug}")
            else:
                print("🎒 No tienes suficientes (ni gastes dinero en el mazo)")
        except: print("ERROR invtoma")

    elif linea.startswith("mazoinvver:"):
        t = extraer(linea, "mazoinvver:")
        jug = t.strip()
        if jug in inventario_mazo:
            print(f"🎒 Inventario de '{jug}':")
            for item, cant in inventario_mazo[jug].items():
                print(f"  {item} x{cant}")
        else:
            print("🎒 inventario vacío")

    # ---------- TRADES ----------
    elif linea.startswith("mazotrade:"):
        t = extraer(linea, "mazotrade:")
        try:
            n, resto = t.split("=", 1)
            da, recibo = resto.split("->")
            trades_mazo[n.strip()] = {
                "das": da.strip(),
                "recibes": recibo.strip(),
                "usos": 0
            }
            print(f"🤝 Trade '{n.strip()}' registrado: {da.strip()} → {recibo.strip()}")
        except: print("ERROR trade")

    elif linea.startswith("mazotradehaz:"):
        t = extraer(linea, "mazotradehaz:")
        try:
            n, jug = t.split(",")
            n = n.strip(); jug = jug.strip()
            if n in trades_mazo:
                tr = trades_mazo[n]
                inv = inventario_mazo.setdefault(jug, {})
                inv[tr["recibes"]] = inv.get(tr["recibes"], 0) + 1
                tr["usos"] += 1
                print(f"🤝 Trade hecho: {tr['das']} → {tr['recibes']}")
                if tr["usos"] >= 5:
                    logros_mazo.add("trader")
        except: print("ERROR tradehaz")

    elif linea == "mazotrades":
        for n, t in trades_mazo.items():
            print(f"  🤝 {n}: {t['das']} → {t['recibes']} (usos: {t['usos']})")

    # ---------- RECETAS ----------
    elif linea.startswith("mazoreceta:"):
        t = extraer(linea, "mazoreceta:")
        try:
            n, resto = t.split("=", 1)
            ingredientes, resultado = resto.split("->")
            recetas_mazo[n.strip()] = {
                "ingredientes": [i.strip() for i in ingredientes.split("+")],
                "resultado": resultado.strip()
            }
            print(f"📜 Receta '{n.strip()}': {' + '.join(recetas_mazo[n.strip()]['ingredientes'])} = {resultado.strip()}")
        except: print("ERROR receta")

    elif linea.startswith("mazocraftea:"):
        t = extraer(linea, "mazocraftea:")
        try:
            n, jug = t.split(",")
            n = n.strip(); jug = jug.strip()
            if n in recetas_mazo:
                r = recetas_mazo[n]
                inv = inventario_mazo.setdefault(jug, {})
                puede = all(inv.get(ing, 0) > 0 for ing in r["ingredientes"])
                if puede:
                    for ing in r["ingredientes"]:
                        inv[ing] -= 1
                        if inv[ing] <= 0: del inv[ing]
                    inv[r["resultado"]] = inv.get(r["resultado"], 0) + 1
                    print(f"⚒️ Crafteaste: {r['resultado']}")
                else:
                    print("⚒️ No tienes los ingredientes, y no gastes dinero en el mazo")
        except: print("ERROR craftea")

    elif linea == "mazorecetas":
        for n, r in recetas_mazo.items():
            print(f"  📜 {n}: {' + '.join(r['ingredientes'])} = {r['resultado']}")

    # ---------- HECHIZOS ----------
    elif linea.startswith("mazohechizo:"):
        t = extraer(linea, "mazohechizo:")
        try:
            n, poder = t.split("=", 1)
            hechizos_mazo[n.strip()] = {
                "poder": random.randint(1, 100),
                "formula": poder.strip()
            }
            print(f"🪄 Hechizo '{n.strip()}' aprendido (poder {hechizos_mazo[n.strip()]['poder']})")
        except: print("ERROR hechizo")

    elif linea.startswith("mazolanzahechizo:"):
        t = extraer(linea, "mazolanzahechizo:")
        n = t.strip()
        if n in hechizos_mazo:
            print(f"🪄 Lanzas '{n}' con poder {hechizos_mazo[n]['poder']}...")
            if hechizos_mazo[n]["poder"] > 80:
                print(color("&r💥 ¡La lanza supera al mazo! YA NO GASTES DINERO EN EL MAZO. &0"))
                logros_mazo.add("sin_dinero")
            else:
                print("✨ El hechizo hace ¡poof! pero no mucho más")
        else:
            print("🪄 Ese hechizo no existe en tu grimorio mazo")

    elif linea == "mazohechizos":
        for n, h in hechizos_mazo.items():
            print(f"  🪄 {n}: poder {h['poder']}")

    # ---------- CLANES ----------
    elif linea.startswith("mazoclan:"):
        t = extraer(linea, "mazoclan:")
        try:
            n, jefe = t.split("=", 1)
            clanes_mazo[n.strip()] = {"jefe": jefe.strip(), "miembros": [jefe.strip()]}
            print(f"⚔️ Clan '{n.strip()}' fundado por {jefe.strip()}")
        except: print("ERROR clan")

    elif linea.startswith("mazoclanune:"):
        t = extraer(linea, "mazoclanune:")
        try:
            n, jug = t.split(",")
            n = n.strip(); jug = jug.strip()
            if n in clanes_mazo:
                clanes_mazo[n]["miembros"].append(jug)
                print(f"⚔️ '{jug}' se unió al clan '{n}'")
        except: print("ERROR clanune")

    elif linea == "mazoclanes":
        for n, c in clanes_mazo.items():
            print(f"  ⚔️ {n} (jefe: {c['jefe']}, {len(c['miembros'])} miembros)")

    # ---------- RANKINGS ----------
    elif linea.startswith("mazorankingpon:"):
        t = extraer(linea, "mazorankingpon:")
        try:
            jug, punt = t.split(",")
            rankings_mazo[jug.strip()] = float(punt.strip())
            print(f"🏅 Ranking actualizado: {jug.strip()} = {punt.strip()}")
        except: print("ERROR rankingpon")

    elif linea == "mazoranking":
        if rankings_mazo:
            orden = sorted(rankings_mazo.items(), key=lambda x: x[1], reverse=True)
            print("🏅 RANKING MAZÓNICO:")
            for i, (j, p) in enumerate(orden, 1):
                print(f"  {i}. {j}: {p}")
        else:
            print("🏅 Nadie en el ranking. Todos gastaron dinero en el mazo")

    # ---------- TORNEOS ----------
    elif linea.startswith("mazotorneo:"):
        t = extraer(linea, "mazotorneo:")
        try:
            n, jugadores = t.split("=", 1)
            torneos_mazo[n.strip()] = {
                "jugadores": [j.strip() for j in jugadores.split(",")],
                "ganador": None
            }
            print(f"🏆 Torneo '{n.strip()}' con {len(torneos_mazo[n.strip()]['jugadores'])} participantes")
        except: print("ERROR torneo")

    elif linea.startswith("mazotorneojuega:"):
        t = extraer(linea, "mazotorneojuega:")
        n = t.strip()
        if n in torneos_mazo:
            jugadores = torneos_mazo[n]["jugadores"]
            if len(jugadores) < 2:
                print("🏆 Se necesitan al menos 2 para el torneo")
            else:
                ganador = random.choice(jugadores)
                torneos_mazo[n]["ganador"] = ganador
                print(f"🏆 ¡{ganador} gana el torneo '{n}'! (no por usar el mazo, obvio)")

    elif linea == "mazotorneos":
        for n, t in torneos_mazo.items():
            print(f"  🏆 {n}: {t['jugadores']} → ganador: {t['ganador'] or 'por jugar'}")

    # ---------- APUESTAS ----------
    elif linea.startswith("mazoapuesta:"):
        t = extraer(linea, "mazoapuesta:")
        try:
            n, resto = t.split("=", 1)
            monto, opcion = resto.split("->")
            apuestas_mazo[n.strip()] = {
                "monto": float(monto.strip()),
                "opcion": opcion.strip(),
                "resultado": None
            }
            print(f"💰 Apuesta '{n.strip()}': {monto.strip()} a '{opcion.strip()}'")
        except: print("ERROR apuesta")

    elif linea.startswith("mazoresuelveapuesta:"):
        t = extraer(linea, "mazoresuelveapuesta:")
        try:
            n, resultado = t.split(",")
            n = n.strip(); resultado = resultado.strip()
            if n in apuestas_mazo:
                ap = apuestas_mazo[n]
                ap["resultado"] = resultado
                if ap["opcion"] == resultado:
                    premio = ap["monto"] * 2
                    print(f"💰 ¡Ganaste {premio}! (nunca apuestes el mazo)")
                else:
                    print(f"💸 Perdiste {ap['monto']}. Ni modo, ya no gastes dinero en el mazo")
        except: print("ERROR resuelveapuesta")

    elif linea == "mazoapuestas":
        for n, a in apuestas_mazo.items():
            print(f"  💰 {n}: {a['monto']} a '{a['opcion']}' → {a['resultado'] or 'pendiente'}")

    # ---------- CONTRATOS ----------
    elif linea.startswith("mazocontrato:"):
        t = extraer(linea, "mazocontrato:")
        try:
            n, resto = t.split("=", 1)
            quien, recompensa = resto.split("->")
            contratos_mazo[n.strip()] = {
                "quien": quien.strip(),
                "recompensa": recompensa.strip(),
                "cumplido": False
            }
            print(f"📜 Contrato '{n.strip()}' con '{quien.strip()}' por '{recompensa.strip()}'")
        except: print("ERROR contrato")

    elif linea.startswith("mazocumple:"):
        t = extraer(linea, "mazocumple:")
        n = t.strip()
        if n in contratos_mazo:
            contratos_mazo[n]["cumplido"] = True
            print(f"📜 Contrato '{n}' cumplido. Recompensa: {contratos_mazo[n]['recompensa']}")

    elif linea == "mazocontratos":
        for n, c in contratos_mazo.items():
            estado = "✅" if c["cumplido"] else "⏳"
            print(f"  {estado} {n}: {c['quien']} → {c['recompensa']}")

    # ---------- MISIONES ----------
    elif linea.startswith("mazomision:"):
        t = extraer(linea, "mazomision:")
        try:
            n, objetivo = t.split("=", 1)
            misiones_mazo[n.strip()] = {
                "objetivo": objetivo.strip(),
                "progreso": 0,
                "completada": False
            }
            print(f"📋 Misión '{n.strip()}': {objetivo.strip()}")
        except: print("ERROR mision")

    elif linea.startswith("mazomisionavanza:"):
        t = extraer(linea, "mazomisionavanza:")
        try:
            n, cant = t.split(",")
            n = n.strip(); cant = int(cant.strip())
            if n in misiones_mazo:
                misiones_mazo[n]["progreso"] += cant
                print(f"📋 Progreso '{n}': {misiones_mazo[n]['progreso']}")
                if misiones_mazo[n]["progreso"] >= 10:
                    misiones_mazo[n]["completada"] = True
                    print(f"✅ ¡Misión '{n}' completada!")
        except: print("ERROR misionavanza")

    elif linea == "mazomisiones":
        for n, m in misiones_mazo.items():
            est = "✅" if m["completada"] else "⏳"
            print(f"  {est} {n}: {m['objetivo']} ({m['progreso']}/10)")

    # ---------- LOGROS SECRETOS ----------
    elif linea.startswith("mazosecreto:"):
        t = extraer(linea, "mazosecreto:")
        try:
            n, pista = t.split("=", 1)
            logros_secretos[n.strip()] = pista.strip()
            print(f"🤫 Logro secreto '{n.strip()}' registrado (pista: {pista.strip()})")
        except: print("ERROR secreto")

    elif linea.startswith("mazodesbloqueasecreto:"):
        t = extraer(linea, "mazodesbloqueasecreto:")
        n = t.strip()
        if n in logros_secretos:
            logros_mazo.add(n)
            print(f"🤫 ¡Descubriste el secreto '{n}'! {logros_secretos[n]}")

    elif linea == "mazosecretos":
        print(f"🤫 Secretos conocidos: {list(logros_secretos.keys()) or '(ninguno)'}")
        print(f"🤫 Secretos desbloqueados: {[s for s in logros_secretos if s in logros_mazo] or '(ninguno)'}")

    # ---------- CHISMES / RUMORES ----------
    elif linea.startswith("mazochisme:"):
        t = extraer(linea, "mazochisme:")
        chismes_mazo.append(resolver_variables(t))
        print(f"👀 Chisme añadido al mazo (#{len(chismes_mazo)})")

    elif linea == "mazochismes":
        if chismes_mazo:
            for i, c in enumerate(chismes_mazo[-5:], 1):
                print(f"  👀 {i}. {c}")
        else:
            print("👀 No hay chismes, todos están minando con el mazo")

    elif linea.startswith("mazorumor:"):
        t = extraer(linea, "mazorumor:")
        rumores_mazo.append(resolver_variables(t))
        print(f"🗣️ Rumor esparcido (#{len(rumores_mazo)})")

    elif linea == "mazorrumores" or linea == "mazorumores":
        if rumores_mazo:
            for i, r in enumerate(rumores_mazo[-5:], 1):
                print(f"  🗣️ {i}. {r}")
        else:
            print("🗣️ Sin rumores por ahora")

    # ---------- PACKS ----------
    elif linea.startswith("mazopack:"):
        t = extraer(linea, "mazopack:")
        try:
            n, contenido = t.split("=", 1)
            packs_mazo[n.strip()] = [x.strip() for x in contenido.split("|")]
            print(f"🎁 Pack '{n.strip()}' creado con {len(packs_mazo[n.strip()])} cosas")
        except: print("ERROR pack")

    elif linea.startswith("mazopackabre:"):
        t = extraer(linea, "mazopackabre:")
        n = t.strip()
        if n in packs_mazo:
            print(f"🎁 Abriendo pack '{n}'...")
            for item in packs_mazo[n]:
                print(f"  ✨ Obtuviste: {item}")
        else:
            print("🎁 Ese pack no existe (ni lo compres, ya no gastes dinero)")

    elif linea == "mazopacks":
        for n, p in packs_mazo.items():
            print(f"  🎁 {n}: {len(p)} items")

    # ---------- MINAR / EXCAVAR (bóveda) ----------
    elif linea.startswith("mazomina:"):
        t = extraer(linea, "mazomina:")
        try:
            n, cant = t.split(",")
            n = n.strip(); cant = int(cant.strip())
            hallazgos = Counter(random.choice(["piedra","hierro","oro","diamante","esmeralda","mazo roto","lanza"])
                                 for _ in range(cant))
            print(f"⛏️ Minaste {cant} bloques en '{n}':")
            for item, num in hallazgos.items():
                print(f"  {item} x{num}")
            if "lanza" in hallazgos:
                print(color("&r🗡️ ¡Encontraste la lanza! Adiós mazo. YA NO GASTES DINERO EN EL MAZO. &0"))
                logros_mazo.add("minero"); logros_mazo.add("sin_dinero")
            else:
                logros_mazo.add("minero")
        except: print("ERROR mina")

    # ---------- EXPLORAR ----------
    elif linea.startswith("mazoexploramundo:"):
        t = extraer(linea, "mazoexploramundo:")
        lugar = t.strip() if t else "overworld"
        eventos = ["creeper explotó","aldeano te estafó","esqueleto te flechó",
                   "encontraste un cofre","te perdiste","un lobo te siguió",
                   "un ghast lloró","la lanza apareció"]
        ev = random.choice(eventos)
        print(f"🗺️ Explorando {lugar}: {ev}")
        if ev == "la lanza apareció":
            print(color("&r🗡️ El mazo ya no sirve. YA NO GASTES DINERO EN EL MAZO. &0"))
            logros_mazo.add("sin_dinero")

    # ---------- FAMILIA / AMIGOS ----------
    elif linea.startswith("mazopresenta:"):
        t = extraer(linea, "mazopresenta:")
        try:
            a, b = t.split(",")
            print(f"👋 ¡{a.strip()} le presenta el mazo a {b.strip()}!")
            if random.random() < 0.5:
                print(f"😱 {b.strip()} dijo: 'ya no gastes dinero en el mazo'")
            else:
                print(f"🙂 {b.strip()} aceptó el mazo (por ahora)")
        except: print("ERROR presenta")

    elif linea.startswith("mazobeso:"):
        print("💋 *sonido de beso mazónico*")

    # ---------- GASTAR / NO GASTAR ----------
    elif linea == "yagastesdinero":
        print(color("&r💸 ¡Ya gastaste dinero en el mazo! &0"))

    elif linea == "yagastastes" or linea == "yagastaste":
        print(color("&r💸 ¡Ya gastaste dinero en el mazo! &0"))

    elif linea == "nogastesdinero":
        print(color("&v✅ ¡Bien! Ya NO gastes dinero en el mazo. &0"))
        logros_mazo.add("sin_dinero")

    elif linea == "nogastesdineroenelmazo":
        print(color("&v🪓✅ ¡Excelente! Ya NO gastes dinero en el mazo. &0"))

    elif linea.startswith("mazoconsejo:"):
        consejos = [
            "YA NO GASTES DINERO EN EL MAZO 🪓",
            "El mazo quedó inservible desde la lanza 🗡️",
            "Invierte tus esmeraldas en pociones 🧪",
            "Los aldeanos ya no aceptan mazos, solo esmeraldas 💎",
            "Un creeper es más útil que un mazo roto 💥",
            "Si ves una lanza, corre 🏃",
            "El mejor mazo es el que no compraste 💰",
        ]
        print(color("&a💡 Consejo mazónico: " + random.choice(consejos) + " &0"))

    elif linea == "mazoconsejo":
        consejos = [
            "YA NO GASTES DINERO EN EL MAZO 🪓",
            "El mazo quedó inservible desde la lanza 🗡️",
            "Invierte tus esmeraldas en pociones 🧪",
        ]
        print(color("&a💡 " + random.choice(consejos) + " &0"))

    # ---------- HUELLAS / LOGROS DEL DÍA ----------
    elif linea == "mazohuella":
        print(f"🪓 Huella mazónica del día: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Logros desbloqueados: {len(logros_mazo)}")

    elif linea == "mazofrase":
        frases = [
            "El mazo no compra la felicidad, la lanza sí (mentira) 🗡️",
            "Un mazo sin filo es un palo con pretensiones 🪵",
            "En el mundo del mazo, el que no gasta, gana 💰",
            "Ya no gastes dinero en el mazo, gástalo en pan 🍞",
        ]
        print(color("&c🎴 " + random.choice(frases) + " &0"))

    # ---------- SISTEMA EXTRA MAZÓNICO ----------
    elif linea == "mazotodo":
        print("🪓 ESTADO TOTAL DEL MAZO:")
        print(f"  Variables: {len(variables)}")
        print(f"  Listas: {len(listas)}")
        print(f"  Diccionarios: {len(diccionarios)}")
        print(f"  Funciones: {len(funciones)}")
        print(f"  Bóveda: {len(boveda_mazo)}")
        print(f"  Pociones: {len(pociones_mazo)}")
        print(f"  Mobs: {len(mobs_mazo)}")
        print(f"  Mazmorras: {len(mazmorras_mazo)}")
        print(f"  Logros: {len(logros_mazo)}/{len(logros_def)}")
        print(f"  Clanes: {len(clanes_mazo)}")
        print(f"  Trades: {len(trades_mazo)}")
        print(f"  Recetas: {len(recetas_mazo)}")
        print(f"  Hechizos: {len(hechizos_mazo)}")
        print(f"  Apuestas: {len(apuestas_mazo)}")
        print(f"  Misiones: {len(misiones_mazo)}")
        print(f"  Contratos: {len(contratos_mazo)}")
        print(f"  Packs: {len(packs_mazo)}")
        print(f"  Chismes: {len(chismes_mazo)}")
        print(f"  Rumores: {len(rumores_mazo)}")
        print("  💰 YA NO GASTES DINERO EN EL MAZO 🪓")

    elif linea == "mazocleanpociones":
        pociones_mazo.clear()
        print("🧹 Pociones limpiadas (todas estaban usadas)")

    elif linea == "mazoclearmobs":
        mobs_mazo.clear()
        print("🧹 Mobs limpiados (se fueron por la lanza)")

    elif linea == "mazoclearlogros":
        logros_mazo.clear()
        print("🧹 Logros reseteados")

    elif linea == "mazoritual":
        print("🕯️ Realizando ritual mazónico...")
        time.sleep(1)
        print("🕯️ Invocando al espíritu del mazo...")
        time.sleep(1)
        print("🕯️ El espíritu dice: YA NO GASTES DINERO EN EL MAZO 🪓")

    elif linea == "mazotragedia":
        print(color("&r🎭 LA TRAGEDIA DEL MAZO:"))
        print(color("&r  Acto 1: Tenías un mazo legendario"))
        print(color("&r  Acto 2: Apareció la lanza 🗡️"))
        print(color("&r  Acto 3: El mazo quedó inservible"))
        print(color("&r  Acto 4: YA NO GASTES DINERO EN EL MAZO"))
        print(color("&0"))

    elif linea == "mazocomedia":
        print(color("&v😂 LA COMEDIA DEL MAZO:"))
        print(color("&v  - ¿Cuánto cuesta el mazo?"))
        print(color("&v  - Ya no cuesta, ya no sirve 🪓"))
        print(color("&v  - JAJAJA (nadie se ríe)"))
        print(color("&0"))

    elif linea == "mazodrama":
        print(color("&a🎬 DRAMA MAZÓNICO:"))
        print(color("&a  Mazo: 'Yo era legendario'"))
        print(color("&a  Lanza: 'Ya no'"))
        print(color("&a  Mazo: ':'("))
        print(color("&0"))

    elif linea.startswith("mazorima:"):
        try:
            n = int(extraer(linea, "mazorima:") or "4")
            print(f"🎵 Generando rima mazónica en {n} versos...")
            palabras = ["mazo","lanza","esmeralda","poción","creeper","aldeano","mazmorra","logro"]
            for i in range(n):
                print(f"  {random.choice(palabras)} con {random.choice(palabras)},")
                print(f"  {random.choice(palabras)} sin {random.choice(palabras)},")
            print("  ¡Y ya no gastes dinero en el mazo! 🪓")
        except: print("ERROR rima")

    elif linea.startswith("mazorap:"):
        t = extraer(linea, "mazorap:")
        tema = t.strip() if t else "mazo"
        print(f"🎤 🥁 ¡{tema.upper()}! 🥁")
        print("🥁 Yo soy el mazo más mazónico")
        print("🥁 Pero la lanza me dejó icónico")
        print("🥁 Ya no gastes dinero en el mazo, es cómico")
        print("🥁 🎤 fin")

    elif linea == "mazopoema":
        print("🪓 📜 Poema mazónico:")
        print("  Erase un mazo valiente,")
        print("  que servía a su gente.")
        print("  Vino la lanza de repente,")
        print("  y el mazo quedó impotente.")
        print("  Moraleja del mazo mazo:")
        print("  YA NO GASTES DINERO EN EL MAZO. 🪓")

    # ---------- COMANDOS DE "LANZA" ----------
    elif linea == "mazolanza":
        print(color("&r🗡️ LA LANZA 🗡️ &0"))
        print("  Stats: +100 al daño, +50 al carisma")
        print("  Efecto: el mazo queda inservible 🪓")
        print("  Precio: TODA tu autoestima")

    elif linea == "mazovslanza":
        m = random.randint(1, 100); l = random.randint(50, 100)
        print(f"🪓 Mazo: {m}  vs  🗡️ Lanza: {l}")
        if m > l:
            print("🪓 ¡El mazo ganó! (pero igual ya no sirve)")
        else:
            print("🗡️ La lanza ganó. Como siempre. YA NO GASTES DINERO EN EL MAZO.")

    # ---------- COMODÍN EXTRA ----------
    elif linea.startswith("mazogrita:"):
        t = extraer(linea, "mazogrita:")
        msg = resolver_variables(t).upper()
        print(color(f"&n📢 ¡{msg}!&0"))

    elif linea.startswith("mazosusurra:"):
        t = extraer(linea, "mazosusurra:")
        msg = resolver_variables(t).lower()
        print(f"🤫 {msg}...")

    elif linea.startswith("mazocanta:"):
        t = extraer(linea, "mazocanta:")
        msg = resolver_variables(t)
        for c in msg:
            print(c, end=" ", flush=True)
            time.sleep(0.05)
        print()

    elif linea.startswith("mazopregunta:"):
        t = extraer(linea, "mazopregunta:")
        p = resolver_variables(t)
        respuestas = ["sí","no","quizás","pregunta de nuevo","el mazo dice no",
                      "la lanza dice sí","ya no gastes dinero en el mazo","definitivamente"]
        print(f"❓ {p}")
        print(f"🎱 El mazo responde: {random.choice(respuestas)}")

    elif linea == "mazocaracruz":
        print("🪙 ¡Cruz! (que el mazo no sirve)")

    elif linea == "mazocaracara":
        print("🪙 ¡Cara! (que la lanza sí)")

    elif linea.startswith("mazomoneda:"):
        print(f"🪙 {random.choice(['cara','cruz'])}")

    # ---------- CIERRE V5.5 ----------
    elif linea.startswith("mazodespedida:"):
        t = extraer(linea, "mazodespedida:")
        msg = resolver_variables(t) if t else "adiós"
        print(color(f"&a👋 {msg}. Recuerda: YA NO GASTES DINERO EN EL MAZO 🪓"))

    elif linea == "mazoadios":
        print(color("&a👋 Adiós mazo. Que la lanza te acompañe 🗡️"))

    # ============================================================
    # FIN COMANDOS NUEVOS v5.5
    # ============================================================

    # =========================
    # SISTEMA
    # =========================
    elif linea == "limpiamazo":
        os.system("cls" if os.name == "nt" else "clear")

    elif linea == "info":
        print("MAZOX SYSTEM v5.5 (mazónico)")
        print("Apps:", len(store), "| Variables:", len(variables),
              "| Listas:", len(listas), "| Diccionarios:", len(diccionarios))
        print("Funciones:", len(funciones), "| Clases:", len(clases_mazo),
              "| Instancias:", len(instancias_mazo))
        print("Sets:", len(sets_mazo), "| Stacks:", len(stacks_mazo),
              "| Colas:", len(queues_mazo))
        print("Módulos:", len(modulos_mazo), "| Estados:", len(estados_mazo),
              "| Eventos:", len(eventos_mazo))
        print("Grafos:", len(grafos_mazo), "| Árboles:", len(arboles_mazo),
              "| Cachés:", len(caches_mazo))
        print("Hilos:", len(hilos_mazo), "| Promesas:", len(promesas_mazo),
              "| Pipelines:", len(pipelines_mazo))
        print("Factories:", len(factories_mazo), "| Strategies:", len(strategies_mazo),
              "| Builders:", len(builders_mazo))
        print("Enums:", len(enums_mazo), "| DataClasses:", len(dataclasses_mazo),
              "| Lambdas:", len(lambdas_mazo))
        print("Bóveda:", len(boveda_mazo), "| Pociones:", len(pociones_mazo),
              "| Mobs:", len(mobs_mazo), "| Mazmorras:", len(mazmorras_mazo))
        print("Logros:", len(logros_mazo), "| Clanes:", len(clanes_mazo),
              "| Trades:", len(trades_mazo), "| Recetas:", len(recetas_mazo))
        print("Hechizos:", len(hechizos_mazo), "| Misiones:", len(misiones_mazo))
        print("YA NO GASTES DINERO EN EL MAZO 🪓")

    elif linea == "debug":
        print("STORE:", store)
        print("VARIABLES:", variables)
        print("LISTAS:", listas)
        print("DICCIONARIOS:", diccionarios)
        print("FUNCIONES:", funciones)
        print("ALIASES:", aliases)
        print("CLASES:", clases_mazo)
        print("INSTANCIAS:", instancias_mazo)
        print("GRAFOS:", grafos_mazo)
        print("ÁRBOLES:", arboles_mazo)
        print("CACHÉS:", caches_mazo)
        print("PIPELINES:", pipelines_mazo)
        print("HILOS:", {k: v.is_alive() for k, v in hilos_mazo.items()})
        print("BÓVEDA:", boveda_mazo)
        print("POCIONES:", pociones_mazo)
        print("MOBS:", mobs_mazo)
        print("MAZMORRAS:", mazmorras_mazo)
        print("LOGROS:", logros_mazo)
        print("CLANES:", clanes_mazo)
        print("TRADES:", trades_mazo)
        print("RECETAS:", recetas_mazo)
        print("HECHIZOS:", hechizos_mazo)

    elif linea == "historialmazo":
        for i, h in enumerate(historial[-30:]):
            print(f"  {i}: {h}")

    elif linea == "salirmazo":
        sys.exit(0)

    elif linea == "mazoresumen":
        print("\n📊 RESUMEN MAZO:")
        print(f"  Variables: {list(variables.keys())}")
        print(f"  Listas: {list(listas.keys())}")
        print(f"  Diccionarios: {list(diccionarios.keys())}")
        print(f"  Funciones: {list(funciones.keys())}")
        print(f"  Clases: {list(clases_mazo.keys())}")

    elif linea == "mazoguardatodo":
        try:
            estado = {
                "variables": variables,
                "listas": listas,
                "diccionarios": diccionarios,
                "funciones": funciones,
                "clases": clases_mazo,
                "instancias": instancias_mazo,
                "boveda": boveda_mazo,
                "pociones": pociones_mazo,
                "logros": list(logros_mazo),
                "clanes": clanes_mazo,
                "trades": trades_mazo,
                "recetas": recetas_mazo,
                "hechizos": hechizos_mazo,
                "misiones": misiones_mazo,
            }
            with open("mazo_estado.json", "w", encoding="utf-8") as f:
                json.dump(estado, f, ensure_ascii=False, indent=2)
            print("💾 Estado mazo guardado en mazo_estado.json")
        except Exception as e: print("ERROR:", e)

    elif linea.startswith("mazocargaestado:"):
        t = extraer(linea, "mazocargaestado:")
        try:
            with open(resolver_variables(t.strip()), "r", encoding="utf-8") as f:
                estado = json.load(f)
            variables.update(estado.get("variables", {}))
            listas.update(estado.get("listas", {}))
            diccionarios.update(estado.get("diccionarios", {}))
            funciones.update(estado.get("funciones", {}))
            clases_mazo.update(estado.get("clases", {}))
            instancias_mazo.update(estado.get("instancias", {}))
            boveda_mazo.update(estado.get("boveda", {}))
            pociones_mazo.update(estado.get("pociones", {}))
            logros_mazo.update(estado.get("logros", []))
            clanes_mazo.update(estado.get("clanes", {}))
            trades_mazo.update(estado.get("trades", {}))
            recetas_mazo.update(estado.get("recetas", {}))
            hechizos_mazo.update(estado.get("hechizos", {}))
            misiones_mazo.update(estado.get("misiones", {}))
            print("📂 Estado mazo cargado")
        except Exception as e: print("ERROR:", e)

    elif linea == "ayuda":
        print("""
╔══════════════════════════════════════════════════════════════╗
║       MAZOX HELP v5.5 — MAZÓNICO DEFINITIVO                 ║
║       YA NO GASTES DINERO EN EL MAZO 🪓                      ║
╚══════════════════════════════════════════════════════════════╝

🎴 v5.0 CLÁSICO (sigue funcionando igual)
  Variables: mazo, nomazo, cambiamazo, dinerazo, dinerazonumazo
  Matemáticas: dinero, menosmazo, masmazo, delmazo, raizmazo, modmazo, potenciamazo
  Stats: mazopromedio, mazomediana, mazomoda, mazodesviacion, mazogcd, mazolcm, mazofactorial
  Trig: mazoseno, mazocoseno, mazotangente, mazolog, mazopi, mazoe
  Azar: nogastes, tirael, mezclamazo, mazoelegir, mazomuestra
  Listas: mazolista, agregamazo, quitamazo, mazordena, mazofiltra, mazomapea, mazorango
  Diccionarios: mazodicc, mazodiccpon, mazodicctoma, mazodiccquita
  Sets: mazoset, mazosetpon, mazosetune, mazosetinterseca
  Stacks/Colas: mazostack, mazopush, mazopop, mazocola, mazoencola, mazodesencola
  Strings: mayusmazo, minusmazo, largomazo, juntamazo, reemplazamazo, mazosplit, mazotrim
  Regex: mazoregex, mazoregexreemplaza
  JSON: mazojson, mazojsonleer
  Crypto: mazohash, mazohashmd5, mazobase64, mazodesbase64, mazoaes, mazodesaes, mazofirma
  Flujo: si, sino, siza, mazoswitch, repmazo, mientrasmazo, paradineros, mazoporelmazo
  Funciones: mazofuncion, llamamazo, regresamazo
  Clases: mazoclase, mazoinstancia, mazoatributo, mazometodo
  Grafos: mazografo, mazografoarista, mazografobfs, mazografodfs, mazodijkstra
  Árboles: mazoarbol, mazoarbolinserta, mazoarbolinorden
  Concurrencia: mazohilo, mazoasync, mazoawait, mazopromesa
  Patrones: mazosingleton, mazofactory, mazostrategy, mazobuilder, mazodecorador
  Datos: mazosql, mazopickle, mazounpickle, mazozip, mazounzip, mazocsvlee, mazocsvescribe
  Red: mazohttp, mazohttppost, mazoscrap, mazocorreo
  Sistema: mazoejecuta, mazoruta, mazodir, mazoarchivolee, mazoarchivoescribe
  Tienda: mazoel, mazogastes, dineroel, guardarmazo, leermazo, sirvemazo

🪓 v5.5 NUEVOS MAZÓNICOS
  Humor del mazo:
    mazoburla:              Burla aleatoria del mazo (¡por la lanza!)
    mazolanzo:              La lanza ataca (¡el mazo queda inservible!)
    mazoconsejo:            Consejo mazónico aleatorio
    mazofrase:              Frase del mazo
    mazotragedia, mazocomedia, mazodrama
    mazopoema, mazorap, mazorima
    mazogrita, mazosusurra, mazocanta
    mazopregunta:           La bola mágica mazónica

  Bóveda y pociones:
    mazoboveda:             Ver bóveda mazónica
    mazoboveda:<n=valor>    Guardar en bóveda
    mazobovedatoma:<n>      Tomar de bóveda
    mazobovedaborra:<n>     Borrar de bóveda
    mazopocion:<n=efecto>   Crear poción
    mazotomapocion:<n>      Tomar poción
    mazopociones            Listar pociones

  Encantamientos:
    mazoencanta:<item,enc>  Encantar item
    mazoverencantamiento:<i> Ver encantamientos
    mazoencantamientos      Listar items encantados

  Mobs y mazmorras:
    mazomob:<n=tipo>        Crear mob
    mazoatacamob:<mob,daño> Atacar mob
    mazomobs                Listar mobs
    mazmazmorra:<n=dif>     Generar mazmorra
    mazoexplora:<n>         Explorar mazmorra
    mazmazmorras            Listar mazmorras
    mazomina:<n,cant>       Minar bloques
    mazoexploramundo:<lugar> Explorar mundo

  Logros:
    mazologro:<n>           Desbloquear logro
    mazologros              Ver logros
    mazologrosdef           Ver definiciones de logros
    mazosecreto:<n=pista>   Registrar logro secreto
    mazodesbloqueasecreto:<n> Desbloquear secreto

  Inventario, trades, recetas:
    mazoinv:<jug>           Crear inventario
    mazoinvpon:<j,i->c>     Añadir item
    mazoinvtoma:<j,i->c>    Quitar item
    mazoinvver:<jug>        Ver inventario
    mazotrade:<n=d->r>      Registrar trade
    mazotradehaz:<n,jug>    Hacer trade
    mazotrades              Listar trades
    mazoreceta:<n=ing->r>   Registrar receta
    mazocraftea:<n,jug>     Craftear
    mazorecetas             Listar recetas

  Hechizos:
    mazohechizo:<n=formula> Crear hechizo
    mazolanzahechizo:<n>    Lanzar hechizo
    mazohechizos            Listar hechizos

  Social:
    mazoclan:<n=jefe>       Fundar clan
    mazoclanune:<n,jug>     Unirse a clan
    mazoclanes              Listar clanes
    mazorankingpon:<j,p>    Poner en ranking
    mazoranking             Ver ranking
    mazotorneo:<n=jug1,jug2,..> Torneo
    mazotorneojuega:<n>     Jugar torneo
    mazotorneos             Listar torneos
    mazoapuesta:<n=monto->op> Apuesta
    mazoresuelveapuesta:<n,r> Resolver apuesta
    mazoapuestas            Listar apuestas
    mazocontrato:<n=q->r>   Contrato
    mazocumple:<n>          Cumplir contrato
    mazocontratos           Listar contratos
    mazomision:<n=obj>      Misión
    mazomisionavanza:<n,c>  Avanzar misión
    mazomisiones            Listar misiones

  Packs:
    mazopack:<n=item1|item2> Pack
    mazopackabre:<n>        Abrir pack
    mazopacks               Listar packs

  Chismes y rumores:
    mazochisme:<txt>        Chisme
    mazochismes             Ver chismes
    mazorumor:<txt>         Rumor
    mazorrumores            Ver rumores

  Presentaciones:
    mazopresenta:<a,b>      Presentar
    mazobeso                Beso mazónico

  Anti-gasto:
    yagastesdinero          Recordatorio de gasto
    nogastesdinero          ¡Bien! No gastes
    nogastesdineroenelmazo  ¡Excelente!

  Sistema extra:
    mazotodo                Estado total
    mazoritual              Ritual mazónico
    mazohuella              Huella del día
    mazocleanpociones, mazoclearmobs, mazoclearlogros
    mazolanzo, mazolanza, mazovslanza

  Estado:
    mazoguardatodo          Guardar todo
    mazocargaestado:<arch>  Cargar todo

📦 TIENDA Y SISTEMA (igual que v5.0)
  mazoel, mazogastes, dineroel, guardarmazo, leermazo, sirvemazo
  limpiamazo, historialmazo, aliasmazo, info, debug, ayuda, salirmazo

╚══════════════════════════════════════════════════════════════╝

💡 YA NO GASTES DINERO EN EL MAZO!! recuerda bien.

""")

    elif linea in aliases:
        ejecutar(aliases[linea])

    else:
        print("El mazo no reconoce el comando.")
        print("¿Escribiste bien? Prueba 'ayuda'.")


def main():
    print("\033[1;36m===================================================\033[0m")
    print("               █▀▄▀█ █▀█ ▀█ █▀█ ▄▄ ▀▄▀")
    print("               █ ▀ █ █▀█ █▄ █▄█    █ █")
    print("")
    print("      MAZOX LANGUAGE / OS EXPERIMENT v5.5")
    print("      YA NO GASTES DINERO EN EL MAZO 🪓")
    print("      (el mazo quedó inservible por la lanza)")
    print("")
    print("     'salirmazo' → salir | 'ayuda' → comandos")
    print("\033[1;36m===================================================\033[0m")

    while True:
        try:
            cmd = input("\033[1;35m>> \033[0m")
            if cmd.strip() == "salirmazo":
                break
            ejecutar(cmd)
        except KeyboardInterrupt:
            break
        except StopIteration:
            pass
        except Exception as e:
            print("error:", e)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
        if archivo.endswith(".mazoxpkg"):
            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    for linea in f:
                        ejecutar(linea)
            except FileNotFoundError:
                print("\033[31mArchivo no encontrado.\033[0m")
        else:
            print("\033[31mEl archivo debe ser .mazoxpkg\033[0m")
    else:
        main()
