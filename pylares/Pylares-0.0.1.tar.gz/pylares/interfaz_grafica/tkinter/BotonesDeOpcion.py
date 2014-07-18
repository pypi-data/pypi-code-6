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
import __main__

class BotonesDeOpcion(ControlConOpciones, ControlGenericoVariableEnlazada):

    def __init__(self, nombre, opciones=[], valor = "", etiqueta = ""):
        ControlConOpciones.__init__(self, nombre, opciones, valor, etiqueta)

    def _seleccionMultiple(self):
        return False

    def _actualizarOpciones(self):
        pass

    def _obtenerOpciones(self):
        pass

    def _crearControl(self, master):
        self._variable_enlazada = Tk.StringVar()
        self._variable_enlazada.set(self._valor)
        self._controles = []
        for opcion in self._opciones:
            control = Tk.Radiobutton(
                master=master,
                variable=self._variable_enlazada,
                text=opcion,
                value=opcion,
                justify=Tk.LEFT
            )
            self._controles.append(control)
            control.pack(anchor=Tk.W)

    def _enlazarEventos(self):
        funcion = "CambioEn_" + self._nombre
        try:
            f = getattr(__main__, funcion)
            for control in self._controles:
                control.config(command=self._disparadorEventoOpcional)
        except AttributeError:
            pass

    def _disparadorEventoOpcional(self):
        funcion = "CambioEn_" + self._nombre
        f = getattr(__main__, funcion)
        f()
