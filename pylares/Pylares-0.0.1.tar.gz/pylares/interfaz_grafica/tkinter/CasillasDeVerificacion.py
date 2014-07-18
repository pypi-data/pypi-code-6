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

class CasillasDeVerificacion(ControlConOpciones):

    def __init__(self, nombre, opciones=[], valor = "", etiqueta = ""):
        ControlConOpciones.__init__(self, nombre, opciones, valor, etiqueta)
        self._controles = None

    def _seleccionMultiple(self):
        return False

    def _actualizarOpciones(self):
        for control in self._controles:
            control.destroy()
        for variable in self._variable_enlazada:
            del(variable)

        del(self._controles)
        self._controles = None
        self._crearControl(self._master)
        self._enlazarEventos()

    def _controlListo(self):
        return self._controles is not None

    def _obtenerOpciones(self):
        pass

    def _crearControl(self, master):
        self._variable_enlazada = []
        self._controles = []
        self._master = master
        for opcion in self._opciones:
            variable_enlazada = Tk.IntVar()
            self._variable_enlazada.append(variable_enlazada)
            control = Tk.Checkbutton(
                master=master,
                variable=variable_enlazada,
                text=opcion,
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



    @property
    def valor(self):
        valores = []
        x = 0
        if self._controlListo():
            for control in self._controles:
                if self._variable_enlazada[x].get():
                    valores.append(control.cget("text"))
                x = x + 1

            self._valor = valores
        return self._valor

    @valor.setter
    def valor(self, value):
        valores = []
        # Deseleccionar todas las cajas de verificación
        if self._controlListo():
            for control in self._controles:
                control.deselect()

        # Habilitar solo las casillas para los valores dados que estén definidos
        # entre las opciones válidas del control
        for v in value:
            if v in self._opciones:
                valores.append(v)
                for control in self._controles:
                    if control.cget("text") == v:
                        control.select()

        self._valor = valores
