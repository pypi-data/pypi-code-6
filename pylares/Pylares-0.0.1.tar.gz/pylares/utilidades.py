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

def _ValidarParametro(variable, nombre, tipos):
    if not isinstance(variable, tipos):
        raise(ValueError("El parámetro '" + nombre + "' es de un tipo inválido"))


def py23_unicode(var):
    if sys.version_info < (3,0,0):
        return unicode(var)
    else:
        return str(var)


def py23_iteritems(diccionario):
    try:
        return diccionario.iteritems()
    except:
        return diccionario.items()
