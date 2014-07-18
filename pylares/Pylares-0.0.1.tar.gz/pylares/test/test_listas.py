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
import pytest


class TestListas:


    def test_AgregarEn(self):
        lista = []
        AgregarEn(lista, 4)
        assert lista == [4]
        AgregarEn(lista, 5)
        assert lista == [4, 5]
        AgregarEn(lista, 6)
        assert lista == [4, 5, 6]

        meses = ["Enero"]
        AgregarEn(meses, "Febrero")
        AgregarEn(lista, ["Enero", "Febrero"])

        compuesto = [1, 2]
        AgregarEn(compuesto, [3, 4])
        assert compuesto == [1, 2, [3, 4]]


    def test_ExtenderLista(self):
        meses = ["Enero", "Febrero", "Marzo"]
        ExtenderLista(meses, ["Abril", "Mayo", "Junio"])
        assert meses == ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"]

        lista = []
        ExtenderLista(lista, 4)
        assert lista == [4]
        ExtenderLista(lista, 5)
        assert lista == [4, 5]
        ExtenderLista(lista, 6)
        assert lista == [4, 5, 6]

        compuesto = [1, 2]
        ExtenderLista(compuesto, [3, 4])
        assert compuesto == [1, 2, 3, 4]


    def test_Mezclar(self):
        original = list(range(3000))
        copia = list(range(3000))
        assert original == copia
        Mezclar(copia)
        assert original != copia
        assert len(original) == len(copia)
        for i in original:
            assert i in copia


    def test_BorrarDe(self):
        meses = ["Enero", "Febrero", "Marzo"]
        BorrarDe(meses, 0)
        assert meses == ["Febrero", "Marzo"]
        BorrarDe(meses, 1)
        assert meses == ["Febrero"]
        BorrarDe(meses, 0)
        assert meses == []
        meses.append("Julio")
        assert meses == ["Julio"]
        BorrarDe(meses, 0)
        assert meses == []


    def test_ElegirUnaDe(self):
        lista = [1, 2, 3, 4]

        for i in range(20):
            eleccion = ElegirUnaDe(lista)
            assert eleccion in lista
            assert eleccion >= 1 and eleccion <= 4


    def test_TomarUltimoDe(self):
        meses = ["Enero", "Febrero", "Marzo"]
        ultimo = TomarUltimoDe(meses)
        assert ultimo == "Marzo"
        assert meses == ["Enero", "Febrero"]


    def test_ListaVacia(self):
        lista = [1, 2, 3]
        assert ListaVacia(lista) == False
        assert ListaVacia([]) == True
        otra_lista = [[lista]]
        assert ListaVacia(otra_lista) == False
        vacio = []
        assert ListaVacia(vacio) == True


    def test_EstaEn(self):
        lista = [1, 2, 3, 4]
        assert EstaEn(lista, 3) == True
        assert EstaEn(lista, 5) == False


    def test_CantidadDeElementos(lista):
        lista = [1, 2, 3]
        assert CantidadDeElementos(lista) == 3
        otra_lista = []
        assert CantidadDeElementos(otra_lista) == 0


    def test_ClaveValor(self):
        lista = [1, 2, 3]
        p = 0
        for posicion, valor in ClaveValor(lista):
            assert posicion == p
            assert valor == lista[p]
            p = p + 1

        lista = ["Primero", "Segundo", "Tercero"]
        p = 0
        for posicion, valor in ClaveValor(lista):
            assert posicion == p
            assert valor == lista[p]
            p = p + 1

        cadena = u"Febrero"
        p = 0
        for posicion, valor in ClaveValor(cadena):
            assert posicion == p
            assert valor == cadena[p]
            p = p + 1

        diccionario = {
            "marzo": 3,
            "abril": 4,
            "mayo": 5,
        }

        for nombre, numero in ClaveValor(diccionario):
            assert diccionario[nombre] == numero
