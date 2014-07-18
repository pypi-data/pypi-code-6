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

class TestNumeros:


    def test_DesdeHasta(self):
        # Uso básico
        assert DesdeHasta(1, 4) == [1, 2, 3, 4]
        assert DesdeHasta(4, 1) == [4, 3, 2, 1]
        assert DesdeHasta(1, 4, 2) == [1, 3]

        # Step en reversa
        assert DesdeHasta(0, 10, 2) == [0, 2, 4, 6, 8, 10]
        assert DesdeHasta(10, 0, 2) == [10, 8, 6, 4, 2, 0]

        # Desde negativo a positivo
        assert DesdeHasta(-3, 3) == [-3, -2, -1, 0, 1, 2, 3]
        assert DesdeHasta(-8, 8, 2) == [-8, -6, -4, -2, 0, 2, 4, 6, 8]
        assert DesdeHasta(8, -8, 2) == [8, 6, 4, 2, 0, -2, -4, -6, -8]

        # Step con valor absoluto
        assert DesdeHasta(10, -10, -2) == DesdeHasta(10, -10, 2)
        assert DesdeHasta(-10, 10, -2) == DesdeHasta(-10, 10, 2)

        with pytest.raises(ValueError):
            DesdeHasta("dos", 4)

        with pytest.raises(ValueError):
            DesdeHasta(1.1, 4)

        with pytest.raises(ValueError):
            DesdeHasta(3, "cuatro")

        with pytest.raises(ValueError):
            DesdeHasta(3, 5, "2")


    def test_Aleatorio(self):
        for i in range(100):
            n = Aleatorio(1, 10)
            assert n >= 1 and n <= 10
            r = Aleatorio(50, 100)
            assert r != n

        for i in range(100):
            n = Aleatorio(1.0, 10.0)
            assert n >= 1.0 and n <= 10.0


    def test_ValorAbsoluto(self):
        assert 1 == ValorAbsoluto(1)
        assert 1 == ValorAbsoluto(-1)

        assert 1.2 == ValorAbsoluto(1.2)
        assert 1.2 == ValorAbsoluto(-1.2)


    def test_RaizCuadrada(self):
        assert 5 == RaizCuadrada(25)
        assert 1.5 == RaizCuadrada(2.25)


    def test_Redondear(self):
        assert 2.0 == Redondear(2.123456, 0)
        assert 2.1 == Redondear(2.123456, 1)
        assert 2.12 == Redondear(2.123456, 2)
        assert 2.123 == Redondear(2.123456, 3)

