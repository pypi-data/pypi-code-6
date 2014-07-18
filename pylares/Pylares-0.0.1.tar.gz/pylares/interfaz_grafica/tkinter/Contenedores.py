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


class Columna(ControlGenerico):

    def __init__(self, *controles):
        self._controles = controles
        self.ventana = None
        self._items = {}

    def _contenedorDeControles(self):
        return True

    def _orientacion(self):
        return "vertical"

    def _referenciaVentanaPadre(self, ventana):
        self.ventana = ventana

    def _dibujar(self, master, orientacion):
        self._contenedor = Tk.Frame(
            master=master,
        )
        for i in self._controles:
            if i._contenedorDeControles():
                i._referenciaVentanaPadre(self.ventana)
            else:
                self.ventana._items[i._nombre] = i
                self._items[i._nombre] = i

            i._dibujar(self._contenedor, self._orientacion())
            i._enlazarEventos()

        self._contenedor.pack(expand=1)
        if orientacion == "ventana madre":
            self._contenedor.pack_configure(pady=10, padx=10)
        elif orientacion == "vertical":
            self._contenedor.pack_configure(pady=10)
        else:
            self._contenedor.pack_configure(padx=10)

        if orientacion == "horizontal":
            self._contenedor.pack_configure(fill=Tk.NONE, side=Tk.LEFT)
        else:
            self._contenedor.pack_configure(fill=Tk.BOTH, expand=1)

    def _enlazarEventos(self):
        pass

class Fila(Columna):

    def _orientacion(self):
        return "horizontal"

    def _dibujar(self, master, orientacion):
        Columna._dibujar(self, master, orientacion)
        for i, item in self._iteritems():
            control = item._controlExterno()
            control.pack_configure(pady=0)
            control.pack_configure(side=Tk.LEFT)

    def _iteritems(self):
        try:
            return self._items.iteritems()
        except:
            return self._items.items()

