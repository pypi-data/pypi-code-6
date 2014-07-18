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

class TestTexto:

    frase_original = u"¿Cúando termina este año?"
    frase_longitud = 25
    frase_minuscula = u"¿cúando termina este año?"
    frase_mayuscula = u"¿CÚANDO TERMINA ESTE AÑO?"
    frase_empieza_con = u"¿Cúando"
    frase_termina_con = u"año?"


    def test_Longitud(self):
        # Utf-8
        assert self.frase_longitud == Longitud(self.frase_original)
        assert self.frase_longitud + 9 == Longitud(self.frase_original + u" ¿Cúando?")
        assert self.frase_longitud == Longitud(Minuscula(self.frase_original))
        assert self.frase_longitud == Longitud(Mayuscula(self.frase_original))


    def test_Mayuscula(self):
        assert self.frase_mayuscula == Mayuscula(self.frase_original)
        assert self.frase_mayuscula == Mayuscula(Minuscula(self.frase_original))

    def test_Minuscula(self):
        assert self.frase_minuscula == Minuscula(self.frase_original)
        assert self.frase_minuscula == Minuscula(Mayuscula(self.frase_original))


    def test_EmpiezaCon(self):
        assert EmpiezaCon(self.frase_original, self.frase_empieza_con)
        assert EmpiezaCon(self.frase_original, self.frase_original[:7])
        assert EmpiezaCon(1234, 1)
        assert EmpiezaCon(1234, 2) == False
        assert EmpiezaCon(12.34, 1)
        assert EmpiezaCon(12.34, 2) == False


    def test_TerminaCon(self):
        assert TerminaCon(self.frase_original, self.frase_termina_con)
        assert TerminaCon(self.frase_original, self.frase_original[-4:])
        assert TerminaCon(1234, 4)
        assert TerminaCon(1234, 2) == False
        assert TerminaCon(12.34, 4)
        assert TerminaCon(12.34, 2) == False


    def test_Separar(self):
        frase = u"Un día soleado"
        lista = Separar(frase, u" ")
        assert lista == [u"Un", u"día", u"soleado"]


    def test_Unir(self):
        lista = [u"Un", u"día", u"soleado"]
        frase = u"Un día soleado"
        assert Unir(lista, " ") == frase


    def test_Contiene(self):
        frase = u"Un día soleado"
        palabra = u"día"
        otra_palabra = u"nublado"
        assert Contiene(frase, palabra)
        assert not Contiene(frase, otra_palabra)


    def test_Reemplazar(self):
        frase = u"Un día soleado"
        buscar = u"soleado"
        reemplazar = u"nublado"

        assert Reemplazar(frase, buscar, reemplazar) == u"Un día nublado"

        frase = u"uno más uno es dos"
        buscar = u"uno"
        reemplazar = u"tres"
        assert Reemplazar(frase, buscar, reemplazar, 1) == u"tres más uno es dos"
        assert Reemplazar(frase, buscar, reemplazar, 2) == u"tres más tres es dos"



