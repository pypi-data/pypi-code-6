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

from pylares import *

class TestListas:


    def test_MostrarVarios(self, capsys):
        MostrarVarios(u"Hola buen día.", u"Bienvenido")
        salida, err = capsys.readouterr()
        assert salida == u"Hola buen día. Bienvenido\n"

        MostrarVarios(u"Usted tiene", 40, u"años")
        salida, err = capsys.readouterr()
        assert salida == u"Usted tiene 40 años\n"

        MostrarVarios(u"Usted tiene", 40, u"años", separador='|')
        salida, err = capsys.readouterr()
        assert salida == u"Usted tiene|40|años\n"

        MostrarVarios(u"Usted tiene", 40, u"años", separador='|', fin='')
        salida, err = capsys.readouterr()
        assert salida == u"Usted tiene|40|años"


    def test_Mostrar(self, capsys):
        Mostrar(u"Hola")
        salida, err = capsys.readouterr()
        assert salida == u"Hola\n"

        Mostrar(False)
        salida, err = capsys.readouterr()
        assert salida == u"Falso\n"

        Mostrar(True)
        salida, err = capsys.readouterr()
        assert salida == u"Verdadero\n"

        Mostrar(None)
        salida, err = capsys.readouterr()
        assert salida == u"\n"

        Mostrar(120)
        salida, err = capsys.readouterr()
        assert salida == u"120\n"

        Mostrar(123.456)
        salida, err = capsys.readouterr()
        assert salida == u"123.456\n"

        Mostrar(u"Hola", color=u"rojo")
        salida, err = capsys.readouterr()
        # La consola de pytest no muestra estos valores: \x1b[1;31m
        assert salida == u"\x1b[1;31mHola\x1b[0;0m\n"
        # Por lo tanto nos aseguramos de que se cumpla la siguiente negación
        assert salida != u"\x1b[1;32mHola\x1b[0;0m\n"


    def test_MostrarEnLinea(self, capsys):
        MostrarEnLinea(u"Hola")
        salida, err = capsys.readouterr()
        assert salida == u"Hola"

        MostrarEnLinea(False)
        salida, err = capsys.readouterr()
        assert salida == u"Falso"

        MostrarEnLinea(True)
        salida, err = capsys.readouterr()
        assert salida == u"Verdadero"

        MostrarEnLinea(None)
        salida, err = capsys.readouterr()
        assert salida == u""

        MostrarEnLinea(120)
        salida, err = capsys.readouterr()
        assert salida == u"120"

        MostrarEnLinea(123.456)
        salida, err = capsys.readouterr()
        assert salida == u"123.456"

        MostrarEnLinea(u"Hola", color=u"rojo")
        salida, err = capsys.readouterr()
        # La consola de pytest no muestra estos valores: \x1b[1;31m
        assert salida == u"\x1b[1;31mHola\x1b[0;0m"
        # Por lo tanto nos aseguramos de que se cumpla la siguiente negación
        assert salida != u"\x1b[1;32mHola\x1b[0;0m"


    def test_LineaEnBlanco(self, capsys):
        LineaEnBlanco(4)
        salida, err = capsys.readouterr()
        assert salida == u"\n\n\n\n"
        assert salida != u"\n\n\n\n\n\n\n\n\n"

