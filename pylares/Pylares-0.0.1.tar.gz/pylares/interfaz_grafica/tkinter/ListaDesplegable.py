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

try:
    import ttk as Ttk
    import Tkinter as Tk
except ImportError:
    from tkinter import ttk as Ttk
    import tkinter as Tk

from .ControlGenerico import ControlConOpciones
from .ControlGenerico import ControlGenericoVariableEnlazada

class ListaDesplegable(ControlConOpciones, ControlGenericoVariableEnlazada):

    def __init__(self, nombre, opciones=[], valor = "", etiqueta = ""):
        ControlConOpciones.__init__(self, nombre, opciones, valor, etiqueta)

        self.eventos = {
            "<<ComboboxSelected>>": "CambioEn_",
        }

    def _seleccionMultiple(self):
        return False

    def _actualizarOpciones(self):
        self._control["values"] = self._opciones

    def _obtenerOpciones(self):
        return self._control["values"]

    def _crearControl(self, master):
        self._control = Ttk.Combobox(
            master=master,
            textvariable=self._variable_enlazada,
            values=self._opciones
        )
        self._control.pack(fill=Tk.X, expand=1)
        # No expandir verticalmente el marco de la etiqueta para evitar
        # separaciones excesivas al redimensionar la ventana.
        self._marco_etiqueta.pack_configure(fill=Tk.X)

