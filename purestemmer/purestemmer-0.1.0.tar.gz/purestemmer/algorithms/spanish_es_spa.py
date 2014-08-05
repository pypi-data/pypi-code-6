#!/usr/bin/env python
# vim:fileencoding=utf-8



# This file was auto-generated on 2014-08-05 20:04:20 using
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

_g_v = set(u'aeiou\xe1\xe9\xed\xf3\xfa\xfc')
_a_1 = ((u'\xe1', '', 0), (u'\xe9', '', 1), (u'\xed', '', 2), (u'\xf3', '', 3), (u'\xfa', '', 4), (u'', '', 5),)
_a_2 = ((u'selas', '', 0), (u'selos', '', 0), (u'sela', '', 0), (u'selo', '', 0), (u'las', '', 0), (u'les', '', 0), (u'los', '', 0), (u'nos', '', 0), (u'me', '', 0), (u'se', '', 0), (u'la', '', 0), (u'le', '', 0), (u'lo', '', 0),)
_a_3 = ((u'i\xe9ndo', '', 0), (u'iendo', '', 5), (u'yendo', '', 6), (u'\xe1ndo', '', 1), (u'ando', '', 5), (u'\xe1r', '', 2), (u'\xe9r', '', 3), (u'\xedr', '', 4), (u'ar', '', 5), (u'er', '', 5), (u'ir', '', 5),)
_a_4 = ((u'amientos', '', 0), (u'imientos', '', 0), (u'amiento', '', 0), (u'imiento', '', 0), (u'aciones', '', 1), (u'uciones', '', 3), (u'adoras', '', 1), (u'adores', '', 1), (u'ancias', '', 1), (u'log\xedas', '', 2), (u'encias', '', 4), (u'amente', '', 5), (u'idades', '', 7), (u'anzas', '', 0), (u'ismos', '', 0), (u'ables', '', 0), (u'ibles', '', 0), (u'istas', '', 0), (u'adora', '', 1), (u'aci\xf3n', '', 1), (u'antes', '', 1), (u'ancia', '', 1), (u'log\xeda', '', 2), (u'uci\xf3n', '', 3), (u'encia', '', 4), (u'mente', '', 6), (u'anza', '', 0), (u'icos', '', 0), (u'icas', '', 0), (u'ismo', '', 0), (u'able', '', 0), (u'ible', '', 0), (u'ista', '', 0), (u'osos', '', 0), (u'osas', '', 0), (u'ador', '', 1), (u'ante', '', 1), (u'idad', '', 7), (u'ivas', '', 8), (u'ivos', '', 8), (u'ico', '', 0), (u'ica', '', 0), (u'oso', '', 0), (u'osa', '', 0), (u'iva', '', 8), (u'ivo', '', 8),)
_a_5 = ((u'iv', '', 0), (u'os', '', 1), (u'ic', '', 1), (u'ad', '', 1),)
_a_6 = ((u'ante', '', 0), (u'able', '', 0), (u'ible', '', 0),)
_a_7 = ((u'abil', '', 0), (u'ic', '', 0), (u'iv', '', 0),)
_a_8 = ((u'yeron', '', 0), (u'yendo', '', 0), (u'yamos', '', 0), (u'yais', '', 0), (u'yan', '', 0), (u'yen', '', 0), (u'yas', '', 0), (u'yes', '', 0), (u'ya', '', 0), (u'ye', '', 0), (u'yo', '', 0), (u'y\xf3', '', 0),)
_a_9 = ((u'ar\xedamos', '', 1), (u'er\xedamos', '', 1), (u'ir\xedamos', '', 1), (u'i\xe9ramos', '', 1), (u'i\xe9semos', '', 1), (u'ar\xedais', '', 1), (u'aremos', '', 1), (u'er\xedais', '', 1), (u'eremos', '', 1), (u'ir\xedais', '', 1), (u'iremos', '', 1), (u'ierais', '', 1), (u'ieseis', '', 1), (u'asteis', '', 1), (u'isteis', '', 1), (u'\xe1bamos', '', 1), (u'\xe1ramos', '', 1), (u'\xe1semos', '', 1), (u'ar\xedan', '', 1), (u'ar\xedas', '', 1), (u'ar\xe9is', '', 1), (u'er\xedan', '', 1), (u'er\xedas', '', 1), (u'er\xe9is', '', 1), (u'ir\xedan', '', 1), (u'ir\xedas', '', 1), (u'ir\xe9is', '', 1), (u'ieran', '', 1), (u'iesen', '', 1), (u'ieron', '', 1), (u'iendo', '', 1), (u'ieras', '', 1), (u'ieses', '', 1), (u'abais', '', 1), (u'arais', '', 1), (u'aseis', '', 1), (u'\xedamos', '', 1), (u'emos', '', 0), (u'ar\xe1n', '', 1), (u'ar\xe1s', '', 1), (u'ar\xeda', '', 1), (u'er\xe1n', '', 1), (u'er\xe1s', '', 1), (u'er\xeda', '', 1), (u'ir\xe1n', '', 1), (u'ir\xe1s', '', 1), (u'ir\xeda', '', 1), (u'iera', '', 1), (u'iese', '', 1), (u'aste', '', 1), (u'iste', '', 1), (u'aban', '', 1), (u'aran', '', 1), (u'asen', '', 1), (u'aron', '', 1), (u'ando', '', 1), (u'abas', '', 1), (u'adas', '', 1), (u'idas', '', 1), (u'aras', '', 1), (u'ases', '', 1), (u'\xedais', '', 1), (u'ados', '', 1), (u'idos', '', 1), (u'amos', '', 1), (u'imos', '', 1), (u'\xe9is', '', 0), (u'ar\xe1', '', 1), (u'ar\xe9', '', 1), (u'er\xe1', '', 1), (u'er\xe9', '', 1), (u'ir\xe1', '', 1), (u'ir\xe9', '', 1), (u'aba', '', 1), (u'ada', '', 1), (u'ida', '', 1), (u'ara', '', 1), (u'ase', '', 1), (u'\xedan', '', 1), (u'ado', '', 1), (u'ido', '', 1), (u'\xedas', '', 1), (u'\xe1is', '', 1), (u'en', '', 0), (u'es', '', 0), (u'\xeda', '', 1), (u'ad', '', 1), (u'ed', '', 1), (u'id', '', 1), (u'an', '', 1), (u'i\xf3', '', 1), (u'ar', '', 1), (u'er', '', 1), (u'ir', '', 1), (u'as', '', 1), (u'\xeds', '', 1),)
_a_10 = ((u'os', '', 0), (u'a', '', 0), (u'o', '', 0), (u'\xe1', '', 0), (u'\xed', '', 0), (u'\xf3', '', 0), (u'e', '', 1), (u'\xe9', '', 1),)

class _Program(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.i_pV = 0
        self.i_p1 = 0
        self.i_p2 = 0

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
                    var3 = s.cursor                                                                                         ##
                    var2 = s.cursor                                                                                   ##    #
                    if s.cursor == s.limit:            ##                                                             #     #
                        r = False                      #                                                              #     #
                    else:                              #                                                              #     #
                        r = s.chars[s.cursor] in _g_v  # grouping check                                               #     #
                    if r:                              #                                                              #     #
                        s.cursor += 1                  ##                                                             #     #
                    if r:                                                                                             #     #
                        var0 = s.cursor                                                                         ##    #     #
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
                            s.cursor = var0                                                                     #     #     #
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
                        s.cursor = var2                                                                               #     #
                        if s.cursor == s.limit:                ##                                                     #     #
                            r = False                          #                                                      #     #
                        else:                                  #                                                      #     #
                            r = s.chars[s.cursor] not in _g_v  # negative grouping check                              #     #
                        if r:                                  #                                                      #     #
                            s.cursor += 1                      ##                                                     #     #
                        if r:                                                                                         #     #
                            var1 = s.cursor                                                        ##                 #     #
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
                                s.cursor = var1                                                    #                  #     #
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
                    s.cursor = var3                                                                                         #
                    r = True                                                                                                ##
                    if r:
                        var4 = s.cursor                                                                                 ##
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
                        s.cursor = var4                                                                                 #
                        r = True                                                                                        ##
        return r
    
    def r_postlude(self, s):
        r = True
        while True:                                                                      ##
            var10 = s.cursor                                                             #
            self.left = s.cursor  ##                                                     #
            r = True              ## [                                                   #
            if r:                                                                        #
                a_1 = None                                        ##                     #
                r = False                                         #                      #
                var6 = s.cursor                                   #                      #
                for var5, var9, var8 in _a_1:                     #                      #
                    if s.starts_with(var5):                       #                      #
                        var7 = s.cursor                           #                      #
                        r = (not var9) or getattr(self, var9)(s)  # substring            #
                        if r:                                     #                      #
                          s.cursor = var7                         #                      #
                          a_1 = var8                              #                      #
                          break                                   #                      #
                    s.cursor = var6                               ##                     #
                if r:                                                                    #
                    self.right = s.cursor  ##                                            # repeat
                    r = True               ## ]                                          #
                    if r:                                                                #
                        if a_1 == 0:                                            ##       #
                            r = s.set_range(self.left, self.right, u'a')  # <-  #        #
                        if a_1 == 1:                                            #        #
                            r = s.set_range(self.left, self.right, u'e')  # <-  #        #
                        if a_1 == 2:                                            #        #
                            r = s.set_range(self.left, self.right, u'i')  # <-  #        #
                        if a_1 == 3:                                            # among  #
                            r = s.set_range(self.left, self.right, u'o')  # <-  #        #
                        if a_1 == 4:                                            #        #
                            r = s.set_range(self.left, self.right, u'u')  # <-  #        #
                        if a_1 == 5:                                            #        #
                            r = s.hop(1)  # next                                ##       #
            if not r:                                                                    #
                s.cursor = var10                                                         #
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
            a_2 = None                                          ##
            r = False                                           #
            var12 = s.cursor                                    #
            for var11, var15, var14 in _a_2:                    #
                if s.starts_with(var11):                        #
                    var13 = s.cursor                            #
                    r = (not var15) or getattr(self, var15)(s)  # substring
                    if r:                                       #
                      s.cursor = var13                          #
                      a_2 = var14                               #
                      break                                     #
                s.cursor = var12                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_2 == 0:  ##
                        r = True  ## among
                    if r:
                        a_3 = None                                          ##
                        r = False                                           #
                        var17 = s.cursor                                    #
                        for var16, var20, var19 in _a_3:                    #
                            if s.starts_with(var16):                        #
                                var18 = s.cursor                            #
                                r = (not var20) or getattr(self, var20)(s)  # substring
                                if r:                                       #
                                  s.cursor = var18                          #
                                  a_3 = var19                               #
                                  break                                     #
                            s.cursor = var17                                ##
                        if r:
                            r = self.r_RV(s)  # routine call
                            if r:
                                if a_3 == 0:                                                    ##
                                    self.right = s.cursor  ##                                   #
                                    r = True               ## ]                                 #
                                    if r:                                                       #
                                        r = s.set_range(self.left, self.right, u'iendo')  # <-  #
                                if a_3 == 1:                                                    #
                                    self.right = s.cursor  ##                                   #
                                    r = True               ## ]                                 #
                                    if r:                                                       #
                                        r = s.set_range(self.left, self.right, u'ando')  # <-   #
                                if a_3 == 2:                                                    #
                                    self.right = s.cursor  ##                                   #
                                    r = True               ## ]                                 #
                                    if r:                                                       #
                                        r = s.set_range(self.left, self.right, u'ar')  # <-     #
                                if a_3 == 3:                                                    # among
                                    self.right = s.cursor  ##                                   #
                                    r = True               ## ]                                 #
                                    if r:                                                       #
                                        r = s.set_range(self.left, self.right, u'er')  # <-     #
                                if a_3 == 4:                                                    #
                                    self.right = s.cursor  ##                                   #
                                    r = True               ## ]                                 #
                                    if r:                                                       #
                                        r = s.set_range(self.left, self.right, u'ir')  # <-     #
                                if a_3 == 5:                                                    #
                                    r = s.set_range(self.left, self.right, u'')  # delete       #
                                if a_3 == 6:                                                    #
                                    r = s.starts_with(u'u')  # character check                  #
                                    if r:                                                       #
                                        r = s.set_range(self.left, self.right, u'')  # delete   ##
        return r
    
    def r_standard_suffix(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_4 = None                                          ##
            r = False                                           #
            var22 = s.cursor                                    #
            for var21, var25, var24 in _a_4:                    #
                if s.starts_with(var21):                        #
                    var23 = s.cursor                            #
                    r = (not var25) or getattr(self, var25)(s)  # substring
                    if r:                                       #
                      s.cursor = var23                          #
                      a_4 = var24                               #
                      break                                     #
                s.cursor = var22                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_4 == 0:                                                                                                               ##
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                    if a_4 == 1:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var26 = len(s) - s.cursor                                              ##                                      #
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
                                    s.cursor = len(s) - var26                                          ##                                      #
                    if a_4 == 2:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'log')  # <-                                                               #
                    if a_4 == 3:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'u')  # <-                                                                 #
                    if a_4 == 4:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'ente')  # <-                                                              #
                    if a_4 == 5:                                                                                                               #
                        r = self.r_R1(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var32 = len(s) - s.cursor                                                                               ##     #
                                self.left = s.cursor  ##                                                                                #      #
                                r = True              ## [                                                                              #      #
                                if r:                                                                                                   #      #
                                    a_5 = None                                          ##                                              #      #
                                    r = False                                           #                                               #      #
                                    var28 = s.cursor                                    #                                               #      #
                                    for var27, var31, var30 in _a_5:                    #                                               #      #
                                        if s.starts_with(var27):                        #                                               #      #
                                            var29 = s.cursor                            #                                               #      #
                                            r = (not var31) or getattr(self, var31)(s)  # substring                                     #      #
                                            if r:                                       #                                               #      #
                                              s.cursor = var29                          #                                               #      #
                                              a_5 = var30                               #                                               #      #
                                              break                                     #                                               #      #
                                        s.cursor = var28                                ##                                              #      #
                                    if r:                                                                                               #      #
                                        self.right = s.cursor  ##                                                                       #      #
                                        r = True               ## ]                                                                     #      #
                                        if r:                                                                                           #      #
                                            r = self.r_R2(s)  # routine call                                                            # try  #
                                            if r:                                                                                       #      #
                                                r = s.set_range(self.left, self.right, u'')  # delete                                   #      #
                                                if r:                                                                                   #      #
                                                    if a_5 == 0:                                                               ##       #      #
                                                        self.left = s.cursor  ##                                               #        #      #
                                                        r = True              ## [                                             #        #      #
                                                        if r:                                                                  #        #      #
                                                            r = s.starts_with(u'at')  # character check                        #        #      #
                                                            if r:                                                              #        #      #
                                                                self.right = s.cursor  ##                                      #        #      #
                                                                r = True               ## ]                                    # among  #      #
                                                                if r:                                                          #        #      #
                                                                    r = self.r_R2(s)  # routine call                           #        #      #
                                                                    if r:                                                      #        #      #
                                                                        r = s.set_range(self.left, self.right, u'')  # delete  #        #      #
                                                    if a_5 == 1:                                                               #        #      #
                                                        r = True                                                               ##       #      #
                                if not r:                                                                                               #      #
                                    r = True                                                                                            #      #
                                    s.cursor = len(s) - var32                                                                           ##     #
                    if a_4 == 6:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       # among
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var38 = len(s) - s.cursor                                                           ##                         #
                                self.left = s.cursor  ##                                                            #                          #
                                r = True              ## [                                                          #                          #
                                if r:                                                                               #                          #
                                    a_6 = None                                          ##                          #                          #
                                    r = False                                           #                           #                          #
                                    var34 = s.cursor                                    #                           #                          #
                                    for var33, var37, var36 in _a_6:                    #                           #                          #
                                        if s.starts_with(var33):                        #                           #                          #
                                            var35 = s.cursor                            #                           #                          #
                                            r = (not var37) or getattr(self, var37)(s)  # substring                 #                          #
                                            if r:                                       #                           #                          #
                                              s.cursor = var35                          #                           #                          #
                                              a_6 = var36                               #                           # try                      #
                                              break                                     #                           #                          #
                                        s.cursor = var34                                ##                          #                          #
                                    if r:                                                                           #                          #
                                        self.right = s.cursor  ##                                                   #                          #
                                        r = True               ## ]                                                 #                          #
                                        if r:                                                                       #                          #
                                            if a_6 == 0:                                                   ##       #                          #
                                                r = self.r_R2(s)  # routine call                           #        #                          #
                                                if r:                                                      # among  #                          #
                                                    r = s.set_range(self.left, self.right, u'')  # delete  ##       #                          #
                                if not r:                                                                           #                          #
                                    r = True                                                                        #                          #
                                    s.cursor = len(s) - var38                                                       ##                         #
                    if a_4 == 7:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var44 = len(s) - s.cursor                                                           ##                         #
                                self.left = s.cursor  ##                                                            #                          #
                                r = True              ## [                                                          #                          #
                                if r:                                                                               #                          #
                                    a_7 = None                                          ##                          #                          #
                                    r = False                                           #                           #                          #
                                    var40 = s.cursor                                    #                           #                          #
                                    for var39, var43, var42 in _a_7:                    #                           #                          #
                                        if s.starts_with(var39):                        #                           #                          #
                                            var41 = s.cursor                            #                           #                          #
                                            r = (not var43) or getattr(self, var43)(s)  # substring                 #                          #
                                            if r:                                       #                           #                          #
                                              s.cursor = var41                          #                           #                          #
                                              a_7 = var42                               #                           # try                      #
                                              break                                     #                           #                          #
                                        s.cursor = var40                                ##                          #                          #
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
                                    s.cursor = len(s) - var44                                                       ##                         #
                    if a_4 == 8:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var45 = len(s) - s.cursor                                              ##                                      #
                                self.left = s.cursor  ##                                               #                                       #
                                r = True              ## [                                             #                                       #
                                if r:                                                                  #                                       #
                                    r = s.starts_with(u'at')  # character check                        #                                       #
                                    if r:                                                              #                                       #
                                        self.right = s.cursor  ##                                      #                                       #
                                        r = True               ## ]                                    # try                                   #
                                        if r:                                                          #                                       #
                                            r = self.r_R2(s)  # routine call                           #                                       #
                                            if r:                                                      #                                       #
                                                r = s.set_range(self.left, self.right, u'')  # delete  #                                       #
                                if not r:                                                              #                                       #
                                    r = True                                                           #                                       #
                                    s.cursor = len(s) - var45                                          ##                                      ##
        return r
    
    def r_y_verb_suffix(self, s):
        r = True
        var51 = len(s) - s.cursor                                                ##
        var52 = s.limit                                                          #
        r = s.to_mark(self.i_pV)  # tomark                                       #
        if r:                                                                    #
            s.limit = s.cursor                                                   #
            s.cursor = len(s) - var51                                            #
            self.left = s.cursor  ##                                             #
            r = True              ## [                                           #
            if r:                                                                #
                a_8 = None                                          ##           #
                r = False                                           #            #
                var47 = s.cursor                                    #            #
                for var46, var50, var49 in _a_8:                    #            # setlimit
                    if s.starts_with(var46):                        #            #
                        var48 = s.cursor                            #            #
                        r = (not var50) or getattr(self, var50)(s)  # substring  #
                        if r:                                       #            #
                          s.cursor = var48                          #            #
                          a_8 = var49                               #            #
                          break                                     #            #
                    s.cursor = var47                                ##           #
                if r:                                                            #
                    self.right = s.cursor  ##                                    #
                    r = True               ## ]                                  #
            s.limit = var52                                                      ##
        if r:
            if a_8 == 0:                                                   ##
                r = s.starts_with(u'u')  # character check                 #
                if r:                                                      # among
                    r = s.set_range(self.left, self.right, u'')  # delete  ##
        return r
    
    def r_verb_suffix(self, s):
        r = True
        var58 = len(s) - s.cursor                                                ##
        var59 = s.limit                                                          #
        r = s.to_mark(self.i_pV)  # tomark                                       #
        if r:                                                                    #
            s.limit = s.cursor                                                   #
            s.cursor = len(s) - var58                                            #
            self.left = s.cursor  ##                                             #
            r = True              ## [                                           #
            if r:                                                                #
                a_9 = None                                          ##           #
                r = False                                           #            #
                var54 = s.cursor                                    #            #
                for var53, var57, var56 in _a_9:                    #            # setlimit
                    if s.starts_with(var53):                        #            #
                        var55 = s.cursor                            #            #
                        r = (not var57) or getattr(self, var57)(s)  # substring  #
                        if r:                                       #            #
                          s.cursor = var55                          #            #
                          a_9 = var56                               #            #
                          break                                     #            #
                    s.cursor = var54                                ##           #
                if r:                                                            #
                    self.right = s.cursor  ##                                    #
                    r = True               ## ]                                  #
            s.limit = var59                                                      ##
        if r:
            if a_9 == 0:                                                       ##
                var61 = len(s) - s.cursor                               ##     #
                r = s.starts_with(u'u')  # character check              #      #
                if r:                                                   #      #
                    var60 = len(s) - s.cursor                   ##      #      #
                    r = s.starts_with(u'g')  # character check  # test  # try  #
                    s.cursor = len(s) - var60                   ##      #      #
                if not r:                                               #      #
                    r = True                                            #      # among
                    s.cursor = len(s) - var61                           ##     #
                if r:                                                          #
                    self.right = s.cursor  ##                                  #
                    r = True               ## ]                                #
                    if r:                                                      #
                        r = s.set_range(self.left, self.right, u'')  # delete  #
            if a_9 == 1:                                                       #
                r = s.set_range(self.left, self.right, u'')  # delete          ##
        return r
    
    def r_residual_suffix(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_10 = None                                         ##
            r = False                                           #
            var63 = s.cursor                                    #
            for var62, var66, var65 in _a_10:                   #
                if s.starts_with(var62):                        #
                    var64 = s.cursor                            #
                    r = (not var66) or getattr(self, var66)(s)  # substring
                    if r:                                       #
                      s.cursor = var64                          #
                      a_10 = var65                              #
                      break                                     #
                s.cursor = var63                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_10 == 0:                                                                                 ##
                        r = self.r_RV(s)  # routine call                                                          #
                        if r:                                                                                     #
                            r = s.set_range(self.left, self.right, u'')  # delete                                 #
                    if a_10 == 1:                                                                                 #
                        r = self.r_RV(s)  # routine call                                                          #
                        if r:                                                                                     #
                            r = s.set_range(self.left, self.right, u'')  # delete                                 #
                            if r:                                                                                 #
                                var68 = len(s) - s.cursor                                                  ##     #
                                self.left = s.cursor  ##                                                   #      #
                                r = True              ## [                                                 #      #
                                if r:                                                                      #      #
                                    r = s.starts_with(u'u')  # character check                             #      #
                                    if r:                                                                  #      # among
                                        self.right = s.cursor  ##                                          #      #
                                        r = True               ## ]                                        #      #
                                        if r:                                                              #      #
                                            var67 = len(s) - s.cursor                   ##                 # try  #
                                            r = s.starts_with(u'g')  # character check  # test             #      #
                                            s.cursor = len(s) - var67                   ##                 #      #
                                            if r:                                                          #      #
                                                r = self.r_RV(s)  # routine call                           #      #
                                                if r:                                                      #      #
                                                    r = s.set_range(self.left, self.right, u'')  # delete  #      #
                                if not r:                                                                  #      #
                                    r = True                                                               #      #
                                    s.cursor = len(s) - var68                                              ##     ##
        return r
    
    def r_stem(self, s):
        r = True
        var69 = s.cursor                            ##
        r = self.r_mark_regions(s)  # routine call  #
        s.cursor = var69                            # do
        r = True                                    ##
        if r:
            var75 = s.cursor                                                       ##
            var76 = len(s) - s.limit                                               #
            s.direction *= -1                                                      #
            s.cursor, s.limit = s.limit, s.cursor                                  #
            var70 = len(s) - s.cursor                       ##                     #
            r = self.r_attached_pronoun(s)  # routine call  #                      #
            s.cursor = len(s) - var70                       # do                   #
            r = True                                        ##                     #
            if r:                                                                  #
                var73 = len(s) - s.cursor                                    ##    #
                var72 = len(s) - s.cursor                              ##    #     #
                var71 = len(s) - s.cursor                        ##    #     #     #
                r = self.r_standard_suffix(s)  # routine call    #     #     #     #
                if not r:                                        # or  #     #     #
                    s.cursor = len(s) - var71                    #     # or  #     # backwards
                    r = self.r_y_verb_suffix(s)  # routine call  ##    #     # do  #
                if not r:                                              #     #     #
                    s.cursor = len(s) - var72                          #     #     #
                    r = self.r_verb_suffix(s)  # routine call          ##    #     #
                s.cursor = len(s) - var73                                    #     #
                r = True                                                     ##    #
                if r:                                                              #
                    var74 = len(s) - s.cursor                      ##              #
                    r = self.r_residual_suffix(s)  # routine call  #               #
                    s.cursor = len(s) - var74                      # do            #
                    r = True                                       ##              #
            s.direction *= -1                                                      #
            s.cursor = var75                                                       #
            s.limit = len(s) - var76                                               ##
            if r:
                var77 = s.cursor                        ##
                r = self.r_postlude(s)  # routine call  #
                s.cursor = var77                        # do
                r = True                                ##
        return r
