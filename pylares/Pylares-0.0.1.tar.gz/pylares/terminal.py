# -*- coding: utf-8 -*-
"""
Copyright 2014 Mariano D'Agostino

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import os
from pylares.contrib import getch
from pylares import utilidades

try:
    from ctypes import windll
    from pylares.contrib import terminal_w
    plataforma = "windows"
except ImportError:
    plataforma = "linux"

colores_linux = {
    "negro": "1;30",
    "rojo": "1;31",
    "verde": "1;32",
    "amarillo": "1;33",
    "azul": "1;34",
    "violeta": "1;35",
    "celeste": "1;36",
    "blanco": "1;37"
}

colores_windows = {
    "negro": 0x0000,
    "azul": 0x0001,
    "verde": 0x0002,
    "celeste": 0x0003,
    "rojo": 0x0004,
    "violeta": 0x0005,
    "amarillo": 0x0006,
    "blanco": 0x000F,
}


def py23_print(*args, **kargs):
    separador = kargs.pop('separador', u' ')
    fin = kargs.pop('fin', '\n')
    color = kargs.pop('color', None)
    salida_estandar = kargs.pop('salida', sys.stdout)
    if kargs:
        raise TypeError(u'Parámetros no soportados: %s' % kargs)

    salida = None
    for arg in args:
        if salida is None:
            salida = utilidades.py23_unicode(arg)
        else:
            salida += separador + utilidades.py23_unicode(arg)

    info = _PreprocesarSalida(salida, color, salida_estandar)
    salida_estandar.write(info["salida"])
    _PostprocesarSalida(info)
    salida_estandar.write(fin)

    # Para que se muestren los valores cuando se combina con temporizadores
    if salida_estandar == sys.stdout:
        salida_estandar.flush()


def _PreprocesarSalida(salida, color, salida_estandar):
    if color is not None:
        if plataforma == "linux":
            info = {"salida": "\033[" + colores_linux[color] + "m" + salida + "\033[0;0m"}
            return info
        elif plataforma == "windows":
            color_anterior = terminal_w.get_text_attr()
            terminal_w.set_text_attr(colores_windows[color])
            return {"salida": salida, "color_anterior": color_anterior}

    info = {"salida": salida}
    return info


def _PostprocesarSalida(info):
    if plataforma == "windows" and "color_anterior" in info.keys():
        terminal_w.set_text_attr(info["color_anterior"])


def MostrarVarios(*valores, **kargs):
    salida = kargs.pop('salida', sys.stdout)
    py23_print(*valores, **kargs)


def Mostrar(valor=None, color=None):

    if valor is False:
        valor = u"Falso"
    elif valor is True:
        valor = u"Verdadero"
    elif valor is None:
        py23_print("")
        return

    py23_print(valor, color=color)


def MostrarEnLinea(valor=None, color=None):

    if valor is False:
        valor = u"Falso"
    elif valor is True:
        valor = u"Verdadero"
    elif valor is None:
        py23_print("", fin="")
        return

    py23_print(valor, color=color, fin="")


def LineaEnBlanco(cantidad = 1):
    for i in range(cantidad):
        Mostrar()


def Leer(mensaje = None):
    if mensaje is not None:
        MostrarEnLinea(mensaje)

    if sys.version_info < (3,0,0):
        valor = utilidades.py23_unicode(raw_input())
    else:
        valor = input()

    if valor.find('.') == -1:
        try:
            numero = int(valor)
            return numero
        except:
            if sys.version_info < (3,0,0):
                return utilidades.py23_unicode(valor)
            else:
                return valor
    else:
        try:
            numero = float(valor)
            return numero
        except ValueError:
            if sys.version_info < (3,0,0):
                return utilidades.py23_unicode(valor)
            else:
                return valor



def LimpiarPantalla():
    """
    Limpia la pantalla. Esto implica quitar todo el texto
    de la terminal.

    Sintáxis: LimpiarPantalla()

    Ejemplos:
    LimpiarPantalla()
    """
    if os.name == 'posix':
        os.system("clear")
    else:
        os.system("cls")


def Esperar(segundos):
    import time
    time.sleep(segundos)


def Pausa(mensaje = None):
    if mensaje is None:
        Mostrar("Presione una tecla para continuar...")
    else:
        Mostrar(mensaje)

    getch._Getch()()


def FinDelPrograma():
    Pausa("Presione una tecla para salir...")
    exit()
