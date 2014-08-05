#!/usr/bin/env python
# vim:fileencoding=utf-8



# This file was auto-generated on 2014-08-05 20:04:17 using
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

_g_v = set(u'aeiou\xe2\xee\u0103')
_a_1 = ((u'I', '', 0), (u'U', '', 1), (u'', '', 2),)
_a_2 = ((u'iilor', '', 3), (u'ului', '', 0), (u'elor', '', 2), (u'iile', '', 3), (u'ilor', '', 3), (u'atei', '', 5), (u'a\u0163ie', '', 6), (u'a\u0163ia', '', 6), (u'aua', '', 1), (u'ele', '', 2), (u'iua', '', 3), (u'iei', '', 3), (u'ile', '', 4), (u'ul', '', 0), (u'ea', '', 2), (u'ii', '', 3),)
_a_3 = ((u'abilitate', '', 0), (u'abilitati', '', 0), (u'abilit\u0103\u0163i', '', 0), (u'ibilitate', '', 1), (u'abilit\u0103i', '', 0), (u'ivitate', '', 2), (u'ivitati', '', 2), (u'ivit\u0103\u0163i', '', 2), (u'icitate', '', 3), (u'icitati', '', 3), (u'icit\u0103\u0163i', '', 3), (u'icatori', '', 3), (u'ivit\u0103i', '', 2), (u'icit\u0103i', '', 3), (u'icator', '', 3), (u'a\u0163iune', '', 4), (u'atoare', '', 4), (u'\u0103toare', '', 4), (u'i\u0163iune', '', 5), (u'itoare', '', 5), (u'iciva', '', 3), (u'icive', '', 3), (u'icivi', '', 3), (u'iciv\u0103', '', 3), (u'icala', '', 3), (u'icale', '', 3), (u'icali', '', 3), (u'ical\u0103', '', 3), (u'ativa', '', 4), (u'ative', '', 4), (u'ativi', '', 4), (u'ativ\u0103', '', 4), (u'atori', '', 4), (u'\u0103tori', '', 4), (u'itiva', '', 5), (u'itive', '', 5), (u'itivi', '', 5), (u'itiv\u0103', '', 5), (u'itori', '', 5), (u'iciv', '', 3), (u'ical', '', 3), (u'ativ', '', 4), (u'ator', '', 4), (u'\u0103tor', '', 4), (u'itiv', '', 5), (u'itor', '', 5),)
_a_4 = ((u'abila', '', 0), (u'abile', '', 0), (u'abili', '', 0), (u'abil\u0103', '', 0), (u'ibila', '', 0), (u'ibile', '', 0), (u'ibili', '', 0), (u'ibil\u0103', '', 0), (u'atori', '', 0), (u'itate', '', 0), (u'itati', '', 0), (u'it\u0103\u0163i', '', 0), (u'abil', '', 0), (u'ibil', '', 0), (u'oasa', '', 0), (u'oas\u0103', '', 0), (u'oase', '', 0), (u'anta', '', 0), (u'ante', '', 0), (u'anti', '', 0), (u'ant\u0103', '', 0), (u'ator', '', 0), (u'it\u0103i', '', 0), (u'iune', '', 1), (u'iuni', '', 1), (u'isme', '', 2), (u'ista', '', 2), (u'iste', '', 2), (u'isti', '', 2), (u'ist\u0103', '', 2), (u'i\u015fti', '', 2), (u'ata', '', 0), (u'at\u0103', '', 0), (u'ati', '', 0), (u'ate', '', 0), (u'uta', '', 0), (u'ut\u0103', '', 0), (u'uti', '', 0), (u'ute', '', 0), (u'ita', '', 0), (u'it\u0103', '', 0), (u'iti', '', 0), (u'ite', '', 0), (u'ica', '', 0), (u'ice', '', 0), (u'ici', '', 0), (u'ic\u0103', '', 0), (u'osi', '', 0), (u'o\u015fi', '', 0), (u'ant', '', 0), (u'iva', '', 0), (u'ive', '', 0), (u'ivi', '', 0), (u'iv\u0103', '', 0), (u'ism', '', 2), (u'ist', '', 2), (u'at', '', 0), (u'ut', '', 0), (u'it', '', 0), (u'ic', '', 0), (u'os', '', 0), (u'iv', '', 0),)
_a_5 = ((u'seser\u0103\u0163i', '', 1), (u'aser\u0103\u0163i', '', 0), (u'iser\u0103\u0163i', '', 0), (u'\xe2ser\u0103\u0163i', '', 0), (u'user\u0103\u0163i', '', 0), (u'seser\u0103m', '', 1), (u'aser\u0103m', '', 0), (u'iser\u0103m', '', 0), (u'\xe2ser\u0103m', '', 0), (u'user\u0103m', '', 0), (u'ser\u0103\u0163i', '', 1), (u'sese\u015fi', '', 1), (u'seser\u0103', '', 1), (u'easc\u0103', '', 0), (u'ar\u0103\u0163i', '', 0), (u'ur\u0103\u0163i', '', 0), (u'ir\u0103\u0163i', '', 0), (u'\xe2r\u0103\u0163i', '', 0), (u'ase\u015fi', '', 0), (u'aser\u0103', '', 0), (u'ise\u015fi', '', 0), (u'iser\u0103', '', 0), (u'\xe2se\u015fi', '', 0), (u'\xe2ser\u0103', '', 0), (u'use\u015fi', '', 0), (u'user\u0103', '', 0), (u'ser\u0103m', '', 1), (u'sesem', '', 1), (u'indu', '', 0), (u'\xe2ndu', '', 0), (u'eaz\u0103', '', 0), (u'e\u015fti', '', 0), (u'e\u015fte', '', 0), (u'\u0103\u015fti', '', 0), (u'\u0103\u015fte', '', 0), (u'ea\u0163i', '', 0), (u'ia\u0163i', '', 0), (u'ar\u0103m', '', 0), (u'ur\u0103m', '', 0), (u'ir\u0103m', '', 0), (u'\xe2r\u0103m', '', 0), (u'asem', '', 0), (u'isem', '', 0), (u'\xe2sem', '', 0), (u'usem', '', 0), (u'se\u015fi', '', 1), (u'ser\u0103', '', 1), (u'sese', '', 1), (u'are', '', 0), (u'ere', '', 0), (u'ire', '', 0), (u'\xe2re', '', 0), (u'ind', '', 0), (u'\xe2nd', '', 0), (u'eze', '', 0), (u'ezi', '', 0), (u'esc', '', 0), (u'\u0103sc', '', 0), (u'eam', '', 0), (u'eai', '', 0), (u'eau', '', 0), (u'iam', '', 0), (u'iai', '', 0), (u'iau', '', 0), (u'a\u015fi', '', 0), (u'ar\u0103', '', 0), (u'u\u015fi', '', 0), (u'ur\u0103', '', 0), (u'i\u015fi', '', 0), (u'ir\u0103', '', 0), (u'\xe2\u015fi', '', 0), (u'\xe2r\u0103', '', 0), (u'ase', '', 0), (u'ise', '', 0), (u'\xe2se', '', 0), (u'use', '', 0), (u'a\u0163i', '', 1), (u'e\u0163i', '', 1), (u'i\u0163i', '', 1), (u'\xe2\u0163i', '', 1), (u'sei', '', 1), (u'ez', '', 0), (u'am', '', 0), (u'ai', '', 0), (u'au', '', 0), (u'ea', '', 0), (u'ia', '', 0), (u'ui', '', 0), (u'\xe2i', '', 0), (u'\u0103m', '', 1), (u'em', '', 1), (u'im', '', 1), (u'\xe2m', '', 1), (u'se', '', 1),)
_a_6 = ((u'ie', '', 0), (u'a', '', 0), (u'e', '', 0), (u'i', '', 0), (u'\u0103', '', 0),)

class _Program(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.i_pV = 0
        self.i_p1 = 0
        self.i_p2 = 0
        self.b_standard_suffix_removed = True

    def r_prelude(self, s):
        r = True
        while True:                                                                                       ##
            var2 = s.cursor                                                                               #
            while True:                                                                           ##      #
                var1 = s.cursor                                                                   #       #
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
                        var0 = s.cursor                                                     ##    #       #
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
                            s.cursor = var0                                                 #     #       #
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
                    s.cursor = var1                                                               #       #
                    break                                                                         #       #
                s.cursor = var1 + 1                                                               ##      #
            if not r:                                                                                     #
                s.cursor = var2                                                                           #
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
                    var6 = s.cursor                                                                                         ##
                    var5 = s.cursor                                                                                   ##    #
                    if s.cursor == s.limit:            ##                                                             #     #
                        r = False                      #                                                              #     #
                    else:                              #                                                              #     #
                        r = s.chars[s.cursor] in _g_v  # grouping check                                               #     #
                    if r:                              #                                                              #     #
                        s.cursor += 1                  ##                                                             #     #
                    if r:                                                                                             #     #
                        var3 = s.cursor                                                                         ##    #     #
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
                            s.cursor = var3                                                                     #     #     #
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
                        s.cursor = var5                                                                               #     #
                        if s.cursor == s.limit:                ##                                                     #     #
                            r = False                          #                                                      #     #
                        else:                                  #                                                      #     #
                            r = s.chars[s.cursor] not in _g_v  # negative grouping check                              #     #
                        if r:                                  #                                                      #     #
                            s.cursor += 1                      ##                                                     #     #
                        if r:                                                                                         #     #
                            var4 = s.cursor                                                        ##                 #     #
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
                                s.cursor = var4                                                    #                  #     #
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
                    s.cursor = var6                                                                                         #
                    r = True                                                                                                ##
                    if r:
                        var7 = s.cursor                                                                                 ##
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
                        s.cursor = var7                                                                                 #
                        r = True                                                                                        ##
        return r
    
    def r_postlude(self, s):
        r = True
        while True:                                                                      ##
            var13 = s.cursor                                                             #
            self.left = s.cursor  ##                                                     #
            r = True              ## [                                                   #
            if r:                                                                        #
                a_1 = None                                          ##                   #
                r = False                                           #                    #
                var9 = s.cursor                                     #                    #
                for var8, var12, var11 in _a_1:                     #                    #
                    if s.starts_with(var8):                         #                    #
                        var10 = s.cursor                            #                    #
                        r = (not var12) or getattr(self, var12)(s)  # substring          #
                        if r:                                       #                    #
                          s.cursor = var10                          #                    #
                          a_1 = var11                               #                    #
                          break                                     #                    # repeat
                    s.cursor = var9                                 ##                   #
                if r:                                                                    #
                    self.right = s.cursor  ##                                            #
                    r = True               ## ]                                          #
                    if r:                                                                #
                        if a_1 == 0:                                            ##       #
                            r = s.set_range(self.left, self.right, u'i')  # <-  #        #
                        if a_1 == 1:                                            #        #
                            r = s.set_range(self.left, self.right, u'u')  # <-  # among  #
                        if a_1 == 2:                                            #        #
                            r = s.hop(1)  # next                                ##       #
            if not r:                                                                    #
                s.cursor = var13                                                         #
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
    
    def r_step_0(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_2 = None                                          ##
            r = False                                           #
            var15 = s.cursor                                    #
            for var14, var18, var17 in _a_2:                    #
                if s.starts_with(var14):                        #
                    var16 = s.cursor                            #
                    r = (not var18) or getattr(self, var18)(s)  # substring
                    if r:                                       #
                      s.cursor = var16                          #
                      a_2 = var17                               #
                      break                                     #
                s.cursor = var15                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = self.r_R1(s)  # routine call
                    if r:
                        if a_2 == 0:                                                   ##
                            r = s.set_range(self.left, self.right, u'')  # delete      #
                        if a_2 == 1:                                                   #
                            r = s.set_range(self.left, self.right, u'a')  # <-         #
                        if a_2 == 2:                                                   #
                            r = s.set_range(self.left, self.right, u'e')  # <-         #
                        if a_2 == 3:                                                   #
                            r = s.set_range(self.left, self.right, u'i')  # <-         #
                        if a_2 == 4:                                                   #
                            var19 = len(s) - s.cursor                    ##            #
                            r = s.starts_with(u'ab')  # character check  #             # among
                            if not r:                                    # not         #
                                s.cursor = len(s) - var19                #             #
                            r = not r                                    ##            #
                            if r:                                                      #
                                r = s.set_range(self.left, self.right, u'i')  # <-     #
                        if a_2 == 5:                                                   #
                            r = s.set_range(self.left, self.right, u'at')  # <-        #
                        if a_2 == 6:                                                   #
                            r = s.set_range(self.left, self.right, u'a\u0163i')  # <-  ##
        return r
    
    def r_combo_suffix(self, s):
        r = True
        var25 = len(s) - s.cursor                                                           ##
        self.left = s.cursor  ##                                                            #
        r = True              ## [                                                          #
        if r:                                                                               #
            a_3 = None                                          ##                          #
            r = False                                           #                           #
            var21 = s.cursor                                    #                           #
            for var20, var24, var23 in _a_3:                    #                           #
                if s.starts_with(var20):                        #                           #
                    var22 = s.cursor                            #                           #
                    r = (not var24) or getattr(self, var24)(s)  # substring                 #
                    if r:                                       #                           #
                      s.cursor = var22                          #                           #
                      a_3 = var23                               #                           #
                      break                                     #                           #
                s.cursor = var21                                ##                          #
            if r:                                                                           #
                self.right = s.cursor  ##                                                   #
                r = True               ## ]                                                 #
                if r:                                                                       # test
                    r = self.r_R1(s)  # routine call                                        #
                    if r:                                                                   #
                        if a_3 == 0:                                               ##       #
                            r = s.set_range(self.left, self.right, u'abil')  # <-  #        #
                        if a_3 == 1:                                               #        #
                            r = s.set_range(self.left, self.right, u'ibil')  # <-  #        #
                        if a_3 == 2:                                               #        #
                            r = s.set_range(self.left, self.right, u'iv')  # <-    #        #
                        if a_3 == 3:                                               # among  #
                            r = s.set_range(self.left, self.right, u'ic')  # <-    #        #
                        if a_3 == 4:                                               #        #
                            r = s.set_range(self.left, self.right, u'at')  # <-    #        #
                        if a_3 == 5:                                               #        #
                            r = s.set_range(self.left, self.right, u'it')  # <-    ##       #
                        if r:                                                               #
                            self.b_standard_suffix_removed = True  ##                       #
                            r = True                               ## set                   #
        s.cursor = len(s) - var25                                                           ##
        return r
    
    def r_standard_suffix(self, s):
        r = True
        self.b_standard_suffix_removed = False  ##
        r = True                                ## unset
        if r:
            while True:                                     ##
                var26 = len(s) - s.cursor                   #
                r = self.r_combo_suffix(s)  # routine call  #
                if not r:                                   # repeat
                    s.cursor = len(s) - var26               #
                    break                                   #
            r = True                                        ##
            if r:
                self.left = s.cursor  ##
                r = True              ## [
                if r:
                    a_4 = None                                          ##
                    r = False                                           #
                    var28 = s.cursor                                    #
                    for var27, var31, var30 in _a_4:                    #
                        if s.starts_with(var27):                        #
                            var29 = s.cursor                            #
                            r = (not var31) or getattr(self, var31)(s)  # substring
                            if r:                                       #
                              s.cursor = var29                          #
                              a_4 = var30                               #
                              break                                     #
                        s.cursor = var28                                ##
                    if r:
                        self.right = s.cursor  ##
                        r = True               ## ]
                        if r:
                            r = self.r_R2(s)  # routine call
                            if r:
                                if a_4 == 0:                                                    ##
                                    r = s.set_range(self.left, self.right, u'')  # delete       #
                                if a_4 == 1:                                                    #
                                    r = s.starts_with(u'\u0163')  # character check             #
                                    if r:                                                       #
                                        self.right = s.cursor  ##                               # among
                                        r = True               ## ]                             #
                                        if r:                                                   #
                                            r = s.set_range(self.left, self.right, u't')  # <-  #
                                if a_4 == 2:                                                    #
                                    r = s.set_range(self.left, self.right, u'ist')  # <-        ##
                                if r:
                                    self.b_standard_suffix_removed = True  ##
                                    r = True                               ## set
        return r
    
    def r_verb_suffix(self, s):
        r = True
        var38 = len(s) - s.cursor                                                                                ##
        var39 = s.limit                                                                                          #
        r = s.to_mark(self.i_pV)  # tomark                                                                       #
        if r:                                                                                                    #
            s.limit = s.cursor                                                                                   #
            s.cursor = len(s) - var38                                                                            #
            self.left = s.cursor  ##                                                                             #
            r = True              ## [                                                                           #
            if r:                                                                                                #
                a_5 = None                                          ##                                           #
                r = False                                           #                                            #
                var33 = s.cursor                                    #                                            #
                for var32, var36, var35 in _a_5:                    #                                            #
                    if s.starts_with(var32):                        #                                            #
                        var34 = s.cursor                            #                                            #
                        r = (not var36) or getattr(self, var36)(s)  # substring                                  #
                        if r:                                       #                                            #
                          s.cursor = var34                          #                                            #
                          a_5 = var35                               #                                            #
                          break                                     #                                            #
                    s.cursor = var33                                ##                                           # setlimit
                if r:                                                                                            #
                    self.right = s.cursor  ##                                                                    #
                    r = True               ## ]                                                                  #
                    if r:                                                                                        #
                        if a_5 == 0:                                                                    ##       #
                            var37 = len(s) - s.cursor                                             ##    #        #
                            if s.cursor == s.limit:                    ##                         #     #        #
                                r = False                              #                          #     #        #
                            else:                                      #                          #     #        #
                                r = s.chars[s.cursor - 1] not in _g_v  # negative grouping check  #     #        #
                            if r:                                      #                          # or  #        #
                                s.cursor -= 1                          ##                         #     # among  #
                            if not r:                                                             #     #        #
                                s.cursor = len(s) - var37                                         #     #        #
                                r = s.starts_with(u'u')  # character check                        ##    #        #
                            if r:                                                                       #        #
                                r = s.set_range(self.left, self.right, u'')  # delete                   #        #
                        if a_5 == 1:                                                                    #        #
                            r = s.set_range(self.left, self.right, u'')  # delete                       ##       #
            s.limit = var39                                                                                      ##
        return r
    
    def r_vowel_suffix(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_6 = None                                          ##
            r = False                                           #
            var41 = s.cursor                                    #
            for var40, var44, var43 in _a_6:                    #
                if s.starts_with(var40):                        #
                    var42 = s.cursor                            #
                    r = (not var44) or getattr(self, var44)(s)  # substring
                    if r:                                       #
                      s.cursor = var42                          #
                      a_6 = var43                               #
                      break                                     #
                s.cursor = var41                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = self.r_RV(s)  # routine call
                    if r:
                        if a_6 == 0:                                               ##
                            r = s.set_range(self.left, self.right, u'')  # delete  ## among
        return r
    
    def r_stem(self, s):
        r = True
        var45 = s.cursor                       ##
        r = self.r_prelude(s)  # routine call  #
        s.cursor = var45                       # do
        r = True                               ##
        if r:
            var46 = s.cursor                            ##
            r = self.r_mark_regions(s)  # routine call  #
            s.cursor = var46                            # do
            r = True                                    ##
            if r:
                var52 = s.cursor                                                                  ##
                var53 = len(s) - s.limit                                                          #
                s.direction *= -1                                                                 #
                s.cursor, s.limit = s.limit, s.cursor                                             #
                var47 = len(s) - s.cursor             ##                                          #
                r = self.r_step_0(s)  # routine call  #                                           #
                s.cursor = len(s) - var47             # do                                        #
                r = True                              ##                                          #
                if r:                                                                             #
                    var48 = len(s) - s.cursor                      ##                             #
                    r = self.r_standard_suffix(s)  # routine call  #                              #
                    s.cursor = len(s) - var48                      # do                           #
                    r = True                                       ##                             #
                    if r:                                                                         #
                        var50 = len(s) - s.cursor                                           ##    #
                        var49 = len(s) - s.cursor                                     ##    #     # backwards
                        r = self.b_standard_suffix_removed  # boolean variable check  #     #     #
                        if not r:                                                     # or  #     #
                            s.cursor = len(s) - var49                                 #     # do  #
                            r = self.r_verb_suffix(s)  # routine call                 ##    #     #
                        s.cursor = len(s) - var50                                           #     #
                        r = True                                                            ##    #
                        if r:                                                                     #
                            var51 = len(s) - s.cursor                   ##                        #
                            r = self.r_vowel_suffix(s)  # routine call  #                         #
                            s.cursor = len(s) - var51                   # do                      #
                            r = True                                    ##                        #
                s.direction *= -1                                                                 #
                s.cursor = var52                                                                  #
                s.limit = len(s) - var53                                                          ##
                if r:
                    var54 = s.cursor                        ##
                    r = self.r_postlude(s)  # routine call  #
                    s.cursor = var54                        # do
                    r = True                                ##
        return r
