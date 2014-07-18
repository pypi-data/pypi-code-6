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

from pylares import utilidades

def AgregarEn(lista, valor):
    lista.append(valor)


def ExtenderLista(lista, extension):
    if isinstance(extension, list):
        lista.extend(extension)
    else:
        lista.append(extension)


def Mezclar(lista):
    import random
    random.shuffle(lista)


def BorrarDe(lista, indice):
    if ListaVacia(lista) == False:
        if indice >= 0 and indice < CantidadDeElementos(lista):
            del lista[indice]


def ElegirUnaDe(lista):
    import random
    return lista[random.randrange(0, len(lista) - 1)]


def TomarUltimoDe(lista):
    if isinstance(lista, list) and ListaVacia(lista) == False:
        return lista.pop()


def ListaVacia(lista):
    if len(lista) == 0:
        return True
    else:
        return False


def EstaEn(lista, valor):
    for v in lista:
        if v == valor:
            return True
    return False


def CantidadDeElementos(lista):
    return len(lista)


def ClaveValor(elementos):
    if isinstance(elementos, (list, str)):
        return enumerate(elementos)
    else:
        import sys
        if sys.version_info < (3, 0, 0) and isinstance(elementos, (unicode)):
            return enumerate(elementos)
        else:
            return utilidades.py23_iteritems(elementos)

