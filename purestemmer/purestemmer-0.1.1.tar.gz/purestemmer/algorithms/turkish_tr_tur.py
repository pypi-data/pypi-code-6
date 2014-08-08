#!/usr/bin/env python
# vim:fileencoding=utf-8



# This file was auto-generated on 2014-08-05 20:04:24 using
# version 0.1.0 of the sbl2py Snowball-to-Python compiler.

import sys

class _String(object):

    def __init__(self, s):
        self.chars = list(unicode(s))
        self.cursor = 0
        self.limit = len(s)
        self.direction = 1

    def __unicode__(self):
        return u''.join(self.chars)

    def __len__(self):
        return len(self.chars)

    def get_range(self, start, stop):
        if self.direction == 1:
            return self.chars[start:stop]
        else:
            n = len(self.chars)
            return self.chars[stop:start]

    def set_range(self, start, stop, chars):
        if self.direction == 1:
            self.chars[start:stop] = chars
        else:
            self.chars[stop:start] = chars
        change = self.direction * (len(chars) - (stop - start))
        if self.direction == 1:
            if self.cursor >= stop:
                self.cursor += change
                self.limit += change
        else:
            if self.cursor > start:
                self.cursor += change
            if self.limit > start:
                self.limit += change
        return True

    def insert(self, chars):
        self.chars[self.cursor:self.cursor] = chars
        if self.direction == 1:
            self.cursor += len(chars)
            self.limit += len(chars)
        return True

    def attach(self, chars):
        self.chars[self.cursor:self.cursor] = chars
        if self.direction == 1:
            self.limit += len(chars)
        else:
            self.cursor += len(chars)
        return True

    def set_chars(self, chars):
        self.chars = chars
        if self.direction == 1:
            self.cursor = 0
            self.limit = len(chars)
        else:
            self.cursor = len(chars)
            self.limit = 0
        return True

    def starts_with(self, chars):
        n = len(chars)
        r = self.get_range(self.cursor, self.limit)[::self.direction][:n]
        if not r == list(chars)[::self.direction]:
            return False
        self.cursor += n * self.direction
        return True

    def hop(self, n):
        if n < 0 or len(self.get_range(self.cursor, self.limit)) < n:
            return False
        self.cursor += n * self.direction
        return True

    def to_mark(self, mark):
        if self.direction == 1:
            if self.cursor > mark or self.limit < mark:
                return False
        else:
            if self.cursor < mark or self.limit > mark:
                return False
        self.cursor = mark
        return True

_g_vowel = set(u'ae\u0131io\xf6u\xfc')
_g_U = set(u'\u0131iu\xfc')
_g_vowel1 = set(u'a\u0131ou')
_g_vowel2 = set(u'ei\xf6\xfc')
_g_vowel3 = set(u'a\u0131')
_g_vowel4 = set(u'ei')
_g_vowel5 = set(u'ou')
_g_vowel6 = set(u'\xf6\xfc')

def stem(s):
    s = _String(s)
    _Program().r_stem(s)
    return unicode(s)

_a_1 = ((u'm\u0131z', '', 0), (u'miz', '', 0), (u'muz', '', 0), (u'm\xfcz', '', 0), (u'n\u0131z', '', 0), (u'niz', '', 0), (u'nuz', '', 0), (u'n\xfcz', '', 0), (u'm', '', 0), (u'n', '', 0),)
_a_2 = ((u'leri', '', 0), (u'lar\u0131', '', 0),)
_a_3 = ((u'n\u0131', '', 0), (u'ni', '', 0), (u'nu', '', 0), (u'n\xfc', '', 0),)
_a_4 = ((u'\u0131n', '', 0), (u'in', '', 0), (u'un', '', 0), (u'\xfcn', '', 0),)
_a_5 = ((u'a', '', 0), (u'e', '', 0),)
_a_6 = ((u'na', '', 0), (u'ne', '', 0),)
_a_7 = ((u'da', '', 0), (u'de', '', 0), (u'ta', '', 0), (u'te', '', 0),)
_a_8 = ((u'nda', '', 0), (u'nde', '', 0),)
_a_9 = ((u'dan', '', 0), (u'den', '', 0), (u'tan', '', 0), (u'ten', '', 0),)
_a_10 = ((u'ndan', '', 0), (u'nden', '', 0),)
_a_11 = ((u'la', '', 0), (u'le', '', 0),)
_a_12 = ((u'ca', '', 0), (u'ce', '', 0),)
_a_13 = ((u'\u0131m', '', 0), (u'im', '', 0), (u'um', '', 0), (u'\xfcm', '', 0),)
_a_14 = ((u's\u0131n', '', 0), (u'sin', '', 0), (u'sun', '', 0), (u's\xfcn', '', 0),)
_a_15 = ((u'\u0131z', '', 0), (u'iz', '', 0), (u'uz', '', 0), (u'\xfcz', '', 0),)
_a_16 = ((u's\u0131n\u0131z', '', 0), (u'siniz', '', 0), (u'sunuz', '', 0), (u's\xfcn\xfcz', '', 0),)
_a_17 = ((u'ler', '', 0), (u'lar', '', 0),)
_a_18 = ((u'n\u0131z', '', 0), (u'niz', '', 0), (u'nuz', '', 0), (u'n\xfcz', '', 0),)
_a_19 = ((u't\u0131r', '', 0), (u'tir', '', 0), (u'tur', '', 0), (u't\xfcr', '', 0), (u'd\u0131r', '', 0), (u'dir', '', 0), (u'dur', '', 0), (u'd\xfcr', '', 0),)
_a_20 = ((u'cas\u0131na', '', 0), (u'cesine', '', 0),)
_a_21 = ((u't\u0131m', '', 0), (u'tim', '', 0), (u'tum', '', 0), (u't\xfcm', '', 0), (u'd\u0131m', '', 0), (u'dim', '', 0), (u'dum', '', 0), (u'd\xfcm', '', 0), (u't\u0131n', '', 0), (u'tin', '', 0), (u'tun', '', 0), (u't\xfcn', '', 0), (u'd\u0131n', '', 0), (u'din', '', 0), (u'dun', '', 0), (u'd\xfcn', '', 0), (u't\u0131k', '', 0), (u'tik', '', 0), (u'tuk', '', 0), (u't\xfck', '', 0), (u'd\u0131k', '', 0), (u'dik', '', 0), (u'duk', '', 0), (u'd\xfck', '', 0), (u't\u0131', '', 0), (u'ti', '', 0), (u'tu', '', 0), (u't\xfc', '', 0), (u'd\u0131', '', 0), (u'di', '', 0), (u'du', '', 0), (u'd\xfc', '', 0),)
_a_22 = ((u'sam', '', 0), (u'san', '', 0), (u'sak', '', 0), (u'sem', '', 0), (u'sen', '', 0), (u'sek', '', 0), (u'sa', '', 0), (u'se', '', 0),)
_a_23 = ((u'm\u0131\u015f', '', 0), (u'mi\u015f', '', 0), (u'mu\u015f', '', 0), (u'm\xfc\u015f', '', 0),)
_a_24 = ((u'b', '', 0), (u'c', '', 1), (u'd', '', 2), (u'\u011f', '', 3),)

class _Program(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.i_strlen = 0
        self.b_continue_stemming_noun_suffixes = True

    def r_check_vowel_harmony(self, s):
        r = True
        var16 = len(s) - s.cursor                                                                                                       ##
        while True:                                                      ##                                                             #
            var0 = len(s) - s.cursor                                     #                                                              #
            if s.cursor == s.limit:                    ##                #                                                              #
                r = False                              #                 #                                                              #
            else:                                      #                 #                                                              #
                r = s.chars[s.cursor - 1] in _g_vowel  # grouping check  #                                                              #
            if r:                                      #                 # goto                                                         #
                s.cursor -= 1                          ##                #                                                              #
            if r or s.cursor == s.limit:                                 #                                                              #
                s.cursor = len(s) - var0                                 #                                                              #
                break                                                    #                                                              #
            s.cursor = len(s) - var0 - 1                                 ##                                                             #
        if r:                                                                                                                           #
            var15 = len(s) - s.cursor                                                                                             ##    #
            var13 = len(s) - s.cursor                                                                                       ##    #     #
            var11 = len(s) - s.cursor                                                                                 ##    #     #     #
            var9 = len(s) - s.cursor                                                                            ##    #     #     #     #
            var7 = len(s) - s.cursor                                                                      ##    #     #     #     #     #
            var5 = len(s) - s.cursor                                                                ##    #     #     #     #     #     #
            var3 = len(s) - s.cursor                                                          ##    #     #     #     #     #     #     #
            r = s.starts_with(u'a')  # character check                                        #     #     #     #     #     #     #     #
            if r:                                                                             #     #     #     #     #     #     #     #
                while True:                                                       ##          #     #     #     #     #     #     #     #
                    var1 = len(s) - s.cursor                                      #           #     #     #     #     #     #     #     #
                    if s.cursor == s.limit:                     ##                #           #     #     #     #     #     #     #     #
                        r = False                               #                 #           #     #     #     #     #     #     #     #
                    else:                                       #                 #           #     #     #     #     #     #     #     #
                        r = s.chars[s.cursor - 1] in _g_vowel1  # grouping check  #           #     #     #     #     #     #     #     #
                    if r:                                       #                 # goto      #     #     #     #     #     #     #     #
                        s.cursor -= 1                           ##                #           #     #     #     #     #     #     #     #
                    if r or s.cursor == s.limit:                                  #           #     #     #     #     #     #     #     #
                        s.cursor = len(s) - var1                                  #           #     #     #     #     #     #     #     #
                        break                                                     #           #     #     #     #     #     #     #     #
                    s.cursor = len(s) - var1 - 1                                  ##          #     #     #     #     #     #     #     #
            if not r:                                                                         # or  #     #     #     #     #     #     #
                s.cursor = len(s) - var3                                                      #     #     #     #     #     #     #     #
                r = s.starts_with(u'e')  # character check                                    #     #     #     #     #     #     #     #
                if r:                                                                         #     #     #     #     #     #     #     #
                    while True:                                                       ##      #     #     #     #     #     #     #     #
                        var2 = len(s) - s.cursor                                      #       #     #     #     #     #     #     #     #
                        if s.cursor == s.limit:                     ##                #       #     #     #     #     #     #     #     #
                            r = False                               #                 #       #     #     #     #     #     #     #     #
                        else:                                       #                 #       #     # or  #     #     #     #     #     #
                            r = s.chars[s.cursor - 1] in _g_vowel2  # grouping check  #       #     #     #     #     #     #     #     #
                        if r:                                       #                 # goto  #     #     #     #     #     #     #     #
                            s.cursor -= 1                           ##                #       #     #     #     #     #     #     #     #
                        if r or s.cursor == s.limit:                                  #       #     #     #     #     #     #     #     #
                            s.cursor = len(s) - var2                                  #       #     #     #     #     #     #     #     #
                            break                                                     #       #     #     #     #     #     #     #     #
                        s.cursor = len(s) - var2 - 1                                  ##      ##    #     # or  #     #     #     #     #
            if not r:                                                                               #     #     #     #     #     #     #
                s.cursor = len(s) - var5                                                            #     #     #     #     #     #     #
                r = s.starts_with(u'\u0131')  # character check                                     #     #     #     #     #     #     #
                if r:                                                                               #     #     #     #     #     #     #
                    while True:                                                       ##            #     #     #     #     #     #     #
                        var4 = len(s) - s.cursor                                      #             #     #     #     #     #     #     #
                        if s.cursor == s.limit:                     ##                #             #     #     #     #     #     #     #
                            r = False                               #                 #             #     #     # or  #     #     #     #
                        else:                                       #                 #             #     #     #     #     #     #     #
                            r = s.chars[s.cursor - 1] in _g_vowel3  # grouping check  #             #     #     #     #     #     #     #
                        if r:                                       #                 # goto        #     #     #     #     #     #     #
                            s.cursor -= 1                           ##                #             #     #     #     #     #     #     #
                        if r or s.cursor == s.limit:                                  #             #     #     #     #     #     #     #
                            s.cursor = len(s) - var4                                  #             #     #     #     #     #     #     #
                            break                                                     #             #     #     #     # or  #     #     #
                        s.cursor = len(s) - var4 - 1                                  ##            ##    #     #     #     #     #     #
            if not r:                                                                                     #     #     #     #     #     #
                s.cursor = len(s) - var7                                                                  #     #     #     #     #     #
                r = s.starts_with(u'i')  # character check                                                #     #     #     #     #     #
                if r:                                                                                     #     #     #     #     #     #
                    while True:                                                       ##                  #     #     #     #     #     #
                        var6 = len(s) - s.cursor                                      #                   #     #     #     #     #     #
                        if s.cursor == s.limit:                     ##                #                   #     #     #     # or  #     #
                            r = False                               #                 #                   #     #     #     #     #     # test
                        else:                                       #                 #                   #     #     #     #     #     #
                            r = s.chars[s.cursor - 1] in _g_vowel4  # grouping check  #                   #     #     #     #     #     #
                        if r:                                       #                 # goto              #     #     #     #     #     #
                            s.cursor -= 1                           ##                #                   #     #     #     #     #     #
                        if r or s.cursor == s.limit:                                  #                   #     #     #     #     #     #
                            s.cursor = len(s) - var6                                  #                   #     #     #     #     # or  #
                            break                                                     #                   #     #     #     #     #     #
                        s.cursor = len(s) - var6 - 1                                  ##                  ##    #     #     #     #     #
            if not r:                                                                                           #     #     #     #     #
                s.cursor = len(s) - var9                                                                        #     #     #     #     #
                r = s.starts_with(u'o')  # character check                                                      #     #     #     #     #
                if r:                                                                                           #     #     #     #     #
                    while True:                                                       ##                        #     #     #     #     #
                        var8 = len(s) - s.cursor                                      #                         #     #     #     #     #
                        if s.cursor == s.limit:                     ##                #                         #     #     #     #     #
                            r = False                               #                 #                         #     #     #     #     #
                        else:                                       #                 #                         #     #     #     #     #
                            r = s.chars[s.cursor - 1] in _g_vowel5  # grouping check  #                         #     #     #     #     #
                        if r:                                       #                 # goto                    #     #     #     #     #
                            s.cursor -= 1                           ##                #                         #     #     #     #     #
                        if r or s.cursor == s.limit:                                  #                         #     #     #     #     #
                            s.cursor = len(s) - var8                                  #                         #     #     #     #     #
                            break                                                     #                         #     #     #     #     #
                        s.cursor = len(s) - var8 - 1                                  ##                        ##    #     #     #     #
            if not r:                                                                                                 #     #     #     #
                s.cursor = len(s) - var11                                                                             #     #     #     #
                r = s.starts_with(u'\xf6')  # character check                                                         #     #     #     #
                if r:                                                                                                 #     #     #     #
                    while True:                                                       ##                              #     #     #     #
                        var10 = len(s) - s.cursor                                     #                               #     #     #     #
                        if s.cursor == s.limit:                     ##                #                               #     #     #     #
                            r = False                               #                 #                               #     #     #     #
                        else:                                       #                 #                               #     #     #     #
                            r = s.chars[s.cursor - 1] in _g_vowel6  # grouping check  #                               #     #     #     #
                        if r:                                       #                 # goto                          #     #     #     #
                            s.cursor -= 1                           ##                #                               #     #     #     #
                        if r or s.cursor == s.limit:                                  #                               #     #     #     #
                            s.cursor = len(s) - var10                                 #                               #     #     #     #
                            break                                                     #                               #     #     #     #
                        s.cursor = len(s) - var10 - 1                                 ##                              ##    #     #     #
            if not r:                                                                                                       #     #     #
                s.cursor = len(s) - var13                                                                                   #     #     #
                r = s.starts_with(u'u')  # character check                                                                  #     #     #
                if r:                                                                                                       #     #     #
                    while True:                                                       ##                                    #     #     #
                        var12 = len(s) - s.cursor                                     #                                     #     #     #
                        if s.cursor == s.limit:                     ##                #                                     #     #     #
                            r = False                               #                 #                                     #     #     #
                        else:                                       #                 #                                     #     #     #
                            r = s.chars[s.cursor - 1] in _g_vowel5  # grouping check  #                                     #     #     #
                        if r:                                       #                 # goto                                #     #     #
                            s.cursor -= 1                           ##                #                                     #     #     #
                        if r or s.cursor == s.limit:                                  #                                     #     #     #
                            s.cursor = len(s) - var12                                 #                                     #     #     #
                            break                                                     #                                     #     #     #
                        s.cursor = len(s) - var12 - 1                                 ##                                    ##    #     #
            if not r:                                                                                                             #     #
                s.cursor = len(s) - var15                                                                                         #     #
                r = s.starts_with(u'\xfc')  # character check                                                                     #     #
                if r:                                                                                                             #     #
                    while True:                                                       ##                                          #     #
                        var14 = len(s) - s.cursor                                     #                                           #     #
                        if s.cursor == s.limit:                     ##                #                                           #     #
                            r = False                               #                 #                                           #     #
                        else:                                       #                 #                                           #     #
                            r = s.chars[s.cursor - 1] in _g_vowel6  # grouping check  #                                           #     #
                        if r:                                       #                 # goto                                      #     #
                            s.cursor -= 1                           ##                #                                           #     #
                        if r or s.cursor == s.limit:                                  #                                           #     #
                            s.cursor = len(s) - var14                                 #                                           #     #
                            break                                                     #                                           #     #
                        s.cursor = len(s) - var14 - 1                                 ##                                          ##    #
        s.cursor = len(s) - var16                                                                                                       ##
        return r
    
    def r_mark_suffix_with_optional_n_consonant(self, s):
        r = True
        var23 = len(s) - s.cursor                                                                ##
        var17 = len(s) - s.cursor                   ##                                           #
        r = s.starts_with(u'n')  # character check  # test                                       #
        s.cursor = len(s) - var17                   ##                                           #
        if r:                                                                                    #
            r = s.hop(1)  # next                                                                 #
            if r:                                                                                #
                var18 = len(s) - s.cursor                                    ##                  #
                if s.cursor == s.limit:                    ##                #                   #
                    r = False                              #                 #                   #
                else:                                      #                 #                   #
                    r = s.chars[s.cursor - 1] in _g_vowel  # grouping check  # test              #
                if r:                                      #                 #                   #
                    s.cursor -= 1                          ##                #                   #
                s.cursor = len(s) - var18                                    ##                  #
        if not r:                                                                                #
            s.cursor = len(s) - var23                                                            #
            var20 = len(s) - s.cursor                           ##                               #
            var19 = len(s) - s.cursor                   ##      #                                # or
            r = s.starts_with(u'n')  # character check  # test  #                                #
            s.cursor = len(s) - var19                   ##      # not                            #
            if not r:                                           #                                #
                s.cursor = len(s) - var20                       #                                #
            r = not r                                           ##                               #
            if r:                                                                                #
                var22 = len(s) - s.cursor                                                ##      #
                r = s.hop(1)  # next                                                     #       #
                if r:                                                                    #       #
                    var21 = len(s) - s.cursor                                    ##      #       #
                    if s.cursor == s.limit:                    ##                #       #       #
                        r = False                              #                 #       #       #
                    else:                                      #                 #       # test  #
                        r = s.chars[s.cursor - 1] in _g_vowel  # grouping check  # test  #       #
                    if r:                                      #                 #       #       #
                        s.cursor -= 1                          ##                #       #       #
                    s.cursor = len(s) - var21                                    ##      #       #
                s.cursor = len(s) - var22                                                ##      ##
        return r
    
    def r_mark_suffix_with_optional_s_consonant(self, s):
        r = True
        var30 = len(s) - s.cursor                                                                ##
        var24 = len(s) - s.cursor                   ##                                           #
        r = s.starts_with(u's')  # character check  # test                                       #
        s.cursor = len(s) - var24                   ##                                           #
        if r:                                                                                    #
            r = s.hop(1)  # next                                                                 #
            if r:                                                                                #
                var25 = len(s) - s.cursor                                    ##                  #
                if s.cursor == s.limit:                    ##                #                   #
                    r = False                              #                 #                   #
                else:                                      #                 #                   #
                    r = s.chars[s.cursor - 1] in _g_vowel  # grouping check  # test              #
                if r:                                      #                 #                   #
                    s.cursor -= 1                          ##                #                   #
                s.cursor = len(s) - var25                                    ##                  #
        if not r:                                                                                #
            s.cursor = len(s) - var30                                                            #
            var27 = len(s) - s.cursor                           ##                               #
            var26 = len(s) - s.cursor                   ##      #                                # or
            r = s.starts_with(u's')  # character check  # test  #                                #
            s.cursor = len(s) - var26                   ##      # not                            #
            if not r:                                           #                                #
                s.cursor = len(s) - var27                       #                                #
            r = not r                                           ##                               #
            if r:                                                                                #
                var29 = len(s) - s.cursor                                                ##      #
                r = s.hop(1)  # next                                                     #       #
                if r:                                                                    #       #
                    var28 = len(s) - s.cursor                                    ##      #       #
                    if s.cursor == s.limit:                    ##                #       #       #
                        r = False                              #                 #       #       #
                    else:                                      #                 #       # test  #
                        r = s.chars[s.cursor - 1] in _g_vowel  # grouping check  # test  #       #
                    if r:                                      #                 #       #       #
                        s.cursor -= 1                          ##                #       #       #
                    s.cursor = len(s) - var28                                    ##      #       #
                s.cursor = len(s) - var29                                                ##      ##
        return r
    
    def r_mark_suffix_with_optional_y_consonant(self, s):
        r = True
        var37 = len(s) - s.cursor                                                                ##
        var31 = len(s) - s.cursor                   ##                                           #
        r = s.starts_with(u'y')  # character check  # test                                       #
        s.cursor = len(s) - var31                   ##                                           #
        if r:                                                                                    #
            r = s.hop(1)  # next                                                                 #
            if r:                                                                                #
                var32 = len(s) - s.cursor                                    ##                  #
                if s.cursor == s.limit:                    ##                #                   #
                    r = False                              #                 #                   #
                else:                                      #                 #                   #
                    r = s.chars[s.cursor - 1] in _g_vowel  # grouping check  # test              #
                if r:                                      #                 #                   #
                    s.cursor -= 1                          ##                #                   #
                s.cursor = len(s) - var32                                    ##                  #
        if not r:                                                                                #
            s.cursor = len(s) - var37                                                            #
            var34 = len(s) - s.cursor                           ##                               #
            var33 = len(s) - s.cursor                   ##      #                                # or
            r = s.starts_with(u'y')  # character check  # test  #                                #
            s.cursor = len(s) - var33                   ##      # not                            #
            if not r:                                           #                                #
                s.cursor = len(s) - var34                       #                                #
            r = not r                                           ##                               #
            if r:                                                                                #
                var36 = len(s) - s.cursor                                                ##      #
                r = s.hop(1)  # next                                                     #       #
                if r:                                                                    #       #
                    var35 = len(s) - s.cursor                                    ##      #       #
                    if s.cursor == s.limit:                    ##                #       #       #
                        r = False                              #                 #       #       #
                    else:                                      #                 #       # test  #
                        r = s.chars[s.cursor - 1] in _g_vowel  # grouping check  # test  #       #
                    if r:                                      #                 #       #       #
                        s.cursor -= 1                          ##                #       #       #
                    s.cursor = len(s) - var35                                    ##      #       #
                s.cursor = len(s) - var36                                                ##      ##
        return r
    
    def r_mark_suffix_with_optional_U_vowel(self, s):
        r = True
        var44 = len(s) - s.cursor                                                                             ##
        var38 = len(s) - s.cursor                                ##                                           #
        if s.cursor == s.limit:                ##                #                                            #
            r = False                          #                 #                                            #
        else:                                  #                 #                                            #
            r = s.chars[s.cursor - 1] in _g_U  # grouping check  # test                                       #
        if r:                                  #                 #                                            #
            s.cursor -= 1                      ##                #                                            #
        s.cursor = len(s) - var38                                ##                                           #
        if r:                                                                                                 #
            r = s.hop(1)  # next                                                                              #
            if r:                                                                                             #
                var39 = len(s) - s.cursor                                                 ##                  #
                if s.cursor == s.limit:                        ##                         #                   #
                    r = False                                  #                          #                   #
                else:                                          #                          #                   #
                    r = s.chars[s.cursor - 1] not in _g_vowel  # negative grouping check  # test              #
                if r:                                          #                          #                   #
                    s.cursor -= 1                              ##                         #                   #
                s.cursor = len(s) - var39                                                 ##                  #
        if not r:                                                                                             #
            s.cursor = len(s) - var44                                                                         #
            var41 = len(s) - s.cursor                                        ##                               #
            var40 = len(s) - s.cursor                                ##      #                                # or
            if s.cursor == s.limit:                ##                #       #                                #
                r = False                          #                 #       #                                #
            else:                                  #                 #       #                                #
                r = s.chars[s.cursor - 1] in _g_U  # grouping check  # test  #                                #
            if r:                                  #                 #       # not                            #
                s.cursor -= 1                      ##                #       #                                #
            s.cursor = len(s) - var40                                ##      #                                #
            if not r:                                                        #                                #
                s.cursor = len(s) - var41                                    #                                #
            r = not r                                                        ##                               #
            if r:                                                                                             #
                var43 = len(s) - s.cursor                                                             ##      #
                r = s.hop(1)  # next                                                                  #       #
                if r:                                                                                 #       #
                    var42 = len(s) - s.cursor                                                 ##      #       #
                    if s.cursor == s.limit:                        ##                         #       #       #
                        r = False                                  #                          #       #       #
                    else:                                          #                          #       # test  #
                        r = s.chars[s.cursor - 1] not in _g_vowel  # negative grouping check  # test  #       #
                    if r:                                          #                          #       #       #
                        s.cursor -= 1                              ##                         #       #       #
                    s.cursor = len(s) - var42                                                 ##      #       #
                s.cursor = len(s) - var43                                                             ##      ##
        return r
    
    def r_mark_possessives(self, s):
        r = True
        a_1 = None                                          ##
        r = False                                           #
        var46 = s.cursor                                    #
        for var45, var49, var48 in _a_1:                    #
            if s.starts_with(var45):                        #
                var47 = s.cursor                            #
                r = (not var49) or getattr(self, var49)(s)  #
                if r:                                       # among
                  s.cursor = var47                          #
                  a_1 = var48                               #
                  break                                     #
            s.cursor = var46                                #
        if r:                                               #
            if a_1 == 0:                                    #
                r = True                                    ##
        if r:
            r = self.r_mark_suffix_with_optional_U_vowel(s)  # routine call
        return r
    
    def r_mark_sU(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            if s.cursor == s.limit:                ##
                r = False                          #
            else:                                  #
                r = s.chars[s.cursor - 1] in _g_U  # grouping check
            if r:                                  #
                s.cursor -= 1                      ##
            if r:
                r = self.r_mark_suffix_with_optional_s_consonant(s)  # routine call
        return r
    
    def r_mark_lArI(self, s):
        r = True
        a_2 = None                                          ##
        r = False                                           #
        var51 = s.cursor                                    #
        for var50, var54, var53 in _a_2:                    #
            if s.starts_with(var50):                        #
                var52 = s.cursor                            #
                r = (not var54) or getattr(self, var54)(s)  #
                if r:                                       # among
                  s.cursor = var52                          #
                  a_2 = var53                               #
                  break                                     #
            s.cursor = var51                                #
        if r:                                               #
            if a_2 == 0:                                    #
                r = True                                    ##
        return r
    
    def r_mark_yU(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            if s.cursor == s.limit:                ##
                r = False                          #
            else:                                  #
                r = s.chars[s.cursor - 1] in _g_U  # grouping check
            if r:                                  #
                s.cursor -= 1                      ##
            if r:
                r = self.r_mark_suffix_with_optional_y_consonant(s)  # routine call
        return r
    
    def r_mark_nU(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_3 = None                                          ##
            r = False                                           #
            var56 = s.cursor                                    #
            for var55, var59, var58 in _a_3:                    #
                if s.starts_with(var55):                        #
                    var57 = s.cursor                            #
                    r = (not var59) or getattr(self, var59)(s)  #
                    if r:                                       # among
                      s.cursor = var57                          #
                      a_3 = var58                               #
                      break                                     #
                s.cursor = var56                                #
            if r:                                               #
                if a_3 == 0:                                    #
                    r = True                                    ##
        return r
    
    def r_mark_nUn(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_4 = None                                          ##
            r = False                                           #
            var61 = s.cursor                                    #
            for var60, var64, var63 in _a_4:                    #
                if s.starts_with(var60):                        #
                    var62 = s.cursor                            #
                    r = (not var64) or getattr(self, var64)(s)  #
                    if r:                                       # among
                      s.cursor = var62                          #
                      a_4 = var63                               #
                      break                                     #
                s.cursor = var61                                #
            if r:                                               #
                if a_4 == 0:                                    #
                    r = True                                    ##
            if r:
                r = self.r_mark_suffix_with_optional_n_consonant(s)  # routine call
        return r
    
    def r_mark_yA(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_5 = None                                          ##
            r = False                                           #
            var66 = s.cursor                                    #
            for var65, var69, var68 in _a_5:                    #
                if s.starts_with(var65):                        #
                    var67 = s.cursor                            #
                    r = (not var69) or getattr(self, var69)(s)  #
                    if r:                                       # among
                      s.cursor = var67                          #
                      a_5 = var68                               #
                      break                                     #
                s.cursor = var66                                #
            if r:                                               #
                if a_5 == 0:                                    #
                    r = True                                    ##
            if r:
                r = self.r_mark_suffix_with_optional_y_consonant(s)  # routine call
        return r
    
    def r_mark_nA(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_6 = None                                          ##
            r = False                                           #
            var71 = s.cursor                                    #
            for var70, var74, var73 in _a_6:                    #
                if s.starts_with(var70):                        #
                    var72 = s.cursor                            #
                    r = (not var74) or getattr(self, var74)(s)  #
                    if r:                                       # among
                      s.cursor = var72                          #
                      a_6 = var73                               #
                      break                                     #
                s.cursor = var71                                #
            if r:                                               #
                if a_6 == 0:                                    #
                    r = True                                    ##
        return r
    
    def r_mark_DA(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_7 = None                                          ##
            r = False                                           #
            var76 = s.cursor                                    #
            for var75, var79, var78 in _a_7:                    #
                if s.starts_with(var75):                        #
                    var77 = s.cursor                            #
                    r = (not var79) or getattr(self, var79)(s)  #
                    if r:                                       # among
                      s.cursor = var77                          #
                      a_7 = var78                               #
                      break                                     #
                s.cursor = var76                                #
            if r:                                               #
                if a_7 == 0:                                    #
                    r = True                                    ##
        return r
    
    def r_mark_ndA(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_8 = None                                          ##
            r = False                                           #
            var81 = s.cursor                                    #
            for var80, var84, var83 in _a_8:                    #
                if s.starts_with(var80):                        #
                    var82 = s.cursor                            #
                    r = (not var84) or getattr(self, var84)(s)  #
                    if r:                                       # among
                      s.cursor = var82                          #
                      a_8 = var83                               #
                      break                                     #
                s.cursor = var81                                #
            if r:                                               #
                if a_8 == 0:                                    #
                    r = True                                    ##
        return r
    
    def r_mark_DAn(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_9 = None                                          ##
            r = False                                           #
            var86 = s.cursor                                    #
            for var85, var89, var88 in _a_9:                    #
                if s.starts_with(var85):                        #
                    var87 = s.cursor                            #
                    r = (not var89) or getattr(self, var89)(s)  #
                    if r:                                       # among
                      s.cursor = var87                          #
                      a_9 = var88                               #
                      break                                     #
                s.cursor = var86                                #
            if r:                                               #
                if a_9 == 0:                                    #
                    r = True                                    ##
        return r
    
    def r_mark_ndAn(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_10 = None                                         ##
            r = False                                           #
            var91 = s.cursor                                    #
            for var90, var94, var93 in _a_10:                   #
                if s.starts_with(var90):                        #
                    var92 = s.cursor                            #
                    r = (not var94) or getattr(self, var94)(s)  #
                    if r:                                       # among
                      s.cursor = var92                          #
                      a_10 = var93                              #
                      break                                     #
                s.cursor = var91                                #
            if r:                                               #
                if a_10 == 0:                                   #
                    r = True                                    ##
        return r
    
    def r_mark_ylA(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_11 = None                                         ##
            r = False                                           #
            var96 = s.cursor                                    #
            for var95, var99, var98 in _a_11:                   #
                if s.starts_with(var95):                        #
                    var97 = s.cursor                            #
                    r = (not var99) or getattr(self, var99)(s)  #
                    if r:                                       # among
                      s.cursor = var97                          #
                      a_11 = var98                              #
                      break                                     #
                s.cursor = var96                                #
            if r:                                               #
                if a_11 == 0:                                   #
                    r = True                                    ##
            if r:
                r = self.r_mark_suffix_with_optional_y_consonant(s)  # routine call
        return r
    
    def r_mark_ki(self, s):
        r = True
        r = s.starts_with(u'ki')  # character check
        return r
    
    def r_mark_ncA(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_12 = None                                           ##
            r = False                                             #
            var101 = s.cursor                                     #
            for var100, var104, var103 in _a_12:                  #
                if s.starts_with(var100):                         #
                    var102 = s.cursor                             #
                    r = (not var104) or getattr(self, var104)(s)  #
                    if r:                                         # among
                      s.cursor = var102                           #
                      a_12 = var103                               #
                      break                                       #
                s.cursor = var101                                 #
            if r:                                                 #
                if a_12 == 0:                                     #
                    r = True                                      ##
            if r:
                r = self.r_mark_suffix_with_optional_n_consonant(s)  # routine call
        return r
    
    def r_mark_yUm(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_13 = None                                           ##
            r = False                                             #
            var106 = s.cursor                                     #
            for var105, var109, var108 in _a_13:                  #
                if s.starts_with(var105):                         #
                    var107 = s.cursor                             #
                    r = (not var109) or getattr(self, var109)(s)  #
                    if r:                                         # among
                      s.cursor = var107                           #
                      a_13 = var108                               #
                      break                                       #
                s.cursor = var106                                 #
            if r:                                                 #
                if a_13 == 0:                                     #
                    r = True                                      ##
            if r:
                r = self.r_mark_suffix_with_optional_y_consonant(s)  # routine call
        return r
    
    def r_mark_sUn(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_14 = None                                           ##
            r = False                                             #
            var111 = s.cursor                                     #
            for var110, var114, var113 in _a_14:                  #
                if s.starts_with(var110):                         #
                    var112 = s.cursor                             #
                    r = (not var114) or getattr(self, var114)(s)  #
                    if r:                                         # among
                      s.cursor = var112                           #
                      a_14 = var113                               #
                      break                                       #
                s.cursor = var111                                 #
            if r:                                                 #
                if a_14 == 0:                                     #
                    r = True                                      ##
        return r
    
    def r_mark_yUz(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_15 = None                                           ##
            r = False                                             #
            var116 = s.cursor                                     #
            for var115, var119, var118 in _a_15:                  #
                if s.starts_with(var115):                         #
                    var117 = s.cursor                             #
                    r = (not var119) or getattr(self, var119)(s)  #
                    if r:                                         # among
                      s.cursor = var117                           #
                      a_15 = var118                               #
                      break                                       #
                s.cursor = var116                                 #
            if r:                                                 #
                if a_15 == 0:                                     #
                    r = True                                      ##
            if r:
                r = self.r_mark_suffix_with_optional_y_consonant(s)  # routine call
        return r
    
    def r_mark_sUnUz(self, s):
        r = True
        a_16 = None                                           ##
        r = False                                             #
        var121 = s.cursor                                     #
        for var120, var124, var123 in _a_16:                  #
            if s.starts_with(var120):                         #
                var122 = s.cursor                             #
                r = (not var124) or getattr(self, var124)(s)  #
                if r:                                         # among
                  s.cursor = var122                           #
                  a_16 = var123                               #
                  break                                       #
            s.cursor = var121                                 #
        if r:                                                 #
            if a_16 == 0:                                     #
                r = True                                      ##
        return r
    
    def r_mark_lAr(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_17 = None                                           ##
            r = False                                             #
            var126 = s.cursor                                     #
            for var125, var129, var128 in _a_17:                  #
                if s.starts_with(var125):                         #
                    var127 = s.cursor                             #
                    r = (not var129) or getattr(self, var129)(s)  #
                    if r:                                         # among
                      s.cursor = var127                           #
                      a_17 = var128                               #
                      break                                       #
                s.cursor = var126                                 #
            if r:                                                 #
                if a_17 == 0:                                     #
                    r = True                                      ##
        return r
    
    def r_mark_nUz(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_18 = None                                           ##
            r = False                                             #
            var131 = s.cursor                                     #
            for var130, var134, var133 in _a_18:                  #
                if s.starts_with(var130):                         #
                    var132 = s.cursor                             #
                    r = (not var134) or getattr(self, var134)(s)  #
                    if r:                                         # among
                      s.cursor = var132                           #
                      a_18 = var133                               #
                      break                                       #
                s.cursor = var131                                 #
            if r:                                                 #
                if a_18 == 0:                                     #
                    r = True                                      ##
        return r
    
    def r_mark_DUr(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_19 = None                                           ##
            r = False                                             #
            var136 = s.cursor                                     #
            for var135, var139, var138 in _a_19:                  #
                if s.starts_with(var135):                         #
                    var137 = s.cursor                             #
                    r = (not var139) or getattr(self, var139)(s)  #
                    if r:                                         # among
                      s.cursor = var137                           #
                      a_19 = var138                               #
                      break                                       #
                s.cursor = var136                                 #
            if r:                                                 #
                if a_19 == 0:                                     #
                    r = True                                      ##
        return r
    
    def r_mark_cAsInA(self, s):
        r = True
        a_20 = None                                           ##
        r = False                                             #
        var141 = s.cursor                                     #
        for var140, var144, var143 in _a_20:                  #
            if s.starts_with(var140):                         #
                var142 = s.cursor                             #
                r = (not var144) or getattr(self, var144)(s)  #
                if r:                                         # among
                  s.cursor = var142                           #
                  a_20 = var143                               #
                  break                                       #
            s.cursor = var141                                 #
        if r:                                                 #
            if a_20 == 0:                                     #
                r = True                                      ##
        return r
    
    def r_mark_yDU(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_21 = None                                           ##
            r = False                                             #
            var146 = s.cursor                                     #
            for var145, var149, var148 in _a_21:                  #
                if s.starts_with(var145):                         #
                    var147 = s.cursor                             #
                    r = (not var149) or getattr(self, var149)(s)  #
                    if r:                                         # among
                      s.cursor = var147                           #
                      a_21 = var148                               #
                      break                                       #
                s.cursor = var146                                 #
            if r:                                                 #
                if a_21 == 0:                                     #
                    r = True                                      ##
            if r:
                r = self.r_mark_suffix_with_optional_y_consonant(s)  # routine call
        return r
    
    def r_mark_ysA(self, s):
        r = True
        a_22 = None                                           ##
        r = False                                             #
        var151 = s.cursor                                     #
        for var150, var154, var153 in _a_22:                  #
            if s.starts_with(var150):                         #
                var152 = s.cursor                             #
                r = (not var154) or getattr(self, var154)(s)  #
                if r:                                         # among
                  s.cursor = var152                           #
                  a_22 = var153                               #
                  break                                       #
            s.cursor = var151                                 #
        if r:                                                 #
            if a_22 == 0:                                     #
                r = True                                      ##
        if r:
            r = self.r_mark_suffix_with_optional_y_consonant(s)  # routine call
        return r
    
    def r_mark_ymUs_(self, s):
        r = True
        r = self.r_check_vowel_harmony(s)  # routine call
        if r:
            a_23 = None                                           ##
            r = False                                             #
            var156 = s.cursor                                     #
            for var155, var159, var158 in _a_23:                  #
                if s.starts_with(var155):                         #
                    var157 = s.cursor                             #
                    r = (not var159) or getattr(self, var159)(s)  #
                    if r:                                         # among
                      s.cursor = var157                           #
                      a_23 = var158                               #
                      break                                       #
                s.cursor = var156                                 #
            if r:                                                 #
                if a_23 == 0:                                     #
                    r = True                                      ##
            if r:
                r = self.r_mark_suffix_with_optional_y_consonant(s)  # routine call
        return r
    
    def r_mark_yken(self, s):
        r = True
        r = s.starts_with(u'ken')  # character check
        if r:
            r = self.r_mark_suffix_with_optional_y_consonant(s)  # routine call
        return r
    
    def r_stem_nominal_verb_suffixes(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            self.b_continue_stemming_noun_suffixes = True  ##
            r = True                                       ## set
            if r:
                var187 = len(s) - s.cursor                                                                                 ##
                var180 = len(s) - s.cursor                                                                           ##    #
                var175 = len(s) - s.cursor                                                                     ##    #     #
                var173 = len(s) - s.cursor                                                               ##    #     #     #
                var168 = len(s) - s.cursor                                                        ##     #     #     #     #
                var162 = len(s) - s.cursor                              ##                        #      #     #     #     #
                var161 = len(s) - s.cursor                        ##    #                         #      #     #     #     #
                var160 = len(s) - s.cursor                  ##    #     #                         #      #     #     #     #
                r = self.r_mark_ymUs_(s)  # routine call    #     #     #                         #      #     #     #     #
                if not r:                                   # or  #     #                         #      #     #     #     #
                    s.cursor = len(s) - var160              #     # or  #                         #      #     #     #     #
                    r = self.r_mark_yDU(s)  # routine call  ##    #     # or                      #      #     #     #     #
                if not r:                                         #     #                         #      #     #     #     #
                    s.cursor = len(s) - var161                    #     #                         #      #     #     #     #
                    r = self.r_mark_ysA(s)  # routine call        ##    #                         #      #     #     #     #
                if not r:                                               #                         #      #     #     #     #
                    s.cursor = len(s) - var162                          #                         #      #     #     #     #
                    r = self.r_mark_yken(s)  # routine call             ##                        #      #     #     #     #
                if not r:                                                                         #      #     #     #     #
                    s.cursor = len(s) - var168                                                    #      #     #     #     #
                    r = self.r_mark_cAsInA(s)  # routine call                                     #      #     #     #     #
                    if r:                                                                         #      #     #     #     #
                        var167 = len(s) - s.cursor                                          ##    #      #     #     #     #
                        var166 = len(s) - s.cursor                                    ##    #     #      #     #     #     #
                        var165 = len(s) - s.cursor                              ##    #     #     # or   #     #     #     #
                        var164 = len(s) - s.cursor                        ##    #     #     #     #      #     #     #     #
                        var163 = len(s) - s.cursor                  ##    #     #     #     #     #      #     #     #     #
                        r = self.r_mark_sUnUz(s)  # routine call    #     #     #     #     #     #      #     #     #     #
                        if not r:                                   # or  #     #     #     #     #      #     #     #     #
                            s.cursor = len(s) - var163              #     # or  #     #     #     #      #     #     #     #
                            r = self.r_mark_lAr(s)  # routine call  ##    #     # or  #     #     #      #     #     #     #
                        if not r:                                         #     #     # or  #     #      #     #     #     #
                            s.cursor = len(s) - var164                    #     #     #     # or  #      #     #     #     #
                            r = self.r_mark_yUm(s)  # routine call        ##    #     #     #     #      #     #     #     #
                        if not r:                                               #     #     #     #      #     #     #     #
                            s.cursor = len(s) - var165                          #     #     #     #      #     #     #     #
                            r = self.r_mark_sUn(s)  # routine call              ##    #     #     #      #     #     #     #
                        if not r:                                                     #     #     #      #     #     #     #
                            s.cursor = len(s) - var166                                #     #     #      #     #     #     #
                            r = self.r_mark_yUz(s)  # routine call                    ##    #     #      #     #     #     #
                        if not r:                                                           #     #      # or  #     #     #
                            s.cursor = len(s) - var167                                      #     #      #     #     #     #
                            r = True  # true                                                ##    #      #     #     #     #
                        if r:                                                                     #      #     #     #     #
                            r = self.r_mark_ymUs_(s)  # routine call                              ##     #     # or  #     #
                if not r:                                                                                #     #     #     #
                    s.cursor = len(s) - var173                                                           #     #     #     #
                    r = self.r_mark_lAr(s)  # routine call                                               #     #     #     #
                    if r:                                                                                #     #     #     #
                        self.right = s.cursor  ##                                                        #     #     #     #
                        r = True               ## ]                                                      #     #     #     #
                        if r:                                                                            #     #     #     #
                            r = s.set_range(self.left, self.right, u'')  # delete                        #     #     #     #
                            if r:                                                                        #     #     #     #
                                var172 = len(s) - s.cursor                                        ##     #     #     #     #
                                self.left = s.cursor  ##                                          #      #     #     #     #
                                r = True              ## [                                        #      #     #     #     #
                                if r:                                                             #      #     #     #     #
                                    var171 = len(s) - s.cursor                              ##    #      #     #     # or  #
                                    var170 = len(s) - s.cursor                        ##    #     #      #     #     #     #
                                    var169 = len(s) - s.cursor                  ##    #     #     #      #     #     #     #
                                    r = self.r_mark_DUr(s)  # routine call      #     #     #     #      #     #     #     #
                                    if not r:                                   # or  #     #     #      #     #     #     #
                                        s.cursor = len(s) - var169              #     # or  #     #      #     #     #     #
                                        r = self.r_mark_yDU(s)  # routine call  ##    #     # or  # try  #     #     #     #
                                    if not r:                                         #     #     #      #     #     #     #
                                        s.cursor = len(s) - var170                    #     #     #      #     #     #     #
                                        r = self.r_mark_ysA(s)  # routine call        ##    #     #      #     #     #     #
                                    if not r:                                               #     #      #     #     #     #
                                        s.cursor = len(s) - var171                          #     #      #     #     #     #
                                        r = self.r_mark_ymUs_(s)  # routine call            ##    #      #     #     #     #
                                if not r:                                                         #      #     #     #     #
                                    r = True                                                      #      #     #     #     #
                                    s.cursor = len(s) - var172                                    ##     #     #     #     #
                                if r:                                                                    #     #     #     #
                                    self.b_continue_stemming_noun_suffixes = False  ##                   #     #     #     #
                                    r = True                                        ## unset             ##    #     #     #
                if not r:                                                                                      #     #     # or
                    s.cursor = len(s) - var175                                                                 #     #     #
                    r = self.r_mark_nUz(s)  # routine call                                                     #     #     #
                    if r:                                                                                      #     #     #
                        var174 = len(s) - s.cursor                  ##                                         #     #     #
                        r = self.r_mark_yDU(s)  # routine call      #                                          #     #     #
                        if not r:                                   # or                                       #     #     #
                            s.cursor = len(s) - var174              #                                          #     #     #
                            r = self.r_mark_ysA(s)  # routine call  ##                                         ##    #     #
                if not r:                                                                                            #     #
                    s.cursor = len(s) - var180                                                                       #     #
                    var178 = len(s) - s.cursor                              ##                                       #     #
                    var177 = len(s) - s.cursor                        ##    #                                        #     #
                    var176 = len(s) - s.cursor                  ##    #     #                                        #     #
                    r = self.r_mark_sUnUz(s)  # routine call    #     #     #                                        #     #
                    if not r:                                   # or  #     #                                        #     #
                        s.cursor = len(s) - var176              #     # or  #                                        #     #
                        r = self.r_mark_yUz(s)  # routine call  ##    #     # or                                     #     #
                    if not r:                                         #     #                                        #     #
                        s.cursor = len(s) - var177                    #     #                                        #     #
                        r = self.r_mark_sUn(s)  # routine call        ##    #                                        #     #
                    if not r:                                               #                                        #     #
                        s.cursor = len(s) - var178                          #                                        #     #
                        r = self.r_mark_yUm(s)  # routine call              ##                                       #     #
                    if r:                                                                                            #     #
                        self.right = s.cursor  ##                                                                    #     #
                        r = True               ## ]                                                                  #     #
                        if r:                                                                                        #     #
                            r = s.set_range(self.left, self.right, u'')  # delete                                    #     #
                            if r:                                                                                    #     #
                                var179 = len(s) - s.cursor                    ##                                     #     #
                                self.left = s.cursor  ##                      #                                      #     #
                                r = True              ## [                    #                                      #     #
                                if r:                                         #                                      #     #
                                    r = self.r_mark_ymUs_(s)  # routine call  # try                                  #     #
                                if not r:                                     #                                      #     #
                                    r = True                                  #                                      #     #
                                    s.cursor = len(s) - var179                ##                                     ##    #
                if not r:                                                                                                  #
                    s.cursor = len(s) - var187                                                                             #
                    r = self.r_mark_DUr(s)  # routine call                                                                 #
                    if r:                                                                                                  #
                        self.right = s.cursor  ##                                                                          #
                        r = True               ## ]                                                                        #
                        if r:                                                                                              #
                            r = s.set_range(self.left, self.right, u'')  # delete                                          #
                            if r:                                                                                          #
                                var186 = len(s) - s.cursor                                                    ##           #
                                self.left = s.cursor  ##                                                      #            #
                                r = True              ## [                                                    #            #
                                if r:                                                                         #            #
                                    var185 = len(s) - s.cursor                                          ##    #            #
                                    var184 = len(s) - s.cursor                                    ##    #     #            #
                                    var183 = len(s) - s.cursor                              ##    #     #     #            #
                                    var182 = len(s) - s.cursor                        ##    #     #     #     #            #
                                    var181 = len(s) - s.cursor                  ##    #     #     #     #     #            #
                                    r = self.r_mark_sUnUz(s)  # routine call    #     #     #     #     #     #            #
                                    if not r:                                   # or  #     #     #     #     #            #
                                        s.cursor = len(s) - var181              #     # or  #     #     #     #            #
                                        r = self.r_mark_lAr(s)  # routine call  ##    #     # or  #     #     #            #
                                    if not r:                                         #     #     # or  #     #            #
                                        s.cursor = len(s) - var182                    #     #     #     # or  #            #
                                        r = self.r_mark_yUm(s)  # routine call        ##    #     #     #     # try        #
                                    if not r:                                               #     #     #     #            #
                                        s.cursor = len(s) - var183                          #     #     #     #            #
                                        r = self.r_mark_sUn(s)  # routine call              ##    #     #     #            #
                                    if not r:                                                     #     #     #            #
                                        s.cursor = len(s) - var184                                #     #     #            #
                                        r = self.r_mark_yUz(s)  # routine call                    ##    #     #            #
                                    if not r:                                                           #     #            #
                                        s.cursor = len(s) - var185                                      #     #            #
                                        r = True  # true                                                ##    #            #
                                    if r:                                                                     #            #
                                        r = self.r_mark_ymUs_(s)  # routine call                              #            #
                                if not r:                                                                     #            #
                                    r = True                                                                  #            #
                                    s.cursor = len(s) - var186                                                ##           ##
                if r:
                    self.right = s.cursor  ##
                    r = True               ## ]
                    if r:
                        r = s.set_range(self.left, self.right, u'')  # delete
        return r
    
    def r_stem_suffix_chain_before_ki(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            r = self.r_mark_ki(s)  # routine call
            if r:
                var201 = len(s) - s.cursor                                                                                                                         ##
                var197 = len(s) - s.cursor                                                                                                                   ##    #
                r = self.r_mark_DA(s)  # routine call                                                                                                        #     #
                if r:                                                                                                                                        #     #
                    self.right = s.cursor  ##                                                                                                                #     #
                    r = True               ## ]                                                                                                              #     #
                    if r:                                                                                                                                    #     #
                        r = s.set_range(self.left, self.right, u'')  # delete                                                                                #     #
                        if r:                                                                                                                                #     #
                            var191 = len(s) - s.cursor                                                                                  ##                   #     #
                            self.left = s.cursor  ##                                                                                    #                    #     #
                            r = True              ## [                                                                                  #                    #     #
                            if r:                                                                                                       #                    #     #
                                var190 = len(s) - s.cursor                                                                        ##    #                    #     #
                                r = self.r_mark_lAr(s)  # routine call                                                            #     #                    #     #
                                if r:                                                                                             #     #                    #     #
                                    self.right = s.cursor  ##                                                                     #     #                    #     #
                                    r = True               ## ]                                                                   #     #                    #     #
                                    if r:                                                                                         #     #                    #     #
                                        r = s.set_range(self.left, self.right, u'')  # delete                                     #     #                    #     #
                                        if r:                                                                                     #     #                    #     #
                                            var188 = len(s) - s.cursor                                 ##                         #     #                    #     #
                                            r = self.r_stem_suffix_chain_before_ki(s)  # routine call  #                          #     #                    #     #
                                            if not r:                                                  # try                      #     #                    #     #
                                                r = True                                               #                          #     #                    #     #
                                                s.cursor = len(s) - var188                             ##                         #     #                    #     #
                                if not r:                                                                                         #     #                    #     #
                                    s.cursor = len(s) - var190                                                                    #     #                    #     #
                                    r = self.r_mark_possessives(s)  # routine call                                                #     #                    #     #
                                    if r:                                                                                         #     #                    #     #
                                        self.right = s.cursor  ##                                                                 #     #                    #     #
                                        r = True               ## ]                                                               # or  # try                #     #
                                        if r:                                                                                     #     #                    #     #
                                            r = s.set_range(self.left, self.right, u'')  # delete                                 #     #                    #     #
                                            if r:                                                                                 #     #                    #     #
                                                var189 = len(s) - s.cursor                                                 ##     #     #                    #     #
                                                self.left = s.cursor  ##                                                   #      #     #                    #     #
                                                r = True              ## [                                                 #      #     #                    #     #
                                                if r:                                                                      #      #     #                    #     #
                                                    r = self.r_mark_lAr(s)  # routine call                                 #      #     #                    #     #
                                                    if r:                                                                  #      #     #                    #     #
                                                        self.right = s.cursor  ##                                          #      #     #                    #     #
                                                        r = True               ## ]                                        # try  #     #                    #     #
                                                        if r:                                                              #      #     #                    #     #
                                                            r = s.set_range(self.left, self.right, u'')  # delete          #      #     #                    #     #
                                                            if r:                                                          #      #     #                    #     #
                                                                r = self.r_stem_suffix_chain_before_ki(s)  # routine call  #      #     #                    #     #
                                                if not r:                                                                  #      #     #                    #     #
                                                    r = True                                                               #      #     #                    #     #
                                                    s.cursor = len(s) - var189                                             ##     ##    #                    #     #
                            if not r:                                                                                                   #                    #     #
                                r = True                                                                                                #                    #     #
                                s.cursor = len(s) - var191                                                                              ##                   #     #
                if not r:                                                                                                                                    #     #
                    s.cursor = len(s) - var197                                                                                                               #     #
                    r = self.r_mark_nUn(s)  # routine call                                                                                                   #     #
                    if r:                                                                                                                                    # or  #
                        self.right = s.cursor  ##                                                                                                            #     #
                        r = True               ## ]                                                                                                          #     #
                        if r:                                                                                                                                #     #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                                            #     #
                            if r:                                                                                                                            #     #
                                var196 = len(s) - s.cursor                                                                                            ##     #     #
                                self.left = s.cursor  ##                                                                                              #      #     #
                                r = True              ## [                                                                                            #      #     #
                                if r:                                                                                                                 #      #     #
                                    var195 = len(s) - s.cursor                                                                                  ##    #      #     #
                                    var194 = len(s) - s.cursor                                                                            ##    #     #      #     #
                                    r = self.r_mark_lArI(s)  # routine call                                                               #     #     #      #     #
                                    if r:                                                                                                 #     #     #      #     #
                                        self.right = s.cursor  ##                                                                         #     #     #      #     #
                                        r = True               ## ]                                                                       #     #     #      #     #
                                        if r:                                                                                             #     #     #      #     #
                                            r = s.set_range(self.left, self.right, u'')  # delete                                         #     #     #      #     #
                                    if not r:                                                                                             #     #     #      #     #
                                        s.cursor = len(s) - var194                                                                        #     #     #      #     # or
                                        self.left = s.cursor  ##                                                                          #     #     #      #     #
                                        r = True              ## [                                                                        #     #     #      #     #
                                        if r:                                                                                             #     #     #      #     #
                                            var192 = len(s) - s.cursor                      ##                                            #     #     #      #     #
                                            r = self.r_mark_possessives(s)  # routine call  #                                             #     #     #      #     #
                                            if not r:                                       # or                                          #     #     #      #     #
                                                s.cursor = len(s) - var192                  #                                             #     #     #      #     #
                                                r = self.r_mark_sU(s)  # routine call       ##                                            #     #     #      #     #
                                            if r:                                                                                         #     #     #      #     #
                                                self.right = s.cursor  ##                                                                 #     #     #      #     #
                                                r = True               ## ]                                                               # or  #     # try  #     #
                                                if r:                                                                                     #     # or  #      #     #
                                                    r = s.set_range(self.left, self.right, u'')  # delete                                 #     #     #      #     #
                                                    if r:                                                                                 #     #     #      #     #
                                                        var193 = len(s) - s.cursor                                                 ##     #     #     #      #     #
                                                        self.left = s.cursor  ##                                                   #      #     #     #      #     #
                                                        r = True              ## [                                                 #      #     #     #      #     #
                                                        if r:                                                                      #      #     #     #      #     #
                                                            r = self.r_mark_lAr(s)  # routine call                                 #      #     #     #      #     #
                                                            if r:                                                                  #      #     #     #      #     #
                                                                self.right = s.cursor  ##                                          #      #     #     #      #     #
                                                                r = True               ## ]                                        # try  #     #     #      #     #
                                                                if r:                                                              #      #     #     #      #     #
                                                                    r = s.set_range(self.left, self.right, u'')  # delete          #      #     #     #      #     #
                                                                    if r:                                                          #      #     #     #      #     #
                                                                        r = self.r_stem_suffix_chain_before_ki(s)  # routine call  #      #     #     #      #     #
                                                        if not r:                                                                  #      #     #     #      #     #
                                                            r = True                                                               #      #     #     #      #     #
                                                            s.cursor = len(s) - var193                                             ##     ##    #     #      #     #
                                    if not r:                                                                                                   #     #      #     #
                                        s.cursor = len(s) - var195                                                                              #     #      #     #
                                        r = self.r_stem_suffix_chain_before_ki(s)  # routine call                                               ##    #      #     #
                                if not r:                                                                                                             #      #     #
                                    r = True                                                                                                          #      #     #
                                    s.cursor = len(s) - var196                                                                                        ##     ##    #
                if not r:                                                                                                                                          #
                    s.cursor = len(s) - var201                                                                                                                     #
                    r = self.r_mark_ndA(s)  # routine call                                                                                                         #
                    if r:                                                                                                                                          #
                        var200 = len(s) - s.cursor                                                                              ##                                 #
                        var199 = len(s) - s.cursor                                                                        ##    #                                  #
                        r = self.r_mark_lArI(s)  # routine call                                                           #     #                                  #
                        if r:                                                                                             #     #                                  #
                            self.right = s.cursor  ##                                                                     #     #                                  #
                            r = True               ## ]                                                                   #     #                                  #
                            if r:                                                                                         #     #                                  #
                                r = s.set_range(self.left, self.right, u'')  # delete                                     #     #                                  #
                        if not r:                                                                                         #     #                                  #
                            s.cursor = len(s) - var199                                                                    #     #                                  #
                            r = self.r_mark_sU(s)  # routine call                                                         #     #                                  #
                            if r:                                                                                         #     #                                  #
                                self.right = s.cursor  ##                                                                 #     #                                  #
                                r = True               ## ]                                                               #     #                                  #
                                if r:                                                                                     #     #                                  #
                                    r = s.set_range(self.left, self.right, u'')  # delete                                 #     #                                  #
                                    if r:                                                                                 # or  #                                  #
                                        var198 = len(s) - s.cursor                                                 ##     #     # or                               #
                                        self.left = s.cursor  ##                                                   #      #     #                                  #
                                        r = True              ## [                                                 #      #     #                                  #
                                        if r:                                                                      #      #     #                                  #
                                            r = self.r_mark_lAr(s)  # routine call                                 #      #     #                                  #
                                            if r:                                                                  #      #     #                                  #
                                                self.right = s.cursor  ##                                          #      #     #                                  #
                                                r = True               ## ]                                        # try  #     #                                  #
                                                if r:                                                              #      #     #                                  #
                                                    r = s.set_range(self.left, self.right, u'')  # delete          #      #     #                                  #
                                                    if r:                                                          #      #     #                                  #
                                                        r = self.r_stem_suffix_chain_before_ki(s)  # routine call  #      #     #                                  #
                                        if not r:                                                                  #      #     #                                  #
                                            r = True                                                               #      #     #                                  #
                                            s.cursor = len(s) - var198                                             ##     ##    #                                  #
                        if not r:                                                                                               #                                  #
                            s.cursor = len(s) - var200                                                                          #                                  #
                            r = self.r_stem_suffix_chain_before_ki(s)  # routine call                                           ##                                 ##
        return r
    
    def r_stem_noun_suffixes(self, s):
        r = True
        var241 = len(s) - s.cursor                                                                                                                                                                   ##
        var238 = len(s) - s.cursor                                                                                                                                                             ##    #
        var232 = len(s) - s.cursor                                                                                                                                                       ##    #     #
        var231 = len(s) - s.cursor                                                                                                                                                 ##    #     #     #
        var230 = len(s) - s.cursor                                                                                                                                           ##    #     #     #     #
        var223 = len(s) - s.cursor                                                                                                                                     ##    #     #     #     #     #
        var217 = len(s) - s.cursor                                                                                                                               ##    #     #     #     #     #     #
        var213 = len(s) - s.cursor                                                                                                                         ##    #     #     #     #     #     #     #
        var208 = len(s) - s.cursor                                                                                                                   ##    #     #     #     #     #     #     #     #
        self.left = s.cursor  ##                                                                                                                     #     #     #     #     #     #     #     #     #
        r = True              ## [                                                                                                                   #     #     #     #     #     #     #     #     #
        if r:                                                                                                                                        #     #     #     #     #     #     #     #     #
            r = self.r_mark_lAr(s)  # routine call                                                                                                   #     #     #     #     #     #     #     #     #
            if r:                                                                                                                                    #     #     #     #     #     #     #     #     #
                self.right = s.cursor  ##                                                                                                            #     #     #     #     #     #     #     #     #
                r = True               ## ]                                                                                                          #     #     #     #     #     #     #     #     #
                if r:                                                                                                                                #     #     #     #     #     #     #     #     #
                    r = s.set_range(self.left, self.right, u'')  # delete                                                                            #     #     #     #     #     #     #     #     #
                    if r:                                                                                                                            #     #     #     #     #     #     #     #     #
                        var202 = len(s) - s.cursor                                 ##                                                                #     #     #     #     #     #     #     #     #
                        r = self.r_stem_suffix_chain_before_ki(s)  # routine call  #                                                                 #     #     #     #     #     #     #     #     #
                        if not r:                                                  # try                                                             #     #     #     #     #     #     #     #     #
                            r = True                                               #                                                                 #     #     #     #     #     #     #     #     #
                            s.cursor = len(s) - var202                             ##                                                                #     #     #     #     #     #     #     #     #
        if not r:                                                                                                                                    #     #     #     #     #     #     #     #     #
            s.cursor = len(s) - var208                                                                                                               #     #     #     #     #     #     #     #     #
            self.left = s.cursor  ##                                                                                                                 #     #     #     #     #     #     #     #     #
            r = True              ## [                                                                                                               #     #     #     #     #     #     #     #     #
            if r:                                                                                                                                    #     #     #     #     #     #     #     #     #
                r = self.r_mark_ncA(s)  # routine call                                                                                               #     #     #     #     #     #     #     #     #
                if r:                                                                                                                                #     #     #     #     #     #     #     #     #
                    self.right = s.cursor  ##                                                                                                        #     #     #     #     #     #     #     #     #
                    r = True               ## ]                                                                                                      #     #     #     #     #     #     #     #     #
                    if r:                                                                                                                            #     #     #     #     #     #     #     #     #
                        r = s.set_range(self.left, self.right, u'')  # delete                                                                        #     #     #     #     #     #     #     #     #
                        if r:                                                                                                                        #     #     #     #     #     #     #     #     #
                            var207 = len(s) - s.cursor                                                                                        ##     #     #     #     #     #     #     #     #     #
                            var206 = len(s) - s.cursor                                                                                  ##    #      #     #     #     #     #     #     #     #     #
                            var205 = len(s) - s.cursor                                                                            ##    #     #      #     #     #     #     #     #     #     #     #
                            self.left = s.cursor  ##                                                                              #     #     #      #     #     #     #     #     #     #     #     #
                            r = True              ## [                                                                            #     #     #      #     #     #     #     #     #     #     #     #
                            if r:                                                                                                 #     #     #      #     #     #     #     #     #     #     #     #
                                r = self.r_mark_lArI(s)  # routine call                                                           #     #     #      #     #     #     #     #     #     #     #     #
                                if r:                                                                                             #     #     #      #     #     #     #     #     #     #     #     #
                                    self.right = s.cursor  ##                                                                     #     #     #      #     #     #     #     #     #     #     #     #
                                    r = True               ## ]                                                                   #     #     #      #     #     #     #     #     #     #     #     #
                                    if r:                                                                                         #     #     #      #     #     #     #     #     #     #     #     #
                                        r = s.set_range(self.left, self.right, u'')  # delete                                     #     #     #      #     #     #     #     #     #     #     #     #
                            if not r:                                                                                             #     #     #      #     #     #     #     #     #     #     #     #
                                s.cursor = len(s) - var205                                                                        #     #     #      #     #     #     #     #     #     #     #     #
                                self.left = s.cursor  ##                                                                          #     #     #      #     #     #     #     #     #     #     #     #
                                r = True              ## [                                                                        #     #     #      # or  #     #     #     #     #     #     #     #
                                if r:                                                                                             #     #     #      #     #     #     #     #     #     #     #     #
                                    var203 = len(s) - s.cursor                      ##                                            #     #     #      #     #     #     #     #     #     #     #     #
                                    r = self.r_mark_possessives(s)  # routine call  #                                             #     #     #      #     #     #     #     #     #     #     #     #
                                    if not r:                                       # or                                          #     #     #      #     #     #     #     #     #     #     #     #
                                        s.cursor = len(s) - var203                  #                                             #     #     #      #     #     #     #     #     #     #     #     #
                                        r = self.r_mark_sU(s)  # routine call       ##                                            #     #     #      #     #     #     #     #     #     #     #     #
                                    if r:                                                                                         # or  #     #      #     #     #     #     #     #     #     #     #
                                        self.right = s.cursor  ##                                                                 #     #     #      #     #     #     #     #     #     #     #     #
                                        r = True               ## ]                                                               #     #     #      #     #     #     #     #     #     #     #     #
                                        if r:                                                                                     #     #     #      #     #     #     #     #     #     #     #     #
                                            r = s.set_range(self.left, self.right, u'')  # delete                                 #     #     #      #     #     #     #     #     #     #     #     #
                                            if r:                                                                                 #     #     #      #     #     #     #     #     #     #     #     #
                                                var204 = len(s) - s.cursor                                                 ##     #     # or  #      #     #     #     #     #     #     #     #     #
                                                self.left = s.cursor  ##                                                   #      #     #     # try  #     #     #     #     #     #     #     #     #
                                                r = True              ## [                                                 #      #     #     #      #     #     #     #     #     #     #     #     #
                                                if r:                                                                      #      #     #     #      #     #     #     #     #     #     #     #     #
                                                    r = self.r_mark_lAr(s)  # routine call                                 #      #     #     #      #     #     #     #     #     #     #     #     #
                                                    if r:                                                                  #      #     #     #      #     #     #     #     #     #     #     #     #
                                                        self.right = s.cursor  ##                                          #      #     #     #      #     #     #     #     #     #     #     #     #
                                                        r = True               ## ]                                        # try  #     #     #      #     #     #     #     #     #     #     #     #
                                                        if r:                                                              #      #     #     #      #     #     #     #     #     #     #     #     #
                                                            r = s.set_range(self.left, self.right, u'')  # delete          #      #     #     #      #     #     #     #     #     #     #     #     #
                                                            if r:                                                          #      #     #     #      #     # or  #     #     #     #     #     #     #
                                                                r = self.r_stem_suffix_chain_before_ki(s)  # routine call  #      #     #     #      #     #     #     #     #     #     #     #     #
                                                if not r:                                                                  #      #     #     #      #     #     #     #     #     #     #     #     #
                                                    r = True                                                               #      #     #     #      #     #     #     #     #     #     #     #     #
                                                    s.cursor = len(s) - var204                                             ##     ##    #     #      #     #     #     #     #     #     #     #     #
                            if not r:                                                                                                   #     #      #     #     #     #     #     #     #     #     #
                                s.cursor = len(s) - var206                                                                              #     #      #     #     #     #     #     #     #     #     #
                                self.left = s.cursor  ##                                                                                #     #      #     #     #     #     #     #     #     #     #
                                r = True              ## [                                                                              #     #      #     #     #     #     #     #     #     #     #
                                if r:                                                                                                   #     #      #     #     #     #     #     #     #     #     #
                                    r = self.r_mark_lAr(s)  # routine call                                                              #     #      #     #     #     #     #     #     #     #     #
                                    if r:                                                                                               #     #      #     #     #     #     #     #     #     #     #
                                        self.right = s.cursor  ##                                                                       #     #      #     #     #     #     #     #     #     #     #
                                        r = True               ## ]                                                                     #     #      #     #     #     #     #     #     #     #     #
                                        if r:                                                                                           #     #      #     #     #     #     #     #     #     #     #
                                            r = s.set_range(self.left, self.right, u'')  # delete                                       #     #      #     #     #     #     #     #     #     #     #
                                            if r:                                                                                       #     #      #     #     #     #     #     #     #     #     #
                                                r = self.r_stem_suffix_chain_before_ki(s)  # routine call                               ##    #      #     #     #     #     #     #     #     #     #
                            if not r:                                                                                                         #      #     #     # or  #     #     #     #     #     #
                                r = True                                                                                                      #      #     #     #     #     #     #     #     #     #
                                s.cursor = len(s) - var207                                                                                    ##     ##    #     #     #     #     #     #     #     #
        if not r:                                                                                                                                          #     #     #     #     #     #     #     #
            s.cursor = len(s) - var213                                                                                                                     #     #     #     #     #     #     #     #
            self.left = s.cursor  ##                                                                                                                       #     #     #     #     #     #     #     #
            r = True              ## [                                                                                                                     #     #     #     #     #     #     #     #
            if r:                                                                                                                                          #     #     #     #     #     #     #     #
                var209 = len(s) - s.cursor                 ##                                                                                              #     #     #     #     #     #     #     #
                r = self.r_mark_ndA(s)  # routine call     #                                                                                               #     #     #     #     #     #     #     #
                if not r:                                  # or                                                                                            #     #     #     #     #     #     #     #
                    s.cursor = len(s) - var209             #                                                                                               #     #     #     #     #     #     #     #
                    r = self.r_mark_nA(s)  # routine call  ##                                                                                              #     #     #     #     #     #     #     #
                if r:                                                                                                                                      #     #     #     #     #     #     #     #
                    var212 = len(s) - s.cursor                                                                              ##                             #     #     #     #     #     #     #     #
                    var211 = len(s) - s.cursor                                                                        ##    #                              #     #     #     #     #     #     #     #
                    r = self.r_mark_lArI(s)  # routine call                                                           #     #                              #     #     #     #     #     #     #     #
                    if r:                                                                                             #     #                              #     #     #     #     #     #     #     #
                        self.right = s.cursor  ##                                                                     #     #                              #     #     #     #     #     #     #     #
                        r = True               ## ]                                                                   #     #                              #     #     #     #     #     #     #     #
                        if r:                                                                                         #     #                              #     #     #     #     #     #     #     #
                            r = s.set_range(self.left, self.right, u'')  # delete                                     #     #                              #     #     #     #     #     #     #     #
                    if not r:                                                                                         #     #                              #     #     #     #     #     #     #     #
                        s.cursor = len(s) - var211                                                                    #     #                              #     #     #     #     #     #     #     #
                        r = self.r_mark_sU(s)  # routine call                                                         #     #                              #     #     #     #     #     #     #     #
                        if r:                                                                                         #     #                              #     #     #     #     #     #     #     #
                            self.right = s.cursor  ##                                                                 #     #                              #     #     #     #     #     #     #     #
                            r = True               ## ]                                                               #     #                              #     #     #     #     #     #     #     #
                            if r:                                                                                     #     #                              #     #     #     #     #     #     #     #
                                r = s.set_range(self.left, self.right, u'')  # delete                                 #     #                              #     #     # or  #     #     #     #     #
                                if r:                                                                                 # or  #                              #     #     #     #     #     #     #     #
                                    var210 = len(s) - s.cursor                                                 ##     #     # or                           #     #     #     #     #     #     #     #
                                    self.left = s.cursor  ##                                                   #      #     #                              #     #     #     #     #     #     #     #
                                    r = True              ## [                                                 #      #     #                              #     #     #     #     #     #     #     #
                                    if r:                                                                      #      #     #                              #     #     #     #     #     #     #     #
                                        r = self.r_mark_lAr(s)  # routine call                                 #      #     #                              #     #     #     #     #     #     #     #
                                        if r:                                                                  #      #     #                              #     #     #     #     #     #     #     #
                                            self.right = s.cursor  ##                                          #      #     #                              #     #     #     #     #     #     #     #
                                            r = True               ## ]                                        # try  #     #                              #     #     #     #     #     #     #     #
                                            if r:                                                              #      #     #                              #     #     #     #     #     #     #     #
                                                r = s.set_range(self.left, self.right, u'')  # delete          #      #     #                              #     #     #     #     #     #     #     #
                                                if r:                                                          #      #     #                              #     #     #     #     #     #     #     #
                                                    r = self.r_stem_suffix_chain_before_ki(s)  # routine call  #      #     #                              #     #     #     #     #     #     #     #
                                    if not r:                                                                  #      #     #                              #     #     #     #     #     #     #     #
                                        r = True                                                               #      #     #                              #     #     #     #     #     #     #     #
                                        s.cursor = len(s) - var210                                             ##     ##    #                              #     #     #     #     #     #     #     #
                    if not r:                                                                                               #                              #     #     #     #     #     #     #     #
                        s.cursor = len(s) - var212                                                                          #                              #     #     #     #     #     #     #     #
                        r = self.r_stem_suffix_chain_before_ki(s)  # routine call                                           ##                             ##    #     #     #     #     #     #     #
        if not r:                                                                                                                                                #     #     #     #     #     #     #
            s.cursor = len(s) - var217                                                                                                                           #     #     #     #     #     #     #
            self.left = s.cursor  ##                                                                                                                             #     #     #     #     #     #     #
            r = True              ## [                                                                                                                           #     #     #     #     #     #     #
            if r:                                                                                                                                                #     #     #     #     #     #     #
                var214 = len(s) - s.cursor                 ##                                                                                                    #     #     #     #     #     #     #
                r = self.r_mark_ndAn(s)  # routine call    #                                                                                                     #     #     #     #     #     #     #
                if not r:                                  # or                                                                                                  #     #     #     #     #     #     #
                    s.cursor = len(s) - var214             #                                                                                                     #     #     #     #     #     #     #
                    r = self.r_mark_nU(s)  # routine call  ##                                                                                                    #     #     #     #     #     #     #
                if r:                                                                                                                                            #     #     #     #     #     #     #
                    var216 = len(s) - s.cursor                                                                    ##                                             #     #     #     #     #     #     #
                    r = self.r_mark_sU(s)  # routine call                                                         #                                              #     #     #     #     #     #     #
                    if r:                                                                                         #                                              #     #     # or  #     #     #     #
                        self.right = s.cursor  ##                                                                 #                                              #     #     #     #     #     #     #
                        r = True               ## ]                                                               #                                              #     #     #     #     #     #     #
                        if r:                                                                                     #                                              #     #     #     #     #     #     #
                            r = s.set_range(self.left, self.right, u'')  # delete                                 #                                              #     #     #     #     #     #     #
                            if r:                                                                                 #                                              #     #     #     # or  #     #     #
                                var215 = len(s) - s.cursor                                                 ##     #                                              #     #     #     #     # or  #     #
                                self.left = s.cursor  ##                                                   #      #                                              #     #     #     #     #     #     #
                                r = True              ## [                                                 #      #                                              #     #     #     #     #     #     #
                                if r:                                                                      #      #                                              #     #     #     #     #     #     #
                                    r = self.r_mark_lAr(s)  # routine call                                 #      #                                              #     #     #     #     #     #     #
                                    if r:                                                                  #      # or                                           #     #     #     #     #     #     #
                                        self.right = s.cursor  ##                                          #      #                                              #     #     #     #     #     #     #
                                        r = True               ## ]                                        # try  #                                              #     #     #     #     #     #     #
                                        if r:                                                              #      #                                              #     #     #     #     #     #     #
                                            r = s.set_range(self.left, self.right, u'')  # delete          #      #                                              #     #     #     #     #     #     #
                                            if r:                                                          #      #                                              #     #     #     #     #     #     #
                                                r = self.r_stem_suffix_chain_before_ki(s)  # routine call  #      #                                              #     #     #     #     #     #     #
                                if not r:                                                                  #      #                                              #     #     #     #     #     #     #
                                    r = True                                                               #      #                                              #     #     #     #     #     #     #
                                    s.cursor = len(s) - var215                                             ##     #                                              #     #     #     #     #     #     #
                    if not r:                                                                                     #                                              #     #     #     #     #     #     #
                        s.cursor = len(s) - var216                                                                #                                              #     #     #     #     #     #     #
                        r = self.r_mark_lArI(s)  # routine call                                                   ##                                             ##    #     #     #     #     #     #
        if not r:                                                                                                                                                      #     #     #     #     #     #
            s.cursor = len(s) - var223                                                                                                                                 #     #     #     #     #     #
            self.left = s.cursor  ##                                                                                                                                   #     #     #     #     #     #
            r = True              ## [                                                                                                                                 #     #     #     #     #     #
            if r:                                                                                                                                                      #     #     #     #     #     #
                r = self.r_mark_DAn(s)  # routine call                                                                                                                 #     #     #     #     #     #
                if r:                                                                                                                                                  #     #     #     #     #     #
                    self.right = s.cursor  ##                                                                                                                          #     #     #     #     #     #
                    r = True               ## ]                                                                                                                        #     #     #     #     #     #
                    if r:                                                                                                                                              #     #     #     #     #     #
                        r = s.set_range(self.left, self.right, u'')  # delete                                                                                          #     #     #     #     # or  #
                        if r:                                                                                                                                          #     #     #     #     #     #
                            var222 = len(s) - s.cursor                                                                                    ##                           #     #     #     #     #     #
                            self.left = s.cursor  ##                                                                                      #                            #     #     #     #     #     #
                            r = True              ## [                                                                                    #                            #     #     #     #     #     #
                            if r:                                                                                                         #                            #     #     #     #     #     #
                                var221 = len(s) - s.cursor                                                                          ##    #                            #     #     #     #     #     #
                                var220 = len(s) - s.cursor                                                                    ##    #     #                            #     #     #     #     #     #
                                r = self.r_mark_possessives(s)  # routine call                                                #     #     #                            #     #     #     #     #     #
                                if r:                                                                                         #     #     #                            #     #     #     #     #     #
                                    self.right = s.cursor  ##                                                                 #     #     #                            #     #     #     #     #     #
                                    r = True               ## ]                                                               #     #     #                            #     #     #     #     #     #
                                    if r:                                                                                     #     #     #                            #     #     #     #     #     #
                                        r = s.set_range(self.left, self.right, u'')  # delete                                 #     #     #                            #     #     #     #     #     #
                                        if r:                                                                                 #     #     #                            #     #     #     #     #     #
                                            var218 = len(s) - s.cursor                                                 ##     #     #     #                            #     #     #     #     #     # or
                                            self.left = s.cursor  ##                                                   #      #     #     #                            #     #     #     #     #     #
                                            r = True              ## [                                                 #      #     #     #                            #     #     #     #     #     #
                                            if r:                                                                      #      #     #     #                            #     #     #     #     #     #
                                                r = self.r_mark_lAr(s)  # routine call                                 #      #     #     #                            #     #     #     #     #     #
                                                if r:                                                                  #      #     #     #                            #     #     #     #     #     #
                                                    self.right = s.cursor  ##                                          #      #     #     #                            #     #     #     #     #     #
                                                    r = True               ## ]                                        # try  #     #     #                            #     #     #     #     #     #
                                                    if r:                                                              #      #     #     #                            #     #     #     #     #     #
                                                        r = s.set_range(self.left, self.right, u'')  # delete          #      #     #     #                            #     #     #     #     #     #
                                                        if r:                                                          #      # or  #     #                            #     #     #     #     #     #
                                                            r = self.r_stem_suffix_chain_before_ki(s)  # routine call  #      #     # or  # try                        #     #     #     #     #     #
                                            if not r:                                                                  #      #     #     #                            #     #     #     #     #     #
                                                r = True                                                               #      #     #     #                            #     #     #     #     #     #
                                                s.cursor = len(s) - var218                                             ##     #     #     #                            #     #     #     #     #     #
                                if not r:                                                                                     #     #     #                            #     #     #     #     #     #
                                    s.cursor = len(s) - var220                                                                #     #     #                            #     #     #     #     #     #
                                    r = self.r_mark_lAr(s)  # routine call                                                    #     #     #                            #     #     #     #     #     #
                                    if r:                                                                                     #     #     #                            #     #     #     #     #     #
                                        self.right = s.cursor  ##                                                             #     #     #                            #     #     #     #     #     #
                                        r = True               ## ]                                                           #     #     #                            #     #     #     #     #     #
                                        if r:                                                                                 #     #     #                            #     #     #     #     #     #
                                            r = s.set_range(self.left, self.right, u'')  # delete                             #     #     #                            #     #     #     #     #     #
                                            if r:                                                                             #     #     #                            #     #     #     #     #     #
                                                var219 = len(s) - s.cursor                                 ##                 #     #     #                            #     #     #     #     #     #
                                                r = self.r_stem_suffix_chain_before_ki(s)  # routine call  #                  #     #     #                            #     #     #     #     #     #
                                                if not r:                                                  # try              #     #     #                            #     #     #     #     #     #
                                                    r = True                                               #                  #     #     #                            #     #     #     #     #     #
                                                    s.cursor = len(s) - var219                             ##                 ##    #     #                            #     #     #     #     #     #
                                if not r:                                                                                           #     #                            #     #     #     #     #     #
                                    s.cursor = len(s) - var221                                                                      #     #                            #     #     #     #     #     #
                                    r = self.r_stem_suffix_chain_before_ki(s)  # routine call                                       ##    #                            #     #     #     #     #     #
                            if not r:                                                                                                     #                            #     #     #     #     #     #
                                r = True                                                                                                  #                            #     #     #     #     #     #
                                s.cursor = len(s) - var222                                                                                ##                           ##    #     #     #     #     #
        if not r:                                                                                                                                                            #     #     #     #     #
            s.cursor = len(s) - var230                                                                                                                                       #     #     #     #     #
            self.left = s.cursor  ##                                                                                                                                         #     #     #     #     #
            r = True              ## [                                                                                                                                       #     #     #     #     #
            if r:                                                                                                                                                            #     #     #     #     #
                var224 = len(s) - s.cursor                  ##                                                                                                               #     #     #     #     #
                r = self.r_mark_nUn(s)  # routine call      #                                                                                                                #     #     #     #     #
                if not r:                                   # or                                                                                                             #     #     #     #     #
                    s.cursor = len(s) - var224              #                                                                                                                #     #     #     #     #
                    r = self.r_mark_ylA(s)  # routine call  ##                                                                                                               #     #     #     #     #
                if r:                                                                                                                                                        #     #     #     #     #
                    self.right = s.cursor  ##                                                                                                                                #     #     #     #     #
                    r = True               ## ]                                                                                                                              #     #     #     #     #
                    if r:                                                                                                                                                    #     #     #     #     #
                        r = s.set_range(self.left, self.right, u'')  # delete                                                                                                #     #     #     #     #
                        if r:                                                                                                                                                #     #     #     #     #
                            var229 = len(s) - s.cursor                                                                                        ##                             #     #     #     #     #
                            var228 = len(s) - s.cursor                                                                                  ##    #                              #     #     #     #     #
                            var227 = len(s) - s.cursor                                                                            ##    #     #                              #     #     #     #     #
                            self.left = s.cursor  ##                                                                              #     #     #                              #     #     #     #     #
                            r = True              ## [                                                                            #     #     #                              #     #     #     #     #
                            if r:                                                                                                 #     #     #                              #     #     #     #     #
                                r = self.r_mark_lAr(s)  # routine call                                                            #     #     #                              #     #     #     #     #
                                if r:                                                                                             #     #     #                              #     #     #     #     #
                                    self.right = s.cursor  ##                                                                     #     #     #                              #     #     #     #     #
                                    r = True               ## ]                                                                   #     #     #                              #     #     #     #     #
                                    if r:                                                                                         #     #     #                              #     #     #     #     #
                                        r = s.set_range(self.left, self.right, u'')  # delete                                     #     #     #                              #     #     #     #     #
                                        if r:                                                                                     #     #     #                              #     #     #     #     #
                                            r = self.r_stem_suffix_chain_before_ki(s)  # routine call                             #     #     #                              #     #     #     #     #
                            if not r:                                                                                             #     #     #                              #     #     #     #     #
                                s.cursor = len(s) - var227                                                                        #     #     #                              #     #     #     #     #
                                self.left = s.cursor  ##                                                                          #     #     #                              #     #     #     #     #
                                r = True              ## [                                                                        #     #     #                              #     #     #     #     #
                                if r:                                                                                             #     #     #                              #     #     #     #     #
                                    var225 = len(s) - s.cursor                      ##                                            #     #     #                              #     #     #     #     #
                                    r = self.r_mark_possessives(s)  # routine call  #                                             #     #     #                              #     #     #     #     #
                                    if not r:                                       # or                                          #     #     #                              #     #     #     #     #
                                        s.cursor = len(s) - var225                  #                                             #     #     #                              #     #     #     #     #
                                        r = self.r_mark_sU(s)  # routine call       ##                                            # or  #     #                              #     #     #     #     #
                                    if r:                                                                                         #     # or  #                              #     #     #     #     #
                                        self.right = s.cursor  ##                                                                 #     #     # try                          #     #     #     #     #
                                        r = True               ## ]                                                               #     #     #                              #     #     #     #     #
                                        if r:                                                                                     #     #     #                              #     #     #     #     #
                                            r = s.set_range(self.left, self.right, u'')  # delete                                 #     #     #                              #     #     #     #     #
                                            if r:                                                                                 #     #     #                              #     #     #     #     #
                                                var226 = len(s) - s.cursor                                                 ##     #     #     #                              #     #     #     #     #
                                                self.left = s.cursor  ##                                                   #      #     #     #                              #     #     #     #     #
                                                r = True              ## [                                                 #      #     #     #                              #     #     #     #     #
                                                if r:                                                                      #      #     #     #                              #     #     #     #     #
                                                    r = self.r_mark_lAr(s)  # routine call                                 #      #     #     #                              #     #     #     #     #
                                                    if r:                                                                  #      #     #     #                              #     #     #     #     #
                                                        self.right = s.cursor  ##                                          #      #     #     #                              #     #     #     #     #
                                                        r = True               ## ]                                        # try  #     #     #                              #     #     #     #     #
                                                        if r:                                                              #      #     #     #                              #     #     #     #     #
                                                            r = s.set_range(self.left, self.right, u'')  # delete          #      #     #     #                              #     #     #     #     #
                                                            if r:                                                          #      #     #     #                              #     #     #     #     #
                                                                r = self.r_stem_suffix_chain_before_ki(s)  # routine call  #      #     #     #                              #     #     #     #     #
                                                if not r:                                                                  #      #     #     #                              #     #     #     #     #
                                                    r = True                                                               #      #     #     #                              #     #     #     #     #
                                                    s.cursor = len(s) - var226                                             ##     ##    #     #                              #     #     #     #     #
                            if not r:                                                                                                   #     #                              #     #     #     #     #
                                s.cursor = len(s) - var228                                                                              #     #                              #     #     #     #     #
                                r = self.r_stem_suffix_chain_before_ki(s)  # routine call                                               ##    #                              #     #     #     #     #
                            if not r:                                                                                                         #                              #     #     #     #     #
                                r = True                                                                                                      #                              #     #     #     #     #
                                s.cursor = len(s) - var229                                                                                    ##                             ##    #     #     #     #
        if not r:                                                                                                                                                                  #     #     #     #
            s.cursor = len(s) - var231                                                                                                                                             #     #     #     #
            self.left = s.cursor  ##                                                                                                                                               #     #     #     #
            r = True              ## [                                                                                                                                             #     #     #     #
            if r:                                                                                                                                                                  #     #     #     #
                r = self.r_mark_lArI(s)  # routine call                                                                                                                            #     #     #     #
                if r:                                                                                                                                                              #     #     #     #
                    self.right = s.cursor  ##                                                                                                                                      #     #     #     #
                    r = True               ## ]                                                                                                                                    #     #     #     #
                    if r:                                                                                                                                                          #     #     #     #
                        r = s.set_range(self.left, self.right, u'')  # delete                                                                                                      ##    #     #     #
        if not r:                                                                                                                                                                        #     #     #
            s.cursor = len(s) - var232                                                                                                                                                   #     #     #
            r = self.r_stem_suffix_chain_before_ki(s)  # routine call                                                                                                                    ##    #     #
        if not r:                                                                                                                                                                              #     #
            s.cursor = len(s) - var238                                                                                                                                                         #     #
            self.left = s.cursor  ##                                                                                                                                                           #     #
            r = True              ## [                                                                                                                                                         #     #
            if r:                                                                                                                                                                              #     #
                var234 = len(s) - s.cursor                       ##                                                                                                                            #     #
                var233 = len(s) - s.cursor                 ##    #                                                                                                                             #     #
                r = self.r_mark_DA(s)  # routine call      #     #                                                                                                                             #     #
                if not r:                                  # or  #                                                                                                                             #     #
                    s.cursor = len(s) - var233             #     # or                                                                                                                          #     #
                    r = self.r_mark_yU(s)  # routine call  ##    #                                                                                                                             #     #
                if not r:                                        #                                                                                                                             #     #
                    s.cursor = len(s) - var234                   #                                                                                                                             #     #
                    r = self.r_mark_yA(s)  # routine call        ##                                                                                                                            #     #
                if r:                                                                                                                                                                          #     #
                    self.right = s.cursor  ##                                                                                                                                                  #     #
                    r = True               ## ]                                                                                                                                                #     #
                    if r:                                                                                                                                                                      #     #
                        r = s.set_range(self.left, self.right, u'')  # delete                                                                                                                  #     #
                        if r:                                                                                                                                                                  #     #
                            var237 = len(s) - s.cursor                                                     ##                                                                                  #     #
                            self.left = s.cursor  ##                                                       #                                                                                   #     #
                            r = True              ## [                                                     #                                                                                   #     #
                            if r:                                                                          #                                                                                   #     #
                                var236 = len(s) - s.cursor                                     ##          #                                                                                   #     #
                                r = self.r_mark_possessives(s)  # routine call                 #           #                                                                                   #     #
                                if r:                                                          #           #                                                                                   #     #
                                    self.right = s.cursor  ##                                  #           #                                                                                   #     #
                                    r = True               ## ]                                #           #                                                                                   #     #
                                    if r:                                                      #           #                                                                                   #     #
                                        r = s.set_range(self.left, self.right, u'')  # delete  #           #                                                                                   #     #
                                        if r:                                                  #           #                                                                                   #     #
                                            var235 = len(s) - s.cursor                  ##     #           #                                                                                   #     #
                                            self.left = s.cursor  ##                    #      # or        #                                                                                   #     #
                                            r = True              ## [                  #      #           #                                                                                   #     #
                                            if r:                                       #      #           #                                                                                   #     #
                                                r = self.r_mark_lAr(s)  # routine call  # try  #           #                                                                                   #     #
                                            if not r:                                   #      #           #                                                                                   #     #
                                                r = True                                #      #           # try                                                                               #     #
                                                s.cursor = len(s) - var235              ##     #           #                                                                                   #     #
                                if not r:                                                      #           #                                                                                   #     #
                                    s.cursor = len(s) - var236                                 #           #                                                                                   #     #
                                    r = self.r_mark_lAr(s)  # routine call                     ##          #                                                                                   #     #
                                if r:                                                                      #                                                                                   #     #
                                    self.right = s.cursor  ##                                              #                                                                                   #     #
                                    r = True               ## ]                                            #                                                                                   #     #
                                    if r:                                                                  #                                                                                   #     #
                                        r = s.set_range(self.left, self.right, u'')  # delete              #                                                                                   #     #
                                        if r:                                                              #                                                                                   #     #
                                            self.left = s.cursor  ##                                       #                                                                                   #     #
                                            r = True              ## [                                     #                                                                                   #     #
                                            if r:                                                          #                                                                                   #     #
                                                r = self.r_stem_suffix_chain_before_ki(s)  # routine call  #                                                                                   #     #
                            if not r:                                                                      #                                                                                   #     #
                                r = True                                                                   #                                                                                   #     #
                                s.cursor = len(s) - var237                                                 ##                                                                                  ##    #
        if not r:                                                                                                                                                                                    #
            s.cursor = len(s) - var241                                                                                                                                                               #
            self.left = s.cursor  ##                                                                                                                                                                 #
            r = True              ## [                                                                                                                                                               #
            if r:                                                                                                                                                                                    #
                var239 = len(s) - s.cursor                      ##                                                                                                                                   #
                r = self.r_mark_possessives(s)  # routine call  #                                                                                                                                    #
                if not r:                                       # or                                                                                                                                 #
                    s.cursor = len(s) - var239                  #                                                                                                                                    #
                    r = self.r_mark_sU(s)  # routine call       ##                                                                                                                                   #
                if r:                                                                                                                                                                                #
                    self.right = s.cursor  ##                                                                                                                                                        #
                    r = True               ## ]                                                                                                                                                      #
                    if r:                                                                                                                                                                            #
                        r = s.set_range(self.left, self.right, u'')  # delete                                                                                                                        #
                        if r:                                                                                                                                                                        #
                            var240 = len(s) - s.cursor                                                 ##                                                                                            #
                            self.left = s.cursor  ##                                                   #                                                                                             #
                            r = True              ## [                                                 #                                                                                             #
                            if r:                                                                      #                                                                                             #
                                r = self.r_mark_lAr(s)  # routine call                                 #                                                                                             #
                                if r:                                                                  #                                                                                             #
                                    self.right = s.cursor  ##                                          #                                                                                             #
                                    r = True               ## ]                                        # try                                                                                         #
                                    if r:                                                              #                                                                                             #
                                        r = s.set_range(self.left, self.right, u'')  # delete          #                                                                                             #
                                        if r:                                                          #                                                                                             #
                                            r = self.r_stem_suffix_chain_before_ki(s)  # routine call  #                                                                                             #
                            if not r:                                                                  #                                                                                             #
                                r = True                                                               #                                                                                             #
                                s.cursor = len(s) - var240                                             ##                                                                                            ##
        return r
    
    def r_post_process_last_consonants(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_24 = None                                           ##
            r = False                                             #
            var243 = s.cursor                                     #
            for var242, var246, var245 in _a_24:                  #
                if s.starts_with(var242):                         #
                    var244 = s.cursor                             #
                    r = (not var246) or getattr(self, var246)(s)  # substring
                    if r:                                         #
                      s.cursor = var244                           #
                      a_24 = var245                               #
                      break                                       #
                s.cursor = var243                                 ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_24 == 0:                                              ##
                        r = s.set_range(self.left, self.right, u'p')  # <-     #
                    if a_24 == 1:                                              #
                        r = s.set_range(self.left, self.right, u'\xe7')  # <-  #
                    if a_24 == 2:                                              # among
                        r = s.set_range(self.left, self.right, u't')  # <-     #
                    if a_24 == 3:                                              #
                        r = s.set_range(self.left, self.right, u'k')  # <-     ##
        return r
    
    def r_append_U_to_stems_ending_with_d_or_g(self, s):
        r = True
        var248 = len(s) - s.cursor                            ##
        var247 = len(s) - s.cursor                      ##    #
        r = s.starts_with(u'd')  # character check      #     #
        if not r:                                       # or  # test
            s.cursor = len(s) - var247                  #     #
            r = s.starts_with(u'g')  # character check  ##    #
        s.cursor = len(s) - var248                            ##
        if r:
            var263 = len(s) - s.cursor                                                                       ##
            var259 = len(s) - s.cursor                                                                 ##    #
            var255 = len(s) - s.cursor                                                           ##    #     #
            var251 = len(s) - s.cursor                                               ##          #     #     #
            while True:                                                      ##      #           #     #     #
                var249 = len(s) - s.cursor                                   #       #           #     #     #
                if s.cursor == s.limit:                    ##                #       #           #     #     #
                    r = False                              #                 #       #           #     #     #
                else:                                      #                 #       #           #     #     #
                    r = s.chars[s.cursor - 1] in _g_vowel  # grouping check  #       #           #     #     #
                if r:                                      #                 # goto  #           #     #     #
                    s.cursor -= 1                          ##                #       #           #     #     #
                if r or s.cursor == s.limit:                                 #       #           #     #     #
                    s.cursor = len(s) - var249                               #       # test      #     #     #
                    break                                                    #       #           #     #     #
                s.cursor = len(s) - var249 - 1                               ##      #           #     #     #
            if r:                                                                    #           #     #     #
                var250 = len(s) - s.cursor                           ##              #           #     #     #
                r = s.starts_with(u'a')  # character check           #               #           #     #     #
                if not r:                                            # or            #           #     #     #
                    s.cursor = len(s) - var250                       #               #           #     #     #
                    r = s.starts_with(u'\u0131')  # character check  ##              #           #     #     #
            s.cursor = len(s) - var251                                               ##          #     #     #
            if r:                                                                                #     #     #
                r = s.insert(u'\u0131')  # insert                                                #     #     #
            if not r:                                                                            # or  #     #
                s.cursor = len(s) - var255                                                       #     #     #
                var254 = len(s) - s.cursor                                               ##      #     #     #
                while True:                                                      ##      #       #     #     #
                    var252 = len(s) - s.cursor                                   #       #       #     #     #
                    if s.cursor == s.limit:                    ##                #       #       #     #     #
                        r = False                              #                 #       #       #     #     #
                    else:                                      #                 #       #       #     #     #
                        r = s.chars[s.cursor - 1] in _g_vowel  # grouping check  #       #       #     #     #
                    if r:                                      #                 # goto  #       #     #     #
                        s.cursor -= 1                          ##                #       #       #     #     #
                    if r or s.cursor == s.limit:                                 #       #       #     #     #
                        s.cursor = len(s) - var252                               #       # test  #     # or  #
                        break                                                    #       #       #     #     #
                    s.cursor = len(s) - var252 - 1                               ##      #       #     #     #
                if r:                                                                    #       #     #     #
                    var253 = len(s) - s.cursor                      ##                   #       #     #     #
                    r = s.starts_with(u'e')  # character check      #                    #       #     #     #
                    if not r:                                       # or                 #       #     #     #
                        s.cursor = len(s) - var253                  #                    #       #     #     #
                        r = s.starts_with(u'i')  # character check  ##                   #       #     #     #
                s.cursor = len(s) - var254                                               ##      #     #     #
                if r:                                                                            #     #     #
                    r = s.insert(u'i')  # insert                                                 ##    #     # or
            if not r:                                                                                  #     #
                s.cursor = len(s) - var259                                                             #     #
                var258 = len(s) - s.cursor                                               ##            #     #
                while True:                                                      ##      #             #     #
                    var256 = len(s) - s.cursor                                   #       #             #     #
                    if s.cursor == s.limit:                    ##                #       #             #     #
                        r = False                              #                 #       #             #     #
                    else:                                      #                 #       #             #     #
                        r = s.chars[s.cursor - 1] in _g_vowel  # grouping check  #       #             #     #
                    if r:                                      #                 # goto  #             #     #
                        s.cursor -= 1                          ##                #       #             #     #
                    if r or s.cursor == s.limit:                                 #       #             #     #
                        s.cursor = len(s) - var256                               #       # test        #     #
                        break                                                    #       #             #     #
                    s.cursor = len(s) - var256 - 1                               ##      #             #     #
                if r:                                                                    #             #     #
                    var257 = len(s) - s.cursor                      ##                   #             #     #
                    r = s.starts_with(u'o')  # character check      #                    #             #     #
                    if not r:                                       # or                 #             #     #
                        s.cursor = len(s) - var257                  #                    #             #     #
                        r = s.starts_with(u'u')  # character check  ##                   #             #     #
                s.cursor = len(s) - var258                                               ##            #     #
                if r:                                                                                  #     #
                    r = s.insert(u'u')  # insert                                                       ##    #
            if not r:                                                                                        #
                s.cursor = len(s) - var263                                                                   #
                var262 = len(s) - s.cursor                                               ##                  #
                while True:                                                      ##      #                   #
                    var260 = len(s) - s.cursor                                   #       #                   #
                    if s.cursor == s.limit:                    ##                #       #                   #
                        r = False                              #                 #       #                   #
                    else:                                      #                 #       #                   #
                        r = s.chars[s.cursor - 1] in _g_vowel  # grouping check  #       #                   #
                    if r:                                      #                 # goto  #                   #
                        s.cursor -= 1                          ##                #       #                   #
                    if r or s.cursor == s.limit:                                 #       #                   #
                        s.cursor = len(s) - var260                               #       # test              #
                        break                                                    #       #                   #
                    s.cursor = len(s) - var260 - 1                               ##      #                   #
                if r:                                                                    #                   #
                    var261 = len(s) - s.cursor                         ##                #                   #
                    r = s.starts_with(u'\xf6')  # character check      #                 #                   #
                    if not r:                                          # or              #                   #
                        s.cursor = len(s) - var261                     #                 #                   #
                        r = s.starts_with(u'\xfc')  # character check  ##                #                   #
                s.cursor = len(s) - var262                                               ##                  #
                if r:                                                                                        #
                    r = s.insert(u'\xfc')  # insert                                                          ##
        return r
    
    def r_more_than_one_syllable_word(self, s):
        r = True
        var265 = s.cursor                                                                         ##
        for var264 in xrange(2):                                                       ##         #
            while True:                                                  ##            #          #
                if s.cursor == s.limit:                ##                #             #          #
                    r = False                          #                 #             #          #
                else:                                  #                 #             #          #
                    r = s.chars[s.cursor] in _g_vowel  # grouping check  #             #          #
                if r:                                  #                 # gopast      #          #
                    s.cursor += 1                      ##                #             #          #
                if r or s.cursor == s.limit:                             #             #          #
                    break                                                #             #          #
                s.cursor += 1                                            ##            #          #
            if not r:                                                                  #          #
                break                                                                  #          #
        if r:                                                                          #          #
            while True:                                                                #          #
                var264 = s.cursor                                                      # atleast  # test
                while True:                                                  ##        #          #
                    if s.cursor == s.limit:                ##                #         #          #
                        r = False                          #                 #         #          #
                    else:                                  #                 #         #          #
                        r = s.chars[s.cursor] in _g_vowel  # grouping check  #         #          #
                    if r:                                  #                 # gopast  #          #
                        s.cursor += 1                      ##                #         #          #
                    if r or s.cursor == s.limit:                             #         #          #
                        break                                                #         #          #
                    s.cursor += 1                                            ##        #          #
                if not r:                                                              #          #
                    s.cursor = var264                                                  #          #
                    break                                                              #          #
            r = True                                                                   ##         #
        s.cursor = var265                                                                         ##
        return r
    
    def r_is_reserved_word(self, s):
        r = True
        var268 = s.cursor                                                         ##
        var266 = s.cursor                                          ##             #
        while True:                                      ##        #              #
            r = s.starts_with(u'ad')  # character check  #         #              #
            if r or s.cursor == s.limit:                 # gopast  #              #
                break                                    #         #              #
            s.cursor += 1                                ##        #              #
        if r:                                                      # test         #
            self.i_strlen = 2                                      #              #
            r = True                                               #              #
            if r:                                                  #              #
                r = self.i_strlen == s.limit  # ==                 #              #
        s.cursor = var266                                          ##             #
        if not r:                                                                 # or
            s.cursor = var268                                                     #
            var267 = s.cursor                                             ##      #
            while True:                                         ##        #       #
                r = s.starts_with(u'soyad')  # character check  #         #       #
                if r or s.cursor == s.limit:                    # gopast  #       #
                    break                                       #         #       #
                s.cursor += 1                                   ##        #       #
            if r:                                                         # test  #
                self.i_strlen = 5                                         #       #
                r = True                                                  #       #
                if r:                                                     #       #
                    r = self.i_strlen == s.limit  # ==                    #       #
            s.cursor = var267                                             ##      ##
        return r
    
    def r_postlude(self, s):
        r = True
        var269 = s.cursor                               ##
        r = self.r_is_reserved_word(s)  # routine call  #
        if not r:                                       # not
            s.cursor = var269                           #
        r = not r                                       ##
        if r:
            var272 = s.cursor                                                         ##
            var273 = len(s) - s.limit                                                 #
            s.direction *= -1                                                         #
            s.cursor, s.limit = s.limit, s.cursor                                     #
            var270 = len(s) - s.cursor                                          ##    #
            r = self.r_append_U_to_stems_ending_with_d_or_g(s)  # routine call  #     #
            s.cursor = len(s) - var270                                          # do  #
            r = True                                                            ##    #
            if r:                                                                     # backwards
                var271 = len(s) - s.cursor                                  ##        #
                r = self.r_post_process_last_consonants(s)  # routine call  #         #
                s.cursor = len(s) - var271                                  # do      #
                r = True                                                    ##        #
            s.direction *= -1                                                         #
            s.cursor = var272                                                         #
            s.limit = len(s) - var273                                                 ##
        return r
    
    def r_stem(self, s):
        r = True
        r = self.r_more_than_one_syllable_word(s)  # routine call
        if r:
            var276 = s.cursor                                                         ##
            var277 = len(s) - s.limit                                                 #
            s.direction *= -1                                                         #
            s.cursor, s.limit = s.limit, s.cursor                                     #
            var274 = len(s) - s.cursor                                ##              #
            r = self.r_stem_nominal_verb_suffixes(s)  # routine call  #               #
            s.cursor = len(s) - var274                                # do            #
            r = True                                                  ##              #
            if r:                                                                     #
                r = self.b_continue_stemming_noun_suffixes  # boolean variable check  # backwards
                if r:                                                                 #
                    var275 = len(s) - s.cursor                        ##              #
                    r = self.r_stem_noun_suffixes(s)  # routine call  #               #
                    s.cursor = len(s) - var275                        # do            #
                    r = True                                          ##              #
            s.direction *= -1                                                         #
            s.cursor = var276                                                         #
            s.limit = len(s) - var277                                                 ##
            if r:
                r = self.r_postlude(s)  # routine call
        return r
