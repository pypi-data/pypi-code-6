#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Doc TODO
"""

import random


def _get_comps(base):
    '''
    TODO

    :param int base: The base to find the complementaire
    '''
    # Decide if it will be an addition or a substraction
    comps = range(0, base+1)
    k_comp = random.choice(comps)
    u_comp = base - k_comp
    return {'base': base, 'k_comp': k_comp, 'u_comp': u_comp}


def build_equation(base):
    '''
    TODO
    '''
    eq_elements = _get_comps(base)
    # decide if it will be an add or a sub
    sign = random.choice([0, 2])
    if sign == 0:
        equation = {
            'eq': '%d - %d = _' % (
                eq_elements.get('base'), eq_elements.get('k_comp')
            ),
            'answer': eq_elements.get('u_comp')
        }
    else:
        equation = {
            'eq': '%d + _ = %d' % (
                eq_elements.get('k_comp'), eq_elements.get('base')
            ),
            'answer': eq_elements.get('u_comp')
        }
    return equation


def main():
    '''
    TODO
    '''
    print('Les complémentaires de quel interval de nombres désirez-vous'
          ' pratiquer?')
    _min = int(raw_input('Entrez le plus petit nombre: '))
    _max = int(raw_input('Entrez le plus grand nombre: '))
    nb_exer = int(raw_input("Combien d'exercice voulez-vous faire?: "))
    for exer in range(0, nb_exer):
        base = random.choice(range(_min, _max+1))
        equation = build_equation(base)
        print(equation.get('eq'))
        answer = int(raw_input('>>>'))
        if answer == equation.get('answer'):
            print('Bravo!! Bonne réponse!')
        else:
            print('Mauvaise réponse, la réponse était: %d' % (
                equation.get('answer')
            ))
