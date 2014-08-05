#!/usr/bin/env python
# vim:fileencoding=utf-8



# This file was auto-generated on 2014-08-05 20:04:14 using
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

_g_v = set(u'aeiouy')
_g_v_WXY = (_g_v | set(u'wxY'))
_a_1 = ((u'sses', '', 0), (u'ies', '', 1), (u'ss', '', 2), (u's', '', 3),)
_a_2 = ((u'eed', '', 0), (u'ing', '', 1), (u'ed', '', 1),)
_a_3 = ((u'at', '', 0), (u'bl', '', 0), (u'iz', '', 0), (u'bb', '', 1), (u'dd', '', 1), (u'ff', '', 1), (u'gg', '', 1), (u'mm', '', 1), (u'nn', '', 1), (u'pp', '', 1), (u'rr', '', 1), (u'tt', '', 1), (u'', '', 2),)
_a_4 = ((u'ization', '', 6), (u'ational', '', 7), (u'fulness', '', 10), (u'ousness', '', 11), (u'iveness', '', 12), (u'tional', '', 0), (u'biliti', '', 13), (u'entli', '', 4), (u'ation', '', 7), (u'alism', '', 9), (u'aliti', '', 9), (u'ousli', '', 11), (u'iviti', '', 12), (u'enci', '', 1), (u'anci', '', 2), (u'abli', '', 3), (u'izer', '', 6), (u'ator', '', 7), (u'alli', '', 8), (u'eli', '', 5),)
_a_5 = ((u'alize', '', 0), (u'icate', '', 1), (u'iciti', '', 1), (u'ative', '', 2), (u'ical', '', 1), (u'ness', '', 2), (u'ful', '', 2),)
_a_6 = ((u'ement', '', 0), (u'ance', '', 0), (u'ence', '', 0), (u'able', '', 0), (u'ible', '', 0), (u'ment', '', 0), (u'ant', '', 0), (u'ent', '', 0), (u'ism', '', 0), (u'ate', '', 0), (u'iti', '', 0), (u'ous', '', 0), (u'ive', '', 0), (u'ize', '', 0), (u'ion', '', 1), (u'al', '', 0), (u'er', '', 0), (u'ic', '', 0), (u'ou', '', 0),)

class _Program(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.i_p1 = 0
        self.i_p2 = 0
        self.b_Y_found = True

    def r_shortv(self, s):
        r = True
        if s.cursor == s.limit:                        ##
            r = False                                  #
        else:                                          #
            r = s.chars[s.cursor - 1] not in _g_v_WXY  # negative grouping check
        if r:                                          #
            s.cursor -= 1                              ##
        if r:
            if s.cursor == s.limit:                ##
                r = False                          #
            else:                                  #
                r = s.chars[s.cursor - 1] in _g_v  # grouping check
            if r:                                  #
                s.cursor -= 1                      ##
            if r:
                if s.cursor == s.limit:                    ##
                    r = False                              #
                else:                                      #
                    r = s.chars[s.cursor - 1] not in _g_v  # negative grouping check
                if r:                                      #
                    s.cursor -= 1                          ##
        return r
    
    def r_R1(self, s):
        r = True
        r = self.i_p1 <= s.cursor  # <=
        return r
    
    def r_R2(self, s):
        r = True
        r = self.i_p2 <= s.cursor  # <=
        return r
    
    def r_Step_1a(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_1 = None                                        ##
            r = False                                         #
            var1 = s.cursor                                   #
            for var0, var4, var3 in _a_1:                     #
                if s.starts_with(var0):                       #
                    var2 = s.cursor                           #
                    r = (not var4) or getattr(self, var4)(s)  # substring
                    if r:                                     #
                      s.cursor = var2                         #
                      a_1 = var3                              #
                      break                                   #
                s.cursor = var1                               ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_1 == 0:                                               ##
                        r = s.set_range(self.left, self.right, u'ss')  # <-    #
                    if a_1 == 1:                                               #
                        r = s.set_range(self.left, self.right, u'i')  # <-     #
                    if a_1 == 2:                                               # among
                        pass                                                   #
                    if a_1 == 3:                                               #
                        r = s.set_range(self.left, self.right, u'')  # delete  ##
        return r
    
    def r_Step_1b(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_2 = None                                        ##
            r = False                                         #
            var6 = s.cursor                                   #
            for var5, var9, var8 in _a_2:                     #
                if s.starts_with(var5):                       #
                    var7 = s.cursor                           #
                    r = (not var9) or getattr(self, var9)(s)  # substring
                    if r:                                     #
                      s.cursor = var7                         #
                      a_2 = var8                              #
                      break                                   #
                s.cursor = var6                               ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_2 == 0:                                                                                    ##
                        r = self.r_R1(s)  # routine call                                                            #
                        if r:                                                                                       #
                            r = s.set_range(self.left, self.right, u'ee')  # <-                                     #
                    if a_2 == 1:                                                                                    #
                        var10 = len(s) - s.cursor                                              ##                   #
                        while True:                                                  ##        #                    #
                            if s.cursor == s.limit:                ##                #         #                    #
                                r = False                          #                 #         #                    #
                            else:                                  #                 #         #                    #
                                r = s.chars[s.cursor - 1] in _g_v  # grouping check  #         #                    #
                            if r:                                  #                 # gopast  # test               #
                                s.cursor -= 1                      ##                #         #                    #
                            if r or s.cursor == s.limit:                             #         #                    #
                                break                                                #         #                    #
                            s.cursor -= 1                                            ##        #                    #
                        s.cursor = len(s) - var10                                              ##                   #
                        if r:                                                                                       #
                            r = s.set_range(self.left, self.right, u'')  # delete                                   #
                            if r:                                                                                   #
                                var16 = len(s) - s.cursor                                        ##                 #
                                a_3 = None                                          ##           #                  #
                                r = False                                           #            #                  #
                                var12 = s.cursor                                    #            #                  #
                                for var11, var15, var14 in _a_3:                    #            #                  #
                                    if s.starts_with(var11):                        #            #                  #
                                        var13 = s.cursor                            #            #                  #
                                        r = (not var15) or getattr(self, var15)(s)  # substring  # test             # among
                                        if r:                                       #            #                  #
                                          s.cursor = var13                          #            #                  #
                                          a_3 = var14                               #            #                  #
                                          break                                     #            #                  #
                                    s.cursor = var12                                ##           #                  #
                                s.cursor = len(s) - var16                                        ##                 #
                                if r:                                                                               #
                                    if a_3 == 0:                                                           ##       #
                                        r = s.insert(u'e')  # insert                                       #        #
                                    if a_3 == 1:                                                           #        #
                                        self.left = s.cursor  ##                                           #        #
                                        r = True              ## [                                         #        #
                                        if r:                                                              #        #
                                            r = s.hop(1)  # next                                           #        #
                                            if r:                                                          #        #
                                                self.right = s.cursor  ##                                  #        #
                                                r = True               ## ]                                #        #
                                                if r:                                                      # among  #
                                                    r = s.set_range(self.left, self.right, u'')  # delete  #        #
                                    if a_3 == 2:                                                           #        #
                                        r = (s.cursor == self.i_p1)  # atmark                              #        #
                                        if r:                                                              #        #
                                            var17 = len(s) - s.cursor             ##                       #        #
                                            r = self.r_shortv(s)  # routine call  # test                   #        #
                                            s.cursor = len(s) - var17             ##                       #        #
                                            if r:                                                          #        #
                                                r = s.insert(u'e')  # insert                               ##       ##
        return r
    
    def r_Step_1c(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            var18 = len(s) - s.cursor                       ##
            r = s.starts_with(u'y')  # character check      #
            if not r:                                       # or
                s.cursor = len(s) - var18                   #
                r = s.starts_with(u'Y')  # character check  ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    while True:                                                  ##
                        if s.cursor == s.limit:                ##                #
                            r = False                          #                 #
                        else:                                  #                 #
                            r = s.chars[s.cursor - 1] in _g_v  # grouping check  #
                        if r:                                  #                 # gopast
                            s.cursor -= 1                      ##                #
                        if r or s.cursor == s.limit:                             #
                            break                                                #
                        s.cursor -= 1                                            ##
                    if r:
                        r = s.set_range(self.left, self.right, u'i')  # <-
        return r
    
    def r_Step_2(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_4 = None                                          ##
            r = False                                           #
            var20 = s.cursor                                    #
            for var19, var23, var22 in _a_4:                    #
                if s.starts_with(var19):                        #
                    var21 = s.cursor                            #
                    r = (not var23) or getattr(self, var23)(s)  # substring
                    if r:                                       #
                      s.cursor = var21                          #
                      a_4 = var22                               #
                      break                                     #
                s.cursor = var20                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = self.r_R1(s)  # routine call
                    if r:
                        if a_4 == 0:                                               ##
                            r = s.set_range(self.left, self.right, u'tion')  # <-  #
                        if a_4 == 1:                                               #
                            r = s.set_range(self.left, self.right, u'ence')  # <-  #
                        if a_4 == 2:                                               #
                            r = s.set_range(self.left, self.right, u'ance')  # <-  #
                        if a_4 == 3:                                               #
                            r = s.set_range(self.left, self.right, u'able')  # <-  #
                        if a_4 == 4:                                               #
                            r = s.set_range(self.left, self.right, u'ent')  # <-   #
                        if a_4 == 5:                                               #
                            r = s.set_range(self.left, self.right, u'e')  # <-     #
                        if a_4 == 6:                                               #
                            r = s.set_range(self.left, self.right, u'ize')  # <-   #
                        if a_4 == 7:                                               # among
                            r = s.set_range(self.left, self.right, u'ate')  # <-   #
                        if a_4 == 8:                                               #
                            r = s.set_range(self.left, self.right, u'al')  # <-    #
                        if a_4 == 9:                                               #
                            r = s.set_range(self.left, self.right, u'al')  # <-    #
                        if a_4 == 10:                                              #
                            r = s.set_range(self.left, self.right, u'ful')  # <-   #
                        if a_4 == 11:                                              #
                            r = s.set_range(self.left, self.right, u'ous')  # <-   #
                        if a_4 == 12:                                              #
                            r = s.set_range(self.left, self.right, u'ive')  # <-   #
                        if a_4 == 13:                                              #
                            r = s.set_range(self.left, self.right, u'ble')  # <-   ##
        return r
    
    def r_Step_3(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_5 = None                                          ##
            r = False                                           #
            var25 = s.cursor                                    #
            for var24, var28, var27 in _a_5:                    #
                if s.starts_with(var24):                        #
                    var26 = s.cursor                            #
                    r = (not var28) or getattr(self, var28)(s)  # substring
                    if r:                                       #
                      s.cursor = var26                          #
                      a_5 = var27                               #
                      break                                     #
                s.cursor = var25                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = self.r_R1(s)  # routine call
                    if r:
                        if a_5 == 0:                                               ##
                            r = s.set_range(self.left, self.right, u'al')  # <-    #
                        if a_5 == 1:                                               #
                            r = s.set_range(self.left, self.right, u'ic')  # <-    # among
                        if a_5 == 2:                                               #
                            r = s.set_range(self.left, self.right, u'')  # delete  ##
        return r
    
    def r_Step_4(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_6 = None                                          ##
            r = False                                           #
            var30 = s.cursor                                    #
            for var29, var33, var32 in _a_6:                    #
                if s.starts_with(var29):                        #
                    var31 = s.cursor                            #
                    r = (not var33) or getattr(self, var33)(s)  # substring
                    if r:                                       #
                      s.cursor = var31                          #
                      a_6 = var32                               #
                      break                                     #
                s.cursor = var30                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = self.r_R2(s)  # routine call
                    if r:
                        if a_6 == 0:                                                   ##
                            r = s.set_range(self.left, self.right, u'')  # delete      #
                        if a_6 == 1:                                                   #
                            var34 = len(s) - s.cursor                       ##         #
                            r = s.starts_with(u's')  # character check      #          #
                            if not r:                                       # or       # among
                                s.cursor = len(s) - var34                   #          #
                                r = s.starts_with(u't')  # character check  ##         #
                            if r:                                                      #
                                r = s.set_range(self.left, self.right, u'')  # delete  ##
        return r
    
    def r_Step_5a(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            r = s.starts_with(u'e')  # character check
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    var36 = len(s) - s.cursor                            ##
                    r = self.r_R2(s)  # routine call                     #
                    if not r:                                            #
                        s.cursor = len(s) - var36                        #
                        r = self.r_R1(s)  # routine call                 #
                        if r:                                            # or
                            var35 = len(s) - s.cursor             ##     #
                            r = self.r_shortv(s)  # routine call  #      #
                            if not r:                             # not  #
                                s.cursor = len(s) - var35         #      #
                            r = not r                             ##     ##
                    if r:
                        r = s.set_range(self.left, self.right, u'')  # delete
        return r
    
    def r_Step_5b(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            r = s.starts_with(u'l')  # character check
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = self.r_R2(s)  # routine call
                    if r:
                        r = s.starts_with(u'l')  # character check
                        if r:
                            r = s.set_range(self.left, self.right, u'')  # delete
        return r
    
    def r_stem(self, s):
        r = True
        self.b_Y_found = False  ##
        r = True                ## unset
        if r:
            var37 = s.cursor                                                ##
            self.left = s.cursor  ##                                        #
            r = True              ## [                                      #
            if r:                                                           #
                r = s.starts_with(u'y')  # character check                  #
                if r:                                                       #
                    self.right = s.cursor  ##                               #
                    r = True               ## ]                             # do
                    if r:                                                   #
                        r = s.set_range(self.left, self.right, u'Y')  # <-  #
                        if r:                                               #
                            self.b_Y_found = True  ##                       #
                            r = True               ## set                   #
            s.cursor = var37                                                #
            r = True                                                        ##
            if r:
                var40 = s.cursor                                                               ##
                while True:                                                          ##        #
                    var39 = s.cursor                                                 #         #
                    while True:                                              ##      #         #
                        var38 = s.cursor                                     #       #         #
                        if s.cursor == s.limit:            ##                #       #         #
                            r = False                      #                 #       #         #
                        else:                              #                 #       #         #
                            r = s.chars[s.cursor] in _g_v  # grouping check  #       #         #
                        if r:                              #                 #       #         #
                            s.cursor += 1                  ##                #       #         #
                        if r:                                                #       #         #
                            self.left = s.cursor  ##                         #       #         #
                            r = True              ## [                       # goto  #         #
                            if r:                                            #       #         #
                                r = s.starts_with(u'y')  # character check   #       #         #
                                if r:                                        #       # repeat  #
                                    self.right = s.cursor  ##                #       #         # do
                                    r = True               ## ]              #       #         #
                        if r or s.cursor == s.limit:                         #       #         #
                            s.cursor = var38                                 #       #         #
                            break                                            #       #         #
                        s.cursor = var38 + 1                                 ##      #         #
                    if r:                                                            #         #
                        r = s.set_range(self.left, self.right, u'Y')  # <-           #         #
                        if r:                                                        #         #
                            self.b_Y_found = True  ##                                #         #
                            r = True               ## set                            #         #
                    if not r:                                                        #         #
                        s.cursor = var39                                             #         #
                        break                                                        #         #
                r = True                                                             ##        #
                s.cursor = var40                                                               #
                r = True                                                                       ##
                if r:
                    self.i_p1 = s.limit
                    r = True
                    if r:
                        self.i_p2 = s.limit
                        r = True
                        if r:
                            var41 = s.cursor                                                                                ##
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
                            s.cursor = var41                                                                                #
                            r = True                                                                                        ##
                            if r:
                                var50 = s.cursor                                                         ##
                                var51 = len(s) - s.limit                                                 #
                                s.direction *= -1                                                        #
                                s.cursor, s.limit = s.limit, s.cursor                                    #
                                var42 = len(s) - s.cursor              ##                                #
                                r = self.r_Step_1a(s)  # routine call  #                                 #
                                s.cursor = len(s) - var42              # do                              #
                                r = True                               ##                                #
                                if r:                                                                    #
                                    var43 = len(s) - s.cursor              ##                            #
                                    r = self.r_Step_1b(s)  # routine call  #                             #
                                    s.cursor = len(s) - var43              # do                          #
                                    r = True                               ##                            #
                                    if r:                                                                #
                                        var44 = len(s) - s.cursor              ##                        #
                                        r = self.r_Step_1c(s)  # routine call  #                         #
                                        s.cursor = len(s) - var44              # do                      #
                                        r = True                               ##                        #
                                        if r:                                                            #
                                            var45 = len(s) - s.cursor             ##                     #
                                            r = self.r_Step_2(s)  # routine call  #                      #
                                            s.cursor = len(s) - var45             # do                   #
                                            r = True                              ##                     #
                                            if r:                                                        # backwards
                                                var46 = len(s) - s.cursor             ##                 #
                                                r = self.r_Step_3(s)  # routine call  #                  #
                                                s.cursor = len(s) - var46             # do               #
                                                r = True                              ##                 #
                                                if r:                                                    #
                                                    var47 = len(s) - s.cursor             ##             #
                                                    r = self.r_Step_4(s)  # routine call  #              #
                                                    s.cursor = len(s) - var47             # do           #
                                                    r = True                              ##             #
                                                    if r:                                                #
                                                        var48 = len(s) - s.cursor              ##        #
                                                        r = self.r_Step_5a(s)  # routine call  #         #
                                                        s.cursor = len(s) - var48              # do      #
                                                        r = True                               ##        #
                                                        if r:                                            #
                                                            var49 = len(s) - s.cursor              ##    #
                                                            r = self.r_Step_5b(s)  # routine call  #     #
                                                            s.cursor = len(s) - var49              # do  #
                                                            r = True                               ##    #
                                s.direction *= -1                                                        #
                                s.cursor = var50                                                         #
                                s.limit = len(s) - var51                                                 ##
                                if r:
                                    var54 = s.cursor                                                              ##
                                    r = self.b_Y_found  # boolean variable check                                  #
                                    if r:                                                                         #
                                        while True:                                                     ##        #
                                            var53 = s.cursor                                            #         #
                                            while True:                                         ##      #         #
                                                var52 = s.cursor                                #       #         #
                                                self.left = s.cursor  ##                        #       #         #
                                                r = True              ## [                      #       #         #
                                                if r:                                           #       #         #
                                                    r = s.starts_with(u'Y')  # character check  #       #         #
                                                    if r:                                       # goto  #         #
                                                        self.right = s.cursor  ##               #       #         #
                                                        r = True               ## ]             #       # repeat  # do
                                                if r or s.cursor == s.limit:                    #       #         #
                                                    s.cursor = var52                            #       #         #
                                                    break                                       #       #         #
                                                s.cursor = var52 + 1                            ##      #         #
                                            if r:                                                       #         #
                                                r = s.set_range(self.left, self.right, u'y')  # <-      #         #
                                            if not r:                                                   #         #
                                                s.cursor = var53                                        #         #
                                                break                                                   #         #
                                        r = True                                                        ##        #
                                    s.cursor = var54                                                              #
                                    r = True                                                                      ##
        return r
