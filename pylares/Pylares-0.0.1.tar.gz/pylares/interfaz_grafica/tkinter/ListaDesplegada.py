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


class ListaDesplegada(ControlConOpciones):

    def __init__(self, nombre, opciones=[], valor = "", etiqueta = ""):
        ControlConOpciones.__init__(self, nombre, opciones, valor, etiqueta)

        self.eventos = {
            "<<ListboxSelect>>": "CambioEn_",
        }

    def _incluirDesplazamientoVertical(self):
        return True

    def _actualizarOpciones(self):
        self._control.delete(0, Tk.END)
        for opcion in self._opciones:
            self._control.insert(Tk.END, opcion)

    def _obtenerOpciones(self):
        return self._control.get(0, Tk.END)

    def _crearControl(self, master):
        self._control = Tk.Listbox(
            master=master,
            selectmode=Tk.EXTENDED,
            bd=0, # Se usa el borde de las barras de desplazamiento
        )
        self._actualizarOpciones()

    def _luegoDeCrearControl(self, master):
        self._control.pack(fill=Tk.BOTH, expand=1)


    @property
    def valor(self):
        if self._controlListo():
            seleccionados = self._control.curselection()
            valores = []
            for s in seleccionados:
                valores.append(self._opciones[s])
            self._valor = valores
        return self._valor

    @valor.setter
    def valor(self, value):
        valores = []
        if self._controlListo():
            self._control.selection_clear(0, len(self._opciones))
        for v in value:
            if v in self._opciones:
                valores.append(v)
                if self._control is not None:
                    indice = self._opciones.index(v)
                    self._control.selection_set(indice)
        self._valor = valores
