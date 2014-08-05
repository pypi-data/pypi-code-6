#!/usr/bin/env python
# vim:fileencoding=utf-8



# This file was auto-generated on 2014-08-05 20:04:07 using
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

_g_v = set(u'aeiouy\xe2\xe0\xeb\xe9\xea\xe8\xef\xee\xf4\xfb\xf9')
_a_1 = ((u'par', '', 0), (u'col', '', 0), (u'tap', '', 0),)
_a_2 = ((u'I', '', 0), (u'U', '', 1), (u'Y', '', 2), (u'', '', 3),)
_a_3 = ((u'issements', '', 11), (u'issement', '', 11), (u'atrices', '', 1), (u'atrice', '', 1), (u'ateurs', '', 1), (u'ations', '', 1), (u'logies', '', 2), (u'usions', '', 3), (u'utions', '', 3), (u'ements', '', 5), (u'amment', '', 12), (u'emment', '', 13), (u'ances', '', 0), (u'iqUes', '', 0), (u'ismes', '', 0), (u'ables', '', 0), (u'istes', '', 0), (u'ateur', '', 1), (u'ation', '', 1), (u'logie', '', 2), (u'usion', '', 3), (u'ution', '', 3), (u'ences', '', 4), (u'ement', '', 5), (u'euses', '', 10), (u'ments', '', 14), (u'ance', '', 0), (u'iqUe', '', 0), (u'isme', '', 0), (u'able', '', 0), (u'iste', '', 0), (u'ence', '', 4), (u'it\xe9s', '', 6), (u'ives', '', 7), (u'eaux', '', 8), (u'euse', '', 10), (u'ment', '', 14), (u'eux', '', 0), (u'it\xe9', '', 6), (u'ive', '', 7), (u'ifs', '', 7), (u'aux', '', 9), (u'if', '', 7),)
_a_4 = ((u'eus', '', 1), (u'abl', '', 2), (u'iqU', '', 2), (u'i\xe8r', '', 3), (u'I\xe8r', '', 3), (u'iv', '', 0),)
_a_5 = ((u'abil', '', 0), (u'ic', '', 1), (u'iv', '', 2),)
_a_6 = ((u'issaIent', '', 0), (u'issantes', '', 0), (u'iraIent', '', 0), (u'issante', '', 0), (u'issants', '', 0), (u'issions', '', 0), (u'irions', '', 0), (u'issais', '', 0), (u'issait', '', 0), (u'issant', '', 0), (u'issent', '', 0), (u'issiez', '', 0), (u'issons', '', 0), (u'irais', '', 0), (u'irait', '', 0), (u'irent', '', 0), (u'iriez', '', 0), (u'irons', '', 0), (u'iront', '', 0), (u'isses', '', 0), (u'issez', '', 0), (u'\xeemes', '', 0), (u'\xeetes', '', 0), (u'irai', '', 0), (u'iras', '', 0), (u'irez', '', 0), (u'isse', '', 0), (u'ies', '', 0), (u'ira', '', 0), (u'\xeet', '', 0), (u'ie', '', 0), (u'ir', '', 0), (u'is', '', 0), (u'it', '', 0), (u'i', '', 0),)
_a_7 = ((u'eraIent', '', 1), (u'assions', '', 2), (u'erions', '', 1), (u'assent', '', 2), (u'assiez', '', 2), (u'\xe8rent', '', 1), (u'erais', '', 1), (u'erait', '', 1), (u'eriez', '', 1), (u'erons', '', 1), (u'eront', '', 1), (u'aIent', '', 2), (u'antes', '', 2), (u'asses', '', 2), (u'ions', '', 0), (u'erai', '', 1), (u'eras', '', 1), (u'erez', '', 1), (u'\xe2mes', '', 2), (u'\xe2tes', '', 2), (u'ante', '', 2), (u'ants', '', 2), (u'asse', '', 2), (u'\xe9es', '', 1), (u'era', '', 1), (u'iez', '', 1), (u'ais', '', 2), (u'ait', '', 2), (u'ant', '', 2), (u'\xe9e', '', 1), (u'\xe9s', '', 1), (u'er', '', 1), (u'ez', '', 1), (u'\xe2t', '', 2), (u'ai', '', 2), (u'as', '', 2), (u'\xe9', '', 1), (u'a', '', 2),)
_g_keep_with_s = set(u'aiou\xe8s')
_a_8 = ((u'i\xe8re', '', 1), (u'I\xe8re', '', 1), (u'ion', '', 0), (u'ier', '', 1), (u'Ier', '', 1), (u'e', '', 2), (u'\xeb', '', 3),)
_a_9 = ((u'eill', '', 0), (u'enn', '', 0), (u'onn', '', 0), (u'ett', '', 0), (u'ell', '', 0),)

class _Program(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.i_pV = 0
        self.i_p1 = 0
        self.i_p2 = 0

    def r_prelude(self, s):
        r = True
        while True:                                                                                                         ##
            var5 = s.cursor                                                                                                 #
            while True:                                                                                             ##      #
                var4 = s.cursor                                                                                     #       #
                var3 = s.cursor                                                                               ##    #       #
                var2 = s.cursor                                                                         ##    #     #       #
                if s.cursor == s.limit:            ##                                                   #     #     #       #
                    r = False                      #                                                    #     #     #       #
                else:                              #                                                    #     #     #       #
                    r = s.chars[s.cursor] in _g_v  # grouping check                                     #     #     #       #
                if r:                              #                                                    #     #     #       #
                    s.cursor += 1                  ##                                                   #     #     #       #
                if r:                                                                                   #     #     #       #
                    self.left = s.cursor  ##                                                            #     #     #       #
                    r = True              ## [                                                          #     #     #       #
                    if r:                                                                               #     #     #       #
                        var1 = s.cursor                                                           ##    #     #     #       #
                        var0 = s.cursor                                                     ##    #     #     #     #       #
                        r = s.starts_with(u'u')  # character check                          #     #     #     #     #       #
                        if r:                                                               #     #     #     #     #       #
                            self.right = s.cursor  ##                                       #     #     #     #     #       #
                            r = True               ## ]                                     #     #     #     #     #       #
                            if r:                                                           #     #     #     #     #       #
                                if s.cursor == s.limit:            ##                       #     #     #     #     #       #
                                    r = False                      #                        #     #     #     #     #       #
                                else:                              #                        #     #     #     #     #       #
                                    r = s.chars[s.cursor] in _g_v  # grouping check         #     #     #     #     #       #
                                if r:                              #                        #     #     #     #     #       #
                                    s.cursor += 1                  ##                       #     #     #     #     #       #
                                if r:                                                       #     #     #     #     #       #
                                    r = s.set_range(self.left, self.right, u'U')  # <-      #     #     #     #     #       #
                        if not r:                                                           # or  #     #     #     #       #
                            s.cursor = var0                                                 #     #     #     #     #       #
                            r = s.starts_with(u'i')  # character check                      #     #     #     #     #       #
                            if r:                                                           #     #     #     #     #       #
                                self.right = s.cursor  ##                                   #     # or  #     #     #       #
                                r = True               ## ]                                 #     #     #     #     #       #
                                if r:                                                       #     #     #     #     #       #
                                    if s.cursor == s.limit:            ##                   #     #     # or  #     #       #
                                        r = False                      #                    #     #     #     #     #       #
                                    else:                              #                    #     #     #     #     #       #
                                        r = s.chars[s.cursor] in _g_v  # grouping check     #     #     #     #     #       #
                                    if r:                              #                    #     #     #     #     #       #
                                        s.cursor += 1                  ##                   #     #     #     #     #       #
                                    if r:                                                   #     #     #     # or  #       #
                                        r = s.set_range(self.left, self.right, u'I')  # <-  ##    #     #     #     # goto  #
                        if not r:                                                                 #     #     #     #       # repeat
                            s.cursor = var1                                                       #     #     #     #       #
                            r = s.starts_with(u'y')  # character check                            #     #     #     #       #
                            if r:                                                                 #     #     #     #       #
                                self.right = s.cursor  ##                                         #     #     #     #       #
                                r = True               ## ]                                       #     #     #     #       #
                                if r:                                                             #     #     #     #       #
                                    r = s.set_range(self.left, self.right, u'Y')  # <-            ##    #     #     #       #
                if not r:                                                                               #     #     #       #
                    s.cursor = var2                                                                     #     #     #       #
                    self.left = s.cursor  ##                                                            #     #     #       #
                    r = True              ## [                                                          #     #     #       #
                    if r:                                                                               #     #     #       #
                        r = s.starts_with(u'y')  # character check                                      #     #     #       #
                        if r:                                                                           #     #     #       #
                            self.right = s.cursor  ##                                                   #     #     #       #
                            r = True               ## ]                                                 #     #     #       #
                            if r:                                                                       #     #     #       #
                                if s.cursor == s.limit:            ##                                   #     #     #       #
                                    r = False                      #                                    #     #     #       #
                                else:                              #                                    #     #     #       #
                                    r = s.chars[s.cursor] in _g_v  # grouping check                     #     #     #       #
                                if r:                              #                                    #     #     #       #
                                    s.cursor += 1                  ##                                   #     #     #       #
                                if r:                                                                   #     #     #       #
                                    r = s.set_range(self.left, self.right, u'Y')  # <-                  ##    #     #       #
                if not r:                                                                                     #     #       #
                    s.cursor = var3                                                                           #     #       #
                    r = s.starts_with(u'q')  # character check                                                #     #       #
                    if r:                                                                                     #     #       #
                        self.left = s.cursor  ##                                                              #     #       #
                        r = True              ## [                                                            #     #       #
                        if r:                                                                                 #     #       #
                            r = s.starts_with(u'u')  # character check                                        #     #       #
                            if r:                                                                             #     #       #
                                self.right = s.cursor  ##                                                     #     #       #
                                r = True               ## ]                                                   #     #       #
                                if r:                                                                         #     #       #
                                    r = s.set_range(self.left, self.right, u'U')  # <-                        ##    #       #
                if r or s.cursor == s.limit:                                                                        #       #
                    s.cursor = var4                                                                                 #       #
                    break                                                                                           #       #
                s.cursor = var4 + 1                                                                                 ##      #
            if not r:                                                                                                       #
                s.cursor = var5                                                                                             #
                break                                                                                                       #
        r = True                                                                                                            ##
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
                    var13 = s.cursor                                                                 ##
                    var12 = s.cursor                                                           ##    #
                    var11 = s.cursor                                                 ##        #     #
                    if s.cursor == s.limit:            ##                            #         #     #
                        r = False                      #                             #         #     #
                    else:                              #                             #         #     #
                        r = s.chars[s.cursor] in _g_v  # grouping check              #         #     #
                    if r:                              #                             #         #     #
                        s.cursor += 1                  ##                            #         #     #
                    if r:                                                            #         #     #
                        if s.cursor == s.limit:            ##                        #         #     #
                            r = False                      #                         #         #     #
                        else:                              #                         #         #     #
                            r = s.chars[s.cursor] in _g_v  # grouping check          #         #     #
                        if r:                              #                         #         #     #
                            s.cursor += 1                  ##                        #         #     #
                        if r:                                                        #         #     #
                            r = s.hop(1)  # next                                     #         #     #
                    if not r:                                                        # or      #     #
                        s.cursor = var11                                             #         #     #
                        a_1 = None                                          ##       #         #     #
                        r = False                                           #        #         #     #
                        var7 = s.cursor                                     #        #         #     #
                        for var6, var10, var9 in _a_1:                      #        #         #     #
                            if s.starts_with(var6):                         #        #         #     #
                                var8 = s.cursor                             #        #         # or  #
                                r = (not var10) or getattr(self, var10)(s)  #        #         #     #
                                if r:                                       # among  #         #     # do
                                  s.cursor = var8                           #        #         #     #
                                  a_1 = var9                                #        #         #     #
                                  break                                     #        #         #     #
                            s.cursor = var7                                 #        #         #     #
                        if r:                                               #        #         #     #
                            if a_1 == 0:                                    #        #         #     #
                                r = True                                    ##       ##        #     #
                    if not r:                                                                  #     #
                        s.cursor = var12                                                       #     #
                        r = s.hop(1)  # next                                                   #     #
                        if r:                                                                  #     #
                            while True:                                              ##        #     #
                                if s.cursor == s.limit:            ##                #         #     #
                                    r = False                      #                 #         #     #
                                else:                              #                 #         #     #
                                    r = s.chars[s.cursor] in _g_v  # grouping check  #         #     #
                                if r:                              #                 # gopast  #     #
                                    s.cursor += 1                  ##                #         #     #
                                if r or s.cursor == s.limit:                         #         #     #
                                    break                                            #         #     #
                                s.cursor += 1                                        ##        ##    #
                    if r:                                                                            #
                        self.i_pV = s.cursor  ##                                                     #
                        r = True              ## setmark                                             #
                    s.cursor = var13                                                                 #
                    r = True                                                                         ##
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
                          break                                     #                    #
                    s.cursor = var16                                ##                   # repeat
                if r:                                                                    #
                    self.right = s.cursor  ##                                            #
                    r = True               ## ]                                          #
                    if r:                                                                #
                        if a_2 == 0:                                            ##       #
                            r = s.set_range(self.left, self.right, u'i')  # <-  #        #
                        if a_2 == 1:                                            #        #
                            r = s.set_range(self.left, self.right, u'u')  # <-  #        #
                        if a_2 == 2:                                            # among  #
                            r = s.set_range(self.left, self.right, u'y')  # <-  #        #
                        if a_2 == 3:                                            #        #
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
    
    def r_standard_suffix(self, s):
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
                    if a_3 == 0:                                                                                                               ##
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                    if a_3 == 1:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var27 = len(s) - s.cursor                                                    ##                                #
                                self.left = s.cursor  ##                                                     #                                 #
                                r = True              ## [                                                   #                                 #
                                if r:                                                                        #                                 #
                                    r = s.starts_with(u'ic')  # character check                              #                                 #
                                    if r:                                                                    #                                 #
                                        self.right = s.cursor  ##                                            #                                 #
                                        r = True               ## ]                                          #                                 #
                                        if r:                                                                #                                 #
                                            var26 = len(s) - s.cursor                                  ##    # try                             #
                                            r = self.r_R2(s)  # routine call                           #     #                                 #
                                            if r:                                                      #     #                                 #
                                                r = s.set_range(self.left, self.right, u'')  # delete  # or  #                                 #
                                            if not r:                                                  #     #                                 #
                                                s.cursor = len(s) - var26                              #     #                                 #
                                                r = s.set_range(self.left, self.right, u'iqU')  # <-   ##    #                                 #
                                if not r:                                                                    #                                 #
                                    r = True                                                                 #                                 #
                                    s.cursor = len(s) - var27                                                ##                                #
                    if a_3 == 2:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'log')  # <-                                                               #
                    if a_3 == 3:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'u')  # <-                                                                 #
                    if a_3 == 4:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'ent')  # <-                                                               #
                    if a_3 == 5:                                                                                                               #
                        r = self.r_RV(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var34 = len(s) - s.cursor                                                                               ##     #
                                self.left = s.cursor  ##                                                                                #      #
                                r = True              ## [                                                                              #      #
                                if r:                                                                                                   #      #
                                    a_4 = None                                          ##                                              #      #
                                    r = False                                           #                                               #      #
                                    var29 = s.cursor                                    #                                               #      #
                                    for var28, var32, var31 in _a_4:                    #                                               #      #
                                        if s.starts_with(var28):                        #                                               #      #
                                            var30 = s.cursor                            #                                               #      #
                                            r = (not var32) or getattr(self, var32)(s)  # substring                                     #      #
                                            if r:                                       #                                               #      #
                                              s.cursor = var30                          #                                               #      #
                                              a_4 = var31                               #                                               #      #
                                              break                                     #                                               #      #
                                        s.cursor = var29                                ##                                              #      #
                                    if r:                                                                                               #      #
                                        self.right = s.cursor  ##                                                                       #      #
                                        r = True               ## ]                                                                     #      #
                                        if r:                                                                                           #      #
                                            if a_4 == 0:                                                                       ##       #      #
                                                r = self.r_R2(s)  # routine call                                               #        #      #
                                                if r:                                                                          #        #      #
                                                    r = s.set_range(self.left, self.right, u'')  # delete                      #        #      #
                                                    if r:                                                                      #        #      #
                                                        self.left = s.cursor  ##                                               #        #      #
                                                        r = True              ## [                                             #        #      #
                                                        if r:                                                                  #        #      #
                                                            r = s.starts_with(u'at')  # character check                        #        # try  #
                                                            if r:                                                              #        #      #
                                                                self.right = s.cursor  ##                                      #        #      #
                                                                r = True               ## ]                                    #        #      #
                                                                if r:                                                          #        #      #
                                                                    r = self.r_R2(s)  # routine call                           #        #      #
                                                                    if r:                                                      #        #      #
                                                                        r = s.set_range(self.left, self.right, u'')  # delete  #        #      #
                                            if a_4 == 1:                                                                       #        #      #
                                                var33 = len(s) - s.cursor                                     ##               # among  #      #
                                                r = self.r_R2(s)  # routine call                              #                #        #      #
                                                if r:                                                         #                #        #      #
                                                    r = s.set_range(self.left, self.right, u'')  # delete     #                #        #      #
                                                if not r:                                                     # or             #        #      #
                                                    s.cursor = len(s) - var33                                 #                #        #      #
                                                    r = self.r_R1(s)  # routine call                          #                #        #      #
                                                    if r:                                                     #                #        #      #
                                                        r = s.set_range(self.left, self.right, u'eux')  # <-  ##               #        #      #
                                            if a_4 == 2:                                                                       #        #      #
                                                r = self.r_R2(s)  # routine call                                               #        #      #
                                                if r:                                                                          #        #      #
                                                    r = s.set_range(self.left, self.right, u'')  # delete                      #        #      #
                                            if a_4 == 3:                                                                       #        #      #
                                                r = self.r_RV(s)  # routine call                                               #        #      #
                                                if r:                                                                          #        #      #
                                                    r = s.set_range(self.left, self.right, u'i')  # <-                         ##       #      #
                                if not r:                                                                                               #      #
                                    r = True                                                                                            #      #
                                    s.cursor = len(s) - var34                                                                           ##     #
                    if a_3 == 6:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var42 = len(s) - s.cursor                                                                 ##                   #
                                self.left = s.cursor  ##                                                                  #                    #
                                r = True              ## [                                                                #                    #
                                if r:                                                                                     #                    #
                                    a_5 = None                                          ##                                #                    #
                                    r = False                                           #                                 #                    #
                                    var36 = s.cursor                                    #                                 #                    #
                                    for var35, var39, var38 in _a_5:                    #                                 #                    #
                                        if s.starts_with(var35):                        #                                 #                    #
                                            var37 = s.cursor                            #                                 #                    #
                                            r = (not var39) or getattr(self, var39)(s)  # substring                       #                    #
                                            if r:                                       #                                 #                    # among
                                              s.cursor = var37                          #                                 #                    #
                                              a_5 = var38                               #                                 #                    #
                                              break                                     #                                 #                    #
                                        s.cursor = var36                                ##                                #                    #
                                    if r:                                                                                 #                    #
                                        self.right = s.cursor  ##                                                         #                    #
                                        r = True               ## ]                                                       #                    #
                                        if r:                                                                             #                    #
                                            if a_5 == 0:                                                         ##       #                    #
                                                var40 = len(s) - s.cursor                                  ##    #        # try                #
                                                r = self.r_R2(s)  # routine call                           #     #        #                    #
                                                if r:                                                      #     #        #                    #
                                                    r = s.set_range(self.left, self.right, u'')  # delete  # or  #        #                    #
                                                if not r:                                                  #     #        #                    #
                                                    s.cursor = len(s) - var40                              #     #        #                    #
                                                    r = s.set_range(self.left, self.right, u'abl')  # <-   ##    #        #                    #
                                            if a_5 == 1:                                                         #        #                    #
                                                var41 = len(s) - s.cursor                                  ##    #        #                    #
                                                r = self.r_R2(s)  # routine call                           #     # among  #                    #
                                                if r:                                                      #     #        #                    #
                                                    r = s.set_range(self.left, self.right, u'')  # delete  # or  #        #                    #
                                                if not r:                                                  #     #        #                    #
                                                    s.cursor = len(s) - var41                              #     #        #                    #
                                                    r = s.set_range(self.left, self.right, u'iqU')  # <-   ##    #        #                    #
                                            if a_5 == 2:                                                         #        #                    #
                                                r = self.r_R2(s)  # routine call                                 #        #                    #
                                                if r:                                                            #        #                    #
                                                    r = s.set_range(self.left, self.right, u'')  # delete        ##       #                    #
                                if not r:                                                                                 #                    #
                                    r = True                                                                              #                    #
                                    s.cursor = len(s) - var42                                                             ##                   #
                    if a_3 == 7:                                                                                                               #
                        r = self.r_R2(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete                                                              #
                            if r:                                                                                                              #
                                var44 = len(s) - s.cursor                                                                        ##            #
                                self.left = s.cursor  ##                                                                         #             #
                                r = True              ## [                                                                       #             #
                                if r:                                                                                            #             #
                                    r = s.starts_with(u'at')  # character check                                                  #             #
                                    if r:                                                                                        #             #
                                        self.right = s.cursor  ##                                                                #             #
                                        r = True               ## ]                                                              #             #
                                        if r:                                                                                    #             #
                                            r = self.r_R2(s)  # routine call                                                     #             #
                                            if r:                                                                                #             #
                                                r = s.set_range(self.left, self.right, u'')  # delete                            #             #
                                                if r:                                                                            #             #
                                                    self.left = s.cursor  ##                                                     #             #
                                                    r = True              ## [                                                   #             #
                                                    if r:                                                                        # try         #
                                                        r = s.starts_with(u'ic')  # character check                              #             #
                                                        if r:                                                                    #             #
                                                            self.right = s.cursor  ##                                            #             #
                                                            r = True               ## ]                                          #             #
                                                            if r:                                                                #             #
                                                                var43 = len(s) - s.cursor                                  ##    #             #
                                                                r = self.r_R2(s)  # routine call                           #     #             #
                                                                if r:                                                      #     #             #
                                                                    r = s.set_range(self.left, self.right, u'')  # delete  # or  #             #
                                                                if not r:                                                  #     #             #
                                                                    s.cursor = len(s) - var43                              #     #             #
                                                                    r = s.set_range(self.left, self.right, u'iqU')  # <-   ##    #             #
                                if not r:                                                                                        #             #
                                    r = True                                                                                     #             #
                                    s.cursor = len(s) - var44                                                                    ##            #
                    if a_3 == 8:                                                                                                               #
                        r = s.set_range(self.left, self.right, u'eau')  # <-                                                                   #
                    if a_3 == 9:                                                                                                               #
                        r = self.r_R1(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'al')  # <-                                                                #
                    if a_3 == 10:                                                                                                              #
                        var45 = len(s) - s.cursor                                     ##                                                       #
                        r = self.r_R2(s)  # routine call                              #                                                        #
                        if r:                                                         #                                                        #
                            r = s.set_range(self.left, self.right, u'')  # delete     #                                                        #
                        if not r:                                                     # or                                                     #
                            s.cursor = len(s) - var45                                 #                                                        #
                            r = self.r_R1(s)  # routine call                          #                                                        #
                            if r:                                                     #                                                        #
                                r = s.set_range(self.left, self.right, u'eux')  # <-  ##                                                       #
                    if a_3 == 11:                                                                                                              #
                        r = self.r_R1(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            if s.cursor == s.limit:                    ##                                                                      #
                                r = False                              #                                                                       #
                            else:                                      #                                                                       #
                                r = s.chars[s.cursor - 1] not in _g_v  # negative grouping check                                               #
                            if r:                                      #                                                                       #
                                s.cursor -= 1                          ##                                                                      #
                            if r:                                                                                                              #
                                r = s.set_range(self.left, self.right, u'')  # delete                                                          #
                    if a_3 == 12:                                                                                                              #
                        r = self.r_RV(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'ant')  # <-  ##                                                           #
                            r = False                                             ## fail                                                      #
                    if a_3 == 13:                                                                                                              #
                        r = self.r_RV(s)  # routine call                                                                                       #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'ent')  # <-  ##                                                           #
                            r = False                                             ## fail                                                      #
                    if a_3 == 14:                                                                                                              #
                        var46 = len(s) - s.cursor                                ##                                                            #
                        if s.cursor == s.limit:                ##                #                                                             #
                            r = False                          #                 #                                                             #
                        else:                                  #                 #                                                             #
                            r = s.chars[s.cursor - 1] in _g_v  # grouping check  #                                                             #
                        if r:                                  #                 # test                                                        #
                            s.cursor -= 1                      ##                #                                                             #
                        if r:                                                    #                                                             #
                            r = self.r_RV(s)  # routine call                     #                                                             #
                        s.cursor = len(s) - var46                                ##                                                            #
                        if r:                                                                                                                  #
                            r = s.set_range(self.left, self.right, u'')  # delete  ##                                                          #
                            r = False                                              ## fail                                                     ##
        return r
    
    def r_i_verb_suffix(self, s):
        r = True
        var52 = len(s) - s.cursor                                                                          ##
        var53 = s.limit                                                                                    #
        r = s.to_mark(self.i_pV)  # tomark                                                                 #
        if r:                                                                                              #
            s.limit = s.cursor                                                                             #
            s.cursor = len(s) - var52                                                                      #
            self.left = s.cursor  ##                                                                       #
            r = True              ## [                                                                     #
            if r:                                                                                          #
                a_6 = None                                          ##                                     #
                r = False                                           #                                      #
                var48 = s.cursor                                    #                                      #
                for var47, var51, var50 in _a_6:                    #                                      #
                    if s.starts_with(var47):                        #                                      #
                        var49 = s.cursor                            #                                      #
                        r = (not var51) or getattr(self, var51)(s)  # substring                            #
                        if r:                                       #                                      #
                          s.cursor = var49                          #                                      # setlimit
                          a_6 = var50                               #                                      #
                          break                                     #                                      #
                    s.cursor = var48                                ##                                     #
                if r:                                                                                      #
                    self.right = s.cursor  ##                                                              #
                    r = True               ## ]                                                            #
                    if r:                                                                                  #
                        if a_6 == 0:                                                              ##       #
                            if s.cursor == s.limit:                    ##                         #        #
                                r = False                              #                          #        #
                            else:                                      #                          #        #
                                r = s.chars[s.cursor - 1] not in _g_v  # negative grouping check  # among  #
                            if r:                                      #                          #        #
                                s.cursor -= 1                          ##                         #        #
                            if r:                                                                 #        #
                                r = s.set_range(self.left, self.right, u'')  # delete             ##       #
            s.limit = var53                                                                                ##
        return r
    
    def r_verb_suffix(self, s):
        r = True
        var60 = len(s) - s.cursor                                                                                  ##
        var61 = s.limit                                                                                            #
        r = s.to_mark(self.i_pV)  # tomark                                                                         #
        if r:                                                                                                      #
            s.limit = s.cursor                                                                                     #
            s.cursor = len(s) - var60                                                                              #
            self.left = s.cursor  ##                                                                               #
            r = True              ## [                                                                             #
            if r:                                                                                                  #
                a_7 = None                                          ##                                             #
                r = False                                           #                                              #
                var55 = s.cursor                                    #                                              #
                for var54, var58, var57 in _a_7:                    #                                              #
                    if s.starts_with(var54):                        #                                              #
                        var56 = s.cursor                            #                                              #
                        r = (not var58) or getattr(self, var58)(s)  # substring                                    #
                        if r:                                       #                                              #
                          s.cursor = var56                          #                                              #
                          a_7 = var57                               #                                              #
                          break                                     #                                              #
                    s.cursor = var55                                ##                                             #
                if r:                                                                                              #
                    self.right = s.cursor  ##                                                                      #
                    r = True               ## ]                                                                    #
                    if r:                                                                                          # setlimit
                        if a_7 == 0:                                                                      ##       #
                            r = self.r_R2(s)  # routine call                                              #        #
                            if r:                                                                         #        #
                                r = s.set_range(self.left, self.right, u'')  # delete                     #        #
                        if a_7 == 1:                                                                      #        #
                            r = s.set_range(self.left, self.right, u'')  # delete                         #        #
                        if a_7 == 2:                                                                      #        #
                            r = s.set_range(self.left, self.right, u'')  # delete                         #        #
                            if r:                                                                         #        #
                                var59 = len(s) - s.cursor                                          ##     #        #
                                self.left = s.cursor  ##                                           #      #        #
                                r = True              ## [                                         #      # among  #
                                if r:                                                              #      #        #
                                    r = s.starts_with(u'e')  # character check                     #      #        #
                                    if r:                                                          #      #        #
                                        self.right = s.cursor  ##                                  # try  #        #
                                        r = True               ## ]                                #      #        #
                                        if r:                                                      #      #        #
                                            r = s.set_range(self.left, self.right, u'')  # delete  #      #        #
                                if not r:                                                          #      #        #
                                    r = True                                                       #      #        #
                                    s.cursor = len(s) - var59                                      ##     ##       #
            s.limit = var61                                                                                        ##
        return r
    
    def r_residual_suffix(self, s):
        r = True
        var63 = len(s) - s.cursor                                                                           ##
        self.left = s.cursor  ##                                                                            #
        r = True              ## [                                                                          #
        if r:                                                                                               #
            r = s.starts_with(u's')  # character check                                                      #
            if r:                                                                                           #
                self.right = s.cursor  ##                                                                   #
                r = True               ## ]                                                                 #
                if r:                                                                                       #
                    var62 = len(s) - s.cursor                                                       ##      #
                    if s.cursor == s.limit:                              ##                         #       #
                        r = False                                        #                          #       # try
                    else:                                                #                          #       #
                        r = s.chars[s.cursor - 1] not in _g_keep_with_s  # negative grouping check  # test  #
                    if r:                                                #                          #       #
                        s.cursor -= 1                                    ##                         #       #
                    s.cursor = len(s) - var62                                                       ##      #
                    if r:                                                                                   #
                        r = s.set_range(self.left, self.right, u'')  # delete                               #
        if not r:                                                                                           #
            r = True                                                                                        #
            s.cursor = len(s) - var63                                                                       ##
        if r:
            var70 = len(s) - s.cursor                                                                   ##
            var71 = s.limit                                                                             #
            r = s.to_mark(self.i_pV)  # tomark                                                          #
            if r:                                                                                       #
                s.limit = s.cursor                                                                      #
                s.cursor = len(s) - var70                                                               #
                self.left = s.cursor  ##                                                                #
                r = True              ## [                                                              #
                if r:                                                                                   #
                    a_8 = None                                          ##                              #
                    r = False                                           #                               #
                    var65 = s.cursor                                    #                               #
                    for var64, var68, var67 in _a_8:                    #                               #
                        if s.starts_with(var64):                        #                               #
                            var66 = s.cursor                            #                               #
                            r = (not var68) or getattr(self, var68)(s)  # substring                     #
                            if r:                                       #                               #
                              s.cursor = var66                          #                               #
                              a_8 = var67                               #                               #
                              break                                     #                               #
                        s.cursor = var65                                ##                              #
                    if r:                                                                               #
                        self.right = s.cursor  ##                                                       # setlimit
                        r = True               ## ]                                                     #
                        if r:                                                                           #
                            if a_8 == 0:                                                       ##       #
                                r = self.r_R2(s)  # routine call                               #        #
                                if r:                                                          #        #
                                    var69 = len(s) - s.cursor                       ##         #        #
                                    r = s.starts_with(u's')  # character check      #          #        #
                                    if not r:                                       # or       #        #
                                        s.cursor = len(s) - var69                   #          #        #
                                        r = s.starts_with(u't')  # character check  ##         #        #
                                    if r:                                                      #        #
                                        r = s.set_range(self.left, self.right, u'')  # delete  # among  #
                            if a_8 == 1:                                                       #        #
                                r = s.set_range(self.left, self.right, u'i')  # <-             #        #
                            if a_8 == 2:                                                       #        #
                                r = s.set_range(self.left, self.right, u'')  # delete          #        #
                            if a_8 == 3:                                                       #        #
                                r = s.starts_with(u'gu')  # character check                    #        #
                                if r:                                                          #        #
                                    r = s.set_range(self.left, self.right, u'')  # delete      ##       #
                s.limit = var71                                                                         ##
        return r
    
    def r_un_double(self, s):
        r = True
        var77 = len(s) - s.cursor                                    ##
        a_9 = None                                          ##       #
        r = False                                           #        #
        var73 = s.cursor                                    #        #
        for var72, var76, var75 in _a_9:                    #        #
            if s.starts_with(var72):                        #        #
                var74 = s.cursor                            #        #
                r = (not var76) or getattr(self, var76)(s)  #        #
                if r:                                       # among  # test
                  s.cursor = var74                          #        #
                  a_9 = var75                               #        #
                  break                                     #        #
            s.cursor = var73                                #        #
        if r:                                               #        #
            if a_9 == 0:                                    #        #
                r = True                                    ##       #
        s.cursor = len(s) - var77                                    ##
        if r:
            self.left = s.cursor  ##
            r = True              ## [
            if r:
                r = s.hop(1)  # next
                if r:
                    self.right = s.cursor  ##
                    r = True               ## ]
                    if r:
                        r = s.set_range(self.left, self.right, u'')  # delete
        return r
    
    def r_un_accent(self, s):
        r = True
        for var78 in xrange(1):                                                       ##
            if s.cursor == s.limit:                    ##                             #
                r = False                              #                              #
            else:                                      #                              #
                r = s.chars[s.cursor - 1] not in _g_v  # negative grouping check      #
            if r:                                      #                              #
                s.cursor -= 1                          ##                             #
            if not r:                                                                 #
                break                                                                 #
        if r:                                                                         #
            while True:                                                               #
                var78 = len(s) - s.cursor                                             # atleast
                if s.cursor == s.limit:                    ##                         #
                    r = False                              #                          #
                else:                                      #                          #
                    r = s.chars[s.cursor - 1] not in _g_v  # negative grouping check  #
                if r:                                      #                          #
                    s.cursor -= 1                          ##                         #
                if not r:                                                             #
                    s.cursor = len(s) - var78                                         #
                    break                                                             #
            r = True                                                                  ##
        if r:
            self.left = s.cursor  ##
            r = True              ## [
            if r:
                var79 = len(s) - s.cursor                          ##
                r = s.starts_with(u'\xe9')  # character check      #
                if not r:                                          # or
                    s.cursor = len(s) - var79                      #
                    r = s.starts_with(u'\xe8')  # character check  ##
                if r:
                    self.right = s.cursor  ##
                    r = True               ## ]
                    if r:
                        r = s.set_range(self.left, self.right, u'e')  # <-
        return r
    
    def r_stem(self, s):
        r = True
        var80 = s.cursor                       ##
        r = self.r_prelude(s)  # routine call  #
        s.cursor = var80                       # do
        r = True                               ##
        if r:
            var81 = s.cursor                            ##
            r = self.r_mark_regions(s)  # routine call  #
            s.cursor = var81                            # do
            r = True                                    ##
            if r:
                var91 = s.cursor                                                                                        ##
                var92 = len(s) - s.limit                                                                                #
                s.direction *= -1                                                                                       #
                s.cursor, s.limit = s.limit, s.cursor                                                                   #
                var88 = len(s) - s.cursor                                                                         ##    #
                var87 = len(s) - s.cursor                                                                   ##    #     #
                var86 = len(s) - s.cursor                                                            ##     #     #     #
                var83 = len(s) - s.cursor                              ##                            #      #     #     #
                var82 = len(s) - s.cursor                        ##    #                             #      #     #     #
                r = self.r_standard_suffix(s)  # routine call    #     #                             #      #     #     #
                if not r:                                        # or  #                             #      #     #     #
                    s.cursor = len(s) - var82                    #     # or                          #      #     #     #
                    r = self.r_i_verb_suffix(s)  # routine call  ##    #                             #      #     #     #
                if not r:                                              #                             #      #     #     #
                    s.cursor = len(s) - var83                          #                             #      #     #     #
                    r = self.r_verb_suffix(s)  # routine call          ##                            #      #     #     #
                if r:                                                                                #      #     #     #
                    s.cursor = len(s) - var86                                                        #      #     #     #
                    var85 = len(s) - s.cursor                                                 ##     #      #     #     #
                    self.left = s.cursor  ##                                                  #      #      #     #     #
                    r = True              ## [                                                #      #      #     #     #
                    if r:                                                                     #      #      #     #     #
                        var84 = len(s) - s.cursor                                       ##    #      #      #     #     #
                        r = s.starts_with(u'Y')  # character check                      #     #      # and  #     #     #
                        if r:                                                           #     #      #      # or  # do  #
                            self.right = s.cursor  ##                                   #     #      #      #     #     #
                            r = True               ## ]                                 #     #      #      #     #     #
                            if r:                                                       #     #      #      #     #     #
                                r = s.set_range(self.left, self.right, u'i')  # <-      #     #      #      #     #     #
                        if not r:                                                       # or  # try  #      #     #     # backwards
                            s.cursor = len(s) - var84                                   #     #      #      #     #     #
                            r = s.starts_with(u'\xe7')  # character check               #     #      #      #     #     #
                            if r:                                                       #     #      #      #     #     #
                                self.right = s.cursor  ##                               #     #      #      #     #     #
                                r = True               ## ]                             #     #      #      #     #     #
                                if r:                                                   #     #      #      #     #     #
                                    r = s.set_range(self.left, self.right, u'c')  # <-  ##    #      #      #     #     #
                    if not r:                                                                 #      #      #     #     #
                        r = True                                                              #      #      #     #     #
                        s.cursor = len(s) - var85                                             ##     ##     #     #     #
                if not r:                                                                                   #     #     #
                    s.cursor = len(s) - var87                                                               #     #     #
                    r = self.r_residual_suffix(s)  # routine call                                           ##    #     #
                s.cursor = len(s) - var88                                                                         #     #
                r = True                                                                                          ##    #
                if r:                                                                                                   #
                    var89 = len(s) - s.cursor                ##                                                         #
                    r = self.r_un_double(s)  # routine call  #                                                          #
                    s.cursor = len(s) - var89                # do                                                       #
                    r = True                                 ##                                                         #
                    if r:                                                                                               #
                        var90 = len(s) - s.cursor                ##                                                     #
                        r = self.r_un_accent(s)  # routine call  #                                                      #
                        s.cursor = len(s) - var90                # do                                                   #
                        r = True                                 ##                                                     #
                s.direction *= -1                                                                                       #
                s.cursor = var91                                                                                        #
                s.limit = len(s) - var92                                                                                ##
                if r:
                    var93 = s.cursor                        ##
                    r = self.r_postlude(s)  # routine call  #
                    s.cursor = var93                        # do
                    r = True                                ##
        return r
