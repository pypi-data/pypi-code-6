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

import __main__

class Ventana():

    def __init__(self, *controles):
        self.ventana = Tk.Tk()
        self._controles = controles
        self._items = {}

    def _orientacion(self):
        return "ventana madre"

    def Dibujar(self):
        for i in self._controles:
            if i._contenedorDeControles():
                i._referenciaVentanaPadre(self)
            else:
                self._items[i._nombre] = i
            i._dibujar(self.ventana, self._orientacion())
            i._enlazarEventos()

        style = Ttk.Style()
        style.theme_use('clam')

        try:
            f = getattr(__main__, 'Inicio_Programa')
            f()
        except AttributeError:
            pass

        self.ventana.title("Pylares")
        self.ventana.mainloop()

    def Titulo(self, titulo):
        """ Define el titulo de la ventana. """
        self.ventana.title(titulo)

    def Dimensiones(self, anchura, altura):
        """ Define las dimensiones de la ventana. """
        dimensiones = "%dx%d" % (anchura, altura)
        self.ventana.geometry(dimensiones)

    def Posicion(self, x, y):
        """ Define la posición de la ventana. """
        posicion = "+%d+%d" % (x, y)
        self.ventana.geometry(posicion)

    def __setitem__(self, nombre, control):
        """ Modifica el control de la vantana con el nombre dado. """
        self._items[nombre] = control

    def __getitem__(self, nombre):
        """ Obtiene el control de la vantana con el nombre dado.
        Usando la notación de listas: ventana[nombre]
        """
        return self._items[nombre]


