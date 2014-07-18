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

    def test_AlgoSeCumple(self):
        assert AlgoSeCumple(True, True, True, False)
        assert AlgoSeCumple(True, True, True, False)
        assert AlgoSeCumple(True, True, False, False)
        assert AlgoSeCumple(True, False, False, False)
        assert AlgoSeCumple(False, False, False, False) == False


    def test_TodoSeCumple(self):
        assert TodoSeCumple(False, False, False, False) == False
        assert TodoSeCumple(False, False, False, True) == False
        assert TodoSeCumple(False, False, True, True) == False
        assert TodoSeCumple(False, True, True, True) == False
        assert TodoSeCumple(True, True, True, True) == True


    def test_NadaSeCumple(self):
        assert NadaSeCumple(False, False, False, False) == True
        assert NadaSeCumple(False, False, False, True) == False
        assert NadaSeCumple(False, False, True, True) == False
        assert NadaSeCumple(False, True, True, True) == False
        assert NadaSeCumple(True, True, True, True) == False

