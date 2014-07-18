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

from .ControlGenerico import ControlGenerico


class EntradaMultilinea(ControlGenerico):

    def __init__(self, nombre, valor="", etiqueta=""):
        ControlGenerico.__init__(self, nombre, valor, etiqueta)

        self._eventos = {
            "<KeyRelease>": "CambioEn_",
        }

    def _incluirDesplazamientoVertical(self):
        return True

    def _crearControl(self, master):
        self._control = Tk.Text(
            master=master
        )

    def _luegoDeCrearControl(self, master):
        self._control.pack(fill=Tk.BOTH, expand=1)

    @property
    def valor(self):
        if self._controlListo():
            self._valor = self._control.get("1.0")
        return self._valor

    @valor.setter
    def valor(self, value):
        self._valor = value
        if self._controlListo():
            self._control.delete("1.0", Tk.END)
            self._control.insert("1.0", self._valor)
