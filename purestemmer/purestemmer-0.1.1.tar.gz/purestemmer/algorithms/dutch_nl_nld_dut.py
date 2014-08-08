#!/usr/bin/env python
# vim:fileencoding=utf-8



# This file was auto-generated on 2014-08-05 20:03:59 using
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

_g_v = set(u'aeiouy\xe8')
_g_v_I = (_g_v | set(u'I'))
_g_v_j = (_g_v | set(u'j'))
_a_1 = ((u'\xe4', '', 0), (u'\xe1', '', 0), (u'\xeb', '', 1), (u'\xe9', '', 1), (u'\xef', '', 2), (u'\xed', '', 2), (u'\xf6', '', 3), (u'\xf3', '', 3), (u'\xfc', '', 4), (u'\xfa', '', 4), (u'', '', 5),)
_a_2 = ((u'Y', '', 0), (u'I', '', 1), (u'', '', 2),)
_a_3 = ((u'kk', '', 0), (u'dd', '', 0), (u'tt', '', 0),)
_a_4 = ((u'heden', '', 0), (u'ene', '', 1), (u'en', '', 1), (u'se', '', 2), (u's', '', 2),)
_a_5 = ((u'lijk', '', 2), (u'baar', '', 3), (u'end', '', 0), (u'ing', '', 0), (u'bar', '', 4), (u'ig', '', 1),)
_a_6 = ((u'aa', '', 0), (u'ee', '', 0), (u'oo', '', 0), (u'uu', '', 0),)

class _Program(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.b_e_found = True
        self.i_p1 = 0
        self.i_p2 = 0

    def r_prelude(self, s):
        r = True
        var6 = s.cursor                                                                            ##
        while True:                                                                      ##        #
            var5 = s.cursor                                                              #         #
            self.left = s.cursor  ##                                                     #         #
            r = True              ## [                                                   #         #
            if r:                                                                        #         #
                a_1 = None                                        ##                     #         #
                r = False                                         #                      #         #
                var1 = s.cursor                                   #                      #         #
                for var0, var4, var3 in _a_1:                     #                      #         #
                    if s.starts_with(var0):                       #                      #         #
                        var2 = s.cursor                           #                      #         #
                        r = (not var4) or getattr(self, var4)(s)  # substring            #         #
                        if r:                                     #                      #         #
                          s.cursor = var2                         #                      #         #
                          a_1 = var3                              #                      #         #
                          break                                   #                      #         #
                    s.cursor = var1                               ##                     #         #
                if r:                                                                    #         #
                    self.right = s.cursor  ##                                            # repeat  # test
                    r = True               ## ]                                          #         #
                    if r:                                                                #         #
                        if a_1 == 0:                                            ##       #         #
                            r = s.set_range(self.left, self.right, u'a')  # <-  #        #         #
                        if a_1 == 1:                                            #        #         #
                            r = s.set_range(self.left, self.right, u'e')  # <-  #        #         #
                        if a_1 == 2:                                            #        #         #
                            r = s.set_range(self.left, self.right, u'i')  # <-  #        #         #
                        if a_1 == 3:                                            # among  #         #
                            r = s.set_range(self.left, self.right, u'o')  # <-  #        #         #
                        if a_1 == 4:                                            #        #         #
                            r = s.set_range(self.left, self.right, u'u')  # <-  #        #         #
                        if a_1 == 5:                                            #        #         #
                            r = s.hop(1)  # next                                ##       #         #
            if not r:                                                                    #         #
                s.cursor = var5                                                          #         #
                break                                                                    #         #
        r = True                                                                         ##        #
        s.cursor = var6                                                                            ##
        if r:
            var7 = s.cursor                                                 ##
            self.left = s.cursor  ##                                        #
            r = True              ## [                                      #
            if r:                                                           #
                r = s.starts_with(u'y')  # character check                  #
                if r:                                                       #
                    self.right = s.cursor  ##                               # try
                    r = True               ## ]                             #
                    if r:                                                   #
                        r = s.set_range(self.left, self.right, u'Y')  # <-  #
            if not r:                                                       #
                r = True                                                    #
                s.cursor = var7                                             ##
            if r:
                while True:                                                                                   ##
                    var10 = s.cursor                                                                          #
                    while True:                                                                       ##      #
                        var9 = s.cursor                                                               #       #
                        if s.cursor == s.limit:            ##                                         #       #
                            r = False                      #                                          #       #
                        else:                              #                                          #       #
                            r = s.chars[s.cursor] in _g_v  # grouping check                           #       #
                        if r:                              #                                          #       #
                            s.cursor += 1                  ##                                         #       #
                        if r:                                                                         #       #
                            self.left = s.cursor  ##                                                  #       #
                            r = True              ## [                                                #       #
                            if r:                                                                     #       #
                                var8 = s.cursor                                                 ##    #       #
                                r = s.starts_with(u'i')  # character check                      #     #       #
                                if r:                                                           #     #       #
                                    self.right = s.cursor  ##                                   #     #       #
                                    r = True               ## ]                                 #     #       #
                                    if r:                                                       #     #       #
                                        if s.cursor == s.limit:            ##                   #     #       #
                                            r = False                      #                    #     # goto  #
                                        else:                              #                    #     #       # repeat
                                            r = s.chars[s.cursor] in _g_v  # grouping check     #     #       #
                                        if r:                              #                    #     #       #
                                            s.cursor += 1                  ##                   # or  #       #
                                        if r:                                                   #     #       #
                                            r = s.set_range(self.left, self.right, u'I')  # <-  #     #       #
                                if not r:                                                       #     #       #
                                    s.cursor = var8                                             #     #       #
                                    r = s.starts_with(u'y')  # character check                  #     #       #
                                    if r:                                                       #     #       #
                                        self.right = s.cursor  ##                               #     #       #
                                        r = True               ## ]                             #     #       #
                                        if r:                                                   #     #       #
                                            r = s.set_range(self.left, self.right, u'Y')  # <-  ##    #       #
                        if r or s.cursor == s.limit:                                                  #       #
                            s.cursor = var9                                                           #       #
                            break                                                                     #       #
                        s.cursor = var9 + 1                                                           ##      #
                    if not r:                                                                                 #
                        s.cursor = var10                                                                      #
                        break                                                                                 #
                r = True                                                                                      ##
        return r
    
    def r_mark_regions(self, s):
        r = True
        self.i_p1 = s.limit
        r = True
        if r:
            self.i_p2 = s.limit
            r = True
            if r:
                while True:                                              ##
                    if s.cursor == s.limit:            ##                #
                        r = False                      #                 #
                    else:                              #                 #
                        r = s.chars[s.cursor] in _g_v  # grouping check  #
                    if r:                              #                 # gopast
                        s.cursor += 1                  ##                #
                    if r or s.cursor == s.limit:                         #
                        break                                            #
                    s.cursor += 1                                        ##
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
                            var11 = s.cursor        ##
                            r = self.i_p1 < 3  # <  #
                            if r:                   #
                                self.i_p1 = 3       #
                                r = True            # try
                            if not r:               #
                                r = True            #
                                s.cursor = var11    ##
                            if r:
                                while True:                                              ##
                                    if s.cursor == s.limit:            ##                #
                                        r = False                      #                 #
                                    else:                              #                 #
                                        r = s.chars[s.cursor] in _g_v  # grouping check  #
                                    if r:                              #                 # gopast
                                        s.cursor += 1                  ##                #
                                    if r or s.cursor == s.limit:                         #
                                        break                                            #
                                    s.cursor += 1                                        ##
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
                                        self.i_p2 = s.cursor  ##
                                        r = True              ## setmark
        return r
    
    def r_postlude(self, s):
        r = True
        while True:                                                                      ##
            var17 = s.cursor                                                             #
            self.left = s.cursor  ##                                                     #
            r = True              ## [                                                   #
            if r:                                                                        #
                a_2 = None                                          ##                   #
                r = False                                           #                    #
                var13 = s.cursor                                    #                    #
                for var12, var16, var15 in _a_2:                    #                    #
                    if s.starts_with(var12):                        #                    #
                        var14 = s.cursor                            #                    #
                        r = (not var16) or getattr(self, var16)(s)  # substring          #
                        if r:                                       #                    #
                          s.cursor = var14                          #                    #
                          a_2 = var15                               #                    #
                          break                                     #                    # repeat
                    s.cursor = var13                                ##                   #
                if r:                                                                    #
                    self.right = s.cursor  ##                                            #
                    r = True               ## ]                                          #
                    if r:                                                                #
                        if a_2 == 0:                                            ##       #
                            r = s.set_range(self.left, self.right, u'y')  # <-  #        #
                        if a_2 == 1:                                            #        #
                            r = s.set_range(self.left, self.right, u'i')  # <-  # among  #
                        if a_2 == 2:                                            #        #
                            r = s.hop(1)  # next                                ##       #
            if not r:                                                                    #
                s.cursor = var17                                                         #
                break                                                                    #
        r = True                                                                         ##
        return r
    
    def r_R1(self, s):
        r = True
        r = self.i_p1 <= s.cursor  # <=
        return r
    
    def r_R2(self, s):
        r = True
        r = self.i_p2 <= s.cursor  # <=
        return r
    
    def r_undouble(self, s):
        r = True
        var23 = len(s) - s.cursor                                    ##
        a_3 = None                                          ##       #
        r = False                                           #        #
        var19 = s.cursor                                    #        #
        for var18, var22, var21 in _a_3:                    #        #
            if s.starts_with(var18):                        #        #
                var20 = s.cursor                            #        #
                r = (not var22) or getattr(self, var22)(s)  #        #
                if r:                                       # among  # test
                  s.cursor = var20                          #        #
                  a_3 = var21                               #        #
                  break                                     #        #
            s.cursor = var19                                #        #
        if r:                                               #        #
            if a_3 == 0:                                    #        #
                r = True                                    ##       #
        s.cursor = len(s) - var23                                    ##
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
    
    def r_e_ending(self, s):
        r = True
        self.b_e_found = False  ##
        r = True                ## unset
        if r:
            self.left = s.cursor  ##
            r = True              ## [
            if r:
                r = s.starts_with(u'e')  # character check
                if r:
                    self.right = s.cursor  ##
                    r = True               ## ]
                    if r:
                        r = self.r_R1(s)  # routine call
                        if r:
                            var24 = len(s) - s.cursor                                             ##
                            if s.cursor == s.limit:                    ##                         #
                                r = False                              #                          #
                            else:                                      #                          #
                                r = s.chars[s.cursor - 1] not in _g_v  # negative grouping check  # test
                            if r:                                      #                          #
                                s.cursor -= 1                          ##                         #
                            s.cursor = len(s) - var24                                             ##
                            if r:
                                r = s.set_range(self.left, self.right, u'')  # delete
                                if r:
                                    self.b_e_found = True  ##
                                    r = True               ## set
                                    if r:
                                        r = self.r_undouble(s)  # routine call
        return r
    
    def r_en_ending(self, s):
        r = True
        r = self.r_R1(s)  # routine call
        if r:
            var26 = len(s) - s.cursor                                             ##
            if s.cursor == s.limit:                    ##                         #
                r = False                              #                          #
            else:                                      #                          #
                r = s.chars[s.cursor - 1] not in _g_v  # negative grouping check  #
            if r:                                      #                          #
                s.cursor -= 1                          ##                         #
            if r:                                                                 # and
                s.cursor = len(s) - var26                                         #
                var25 = len(s) - s.cursor                     ##                  #
                r = s.starts_with(u'gem')  # character check  #                   #
                if not r:                                     # not               #
                    s.cursor = len(s) - var25                 #                   #
                r = not r                                     ##                  ##
            if r:
                r = s.set_range(self.left, self.right, u'')  # delete
                if r:
                    r = self.r_undouble(s)  # routine call
        return r
    
    def r_standard_suffix(self, s):
        r = True
        var32 = len(s) - s.cursor                                                                            ##
        self.left = s.cursor  ##                                                                             #
        r = True              ## [                                                                           #
        if r:                                                                                                #
            a_4 = None                                          ##                                           #
            r = False                                           #                                            #
            var28 = s.cursor                                    #                                            #
            for var27, var31, var30 in _a_4:                    #                                            #
                if s.starts_with(var27):                        #                                            #
                    var29 = s.cursor                            #                                            #
                    r = (not var31) or getattr(self, var31)(s)  # substring                                  #
                    if r:                                       #                                            #
                      s.cursor = var29                          #                                            #
                      a_4 = var30                               #                                            #
                      break                                     #                                            #
                s.cursor = var28                                ##                                           #
            if r:                                                                                            #
                self.right = s.cursor  ##                                                                    #
                r = True               ## ]                                                                  #
                if r:                                                                                        # do
                    if a_4 == 0:                                                                    ##       #
                        r = self.r_R1(s)  # routine call                                            #        #
                        if r:                                                                       #        #
                            r = s.set_range(self.left, self.right, u'heid')  # <-                   #        #
                    if a_4 == 1:                                                                    #        #
                        r = self.r_en_ending(s)  # routine call                                     #        #
                    if a_4 == 2:                                                                    #        #
                        r = self.r_R1(s)  # routine call                                            #        #
                        if r:                                                                       # among  #
                            if s.cursor == s.limit:                      ##                         #        #
                                r = False                                #                          #        #
                            else:                                        #                          #        #
                                r = s.chars[s.cursor - 1] not in _g_v_j  # negative grouping check  #        #
                            if r:                                        #                          #        #
                                s.cursor -= 1                            ##                         #        #
                            if r:                                                                   #        #
                                r = s.set_range(self.left, self.right, u'')  # delete               ##       #
        s.cursor = len(s) - var32                                                                            #
        r = True                                                                                             ##
        if r:
            var33 = len(s) - s.cursor               ##
            r = self.r_e_ending(s)  # routine call  #
            s.cursor = len(s) - var33               # do
            r = True                                ##
            if r:
                var35 = len(s) - s.cursor                                                    ##
                self.left = s.cursor  ##                                                     #
                r = True              ## [                                                   #
                if r:                                                                        #
                    r = s.starts_with(u'heid')  # character check                            #
                    if r:                                                                    #
                        self.right = s.cursor  ##                                            #
                        r = True               ## ]                                          #
                        if r:                                                                #
                            r = self.r_R2(s)  # routine call                                 #
                            if r:                                                            #
                                var34 = len(s) - s.cursor                   ##               #
                                r = s.starts_with(u'c')  # character check  #                #
                                if not r:                                   # not            #
                                    s.cursor = len(s) - var34               #                #
                                r = not r                                   ##               # do
                                if r:                                                        #
                                    r = s.set_range(self.left, self.right, u'')  # delete    #
                                    if r:                                                    #
                                        self.left = s.cursor  ##                             #
                                        r = True              ## [                           #
                                        if r:                                                #
                                            r = s.starts_with(u'en')  # character check      #
                                            if r:                                            #
                                                self.right = s.cursor  ##                    #
                                                r = True               ## ]                  #
                                                if r:                                        #
                                                    r = self.r_en_ending(s)  # routine call  #
                s.cursor = len(s) - var35                                                    #
                r = True                                                                     ##
                if r:
                    var44 = len(s) - s.cursor                                                                                         ##
                    self.left = s.cursor  ##                                                                                          #
                    r = True              ## [                                                                                        #
                    if r:                                                                                                             #
                        a_5 = None                                          ##                                                        #
                        r = False                                           #                                                         #
                        var37 = s.cursor                                    #                                                         #
                        for var36, var40, var39 in _a_5:                    #                                                         #
                            if s.starts_with(var36):                        #                                                         #
                                var38 = s.cursor                            #                                                         #
                                r = (not var40) or getattr(self, var40)(s)  # substring                                               #
                                if r:                                       #                                                         #
                                  s.cursor = var38                          #                                                         #
                                  a_5 = var39                               #                                                         #
                                  break                                     #                                                         #
                            s.cursor = var37                                ##                                                        #
                        if r:                                                                                                         #
                            self.right = s.cursor  ##                                                                                 #
                            r = True               ## ]                                                                               #
                            if r:                                                                                                     #
                                if a_5 == 0:                                                                                 ##       #
                                    r = self.r_R2(s)  # routine call                                                         #        #
                                    if r:                                                                                    #        #
                                        r = s.set_range(self.left, self.right, u'')  # delete                                #        #
                                        if r:                                                                                #        #
                                            var42 = len(s) - s.cursor                                                  ##    #        #
                                            self.left = s.cursor  ##                                                   #     #        #
                                            r = True              ## [                                                 #     #        #
                                            if r:                                                                      #     #        #
                                                r = s.starts_with(u'ig')  # character check                            #     #        #
                                                if r:                                                                  #     #        #
                                                    self.right = s.cursor  ##                                          #     #        #
                                                    r = True               ## ]                                        #     #        #
                                                    if r:                                                              #     #        #
                                                        r = self.r_R2(s)  # routine call                               #     #        #
                                                        if r:                                                          # or  #        #
                                                            var41 = len(s) - s.cursor                   ##             #     #        #
                                                            r = s.starts_with(u'e')  # character check  #              #     #        # do
                                                            if not r:                                   # not          #     #        #
                                                                s.cursor = len(s) - var41               #              #     #        #
                                                            r = not r                                   ##             #     #        #
                                                            if r:                                                      #     #        #
                                                                r = s.set_range(self.left, self.right, u'')  # delete  #     #        #
                                            if not r:                                                                  #     #        #
                                                s.cursor = len(s) - var42                                              #     #        #
                                                r = self.r_undouble(s)  # routine call                                 ##    #        #
                                if a_5 == 1:                                                                                 # among  #
                                    r = self.r_R2(s)  # routine call                                                         #        #
                                    if r:                                                                                    #        #
                                        var43 = len(s) - s.cursor                   ##                                       #        #
                                        r = s.starts_with(u'e')  # character check  #                                        #        #
                                        if not r:                                   # not                                    #        #
                                            s.cursor = len(s) - var43               #                                        #        #
                                        r = not r                                   ##                                       #        #
                                        if r:                                                                                #        #
                                            r = s.set_range(self.left, self.right, u'')  # delete                            #        #
                                if a_5 == 2:                                                                                 #        #
                                    r = self.r_R2(s)  # routine call                                                         #        #
                                    if r:                                                                                    #        #
                                        r = s.set_range(self.left, self.right, u'')  # delete                                #        #
                                        if r:                                                                                #        #
                                            r = self.r_e_ending(s)  # routine call                                           #        #
                                if a_5 == 3:                                                                                 #        #
                                    r = self.r_R2(s)  # routine call                                                         #        #
                                    if r:                                                                                    #        #
                                        r = s.set_range(self.left, self.right, u'')  # delete                                #        #
                                if a_5 == 4:                                                                                 #        #
                                    r = self.r_R2(s)  # routine call                                                         #        #
                                    if r:                                                                                    #        #
                                        r = self.b_e_found  # boolean variable check                                         #        #
                                        if r:                                                                                #        #
                                            r = s.set_range(self.left, self.right, u'')  # delete                            ##       #
                    s.cursor = len(s) - var44                                                                                         #
                    r = True                                                                                                          ##
                    if r:
                        var51 = len(s) - s.cursor                                                             ##
                        if s.cursor == s.limit:                      ##                                       #
                            r = False                                #                                        #
                        else:                                        #                                        #
                            r = s.chars[s.cursor - 1] not in _g_v_I  # negative grouping check                #
                        if r:                                        #                                        #
                            s.cursor -= 1                            ##                                       #
                        if r:                                                                                 #
                            var50 = len(s) - s.cursor                                                 ##      #
                            a_6 = None                                          ##                    #       #
                            r = False                                           #                     #       #
                            var46 = s.cursor                                    #                     #       #
                            for var45, var49, var48 in _a_6:                    #                     #       #
                                if s.starts_with(var45):                        #                     #       #
                                    var47 = s.cursor                            #                     #       #
                                    r = (not var49) or getattr(self, var49)(s)  #                     #       #
                                    if r:                                       # among               #       #
                                      s.cursor = var47                          #                     #       #
                                      a_6 = var48                               #                     #       #
                                      break                                     #                     #       #
                                s.cursor = var46                                #                     # test  #
                            if r:                                               #                     #       #
                                if a_6 == 0:                                    #                     #       # do
                                    r = True                                    ##                    #       #
                            if r:                                                                     #       #
                                if s.cursor == s.limit:                    ##                         #       #
                                    r = False                              #                          #       #
                                else:                                      #                          #       #
                                    r = s.chars[s.cursor - 1] not in _g_v  # negative grouping check  #       #
                                if r:                                      #                          #       #
                                    s.cursor -= 1                          ##                         #       #
                            s.cursor = len(s) - var50                                                 ##      #
                            if r:                                                                             #
                                self.left = s.cursor  ##                                                      #
                                r = True              ## [                                                    #
                                if r:                                                                         #
                                    r = s.hop(1)  # next                                                      #
                                    if r:                                                                     #
                                        self.right = s.cursor  ##                                             #
                                        r = True               ## ]                                           #
                                        if r:                                                                 #
                                            r = s.set_range(self.left, self.right, u'')  # delete             #
                        s.cursor = len(s) - var51                                                             #
                        r = True                                                                              ##
        return r
    
    def r_stem(self, s):
        r = True
        var52 = s.cursor                       ##
        r = self.r_prelude(s)  # routine call  #
        s.cursor = var52                       # do
        r = True                               ##
        if r:
            var53 = s.cursor                            ##
            r = self.r_mark_regions(s)  # routine call  #
            s.cursor = var53                            # do
            r = True                                    ##
            if r:
                var55 = s.cursor                                     ##
                var56 = len(s) - s.limit                             #
                s.direction *= -1                                    #
                s.cursor, s.limit = s.limit, s.cursor                #
                var54 = len(s) - s.cursor                      ##    #
                r = self.r_standard_suffix(s)  # routine call  #     # backwards
                s.cursor = len(s) - var54                      # do  #
                r = True                                       ##    #
                s.direction *= -1                                    #
                s.cursor = var55                                     #
                s.limit = len(s) - var56                             ##
                if r:
                    var57 = s.cursor                        ##
                    r = self.r_postlude(s)  # routine call  #
                    s.cursor = var57                        # do
                    r = True                                ##
        return r
