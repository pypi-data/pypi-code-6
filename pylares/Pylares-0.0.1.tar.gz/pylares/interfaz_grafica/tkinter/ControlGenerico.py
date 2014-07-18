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

from __future__ import print_function

try:
    import ttk as Ttk
    import Tkinter as Tk
except ImportError:
    from tkinter import ttk as Ttk
    import tkinter as Tk

import __main__

TK_EVENTOS = (
 (2, "<KeyPress>"),
 (3, "<KeyRelease>"),
 (4, "<Button>"),
 (4, "<Button-1>"),
 (5, "<ButtonRelease>"),
 (6, "<Motion>"),
 (7, "<Enter>"),
 (8, "<Leave>"),
 (9, "<FocusIn>"),
(10, "<FocusOut>"),
(12, "<Expose>"),
(15, "<Visibility>"),
(17, "<Destroy>"),
(18, "<Unmap>"),
(19, "<Map>"),
(22, "<Configure>"),
(35, "<<ListboxSelect>>"),
(35, "<<ComboboxSelected>>"),
(36, "<Activate>"),
(37, "<Deactivate>"),
(38, "<MouseWheel>")
)


class ControlGenerico(object):

    def __init__(self, nombre, valor="", etiqueta=""):
        # El nombre que identifica al control.
        self._nombre = nombre

        # El valor (o valores) que contiene el control actualmente.
        self._valor = valor

        # El valor de la etiqueta del control.
        self._etiqueta = etiqueta

        # La referencia a la ventana donde se encuentra el control.
        self._ventana = None

        # La referencia al control manejado por la instancia.
        self._control = None

        # La referencia al marco exterior que es usado para mostrar la etiqueta.
        self._marco_etiqueta = None

        # La referencia al marco interior (si es que existe) que es usado
        # para dibujar las barras de desplazamiento.
        self._marco_desplazamiento = None

        # Un diccionario indexado por nombre de evento y prefijo
        # que el control puede manejar.
        self._eventos = {
            # "<Button>": "ClicEn_"
        }

    def _controlListo(self):
        """ Devuelve True si Tkinter ya dibujo el control """
        return self._control is not None

    def _controlExterno(self):
        """ Devuelve el control que representa mejor la geometría de todo
            el conjunto (control y contenedores opcionales).
        """
        if self._marco_etiqueta is not None:
            return self._marco_etiqueta
        elif self._marco_desplazamiento is not None:
            return self._marco_desplazamiento
        else:
            return self._control

    def _puedeEtiquetarse(self):
        """ Determina si el control puede utilizar etiquetas. """
        return True

    def _incluirDesplazamientoVertical(self):
        """ Determina si debe incluirse la barra de desplazamiento vertical
            como parte del control """
        return False

    def _incluirDesplazamientoHorizontal(self):
        """ Determina si debe incluirse la barra de desplazamiento horizontal
            como parte del control """
        return False

    def _eventoObligatorio(self, evento):
        """ Algunos controles, como el Boton, necesitan que se implementen
            ciertos eventos para que su inclusión sea justificada.

            Esta función devuelve True en caso de que el evento indicado
            sea considerado obligatorio para el control.
        """
        return False

    def _iterarEventos(self):
        try:
            return self._eventos.iteritems()
        except:
            return self._eventos.items()

    def _enlazarEventos(self):
        """ Genera los bind necesarios para que los eventos definidos. """
        for evento, prefijo in self._iterarEventos():
            if self._eventoObligatorio(evento):
                self._control.bind(evento, self._disparadorEventoObligatorio)
            else:
                # Antes de enlazar el evento, determinar si la función que se
                # encargará de procesarlo fue definida en el programa principal.
                # En caso de no encontrarse esta función, no se enlaza el evento
                # y de esta forma se convierte en un evento opcional.
                funcion = prefijo + self._nombre
                try:
                    f = getattr(__main__, funcion)
                    self._control.bind(evento, self._disparadorEventoOpcional)
                except AttributeError:
                    # No se encontró la función que procesa el evento,
                    # no hacer nada.
                    pass


    def _disparadorEventoObligatorio(self, evento):
        # Ver definición de TK_EVENTOS al principio de este archivo.
        for i in TK_EVENTOS:
            # Como no sabemos que evento estamos procesando, se hace un mapeo
            # del nombre del evento en base a su código numérico, y se controla
            # si es o no obligatorio.
            if int(evento.type) == i[0] and self._eventoObligatorio(i[1]):
                funcion = self._eventos[i[1]] + self._nombre
                try:
                    f = getattr(__main__, funcion)
                    f()
                except AttributeError as e:
                    # En el caso de no encontrar la función definida para el
                    # evento obligatorio, disparamos una exepción explicando
                    # que código es necesario para que el evento funcione.

                    # como la exepción AttributeError puede dispararse por un
                    # error de código, se debe controlar que el error surja
                    # por no haber definido la función que controla el evento.
                    if funcion in e.args[0]:
                        print("Falta definir " + funcion + "()")
                    else:
                        raise AttributeError(e)

                break

    def _disparadorEventoOpcional(self, evento):
        # Ver definición de TK_EVENTOS al principio de este archivo.
        for i in TK_EVENTOS:
            # Como no sabemos que evento estamos procesando, se hace un mapeo
            # del nombre del evento en base a su código numérico, y se controla
            # si es o no obligatorio.
            if int(evento.type) == i[0] and not self._eventoObligatorio(i[1]):
                if i[1] in self._eventos.keys():
                    funcion = self._eventos[i[1]] + self._nombre
                    try:
                        f = getattr(__main__, funcion)
                        f()
                    except AttributeError:
                        pass

                    break

    def _contenedorDeControles(self):
        return False

    def _dibujar(self, master, orientacion):
        """ Función principal que se encarga de dibujar los marcos y llamar
            a la función que genera el control (implementado en una clase base)
        """

        self._ventana = master
        if self._puedeEtiquetarse():
            # Si el control puede etiquetarse, generar un marco, incluso si el
            # control no tiene una etiqueta definida. Esto hace más simple la
            # inclusión de etiquetas de forma dinámica durante la ejecución
            # del programa.
            self._marco_etiqueta = Tk.LabelFrame(
                master=master,
                text=self._etiqueta,
                borderwidth=0
            )
            master = self._marco_etiqueta
            self._marco_etiqueta.pack(fill=Tk.BOTH, expand=1, padx=10, pady=10)

        if self._incluirDesplazamientoHorizontal() or self._incluirDesplazamientoVertical():
            self._marco_desplazamiento = Tk.Frame(
                master=master,
                # Usar un borde de 1 pixel para que el control tenga mejor
                # apariencia.
                borderwidth=1,
                relief=Tk.SUNKEN
            )
            master = self._marco_desplazamiento

        # Una vez creados los marcos opcionales, se delega la creación del
        # control a la clase hija.
        self._antesDeCrearControl(master)
        self._crearControl(master)
        self._crearDesplazamientos(master)
        self._luegoDeCrearControl(master)


    def _crearDesplazamientos(self, master):
        barras_incluidas = False
        if self._incluirDesplazamientoVertical():
            self._controlvscrol = Ttk.Scrollbar(
                master=master,
                orient=Tk.VERTICAL,
                command=self._control.yview
            )
            self._controlvscrol.pack(side=Tk.RIGHT, fill=Tk.Y)
            barras_incluidas = True

        if self._incluirDesplazamientoHorizontal():
            self._controlhscroll = Ttk.Scrollbar(
                master=master,
                orient=Tk.HORIZONTAL,
                command=self._control.xview
            )
            self.hscroll.pack(side=Tk.BOTTOM, fill=Tk.X)
            barras_incluidas = True

        if barras_incluidas:
            self._marco_desplazamiento.pack(fill=Tk.BOTH, expand=1)



    def _antesDeCrearControl(self, master):
        """ Operaciones opcionales que las clases hijas pueden ejecutar antes
            de que el control sea creado.
        """
        pass

    def _crearControl(self, master, ventana):
        """ Las clases hijas deben crear aqui el widget y guardar la
            referencia en self._control
        """
        raise NotImplementedError

    def _luegoDeCrearControl(self, master):
        """ Operaciones opcionales que las clases hijas pueden ejecutar luego
            de que el control sea creado.
        """
        pass


    # -------------------- Propiedades del control  ------------------------

    @property
    def x(self):
        """ Coordenada x del control """
        if self._controlListo():
            control = self._getControlExterno()
            coordenadas = control.place_info()
            self._x = int(coordenadas['x'])

        return self._x

    @x.setter
    def x(self, value):
        """ Modifica la coordena x del control (mueve el control) """
        self._x = value
        if self._controlListo():
            self._control.place(x=x)

    @property
    def y(self):
        """ Coordenada y del control """
        if self._controlListo():
            control = self._controlExterno()
            coordenadas = control.place_info()
            self._y = int(coordenadas['y'])

        return self._y

    @y.setter
    def y(self, value):
        """ Modifica la coordena y del control (mueve el control) """
        self._y = value
        if self._controlListo():
            control = self._controlExterno()
            control.place(y=y)

    @property
    def ancho(self):
        """ Devuelve el ancho del control """
        if self._controlListo():
            control = self._controlExterno()
            coordenadas = control.place_info()
            self._ancho = int(coordenadas['width'])

        return self._ancho

    @ancho.setter
    def ancho(self, value):
        """ Modifica el ancho del control """
        self._ancho = value
        if self._controlListo():
            control = self._controlExterno()
            control.place(width=ancho)

    @property
    def alto(self):
        """ Devuelve la altura del control """
        if self._controlListo():
            control = self._controlExterno()
            coordenadas = control.place_info()
            self._alto = int(coordenadas['height'])

        return self._alto

    @alto.setter
    def alto(self, value):
        """ Modifica la altura del control """
        self._alto = value
        if self._controlListo():
            control = self._controlExterno()
            control.place(height=alto)

    @property
    def habilitado(self):
        """ Determina si el control está o no habilitado. """
        if self._controlListo():
            self._habilitado = self._control.cget("state")

        return self._habilitado

    @habilitado.setter
    def habilitado(self, value):
        """ True: Habilita, False: deshabilita el control """
        self._habilitado = value
        if self._controlListo():
            if value is True:
                self._control.config(state=Tk.NORMAL)
            else:
                self._control.config(state=Tk.DISABLED)




    def Dimensiones(self, ancho, alto):
        self._ancho = ancho
        self._alto = alto
        if self._controlListo():
            control = self._controlExterno()
            control.place(width=ancho, height=alto)

    def Posicion(self, x, y):
        """ Define la posición del control. """
        self._x = x
        self._y = y
        if self._controlListo():
            control = self._controlExterno()
            control.place(x=x, y=y)



    @property
    def etiqueta(self):
        if not self._puedeEtiquetarse():
            raise NotImplementedError("El control %s no permite etiquetas" % (self._nombre))

        if self._controlListo():
            self._etiqueta = self._marco_etiqueta.cget("text")

        return self._etiqueta

    @etiqueta.setter
    def etiqueta(self, value):
        if not self._puedeEtiquetarse():
            raise NotImplementedError("El control %s no permite etiquetas" % (self._nombre))

        self._etiqueta = value
        if self._controlListo():
            self._marco_etiqueta.config(text=self._etiqueta)

    # ---------- Propiedades que deben implementar las clases hija ------------

    @property
    def valor(self):
        raise NotImplementedError

    @valor.setter
    def valor(self, value):
        raise NotImplementedError


class ControlGenericoVariableEnlazada(ControlGenerico):

    def _antesDeCrearControl(self, master):
        self._variable_enlazada = Tk.StringVar()
        self._variable_enlazada.set(self._valor)

    @property
    def valor(self):
        self._valor = self._variable_enlazada.get()
        return self._valor

    @valor.setter
    def valor(self, value):
        self._valor = value
        self._variable_enlazada.set(self._valor)


class ControlConOpciones(ControlGenerico):

    def __init__(self, nombre, opciones=[], valor = "", etiqueta = ""):
        if self._seleccionMultiple() and valor == "":
            valor = []

        ControlGenerico.__init__(self, nombre, valor, etiqueta)

        self._opciones = opciones

    def _seleccionMultiple(self):
        """ Devuelve True si el control puede aceptar multiples valores al
            al mismo tiempo. False en caso de que solo pueda seleccinarse un
            único valor por vez.
        """
        return True

    def _actualizarOpciones(self):
        """ Las clases hijas deben implementar este método para actualizar las
            opciones del control en base a los valores de self._opciones.
        """
        raise NotImplementedError

    def _obtenerOpciones(self):
        """ Las clases hijas deben implementar este método para obtener las
            opciones del control.
        """
        raise NotImplementedError

    @property
    def opciones(self):
        if self._controlListo():
            self._opciones = self._obtenerOpciones()
        return self._opciones

    @opciones.setter
    def opciones(self, value):
        self._opciones = value
        if self._controlListo():
            self._actualizarOpciones()

