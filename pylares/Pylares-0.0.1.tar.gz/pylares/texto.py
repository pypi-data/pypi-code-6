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
from pylares import utilidades


def Longitud(frase):
    return len(frase)


def Mayuscula(frase):
    return frase.upper()


def Minuscula(frase):
    return frase.lower()


def EmpiezaCon(frase, empieza_con):
    frase = utilidades.py23_unicode(frase)
    empieza_con = utilidades.py23_unicode(empieza_con)
    return frase.startswith(empieza_con)


def TerminaCon(frase, termina_con):
    frase = utilidades.py23_unicode(frase)
    termina_con = utilidades.py23_unicode(termina_con)
    return frase.endswith(termina_con)


def Separar(frase, separador):
    frase = utilidades.py23_unicode(frase)
    return frase.split(separador)


def Unir(lista, separador):
    return separador.join(lista)


def Contiene(frase, palabra):
    return palabra in frase


def Reemplazar(frase, buscar, reemplazar, cantidad=None):
    if cantidad is not None:
        return frase.replace(buscar, reemplazar, cantidad)
    else:
        return frase.replace(buscar, reemplazar)
