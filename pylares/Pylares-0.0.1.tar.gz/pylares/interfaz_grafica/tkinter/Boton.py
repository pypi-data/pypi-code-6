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

from .ControlGenerico import ControlGenericoVariableEnlazada


class Boton(ControlGenericoVariableEnlazada):

    def __init__(self, nombre, valor=""):
        ControlGenericoVariableEnlazada.__init__(self, nombre, valor)

        self._eventos = {
            "<Button-1>": "ClicEn_",
            "<Enter>": "MouseIn_",
            "<Leave>": "MouseOut_"
        }

    def _eventoObligatorio(self, evento):
        if evento == "<Button-1>":
            return True

    def _puedeEtiquetarse(self):
        return False

    def _crearControl(self, master):
        self._control = Ttk.Button(
            master=master,
            textvariable=self._variable_enlazada #Creada por la clase padre.
        )
        self._control.pack(fill=Tk.BOTH, expand=1, padx=10, pady=10)
