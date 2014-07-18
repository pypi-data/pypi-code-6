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

class Temporizador(object):


    def __init__(self, nombre, periodo=1.0, ejecuciones=None):
        # El nombre que identifica al control.
        self._nombre = nombre

        # Cada cuantos segundos se ejecuta el evento del temporizador
        self._periodo = periodo

        # Contador para almacenar cuantas veces se ejecutó el evento del temporizador
        self._ciclos_completados = 0

        # Cantidad de ciclos a ejecutar antes de detener el temporizador
        self._ejecuciones = ejecuciones

        # Referencia al control que manejará el temporizador
        self._temporizador = None

        # Si value True, el evento no se ejecutará y se detendrá el temporizador
        self._pausado = False

    def VueltasCompletadas(self):
        return self._ciclos_completados

    def VueltasTotales(self):
        return self._ejecuciones

    def _enlazarEventos(self):
        pass

    def _dibujar(self, ventana):
        self._temporizador = Tk.Label(text="")

    def Iniciar(self):
        """ Inicia el temporizador """
        self._pausado = False
        self._temporizador.after(int(self._periodo * 1000), self._evento)

    def Reiniciar(self):
        """ Reinicia el temporizador """
        self._pausado = False
        self.Iniciar()

    def Pausar(self):
        """ Detiene el temporizador """
        self._pausado = True

    def _evento(self):
        if self._pausado:
            return
        funcion = "CicloDe_" + self._nombre
        try:
            f = getattr(__main__, funcion)
            f()

            self._ciclos_completados += 1
            if self._ejecuciones is not None:
                if self._ejecuciones > self._ciclos_completados:
                    self._temporizador.after(int(self._periodo * 1000), self._evento)
            else:
                self._temporizador.after(int(self._periodo * 1000), self._evento)

        except AttributeError:
            raise AttributeError("Falta definir CicloDe_" + self._nombre)

