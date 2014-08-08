#!/usr/bin/env python
# vim:fileencoding=utf-8



# This file was auto-generated on 2014-08-05 20:04:16 using
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

_g_v = set(u'aeiou\xe1\xe9\xed\xf3\xfa\xe2\xea\xf4')
_a_1 = ((u'\xe3', '', 0), (u'\xf5', '', 1), (u'', '', 2),)
_a_2 = ((u'a~', '', 0), (u'o~', '', 1), (u'', '', 2),)
_a_3 = ((u'amentos', '', 0), (u'imentos', '', 0), (u'uciones', '', 2), (u'amento', '', 0), (u'imento', '', 0), (u'adoras', '', 0), (u'adores', '', 0), (u'a\xe7o~es', '', 0), (u'log\xedas', '', 1), (u'\xeancias', '', 3), (u'amente', '', 4), (u'idades', '', 6), (u'ismos', '', 0), (u'istas', '', 0), (u'adora', '', 0), (u'a\xe7a~o', '', 0), (u'antes', '', 0), (u'\xe2ncia', '', 0), (u'log\xeda', '', 1), (u'uci\xf3n', '', 2), (u'\xeancia', '', 3), (u'mente', '', 5), (u'idade', '', 6), (u'ezas', '', 0), (u'icos', '', 0), (u'icas', '', 0), (u'ismo', '', 0), (u'\xe1vel', '', 0), (u'\xedvel', '', 0), (u'ista', '', 0), (u'osos', '', 0), (u'osas', '', 0), (u'ador', '', 0), (u'ante', '', 0), (u'ivas', '', 7), (u'ivos', '', 7), (u'iras', '', 8), (u'eza', '', 0), (u'ico', '', 0), (u'ica', '', 0), (u'oso', '', 0), (u'osa', '', 0), (u'iva', '', 7), (u'ivo', '', 7), (u'ira', '', 8),)
_a_4 = ((u'iv', '', 0), (u'os', '', 1), (u'ic', '', 1), (u'ad', '', 1),)
_a_5 = ((u'ante', '', 0), (u'avel', '', 0), (u'\xedvel', '', 0),)
_a_6 = ((u'abil', '', 0), (u'ic', '', 0), (u'iv', '', 0),)
_a_7 = ((u'ar\xedamos', '', 0), (u'er\xedamos', '', 0), (u'ir\xedamos', '', 0), (u'\xe1ssemos', '', 0), (u'\xeassemos', '', 0), (u'\xedssemos', '', 0), (u'ar\xedeis', '', 0), (u'er\xedeis', '', 0), (u'ir\xedeis', '', 0), (u'\xe1sseis', '', 0), (u'\xe9sseis', '', 0), (u'\xedsseis', '', 0), (u'\xe1ramos', '', 0), (u'\xe9ramos', '', 0), (u'\xedramos', '', 0), (u'\xe1vamos', '', 0), (u'aremos', '', 0), (u'eremos', '', 0), (u'iremos', '', 0), (u'ariam', '', 0), (u'eriam', '', 0), (u'iriam', '', 0), (u'assem', '', 0), (u'essem', '', 0), (u'issem', '', 0), (u'ara~o', '', 0), (u'era~o', '', 0), (u'ira~o', '', 0), (u'arias', '', 0), (u'erias', '', 0), (u'irias', '', 0), (u'ardes', '', 0), (u'erdes', '', 0), (u'irdes', '', 0), (u'asses', '', 0), (u'esses', '', 0), (u'isses', '', 0), (u'astes', '', 0), (u'estes', '', 0), (u'istes', '', 0), (u'\xe1reis', '', 0), (u'areis', '', 0), (u'\xe9reis', '', 0), (u'ereis', '', 0), (u'\xedreis', '', 0), (u'ireis', '', 0), (u'\xe1veis', '', 0), (u'\xedamos', '', 0), (u'armos', '', 0), (u'ermos', '', 0), (u'irmos', '', 0), (u'aria', '', 0), (u'eria', '', 0), (u'iria', '', 0), (u'asse', '', 0), (u'esse', '', 0), (u'isse', '', 0), (u'aste', '', 0), (u'este', '', 0), (u'iste', '', 0), (u'arei', '', 0), (u'erei', '', 0), (u'irei', '', 0), (u'aram', '', 0), (u'eram', '', 0), (u'iram', '', 0), (u'avam', '', 0), (u'arem', '', 0), (u'erem', '', 0), (u'irem', '', 0), (u'ando', '', 0), (u'endo', '', 0), (u'indo', '', 0), (u'adas', '', 0), (u'idas', '', 0), (u'ar\xe1s', '', 0), (u'aras', '', 0), (u'er\xe1s', '', 0), (u'eras', '', 0), (u'ir\xe1s', '', 0), (u'avas', '', 0), (u'ares', '', 0), (u'eres', '', 0), (u'ires', '', 0), (u'\xedeis', '', 0), (u'ados', '', 0), (u'idos', '', 0), (u'\xe1mos', '', 0), (u'amos', '', 0), (u'emos', '', 0), (u'imos', '', 0), (u'iras', '', 0), (u'ada', '', 0), (u'ida', '', 0), (u'ar\xe1', '', 0), (u'ara', '', 0), (u'er\xe1', '', 0), (u'era', '', 0), (u'ir\xe1', '', 0), (u'ava', '', 0), (u'iam', '', 0), (u'ado', '', 0), (u'ido', '', 0), (u'ias', '', 0), (u'ais', '', 0), (u'eis', '', 0), (u'ira', '', 0), (u'ia', '', 0), (u'ei', '', 0), (u'am', '', 0), (u'em', '', 0), (u'ar', '', 0), (u'er', '', 0), (u'ir', '', 0), (u'as', '', 0), (u'es', '', 0), (u'is', '', 0), (u'eu', '', 0), (u'iu', '', 0), (u'ou', '', 0),)
_a_8 = ((u'os', '', 0), (u'a', '', 0), (u'i', '', 0), (u'o', '', 0), (u'\xe1', '', 0), (u'\xed', '', 0), (u'\xf3', '', 0),)
_a_9 = ((u'e', '', 0), (u'\xe9', '', 0), (u'\xea', '', 0), (u'\xe7', '', 1),)

class _Program(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.i_pV = 0
        self.i_p1 = 0
        self.i_p2 = 0

    def r_prelude(self, s):
        r = True
        while True:                                                                       ##
            var5 = s.cursor                                                               #
            self.left = s.cursor  ##                                                      #
            r = True              ## [                                                    #
            if r:                                                                         #
                a_1 = None                                        ##                      #
                r = False                                         #                       #
                var1 = s.cursor                                   #                       #
                for var0, var4, var3 in _a_1:                     #                       #
                    if s.starts_with(var0):                       #                       #
                        var2 = s.cursor                           #                       #
                        r = (not var4) or getattr(self, var4)(s)  # substring             #
                        if r:                                     #                       #
                          s.cursor = var2                         #                       #
                          a_1 = var3                              #                       #
                          break                                   #                       # repeat
                    s.cursor = var1                               ##                      #
                if r:                                                                     #
                    self.right = s.cursor  ##                                             #
                    r = True               ## ]                                           #
                    if r:                                                                 #
                        if a_1 == 0:                                             ##       #
                            r = s.set_range(self.left, self.right, u'a~')  # <-  #        #
                        if a_1 == 1:                                             #        #
                            r = s.set_range(self.left, self.right, u'o~')  # <-  # among  #
                        if a_1 == 2:                                             #        #
                            r = s.hop(1)  # next                                 ##       #
            if not r:                                                                     #
                s.cursor = var5                                                           #
                break                                                                     #
        r = True                                                                          ##
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
                    var9 = s.cursor                                                                                         ##
                    var8 = s.cursor                                                                                   ##    #
                    if s.cursor == s.limit:            ##                                                             #     #
                        r = False                      #                                                              #     #
                    else:                              #                                                              #     #
                        r = s.chars[s.cursor] in _g_v  # grouping check                                               #     #
                    if r:                              #                                                              #     #
                        s.cursor += 1                  ##                                                             #     #
                    if r:                                                                                             #     #
                        var6 = s.cursor                                                                         ##    #     #
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
                            s.cursor = var6                                                                     #     #     #
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
                        s.cursor = var8                                                                               #     #
                        if s.cursor == s.limit:                ##                                                     #     #
                            r = False                          #                                                      #     #
                        else:                                  #                                                      #     #
                            r = s.chars[s.cursor] not in _g_v  # negative grouping check                              #     #
                        if r:                                  #                                                      #     #
                            s.cursor += 1                      ##                                                     #     #
                        if r:                                                                                         #     #
                            var7 = s.cursor                                                        ##                 #     #
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
                                s.cursor = var7                                                    #                  #     #
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
                    s.cursor = var9                                                                                         #
                    r = True                                                                                                ##
                    if r:
                        var10 = s.cursor                                                                                ##
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
                        s.cursor = var10                                                                                #
                        r = True                                                                                        ##
        return r
    
    def r_postlude(self, s):
        r = True
        while True:                                                                         ##
            var16 = s.cursor                                                                #
            self.left = s.cursor  ##                                                        #
            r = True              ## [                                                      #
            if r:                                                                           #
                a_2 = None                                          ##                      #
                r = False                                           #                       #
                var12 = s.cursor                                    #                       #
                for var11, var15, var14 in _a_2:                    #                       #
                    if s.starts_with(var11):                        #                       #
                        var13 = s.cursor                            #                       #
                        r = (not var15) or getattr(self, var15)(s)  # substring             #
                        if r:                                       #                       #
                          s.cursor = var13                          #                       #
                          a_2 = var14                               #                       #
                          break                                     #                       # repeat
                    s.cursor = var12                                ##                      #
                if r:                                                                       #
                    self.right = s.cursor  ##                                               #
                    r = True               ## ]                                             #
                    if r:                                                                   #
                        if a_2 == 0:                                               ##       #
                            r = s.set_range(self.left, self.right, u'\xe3')  # <-  #        #
                        if a_2 == 1:                                               #        #
                            r = s.set_range(self.left, self.right, u'\xf5')  # <-  # among  #
                        if a_2 == 2:                                               #        #
                            r = s.hop(1)  # next                                   ##       #
            if not r:                                                                       #
                s.cursor = var16                                                            #
                break                                                                       #
        r = True                                                                            ##
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
    
    def r_standard_suffix(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_3 = None                                          ##
            r = False                                           #
            var18 = s.cursor                                    #
            for var17, var21, var20 in _a_3:                    #
                if s.starts_with(var17):                        #
                    var19 = s.cursor                            #
                    r = (not var21) or getattr(self, var21)(s)  # substring
                    if r:                                       #
                      s.cursor = var19                          #
                      a_3 = var20                               #
                      break                                     #
                s.cursor = var18                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_3 == 0:                                                                                                               ##
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                    if a_3 == 1:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'log')  # <-                                                               #
                    if a_3 == 2:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'u')  # <-                                                                 #
                    if a_3 == 3:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'ente')  # <-                                                              #
                    if a_3 == 4:                                                                                                               #
                        r = self.r_R1(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var27 = len(s) - s.cursor                                                                               ##     #
                                self.left = s.cursor  ##                                                                                #      #
                                r = True              ## [                                                                              #      #
                                if r:                                                                                                   #      #
                                    a_4 = None                                          ##                                              #      #
                                    r = False                                           #                                               #      #
                                    var23 = s.cursor                                    #                                               #      #
                                    for var22, var26, var25 in _a_4:                    #                                               #      #
                                        if s.starts_with(var22):                        #                                               #      #
                                            var24 = s.cursor                            #                                               #      #
                                            r = (not var26) or getattr(self, var26)(s)  # substring                                     #      #
                                            if r:                                       #                                               #      #
                                              s.cursor = var24                          #                                               #      #
                                              a_4 = var25                               #                                               #      #
                                              break                                     #                                               #      #
                                        s.cursor = var23                                ##                                              #      #
                                    if r:                                                                                               #      #
                                        self.right = s.cursor  ##                                                                       #      #
                                        r = True               ## ]                                                                     #      #
                                        if r:                                                                                           #      #
                                            r = self.r_R2(s)  # routine call                                                            # try  #
                                            if r:                                                                                       #      #
                                                r = s.set_range(self.left, self.right, u'')  # delete                                   #      #
                                                if r:                                                                                   #      #
                                                    if a_4 == 0:                                                               ##       #      #
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
                                                    if a_4 == 1:                                                               #        #      #
                                                        r = True                                                               ##       #      #
                                if not r:                                                                                               #      #
                                    r = True                                                                                            #      #
                                    s.cursor = len(s) - var27                                                                           ##     #
                    if a_3 == 5:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var33 = len(s) - s.cursor                                                           ##                         #
                                self.left = s.cursor  ##                                                            #                          #
                                r = True              ## [                                                          #                          #
                                if r:                                                                               #                          #
                                    a_5 = None                                          ##                          #                          #
                                    r = False                                           #                           #                          #
                                    var29 = s.cursor                                    #                           #                          #
                                    for var28, var32, var31 in _a_5:                    #                           #                          #
                                        if s.starts_with(var28):                        #                           #                          #
                                            var30 = s.cursor                            #                           #                          # among
                                            r = (not var32) or getattr(self, var32)(s)  # substring                 #                          #
                                            if r:                                       #                           #                          #
                                              s.cursor = var30                          #                           #                          #
                                              a_5 = var31                               #                           # try                      #
                                              break                                     #                           #                          #
                                        s.cursor = var29                                ##                          #                          #
                                    if r:                                                                           #                          #
                                        self.right = s.cursor  ##                                                   #                          #
                                        r = True               ## ]                                                 #                          #
                                        if r:                                                                       #                          #
                                            if a_5 == 0:                                                   ##       #                          #
                                                r = self.r_R2(s)  # routine call                           #        #                          #
                                                if r:                                                      # among  #                          #
                                                    r = s.set_range(self.left, self.right, u'')  # delete  ##       #                          #
                                if not r:                                                                           #                          #
                                    r = True                                                                        #                          #
                                    s.cursor = len(s) - var33                                                       ##                         #
                    if a_3 == 6:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var39 = len(s) - s.cursor                                                           ##                         #
                                self.left = s.cursor  ##                                                            #                          #
                                r = True              ## [                                                          #                          #
                                if r:                                                                               #                          #
                                    a_6 = None                                          ##                          #                          #
                                    r = False                                           #                           #                          #
                                    var35 = s.cursor                                    #                           #                          #
                                    for var34, var38, var37 in _a_6:                    #                           #                          #
                                        if s.starts_with(var34):                        #                           #                          #
                                            var36 = s.cursor                            #                           #                          #
                                            r = (not var38) or getattr(self, var38)(s)  # substring                 #                          #
                                            if r:                                       #                           #                          #
                                              s.cursor = var36                          #                           #                          #
                                              a_6 = var37                               #                           # try                      #
                                              break                                     #                           #                          #
                                        s.cursor = var35                                ##                          #                          #
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
                                    s.cursor = len(s) - var39                                                       ##                         #
                    if a_3 == 7:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var40 = len(s) - s.cursor                                              ##                                      #
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
                                    s.cursor = len(s) - var40                                          ##                                      #
                    if a_3 == 8:                                                                                                               #
                        r = self.r_RV(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.starts_with(u'e')  # character check                                                                         #
                            if r:                                                                                                              #
                                r = s.set_range(self.left, self.right, u'ir')  # <-                                                            ##
        return r
    
    def r_verb_suffix(self, s):
        r = True
        var46 = len(s) - s.cursor                                                            ##
        var47 = s.limit                                                                      #
        r = s.to_mark(self.i_pV)  # tomark                                                   #
        if r:                                                                                #
            s.limit = s.cursor                                                               #
            s.cursor = len(s) - var46                                                        #
            self.left = s.cursor  ##                                                         #
            r = True              ## [                                                       #
            if r:                                                                            #
                a_7 = None                                          ##                       #
                r = False                                           #                        #
                var42 = s.cursor                                    #                        #
                for var41, var45, var44 in _a_7:                    #                        #
                    if s.starts_with(var41):                        #                        #
                        var43 = s.cursor                            #                        # setlimit
                        r = (not var45) or getattr(self, var45)(s)  # substring              #
                        if r:                                       #                        #
                          s.cursor = var43                          #                        #
                          a_7 = var44                               #                        #
                          break                                     #                        #
                    s.cursor = var42                                ##                       #
                if r:                                                                        #
                    self.right = s.cursor  ##                                                #
                    r = True               ## ]                                              #
                    if r:                                                                    #
                        if a_7 == 0:                                               ##        #
                            r = s.set_range(self.left, self.right, u'')  # delete  ## among  #
            s.limit = var47                                                                  ##
        return r
    
    def r_residual_suffix(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_8 = None                                          ##
            r = False                                           #
            var49 = s.cursor                                    #
            for var48, var52, var51 in _a_8:                    #
                if s.starts_with(var48):                        #
                    var50 = s.cursor                            #
                    r = (not var52) or getattr(self, var52)(s)  # substring
                    if r:                                       #
                      s.cursor = var50                          #
                      a_8 = var51                               #
                      break                                     #
                s.cursor = var49                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_8 == 0:                                                   ##
                        r = self.r_RV(s)  # routine call                           #
                        if r:                                                      # among
                            r = s.set_range(self.left, self.right, u'')  # delete  ##
        return r
    
    def r_residual_form(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_9 = None                                          ##
            r = False                                           #
            var54 = s.cursor                                    #
            for var53, var57, var56 in _a_9:                    #
                if s.starts_with(var53):                        #
                    var55 = s.cursor                            #
                    r = (not var57) or getattr(self, var57)(s)  # substring
                    if r:                                       #
                      s.cursor = var55                          #
                      a_9 = var56                               #
                      break                                     #
                s.cursor = var54                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_9 == 0:                                                                          ##
                        r = self.r_RV(s)  # routine call                                                  #
                        if r:                                                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete                         #
                            if r:                                                                         #
                                self.left = s.cursor  ##                                                  #
                                r = True              ## [                                                #
                                if r:                                                                     #
                                    var60 = len(s) - s.cursor                                       ##    #
                                    r = s.starts_with(u'u')  # character check                      #     #
                                    if r:                                                           #     #
                                        self.right = s.cursor  ##                                   #     #
                                        r = True               ## ]                                 #     #
                                        if r:                                                       #     #
                                            var58 = len(s) - s.cursor                   ##          #     #
                                            r = s.starts_with(u'g')  # character check  # test      #     #
                                            s.cursor = len(s) - var58                   ##          #     # among
                                    if not r:                                                       # or  #
                                        s.cursor = len(s) - var60                                   #     #
                                        r = s.starts_with(u'i')  # character check                  #     #
                                        if r:                                                       #     #
                                            self.right = s.cursor  ##                               #     #
                                            r = True               ## ]                             #     #
                                            if r:                                                   #     #
                                                var59 = len(s) - s.cursor                   ##      #     #
                                                r = s.starts_with(u'c')  # character check  # test  #     #
                                                s.cursor = len(s) - var59                   ##      ##    #
                                    if r:                                                                 #
                                        r = self.r_RV(s)  # routine call                                  #
                                        if r:                                                             #
                                            r = s.set_range(self.left, self.right, u'')  # delete         #
                    if a_9 == 1:                                                                          #
                        r = s.set_range(self.left, self.right, u'c')  # <-                                ##
        return r
    
    def r_stem(self, s):
        r = True
        var61 = s.cursor                       ##
        r = self.r_prelude(s)  # routine call  #
        s.cursor = var61                       # do
        r = True                               ##
        if r:
            var62 = s.cursor                            ##
            r = self.r_mark_regions(s)  # routine call  #
            s.cursor = var62                            # do
            r = True                                    ##
            if r:
                var70 = s.cursor                                                                                        ##
                var71 = len(s) - s.limit                                                                                #
                s.direction *= -1                                                                                       #
                s.cursor, s.limit = s.limit, s.cursor                                                                   #
                var68 = len(s) - s.cursor                                                                         ##    #
                var67 = len(s) - s.cursor                                                                   ##    #     #
                var66 = len(s) - s.cursor                                                            ##     #     #     #
                var63 = len(s) - s.cursor                      ##                                    #      #     #     #
                r = self.r_standard_suffix(s)  # routine call  #                                     #      #     #     #
                if not r:                                      # or                                  #      #     #     #
                    s.cursor = len(s) - var63                  #                                     #      #     #     #
                    r = self.r_verb_suffix(s)  # routine call  ##                                    #      #     #     #
                if r:                                                                                #      #     #     #
                    s.cursor = len(s) - var66                                                        #      #     #     #
                    var65 = len(s) - s.cursor                                                  ##    #      #     #     #
                    self.left = s.cursor  ##                                                   #     #      #     #     #
                    r = True              ## [                                                 #     #      #     #     #
                    if r:                                                                      #     #      #     #     #
                        r = s.starts_with(u'i')  # character check                             #     #      #     #     #
                        if r:                                                                  #     # and  #     #     #
                            self.right = s.cursor  ##                                          #     #      # or  # do  #
                            r = True               ## ]                                        #     #      #     #     #
                            if r:                                                              #     #      #     #     # backwards
                                var64 = len(s) - s.cursor                   ##                 # do  #      #     #     #
                                r = s.starts_with(u'c')  # character check  # test             #     #      #     #     #
                                s.cursor = len(s) - var64                   ##                 #     #      #     #     #
                                if r:                                                          #     #      #     #     #
                                    r = self.r_RV(s)  # routine call                           #     #      #     #     #
                                    if r:                                                      #     #      #     #     #
                                        r = s.set_range(self.left, self.right, u'')  # delete  #     #      #     #     #
                    s.cursor = len(s) - var65                                                  #     #      #     #     #
                    r = True                                                                   ##    ##     #     #     #
                if not r:                                                                                   #     #     #
                    s.cursor = len(s) - var67                                                               #     #     #
                    r = self.r_residual_suffix(s)  # routine call                                           ##    #     #
                s.cursor = len(s) - var68                                                                         #     #
                r = True                                                                                          ##    #
                if r:                                                                                                   #
                    var69 = len(s) - s.cursor                    ##                                                     #
                    r = self.r_residual_form(s)  # routine call  #                                                      #
                    s.cursor = len(s) - var69                    # do                                                   #
                    r = True                                     ##                                                     #
                s.direction *= -1                                                                                       #
                s.cursor = var70                                                                                        #
                s.limit = len(s) - var71                                                                                ##
                if r:
                    var72 = s.cursor                        ##
                    r = self.r_postlude(s)  # routine call  #
                    s.cursor = var72                        # do
                    r = True                                ##
        return r
