#!/usr/bin/env python
# vim:fileencoding=utf-8



# This file was auto-generated on 2014-08-05 20:04:12 using
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


def stem(s):
    s = _String(s)
    _Program().r_stem(s)
    return unicode(s)

_g_v = set(u'aeiou\xe0\xe8\xec\xf2\xf9')
_a_1 = ((u'qu', '', 5), (u'\xe1', '', 0), (u'\xe9', '', 1), (u'\xed', '', 2), (u'\xf3', '', 3), (u'\xfa', '', 4), (u'', '', 6),)
_a_2 = ((u'I', '', 0), (u'U', '', 1), (u'', '', 2),)
_a_3 = ((u'gliela', '', 0), (u'gliele', '', 0), (u'glieli', '', 0), (u'glielo', '', 0), (u'gliene', '', 0), (u'sene', '', 0), (u'mela', '', 0), (u'mele', '', 0), (u'meli', '', 0), (u'melo', '', 0), (u'mene', '', 0), (u'tela', '', 0), (u'tele', '', 0), (u'teli', '', 0), (u'telo', '', 0), (u'tene', '', 0), (u'cela', '', 0), (u'cele', '', 0), (u'celi', '', 0), (u'celo', '', 0), (u'cene', '', 0), (u'vela', '', 0), (u'vele', '', 0), (u'veli', '', 0), (u'velo', '', 0), (u'vene', '', 0), (u'gli', '', 0), (u'ci', '', 0), (u'la', '', 0), (u'le', '', 0), (u'li', '', 0), (u'lo', '', 0), (u'mi', '', 0), (u'ne', '', 0), (u'si', '', 0), (u'ti', '', 0), (u'vi', '', 0),)
_a_4 = ((u'ando', '', 0), (u'endo', '', 0), (u'ar', '', 1), (u'er', '', 1), (u'ir', '', 1),)
_a_5 = ((u'atrice', '', 0), (u'atrici', '', 0), (u'azione', '', 1), (u'azioni', '', 1), (u'uzione', '', 3), (u'uzioni', '', 3), (u'usione', '', 3), (u'usioni', '', 3), (u'amento', '', 5), (u'amenti', '', 5), (u'imento', '', 5), (u'imenti', '', 5), (u'amente', '', 6), (u'abile', '', 0), (u'abili', '', 0), (u'ibile', '', 0), (u'ibili', '', 0), (u'mente', '', 0), (u'atore', '', 1), (u'atori', '', 1), (u'logia', '', 2), (u'logie', '', 2), (u'anza', '', 0), (u'anze', '', 0), (u'iche', '', 0), (u'ichi', '', 0), (u'ismo', '', 0), (u'ismi', '', 0), (u'ista', '', 0), (u'iste', '', 0), (u'isti', '', 0), (u'ist\xe0', '', 0), (u'ist\xe8', '', 0), (u'ist\xec', '', 0), (u'ante', '', 0), (u'anti', '', 0), (u'enza', '', 4), (u'enze', '', 4), (u'ico', '', 0), (u'ici', '', 0), (u'ica', '', 0), (u'ice', '', 0), (u'oso', '', 0), (u'osi', '', 0), (u'osa', '', 0), (u'ose', '', 0), (u'it\xe0', '', 7), (u'ivo', '', 8), (u'ivi', '', 8), (u'iva', '', 8), (u'ive', '', 8),)
_a_6 = ((u'abil', '', 1), (u'iv', '', 0), (u'os', '', 1), (u'ic', '', 1),)
_a_7 = ((u'abil', '', 0), (u'ic', '', 0), (u'iv', '', 0),)
_a_8 = ((u'erebbero', '', 0), (u'irebbero', '', 0), (u'assero', '', 0), (u'assimo', '', 0), (u'eranno', '', 0), (u'erebbe', '', 0), (u'eremmo', '', 0), (u'ereste', '', 0), (u'eresti', '', 0), (u'essero', '', 0), (u'iranno', '', 0), (u'irebbe', '', 0), (u'iremmo', '', 0), (u'ireste', '', 0), (u'iresti', '', 0), (u'iscano', '', 0), (u'iscono', '', 0), (u'issero', '', 0), (u'arono', '', 0), (u'avamo', '', 0), (u'avano', '', 0), (u'avate', '', 0), (u'eremo', '', 0), (u'erete', '', 0), (u'erono', '', 0), (u'evamo', '', 0), (u'evano', '', 0), (u'evate', '', 0), (u'iremo', '', 0), (u'irete', '', 0), (u'irono', '', 0), (u'ivamo', '', 0), (u'ivano', '', 0), (u'ivate', '', 0), (u'ammo', '', 0), (u'ando', '', 0), (u'asse', '', 0), (u'assi', '', 0), (u'emmo', '', 0), (u'enda', '', 0), (u'ende', '', 0), (u'endi', '', 0), (u'endo', '', 0), (u'erai', '', 0), (u'erei', '', 0), (u'Yamo', '', 0), (u'iamo', '', 0), (u'immo', '', 0), (u'irai', '', 0), (u'irei', '', 0), (u'isca', '', 0), (u'isce', '', 0), (u'isci', '', 0), (u'isco', '', 0), (u'ano', '', 0), (u'are', '', 0), (u'ata', '', 0), (u'ate', '', 0), (u'ati', '', 0), (u'ato', '', 0), (u'ava', '', 0), (u'avi', '', 0), (u'avo', '', 0), (u'er\xe0', '', 0), (u'ere', '', 0), (u'er\xf2', '', 0), (u'ete', '', 0), (u'eva', '', 0), (u'evi', '', 0), (u'evo', '', 0), (u'ir\xe0', '', 0), (u'ire', '', 0), (u'ir\xf2', '', 0), (u'ita', '', 0), (u'ite', '', 0), (u'iti', '', 0), (u'ito', '', 0), (u'iva', '', 0), (u'ivi', '', 0), (u'ivo', '', 0), (u'ono', '', 0), (u'uta', '', 0), (u'ute', '', 0), (u'uti', '', 0), (u'uto', '', 0), (u'ar', '', 0), (u'ir', '', 0),)
_g_AEIO = set(u'aeio\xe0\xe8\xec\xf2')
_g_CG = set(u'cg')

class _Program(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.i_pV = 0
        self.i_p1 = 0
        self.i_p2 = 0

    def r_prelude(self, s):
        r = True
        var6 = s.cursor                                                                               ##
        while True:                                                                         ##        #
            var5 = s.cursor                                                                 #         #
            self.left = s.cursor  ##                                                        #         #
            r = True              ## [                                                      #         #
            if r:                                                                           #         #
                a_1 = None                                        ##                        #         #
                r = False                                         #                         #         #
                var1 = s.cursor                                   #                         #         #
                for var0, var4, var3 in _a_1:                     #                         #         #
                    if s.starts_with(var0):                       #                         #         #
                        var2 = s.cursor                           #                         #         #
                        r = (not var4) or getattr(self, var4)(s)  # substring               #         #
                        if r:                                     #                         #         #
                          s.cursor = var2                         #                         #         #
                          a_1 = var3                              #                         #         #
                          break                                   #                         #         #
                    s.cursor = var1                               ##                        #         #
                if r:                                                                       #         #
                    self.right = s.cursor  ##                                               #         #
                    r = True               ## ]                                             # repeat  # test
                    if r:                                                                   #         #
                        if a_1 == 0:                                               ##       #         #
                            r = s.set_range(self.left, self.right, u'\xe0')  # <-  #        #         #
                        if a_1 == 1:                                               #        #         #
                            r = s.set_range(self.left, self.right, u'\xe8')  # <-  #        #         #
                        if a_1 == 2:                                               #        #         #
                            r = s.set_range(self.left, self.right, u'\xec')  # <-  #        #         #
                        if a_1 == 3:                                               #        #         #
                            r = s.set_range(self.left, self.right, u'\xf2')  # <-  # among  #         #
                        if a_1 == 4:                                               #        #         #
                            r = s.set_range(self.left, self.right, u'\xf9')  # <-  #        #         #
                        if a_1 == 5:                                               #        #         #
                            r = s.set_range(self.left, self.right, u'qU')  # <-    #        #         #
                        if a_1 == 6:                                               #        #         #
                            r = s.hop(1)  # next                                   ##       #         #
            if not r:                                                                       #         #
                s.cursor = var5                                                             #         #
                break                                                                       #         #
        r = True                                                                            ##        #
        s.cursor = var6                                                                               ##
        if r:
            while True:                                                                                       ##
                var9 = s.cursor                                                                               #
                while True:                                                                           ##      #
                    var8 = s.cursor                                                                   #       #
                    if s.cursor == s.limit:            ##                                             #       #
                        r = False                      #                                              #       #
                    else:                              #                                              #       #
                        r = s.chars[s.cursor] in _g_v  # grouping check                               #       #
                    if r:                              #                                              #       #
                        s.cursor += 1                  ##                                             #       #
                    if r:                                                                             #       #
                        self.left = s.cursor  ##                                                      #       #
                        r = True              ## [                                                    #       #
                        if r:                                                                         #       #
                            var7 = s.cursor                                                     ##    #       #
                            r = s.starts_with(u'u')  # character check                          #     #       #
                            if r:                                                               #     #       #
                                self.right = s.cursor  ##                                       #     #       #
                                r = True               ## ]                                     #     #       #
                                if r:                                                           #     #       #
                                    if s.cursor == s.limit:            ##                       #     #       #
                                        r = False                      #                        #     #       #
                                    else:                              #                        #     #       #
                                        r = s.chars[s.cursor] in _g_v  # grouping check         #     #       #
                                    if r:                              #                        #     # goto  #
                                        s.cursor += 1                  ##                       #     #       # repeat
                                    if r:                                                       #     #       #
                                        r = s.set_range(self.left, self.right, u'U')  # <-      #     #       #
                            if not r:                                                           # or  #       #
                                s.cursor = var7                                                 #     #       #
                                r = s.starts_with(u'i')  # character check                      #     #       #
                                if r:                                                           #     #       #
                                    self.right = s.cursor  ##                                   #     #       #
                                    r = True               ## ]                                 #     #       #
                                    if r:                                                       #     #       #
                                        if s.cursor == s.limit:            ##                   #     #       #
                                            r = False                      #                    #     #       #
                                        else:                              #                    #     #       #
                                            r = s.chars[s.cursor] in _g_v  # grouping check     #     #       #
                                        if r:                              #                    #     #       #
                                            s.cursor += 1                  ##                   #     #       #
                                        if r:                                                   #     #       #
                                            r = s.set_range(self.left, self.right, u'I')  # <-  ##    #       #
                    if r or s.cursor == s.limit:                                                      #       #
                        s.cursor = var8                                                               #       #
                        break                                                                         #       #
                    s.cursor = var8 + 1                                                               ##      #
                if not r:                                                                                     #
                    s.cursor = var9                                                                           #
                    break                                                                                     #
            r = True                                                                                          ##
        return r
    
    def r_mark_regions(self, s):
        r = True
        self.i_pV = s.limit
        r = True
        if r:
            self.i_p1 = s.limit
            r = True
            if r:
                self.i_p2 = s.limit
                r = True
                if r:
                    var13 = s.cursor                                                                                        ##
                    var12 = s.cursor                                                                                  ##    #
                    if s.cursor == s.limit:            ##                                                             #     #
                        r = False                      #                                                              #     #
                    else:                              #                                                              #     #
                        r = s.chars[s.cursor] in _g_v  # grouping check                                               #     #
                    if r:                              #                                                              #     #
                        s.cursor += 1                  ##                                                             #     #
                    if r:                                                                                             #     #
                        var10 = s.cursor                                                                        ##    #     #
                        if s.cursor == s.limit:                ##                                               #     #     #
                            r = False                          #                                                #     #     #
                        else:                                  #                                                #     #     #
                            r = s.chars[s.cursor] not in _g_v  # negative grouping check                        #     #     #
                        if r:                                  #                                                #     #     #
                            s.cursor += 1                      ##                                               #     #     #
                        if r:                                                                                   #     #     #
                            while True:                                              ##                         #     #     #
                                if s.cursor == s.limit:            ##                #                          #     #     #
                                    r = False                      #                 #                          #     #     #
                                else:                              #                 #                          #     #     #
                                    r = s.chars[s.cursor] in _g_v  # grouping check  #                          #     #     #
                                if r:                              #                 # gopast                   #     #     #
                                    s.cursor += 1                  ##                #                          #     #     #
                                if r or s.cursor == s.limit:                         #                          #     #     #
                                    break                                            #                          #     #     #
                                s.cursor += 1                                        ##                         #     #     #
                        if not r:                                                                               # or  #     #
                            s.cursor = var10                                                                    #     #     #
                            if s.cursor == s.limit:            ##                                               #     #     #
                                r = False                      #                                                #     #     #
                            else:                              #                                                #     #     #
                                r = s.chars[s.cursor] in _g_v  # grouping check                                 #     #     #
                            if r:                              #                                                #     #     #
                                s.cursor += 1                  ##                                               #     #     #
                            if r:                                                                               #     #     #
                                while True:                                                           ##        #     #     #
                                    if s.cursor == s.limit:                ##                         #         #     #     #
                                        r = False                          #                          #         #     #     #
                                    else:                                  #                          #         #     #     #
                                        r = s.chars[s.cursor] not in _g_v  # negative grouping check  #         #     #     #
                                    if r:                                  #                          # gopast  #     #     #
                                        s.cursor += 1                      ##                         #         #     # or  #
                                    if r or s.cursor == s.limit:                                      #         #     #     #
                                        break                                                         #         #     #     # do
                                    s.cursor += 1                                                     ##        ##    #     #
                    if not r:                                                                                         #     #
                        s.cursor = var12                                                                              #     #
                        if s.cursor == s.limit:                ##                                                     #     #
                            r = False                          #                                                      #     #
                        else:                                  #                                                      #     #
                            r = s.chars[s.cursor] not in _g_v  # negative grouping check                              #     #
                        if r:                                  #                                                      #     #
                            s.cursor += 1                      ##                                                     #     #
                        if r:                                                                                         #     #
                            var11 = s.cursor                                                       ##                 #     #
                            if s.cursor == s.limit:                ##                              #                  #     #
                                r = False                          #                               #                  #     #
                            else:                                  #                               #                  #     #
                                r = s.chars[s.cursor] not in _g_v  # negative grouping check       #                  #     #
                            if r:                                  #                               #                  #     #
                                s.cursor += 1                      ##                              #                  #     #
                            if r:                                                                  #                  #     #
                                while True:                                              ##        #                  #     #
                                    if s.cursor == s.limit:            ##                #         #                  #     #
                                        r = False                      #                 #         #                  #     #
                                    else:                              #                 #         #                  #     #
                                        r = s.chars[s.cursor] in _g_v  # grouping check  #         #                  #     #
                                    if r:                              #                 # gopast  #                  #     #
                                        s.cursor += 1                  ##                #         # or               #     #
                                    if r or s.cursor == s.limit:                         #         #                  #     #
                                        break                                            #         #                  #     #
                                    s.cursor += 1                                        ##        #                  #     #
                            if not r:                                                              #                  #     #
                                s.cursor = var11                                                   #                  #     #
                                if s.cursor == s.limit:            ##                              #                  #     #
                                    r = False                      #                               #                  #     #
                                else:                              #                               #                  #     #
                                    r = s.chars[s.cursor] in _g_v  # grouping check                #                  #     #
                                if r:                              #                               #                  #     #
                                    s.cursor += 1                  ##                              #                  #     #
                                if r:                                                              #                  #     #
                                    r = s.hop(1)  # next                                           ##                 ##    #
                    if r:                                                                                                   #
                        self.i_pV = s.cursor  ##                                                                            #
                        r = True              ## setmark                                                                    #
                    s.cursor = var13                                                                                        #
                    r = True                                                                                                ##
                    if r:
                        var14 = s.cursor                                                                                ##
                        while True:                                              ##                                     #
                            if s.cursor == s.limit:            ##                #                                      #
                                r = False                      #                 #                                      #
                            else:                              #                 #                                      #
                                r = s.chars[s.cursor] in _g_v  # grouping check  #                                      #
                            if r:                              #                 # gopast                               #
                                s.cursor += 1                  ##                #                                      #
                            if r or s.cursor == s.limit:                         #                                      #
                                break                                            #                                      #
                            s.cursor += 1                                        ##                                     #
                        if r:                                                                                           #
                            while True:                                                           ##                    #
                                if s.cursor == s.limit:                ##                         #                     #
                                    r = False                          #                          #                     #
                                else:                                  #                          #                     #
                                    r = s.chars[s.cursor] not in _g_v  # negative grouping check  #                     #
                                if r:                                  #                          # gopast              #
                                    s.cursor += 1                      ##                         #                     #
                                if r or s.cursor == s.limit:                                      #                     #
                                    break                                                         #                     #
                                s.cursor += 1                                                     ##                    #
                            if r:                                                                                       #
                                self.i_p1 = s.cursor  ##                                                                #
                                r = True              ## setmark                                                        #
                                if r:                                                                                   #
                                    while True:                                              ##                         # do
                                        if s.cursor == s.limit:            ##                #                          #
                                            r = False                      #                 #                          #
                                        else:                              #                 #                          #
                                            r = s.chars[s.cursor] in _g_v  # grouping check  #                          #
                                        if r:                              #                 # gopast                   #
                                            s.cursor += 1                  ##                #                          #
                                        if r or s.cursor == s.limit:                         #                          #
                                            break                                            #                          #
                                        s.cursor += 1                                        ##                         #
                                    if r:                                                                               #
                                        while True:                                                           ##        #
                                            if s.cursor == s.limit:                ##                         #         #
                                                r = False                          #                          #         #
                                            else:                                  #                          #         #
                                                r = s.chars[s.cursor] not in _g_v  # negative grouping check  #         #
                                            if r:                                  #                          # gopast  #
                                                s.cursor += 1                      ##                         #         #
                                            if r or s.cursor == s.limit:                                      #         #
                                                break                                                         #         #
                                            s.cursor += 1                                                     ##        #
                                        if r:                                                                           #
                                            self.i_p2 = s.cursor  ##                                                    #
                                            r = True              ## setmark                                            #
                        s.cursor = var14                                                                                #
                        r = True                                                                                        ##
        return r
    
    def r_postlude(self, s):
        r = True
        while True:                                                                      ##
            var20 = s.cursor                                                             #
            self.left = s.cursor  ##                                                     #
            r = True              ## [                                                   #
            if r:                                                                        #
                a_2 = None                                          ##                   #
                r = False                                           #                    #
                var16 = s.cursor                                    #                    #
                for var15, var19, var18 in _a_2:                    #                    #
                    if s.starts_with(var15):                        #                    #
                        var17 = s.cursor                            #                    #
                        r = (not var19) or getattr(self, var19)(s)  # substring          #
                        if r:                                       #                    #
                          s.cursor = var17                          #                    #
                          a_2 = var18                               #                    #
                          break                                     #                    # repeat
                    s.cursor = var16                                ##                   #
                if r:                                                                    #
                    self.right = s.cursor  ##                                            #
                    r = True               ## ]                                          #
                    if r:                                                                #
                        if a_2 == 0:                                            ##       #
                            r = s.set_range(self.left, self.right, u'i')  # <-  #        #
                        if a_2 == 1:                                            #        #
                            r = s.set_range(self.left, self.right, u'u')  # <-  # among  #
                        if a_2 == 2:                                            #        #
                            r = s.hop(1)  # next                                ##       #
            if not r:                                                                    #
                s.cursor = var20                                                         #
                break                                                                    #
        r = True                                                                         ##
        return r
    
    def r_RV(self, s):
        r = True
        r = self.i_pV <= s.cursor  # <=
        return r
    
    def r_R1(self, s):
        r = True
        r = self.i_p1 <= s.cursor  # <=
        return r
    
    def r_R2(self, s):
        r = True
        r = self.i_p2 <= s.cursor  # <=
        return r
    
    def r_attached_pronoun(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_3 = None                                          ##
            r = False                                           #
            var22 = s.cursor                                    #
            for var21, var25, var24 in _a_3:                    #
                if s.starts_with(var21):                        #
                    var23 = s.cursor                            #
                    r = (not var25) or getattr(self, var25)(s)  # substring
                    if r:                                       #
                      s.cursor = var23                          #
                      a_3 = var24                               #
                      break                                     #
                s.cursor = var22                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_3 == 0:  ##
                        r = True  ## among
                    if r:
                        a_4 = None                                                         ##
                        r = False                                                          #
                        var27 = s.cursor                                                   #
                        for var26, var30, var29 in _a_4:                                   #
                            if s.starts_with(var26):                                       #
                                var28 = s.cursor                                           #
                                r = (not var30) or getattr(self, var30)(s)                 #
                                if r:                                                      #
                                  s.cursor = var28                                         #
                                  a_4 = var29                                              # among
                                  break                                                    #
                            s.cursor = var27                                               #
                        if r:                                                              #
                            r = self.r_RV(s)  # routine call                               #
                            if r:                                                          #
                                if a_4 == 0:                                               #
                                    r = s.set_range(self.left, self.right, u'')  # delete  #
                                if a_4 == 1:                                               #
                                    r = s.set_range(self.left, self.right, u'e')  # <-     ##
        return r
    
    def r_standard_suffix(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_5 = None                                          ##
            r = False                                           #
            var32 = s.cursor                                    #
            for var31, var35, var34 in _a_5:                    #
                if s.starts_with(var31):                        #
                    var33 = s.cursor                            #
                    r = (not var35) or getattr(self, var35)(s)  # substring
                    if r:                                       #
                      s.cursor = var33                          #
                      a_5 = var34                               #
                      break                                     #
                s.cursor = var32                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_5 == 0:                                                                                                               ##
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                    if a_5 == 1:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var36 = len(s) - s.cursor                                              ##                                      #
                                self.left = s.cursor  ##                                               #                                       #
                                r = True              ## [                                             #                                       #
                                if r:                                                                  #                                       #
                                    r = s.starts_with(u'ic')  # character check                        #                                       #
                                    if r:                                                              #                                       #
                                        self.right = s.cursor  ##                                      #                                       #
                                        r = True               ## ]                                    # try                                   #
                                        if r:                                                          #                                       #
                                            r = self.r_R2(s)  # routine call                           #                                       #
                                            if r:                                                      #                                       #
                                                r = s.set_range(self.left, self.right, u'')  # delete  #                                       #
                                if not r:                                                              #                                       #
                                    r = True                                                           #                                       #
                                    s.cursor = len(s) - var36                                          ##                                      #
                    if a_5 == 2:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'log')  # <-                                                               #
                    if a_5 == 3:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'u')  # <-                                                                 #
                    if a_5 == 4:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'ente')  # <-                                                              #
                    if a_5 == 5:                                                                                                               #
                        r = self.r_RV(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                    if a_5 == 6:                                                                                                               #
                        r = self.r_R1(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var42 = len(s) - s.cursor                                                                               ##     #
                                self.left = s.cursor  ##                                                                                #      #
                                r = True              ## [                                                                              #      #
                                if r:                                                                                                   #      #
                                    a_6 = None                                          ##                                              #      #
                                    r = False                                           #                                               #      #
                                    var38 = s.cursor                                    #                                               #      #
                                    for var37, var41, var40 in _a_6:                    #                                               #      #
                                        if s.starts_with(var37):                        #                                               #      #
                                            var39 = s.cursor                            #                                               #      #
                                            r = (not var41) or getattr(self, var41)(s)  # substring                                     #      #
                                            if r:                                       #                                               #      #
                                              s.cursor = var39                          #                                               #      #
                                              a_6 = var40                               #                                               #      #
                                              break                                     #                                               #      #
                                        s.cursor = var38                                ##                                              #      #
                                    if r:                                                                                               #      #
                                        self.right = s.cursor  ##                                                                       #      #
                                        r = True               ## ]                                                                     #      #
                                        if r:                                                                                           #      #
                                            r = self.r_R2(s)  # routine call                                                            # try  #
                                            if r:                                                                                       #      #
                                                r = s.set_range(self.left, self.right, u'')  # delete                                   #      #
                                                if r:                                                                                   #      #
                                                    if a_6 == 0:                                                               ##       #      #
                                                        self.left = s.cursor  ##                                               #        #      #
                                                        r = True              ## [                                             #        #      #
                                                        if r:                                                                  #        #      #
                                                            r = s.starts_with(u'at')  # character check                        #        #      #
                                                            if r:                                                              #        #      #
                                                                self.right = s.cursor  ##                                      #        #      # among
                                                                r = True               ## ]                                    # among  #      #
                                                                if r:                                                          #        #      #
                                                                    r = self.r_R2(s)  # routine call                           #        #      #
                                                                    if r:                                                      #        #      #
                                                                        r = s.set_range(self.left, self.right, u'')  # delete  #        #      #
                                                    if a_6 == 1:                                                               #        #      #
                                                        r = True                                                               ##       #      #
                                if not r:                                                                                               #      #
                                    r = True                                                                                            #      #
                                    s.cursor = len(s) - var42                                                                           ##     #
                    if a_5 == 7:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var48 = len(s) - s.cursor                                                           ##                         #
                                self.left = s.cursor  ##                                                            #                          #
                                r = True              ## [                                                          #                          #
                                if r:                                                                               #                          #
                                    a_7 = None                                          ##                          #                          #
                                    r = False                                           #                           #                          #
                                    var44 = s.cursor                                    #                           #                          #
                                    for var43, var47, var46 in _a_7:                    #                           #                          #
                                        if s.starts_with(var43):                        #                           #                          #
                                            var45 = s.cursor                            #                           #                          #
                                            r = (not var47) or getattr(self, var47)(s)  # substring                 #                          #
                                            if r:                                       #                           #                          #
                                              s.cursor = var45                          #                           #                          #
                                              a_7 = var46                               #                           # try                      #
                                              break                                     #                           #                          #
                                        s.cursor = var44                                ##                          #                          #
                                    if r:                                                                           #                          #
                                        self.right = s.cursor  ##                                                   #                          #
                                        r = True               ## ]                                                 #                          #
                                        if r:                                                                       #                          #
                                            if a_7 == 0:                                                   ##       #                          #
                                                r = self.r_R2(s)  # routine call                           #        #                          #
                                                if r:                                                      # among  #                          #
                                                    r = s.set_range(self.left, self.right, u'')  # delete  ##       #                          #
                                if not r:                                                                           #                          #
                                    r = True                                                                        #                          #
                                    s.cursor = len(s) - var48                                                       ##                         #
                    if a_5 == 8:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var49 = len(s) - s.cursor                                                                  ##                  #
                                self.left = s.cursor  ##                                                                   #                   #
                                r = True              ## [                                                                 #                   #
                                if r:                                                                                      #                   #
                                    r = s.starts_with(u'at')  # character check                                            #                   #
                                    if r:                                                                                  #                   #
                                        self.right = s.cursor  ##                                                          #                   #
                                        r = True               ## ]                                                        #                   #
                                        if r:                                                                              #                   #
                                            r = self.r_R2(s)  # routine call                                               #                   #
                                            if r:                                                                          #                   #
                                                r = s.set_range(self.left, self.right, u'')  # delete                      #                   #
                                                if r:                                                                      #                   #
                                                    self.left = s.cursor  ##                                               # try               #
                                                    r = True              ## [                                             #                   #
                                                    if r:                                                                  #                   #
                                                        r = s.starts_with(u'ic')  # character check                        #                   #
                                                        if r:                                                              #                   #
                                                            self.right = s.cursor  ##                                      #                   #
                                                            r = True               ## ]                                    #                   #
                                                            if r:                                                          #                   #
                                                                r = self.r_R2(s)  # routine call                           #                   #
                                                                if r:                                                      #                   #
                                                                    r = s.set_range(self.left, self.right, u'')  # delete  #                   #
                                if not r:                                                                                  #                   #
                                    r = True                                                                               #                   #
                                    s.cursor = len(s) - var49                                                              ##                  ##
        return r
    
    def r_verb_suffix(self, s):
        r = True
        var55 = len(s) - s.cursor                                                            ##
        var56 = s.limit                                                                      #
        r = s.to_mark(self.i_pV)  # tomark                                                   #
        if r:                                                                                #
            s.limit = s.cursor                                                               #
            s.cursor = len(s) - var55                                                        #
            self.left = s.cursor  ##                                                         #
            r = True              ## [                                                       #
            if r:                                                                            #
                a_8 = None                                          ##                       #
                r = False                                           #                        #
                var51 = s.cursor                                    #                        #
                for var50, var54, var53 in _a_8:                    #                        #
                    if s.starts_with(var50):                        #                        #
                        var52 = s.cursor                            #                        # setlimit
                        r = (not var54) or getattr(self, var54)(s)  # substring              #
                        if r:                                       #                        #
                          s.cursor = var52                          #                        #
                          a_8 = var53                               #                        #
                          break                                     #                        #
                    s.cursor = var51                                ##                       #
                if r:                                                                        #
                    self.right = s.cursor  ##                                                #
                    r = True               ## ]                                              #
                    if r:                                                                    #
                        if a_8 == 0:                                               ##        #
                            r = s.set_range(self.left, self.right, u'')  # delete  ## among  #
            s.limit = var56                                                                  ##
        return r
    
    def r_vowel_suffix(self, s):
        r = True
        var57 = len(s) - s.cursor                                                                  ##
        self.left = s.cursor  ##                                                                   #
        r = True              ## [                                                                 #
        if r:                                                                                      #
            if s.cursor == s.limit:                   ##                                           #
                r = False                             #                                            #
            else:                                     #                                            #
                r = s.chars[s.cursor - 1] in _g_AEIO  # grouping check                             #
            if r:                                     #                                            #
                s.cursor -= 1                         ##                                           #
            if r:                                                                                  #
                self.right = s.cursor  ##                                                          #
                r = True               ## ]                                                        #
                if r:                                                                              #
                    r = self.r_RV(s)  # routine call                                               #
                    if r:                                                                          #
                        r = s.set_range(self.left, self.right, u'')  # delete                      # try
                        if r:                                                                      #
                            self.left = s.cursor  ##                                               #
                            r = True              ## [                                             #
                            if r:                                                                  #
                                r = s.starts_with(u'i')  # character check                         #
                                if r:                                                              #
                                    self.right = s.cursor  ##                                      #
                                    r = True               ## ]                                    #
                                    if r:                                                          #
                                        r = self.r_RV(s)  # routine call                           #
                                        if r:                                                      #
                                            r = s.set_range(self.left, self.right, u'')  # delete  #
        if not r:                                                                                  #
            r = True                                                                               #
            s.cursor = len(s) - var57                                                              ##
        if r:
            var58 = len(s) - s.cursor                                                  ##
            self.left = s.cursor  ##                                                   #
            r = True              ## [                                                 #
            if r:                                                                      #
                r = s.starts_with(u'h')  # character check                             #
                if r:                                                                  #
                    self.right = s.cursor  ##                                          #
                    r = True               ## ]                                        #
                    if r:                                                              #
                        if s.cursor == s.limit:                 ##                     #
                            r = False                           #                      #
                        else:                                   #                      # try
                            r = s.chars[s.cursor - 1] in _g_CG  # grouping check       #
                        if r:                                   #                      #
                            s.cursor -= 1                       ##                     #
                        if r:                                                          #
                            r = self.r_RV(s)  # routine call                           #
                            if r:                                                      #
                                r = s.set_range(self.left, self.right, u'')  # delete  #
            if not r:                                                                  #
                r = True                                                               #
                s.cursor = len(s) - var58                                              ##
        return r
    
    def r_stem(self, s):
        r = True
        var59 = s.cursor                       ##
        r = self.r_prelude(s)  # routine call  #
        s.cursor = var59                       # do
        r = True                               ##
        if r:
            var60 = s.cursor                            ##
            r = self.r_mark_regions(s)  # routine call  #
            s.cursor = var60                            # do
            r = True                                    ##
            if r:
                var65 = s.cursor                                               ##
                var66 = len(s) - s.limit                                       #
                s.direction *= -1                                              #
                s.cursor, s.limit = s.limit, s.cursor                          #
                var61 = len(s) - s.cursor                       ##             #
                r = self.r_attached_pronoun(s)  # routine call  #              #
                s.cursor = len(s) - var61                       # do           #
                r = True                                        ##             #
                if r:                                                          #
                    var63 = len(s) - s.cursor                            ##    #
                    var62 = len(s) - s.cursor                      ##    #     #
                    r = self.r_standard_suffix(s)  # routine call  #     #     #
                    if not r:                                      # or  #     # backwards
                        s.cursor = len(s) - var62                  #     # do  #
                        r = self.r_verb_suffix(s)  # routine call  ##    #     #
                    s.cursor = len(s) - var63                            #     #
                    r = True                                             ##    #
                    if r:                                                      #
                        var64 = len(s) - s.cursor                   ##         #
                        r = self.r_vowel_suffix(s)  # routine call  #          #
                        s.cursor = len(s) - var64                   # do       #
                        r = True                                    ##         #
                s.direction *= -1                                              #
                s.cursor = var65                                               #
                s.limit = len(s) - var66                                       ##
                if r:
                    var67 = s.cursor                        ##
                    r = self.r_postlude(s)  # routine call  #
                    s.cursor = var67                        # do
                    r = True                                ##
        return r
