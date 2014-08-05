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

_g_v = set(u'aeiouy\xe4\xe5\xf6')
_g_s_ending = set(u'bcdfghjklmnoprtvy')
_a_1 = ((u'heterna', '', 0), (u'hetens', '', 0), (u'anden', '', 0), (u'heten', '', 0), (u'heter', '', 0), (u'arnas', '', 0), (u'ernas', '', 0), (u'ornas', '', 0), (u'andes', '', 0), (u'arens', '', 0), (u'andet', '', 0), (u'arna', '', 0), (u'erna', '', 0), (u'orna', '', 0), (u'ande', '', 0), (u'arne', '', 0), (u'aste', '', 0), (u'aren', '', 0), (u'ades', '', 0), (u'erns', '', 0), (u'ade', '', 0), (u'are', '', 0), (u'ern', '', 0), (u'ens', '', 0), (u'het', '', 0), (u'ast', '', 0), (u'ad', '', 0), (u'en', '', 0), (u'ar', '', 0), (u'er', '', 0), (u'or', '', 0), (u'as', '', 0), (u'es', '', 0), (u'at', '', 0), (u'a', '', 0), (u'e', '', 0), (u's', '', 1),)
_a_2 = ((u'dd', '', 0), (u'gd', '', 0), (u'nn', '', 0), (u'dt', '', 0), (u'gt', '', 0), (u'kt', '', 0), (u'tt', '', 0),)
_a_3 = ((u'fullt', '', 2), (u'l\xf6st', '', 1), (u'lig', '', 0), (u'els', '', 0), (u'ig', '', 0),)

class _Program(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.i_p1 = 0
        self.i_x = 0

    def r_mark_regions(self, s):
        r = True
        self.i_p1 = s.limit
        r = True
        if r:
            var0 = s.cursor                      ##
            r = s.hop(3)  # hop                  #
            if r:                                #
                self.i_x = s.cursor  ##          # test
                r = True             ## setmark  #
            s.cursor = var0                      ##
            if r:
                while True:                                              ##
                    var1 = s.cursor                                      #
                    if s.cursor == s.limit:            ##                #
                        r = False                      #                 #
                    else:                              #                 #
                        r = s.chars[s.cursor] in _g_v  # grouping check  #
                    if r:                              #                 # goto
                        s.cursor += 1                  ##                #
                    if r or s.cursor == s.limit:                         #
                        s.cursor = var1                                  #
                        break                                            #
                    s.cursor = var1 + 1                                  ##
                if r:
                    while True:                                                           ##
                        if s.cursor == s.limit:                ##                         #
                            r = False                          #                          #
                        else:                                  #                          #
                            r = s.chars[s.cursor] not in _g_v  # negative grouping check  #
                        if r:                                  #                          # gopast
                            s.cursor += 1                      ##                         #
                        if r or s.cursor == s.limit:                                      #
                            break                                                         #
                        s.cursor += 1                                                     ##
                    if r:
                        self.i_p1 = s.cursor  ##
                        r = True              ## setmark
                        if r:
                            var2 = s.cursor                ##
                            r = self.i_p1 < self.i_x  # <  #
                            if r:                          #
                                self.i_p1 = self.i_x       #
                                r = True                   # try
                            if not r:                      #
                                r = True                   #
                                s.cursor = var2            ##
        return r
    
    def r_main_suffix(self, s):
        r = True
        var8 = len(s) - s.cursor                                               ##
        var9 = s.limit                                                         #
        r = s.to_mark(self.i_p1)  # tomark                                     #
        if r:                                                                  #
            s.limit = s.cursor                                                 #
            s.cursor = len(s) - var8                                           #
            self.left = s.cursor  ##                                           #
            r = True              ## [                                         #
            if r:                                                              #
                a_1 = None                                        ##           #
                r = False                                         #            #
                var4 = s.cursor                                   #            #
                for var3, var7, var6 in _a_1:                     #            # setlimit
                    if s.starts_with(var3):                       #            #
                        var5 = s.cursor                           #            #
                        r = (not var7) or getattr(self, var7)(s)  # substring  #
                        if r:                                     #            #
                          s.cursor = var5                         #            #
                          a_1 = var6                              #            #
                          break                                   #            #
                    s.cursor = var4                               ##           #
                if r:                                                          #
                    self.right = s.cursor  ##                                  #
                    r = True               ## ]                                #
            s.limit = var9                                                     ##
        if r:
            if a_1 == 0:                                                        ##
                r = s.set_range(self.left, self.right, u'')  # delete           #
            if a_1 == 1:                                                        #
                if s.cursor == s.limit:                       ##                #
                    r = False                                 #                 #
                else:                                         #                 # among
                    r = s.chars[s.cursor - 1] in _g_s_ending  # grouping check  #
                if r:                                         #                 #
                    s.cursor -= 1                             ##                #
                if r:                                                           #
                    r = s.set_range(self.left, self.right, u'')  # delete       ##
        return r
    
    def r_consonant_pair(self, s):
        r = True
        var16 = len(s) - s.cursor                                                         ##
        var17 = s.limit                                                                   #
        r = s.to_mark(self.i_p1)  # tomark                                                #
        if r:                                                                             #
            s.limit = s.cursor                                                            #
            s.cursor = len(s) - var16                                                     #
            var15 = len(s) - s.cursor                                              ##     #
            a_2 = None                                          ##                 #      #
            r = False                                           #                  #      #
            var11 = s.cursor                                    #                  #      #
            for var10, var14, var13 in _a_2:                    #                  #      #
                if s.starts_with(var10):                        #                  #      #
                    var12 = s.cursor                            #                  #      #
                    r = (not var14) or getattr(self, var14)(s)  #                  #      #
                    if r:                                       # among            #      #
                      s.cursor = var12                          #                  #      #
                      a_2 = var13                               #                  #      #
                      break                                     #                  #      # setlimit
                s.cursor = var11                                #                  #      #
            if r:                                               #                  # and  #
                if a_2 == 0:                                    #                  #      #
                    r = True                                    ##                 #      #
            if r:                                                                  #      #
                s.cursor = len(s) - var15                                          #      #
                self.left = s.cursor  ##                                           #      #
                r = True              ## [                                         #      #
                if r:                                                              #      #
                    r = s.hop(1)  # next                                           #      #
                    if r:                                                          #      #
                        self.right = s.cursor  ##                                  #      #
                        r = True               ## ]                                #      #
                        if r:                                                      #      #
                            r = s.set_range(self.left, self.right, u'')  # delete  ##     #
            s.limit = var17                                                               ##
        return r
    
    def r_other_suffix(self, s):
        r = True
        var23 = len(s) - s.cursor                                                             ##
        var24 = s.limit                                                                       #
        r = s.to_mark(self.i_p1)  # tomark                                                    #
        if r:                                                                                 #
            s.limit = s.cursor                                                                #
            s.cursor = len(s) - var23                                                         #
            self.left = s.cursor  ##                                                          #
            r = True              ## [                                                        #
            if r:                                                                             #
                a_3 = None                                          ##                        #
                r = False                                           #                         #
                var19 = s.cursor                                    #                         #
                for var18, var22, var21 in _a_3:                    #                         #
                    if s.starts_with(var18):                        #                         #
                        var20 = s.cursor                            #                         #
                        r = (not var22) or getattr(self, var22)(s)  # substring               #
                        if r:                                       #                         # setlimit
                          s.cursor = var20                          #                         #
                          a_3 = var21                               #                         #
                          break                                     #                         #
                    s.cursor = var19                                ##                        #
                if r:                                                                         #
                    self.right = s.cursor  ##                                                 #
                    r = True               ## ]                                               #
                    if r:                                                                     #
                        if a_3 == 0:                                                 ##       #
                            r = s.set_range(self.left, self.right, u'')  # delete    #        #
                        if a_3 == 1:                                                 #        #
                            r = s.set_range(self.left, self.right, u'l\xf6s')  # <-  # among  #
                        if a_3 == 2:                                                 #        #
                            r = s.set_range(self.left, self.right, u'full')  # <-    ##       #
            s.limit = var24                                                                   ##
        return r
    
    def r_stem(self, s):
        r = True
        var25 = s.cursor                            ##
        r = self.r_mark_regions(s)  # routine call  #
        s.cursor = var25                            # do
        r = True                                    ##
        if r:
            var29 = s.cursor                                          ##
            var30 = len(s) - s.limit                                  #
            s.direction *= -1                                         #
            s.cursor, s.limit = s.limit, s.cursor                     #
            var26 = len(s) - s.cursor                  ##             #
            r = self.r_main_suffix(s)  # routine call  #              #
            s.cursor = len(s) - var26                  # do           #
            r = True                                   ##             #
            if r:                                                     #
                var27 = len(s) - s.cursor                     ##      #
                r = self.r_consonant_pair(s)  # routine call  #       # backwards
                s.cursor = len(s) - var27                     # do    #
                r = True                                      ##      #
                if r:                                                 #
                    var28 = len(s) - s.cursor                   ##    #
                    r = self.r_other_suffix(s)  # routine call  #     #
                    s.cursor = len(s) - var28                   # do  #
                    r = True                                    ##    #
            s.direction *= -1                                         #
            s.cursor = var29                                          #
            s.limit = len(s) - var30                                  ##
        return r
