# -*- coding: utf-8 -*-

__version__ = '0.0.1'
# python 3.4.1

# Korean version of loremipsum
# text source: from http://kimkoo.or.kr/

import random
import data


unit = {
    'sentences': data.sentences,
    'words': data.words
}


def _getLength(type_):
    """
    '리스트 길이 - 1'을 리턴
    """
    return random.randint(0, len(unit[type_]) - 1)


def word():
    """
    전체 단어에서 임의의 한 단어를 리턴
    """
    type_ = 'words'
    i = random.randint(0, _getLength(type_=type_))
    return unit[type_][i]


def words(min=2, max=5):
    """
    전체 단어에서 임의의 단어들을 리턴
    """

    if min < 2:
        min = 2

    _max = len(unit['words'])
    if max > _max:
        max = _max

    rloop = random.randint(min, max)
    n = ' '.join(word() for r in range(rloop))
    return n


def sentence():
    """
    전체 문장에서 임의의 한 문장을 리턴
    """
    type_ = 'sentences'
    i = random.randint(0, _getLength(type_=type_))
    return unit[type_][i]


def para(min=2, max=5):
    """
    전체 문장에서 임의의 문장들을 한 문단으로 리턴
    문장의 갯수는 min보다 크고 max보다 작다.
    """
    type_ = 'sentences'

    if min < 2:
        min = 2

    _max = len(unit[type_])
    if max > _max:
        max = _max

    s = ''
    rloop = random.randint(min, max)
    for r in range(rloop):
        i = random.randint(0, _getLength(type_=type_))
        s += unit[type_][i] + ' '
    return s


def paras(min=2, max=3):
    """
    전체 문장에서 임의의 문장들을 여러 문단으로 리턴
    문단의 갯수는 min보다 크고 max보다 작다.
    """

    if min < 2:
        min = 2

    if max < min:
        max = min

    r = random.randint(min, max)
    p = '\n'.join(para() for r in range(r))
    return p
