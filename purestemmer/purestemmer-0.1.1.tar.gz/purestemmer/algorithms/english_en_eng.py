#!/usr/bin/env python
# vim:fileencoding=utf-8



# This file was auto-generated on 2014-08-05 20:04:02 using
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
_g_valid_LI = set(u'cdeghkmnrt')
_a_1 = ((u'commun', '', 0), (u'gener', '', 0), (u'arsen', '', 0),)
_a_2 = ((u"'s'", '', 0), (u"'s", '', 0), (u"'", '', 0),)
_a_3 = ((u'sses', '', 0), (u'ied', '', 1), (u'ies', '', 1), (u'us', '', 3), (u'ss', '', 3), (u's', '', 2),)
_a_4 = ((u'eedly', '', 0), (u'ingly', '', 1), (u'edly', '', 1), (u'eed', '', 0), (u'ing', '', 1), (u'ed', '', 1),)
_a_5 = ((u'at', '', 0), (u'bl', '', 0), (u'iz', '', 0), (u'bb', '', 1), (u'dd', '', 1), (u'ff', '', 1), (u'gg', '', 1), (u'mm', '', 1), (u'nn', '', 1), (u'pp', '', 1), (u'rr', '', 1), (u'tt', '', 1), (u'', '', 2),)
_a_6 = ((u'ization', '', 5), (u'ational', '', 6), (u'fulness', '', 8), (u'ousness', '', 9), (u'iveness', '', 10), (u'tional', '', 0), (u'biliti', '', 11), (u'lessli', '', 14), (u'entli', '', 4), (u'ation', '', 6), (u'alism', '', 7), (u'aliti', '', 7), (u'ousli', '', 9), (u'iviti', '', 10), (u'fulli', '', 13), (u'enci', '', 1), (u'anci', '', 2), (u'abli', '', 3), (u'izer', '', 5), (u'ator', '', 6), (u'alli', '', 7), (u'bli', '', 11), (u'ogi', '', 12), (u'li', '', 15),)
_a_7 = ((u'ational', '', 1), (u'tional', '', 0), (u'alize', '', 2), (u'icate', '', 3), (u'iciti', '', 3), (u'ative', '', 5), (u'ical', '', 3), (u'ness', '', 4), (u'ful', '', 4),)
_a_8 = ((u'ement', '', 0), (u'ance', '', 0), (u'ence', '', 0), (u'able', '', 0), (u'ible', '', 0), (u'ment', '', 0), (u'ant', '', 0), (u'ent', '', 0), (u'ism', '', 0), (u'ate', '', 0), (u'iti', '', 0), (u'ous', '', 0), (u'ive', '', 0), (u'ize', '', 0), (u'ion', '', 1), (u'al', '', 0), (u'er', '', 0), (u'ic', '', 0),)
_a_9 = ((u'e', '', 0), (u'l', '', 1),)
_a_10 = ((u'canning', '', 0), (u'herring', '', 0), (u'earring', '', 0), (u'proceed', '', 0), (u'succeed', '', 0), (u'inning', '', 0), (u'outing', '', 0), (u'exceed', '', 0),)
_a_11 = ((u'gently', '', 6), (u'singly', '', 10), (u'cosmos', '', 11), (u'skies', '', 1), (u'dying', '', 2), (u'lying', '', 3), (u'tying', '', 4), (u'early', '', 8), (u'atlas', '', 11), (u'andes', '', 11), (u'skis', '', 0), (u'idly', '', 5), (u'ugly', '', 7), (u'only', '', 9), (u'news', '', 11), (u'howe', '', 11), (u'bias', '', 11), (u'sky', '', 11),)

class _Program(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.i_p1 = 0
        self.i_p2 = 0
        self.b_Y_found = True

    def r_prelude(self, s):
        r = True
        self.b_Y_found = False  ##
        r = True                ## unset
        if r:
            var0 = s.cursor                                                    ##
            self.left = s.cursor  ##                                           #
            r = True              ## [                                         #
            if r:                                                              #
                r = s.starts_with(u"'")  # character check                     #
                if r:                                                          #
                    self.right = s.cursor  ##                                  # do
                    r = True               ## ]                                #
                    if r:                                                      #
                        r = s.set_range(self.left, self.right, u'')  # delete  #
            s.cursor = var0                                                    #
            r = True                                                           ##
            if r:
                var1 = s.cursor                                                 ##
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
                s.cursor = var1                                                 #
                r = True                                                        ##
                if r:
                    var4 = s.cursor                                                                ##
                    while True:                                                          ##        #
                        var3 = s.cursor                                                  #         #
                        while True:                                              ##      #         #
                            var2 = s.cursor                                      #       #         #
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
                                s.cursor = var2                                  #       #         #
                                break                                            #       #         #
                            s.cursor = var2 + 1                                  ##      #         #
                        if r:                                                            #         #
                            r = s.set_range(self.left, self.right, u'Y')  # <-           #         #
                            if r:                                                        #         #
                                self.b_Y_found = True  ##                                #         #
                                r = True               ## set                            #         #
                        if not r:                                                        #         #
                            s.cursor = var3                                              #         #
                            break                                                        #         #
                    r = True                                                             ##        #
                    s.cursor = var4                                                                #
                    r = True                                                                       ##
        return r
    
    def r_mark_regions(self, s):
        r = True
        self.i_p1 = s.limit
        r = True
        if r:
            self.i_p2 = s.limit
            r = True
            if r:
                var11 = s.cursor                                                                              ##
                var10 = s.cursor                                                                        ##    #
                a_1 = None                                        ##                                    #     #
                r = False                                         #                                     #     #
                var6 = s.cursor                                   #                                     #     #
                for var5, var9, var8 in _a_1:                     #                                     #     #
                    if s.starts_with(var5):                       #                                     #     #
                        var7 = s.cursor                           #                                     #     #
                        r = (not var9) or getattr(self, var9)(s)  #                                     #     #
                        if r:                                     # among                               #     #
                          s.cursor = var7                         #                                     #     #
                          a_1 = var8                              #                                     #     #
                          break                                   #                                     #     #
                    s.cursor = var6                               #                                     #     #
                if r:                                             #                                     #     #
                    if a_1 == 0:                                  #                                     #     #
                        r = True                                  ##                                    #     #
                if not r:                                                                               #     #
                    s.cursor = var10                                                                    #     #
                    while True:                                              ##                         #     #
                        if s.cursor == s.limit:            ##                #                          # or  #
                            r = False                      #                 #                          #     #
                        else:                              #                 #                          #     #
                            r = s.chars[s.cursor] in _g_v  # grouping check  #                          #     #
                        if r:                              #                 # gopast                   #     #
                            s.cursor += 1                  ##                #                          #     #
                        if r or s.cursor == s.limit:                         #                          #     #
                            break                                            #                          #     #
                        s.cursor += 1                                        ##                         #     #
                    if r:                                                                               #     #
                        while True:                                                           ##        #     #
                            if s.cursor == s.limit:                ##                         #         #     #
                                r = False                          #                          #         #     #
                            else:                                  #                          #         #     #
                                r = s.chars[s.cursor] not in _g_v  # negative grouping check  #         #     #
                            if r:                                  #                          # gopast  #     # do
                                s.cursor += 1                      ##                         #         #     #
                            if r or s.cursor == s.limit:                                      #         #     #
                                break                                                         #         #     #
                            s.cursor += 1                                                     ##        ##    #
                if r:                                                                                         #
                    self.i_p1 = s.cursor  ##                                                                  #
                    r = True              ## setmark                                                          #
                    if r:                                                                                     #
                        while True:                                              ##                           #
                            if s.cursor == s.limit:            ##                #                            #
                                r = False                      #                 #                            #
                            else:                              #                 #                            #
                                r = s.chars[s.cursor] in _g_v  # grouping check  #                            #
                            if r:                              #                 # gopast                     #
                                s.cursor += 1                  ##                #                            #
                            if r or s.cursor == s.limit:                         #                            #
                                break                                            #                            #
                            s.cursor += 1                                        ##                           #
                        if r:                                                                                 #
                            while True:                                                           ##          #
                                if s.cursor == s.limit:                ##                         #           #
                                    r = False                          #                          #           #
                                else:                                  #                          #           #
                                    r = s.chars[s.cursor] not in _g_v  # negative grouping check  #           #
                                if r:                                  #                          # gopast    #
                                    s.cursor += 1                      ##                         #           #
                                if r or s.cursor == s.limit:                                      #           #
                                    break                                                         #           #
                                s.cursor += 1                                                     ##          #
                            if r:                                                                             #
                                self.i_p2 = s.cursor  ##                                                      #
                                r = True              ## setmark                                              #
                s.cursor = var11                                                                              #
                r = True                                                                                      ##
        return r
    
    def r_shortv(self, s):
        r = True
        var12 = len(s) - s.cursor                                                     ##
        if s.cursor == s.limit:                        ##                             #
            r = False                                  #                              #
        else:                                          #                              #
            r = s.chars[s.cursor - 1] not in _g_v_WXY  # negative grouping check      #
        if r:                                          #                              #
            s.cursor -= 1                              ##                             #
        if r:                                                                         #
            if s.cursor == s.limit:                ##                                 #
                r = False                          #                                  #
            else:                                  #                                  #
                r = s.chars[s.cursor - 1] in _g_v  # grouping check                   #
            if r:                                  #                                  #
                s.cursor -= 1                      ##                                 #
            if r:                                                                     #
                if s.cursor == s.limit:                    ##                         #
                    r = False                              #                          #
                else:                                      #                          #
                    r = s.chars[s.cursor - 1] not in _g_v  # negative grouping check  #
                if r:                                      #                          # or
                    s.cursor -= 1                          ##                         #
        if not r:                                                                     #
            s.cursor = len(s) - var12                                                 #
            if s.cursor == s.limit:                    ##                             #
                r = False                              #                              #
            else:                                      #                              #
                r = s.chars[s.cursor - 1] not in _g_v  # negative grouping check      #
            if r:                                      #                              #
                s.cursor -= 1                          ##                             #
            if r:                                                                     #
                if s.cursor == s.limit:                ##                             #
                    r = False                          #                              #
                else:                                  #                              #
                    r = s.chars[s.cursor - 1] in _g_v  # grouping check               #
                if r:                                  #                              #
                    s.cursor -= 1                      ##                             #
                if r:                                                                 #
                    r = (s.cursor == s.limit)  # atlimit                              ##
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
        var18 = len(s) - s.cursor                                                        ##
        self.left = s.cursor  ##                                                         #
        r = True              ## [                                                       #
        if r:                                                                            #
            a_2 = None                                          ##                       #
            r = False                                           #                        #
            var14 = s.cursor                                    #                        #
            for var13, var17, var16 in _a_2:                    #                        #
                if s.starts_with(var13):                        #                        #
                    var15 = s.cursor                            #                        #
                    r = (not var17) or getattr(self, var17)(s)  # substring              #
                    if r:                                       #                        #
                      s.cursor = var15                          #                        # try
                      a_2 = var16                               #                        #
                      break                                     #                        #
                s.cursor = var14                                ##                       #
            if r:                                                                        #
                self.right = s.cursor  ##                                                #
                r = True               ## ]                                              #
                if r:                                                                    #
                    if a_2 == 0:                                               ##        #
                        r = s.set_range(self.left, self.right, u'')  # delete  ## among  #
        if not r:                                                                        #
            r = True                                                                     #
            s.cursor = len(s) - var18                                                    ##
        if r:
            self.left = s.cursor  ##
            r = True              ## [
            if r:
                a_3 = None                                          ##
                r = False                                           #
                var20 = s.cursor                                    #
                for var19, var23, var22 in _a_3:                    #
                    if s.starts_with(var19):                        #
                        var21 = s.cursor                            #
                        r = (not var23) or getattr(self, var23)(s)  # substring
                        if r:                                       #
                          s.cursor = var21                          #
                          a_3 = var22                               #
                          break                                     #
                    s.cursor = var20                                ##
                if r:
                    self.right = s.cursor  ##
                    r = True               ## ]
                    if r:
                        if a_3 == 0:                                                                   ##
                            r = s.set_range(self.left, self.right, u'ss')  # <-                        #
                        if a_3 == 1:                                                                   #
                            var24 = len(s) - s.cursor                                ##                #
                            r = s.hop(2)  # hop                                      #                 #
                            if r:                                                    #                 #
                                r = s.set_range(self.left, self.right, u'i')  # <-   # or              #
                            if not r:                                                #                 #
                                s.cursor = len(s) - var24                            #                 #
                                r = s.set_range(self.left, self.right, u'ie')  # <-  ##                #
                        if a_3 == 2:                                                                   #
                            r = s.hop(1)  # next                                                       #
                            if r:                                                                      #
                                while True:                                                  ##        # among
                                    if s.cursor == s.limit:                ##                #         #
                                        r = False                          #                 #         #
                                    else:                                  #                 #         #
                                        r = s.chars[s.cursor - 1] in _g_v  # grouping check  #         #
                                    if r:                                  #                 # gopast  #
                                        s.cursor -= 1                      ##                #         #
                                    if r or s.cursor == s.limit:                             #         #
                                        break                                                #         #
                                    s.cursor -= 1                                            ##        #
                                if r:                                                                  #
                                    r = s.set_range(self.left, self.right, u'')  # delete              #
                        if a_3 == 3:                                                                   #
                            r = True                                                                   ##
        return r
    
    def r_Step_1b(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_4 = None                                          ##
            r = False                                           #
            var26 = s.cursor                                    #
            for var25, var29, var28 in _a_4:                    #
                if s.starts_with(var25):                        #
                    var27 = s.cursor                            #
                    r = (not var29) or getattr(self, var29)(s)  # substring
                    if r:                                       #
                      s.cursor = var27                          #
                      a_4 = var28                               #
                      break                                     #
                s.cursor = var26                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_4 == 0:                                                                                    ##
                        r = self.r_R1(s)  # routine call                                                            #
                        if r:                                                                                       #
                            r = s.set_range(self.left, self.right, u'ee')  # <-                                     #
                    if a_4 == 1:                                                                                    #
                        var30 = len(s) - s.cursor                                              ##                   #
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
                        s.cursor = len(s) - var30                                              ##                   #
                        if r:                                                                                       #
                            r = s.set_range(self.left, self.right, u'')  # delete                                   #
                            if r:                                                                                   #
                                var36 = len(s) - s.cursor                                        ##                 #
                                a_5 = None                                          ##           #                  #
                                r = False                                           #            #                  #
                                var32 = s.cursor                                    #            #                  #
                                for var31, var35, var34 in _a_5:                    #            #                  #
                                    if s.starts_with(var31):                        #            #                  #
                                        var33 = s.cursor                            #            #                  #
                                        r = (not var35) or getattr(self, var35)(s)  # substring  # test             # among
                                        if r:                                       #            #                  #
                                          s.cursor = var33                          #            #                  #
                                          a_5 = var34                               #            #                  #
                                          break                                     #            #                  #
                                    s.cursor = var32                                ##           #                  #
                                s.cursor = len(s) - var36                                        ##                 #
                                if r:                                                                               #
                                    if a_5 == 0:                                                           ##       #
                                        r = s.insert(u'e')  # insert                                       #        #
                                    if a_5 == 1:                                                           #        #
                                        self.left = s.cursor  ##                                           #        #
                                        r = True              ## [                                         #        #
                                        if r:                                                              #        #
                                            r = s.hop(1)  # next                                           #        #
                                            if r:                                                          #        #
                                                self.right = s.cursor  ##                                  #        #
                                                r = True               ## ]                                #        #
                                                if r:                                                      # among  #
                                                    r = s.set_range(self.left, self.right, u'')  # delete  #        #
                                    if a_5 == 2:                                                           #        #
                                        r = (s.cursor == self.i_p1)  # atmark                              #        #
                                        if r:                                                              #        #
                                            var37 = len(s) - s.cursor             ##                       #        #
                                            r = self.r_shortv(s)  # routine call  # test                   #        #
                                            s.cursor = len(s) - var37             ##                       #        #
                                            if r:                                                          #        #
                                                r = s.insert(u'e')  # insert                               ##       ##
        return r
    
    def r_Step_1c(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            var38 = len(s) - s.cursor                       ##
            r = s.starts_with(u'y')  # character check      #
            if not r:                                       # or
                s.cursor = len(s) - var38                   #
                r = s.starts_with(u'Y')  # character check  ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if s.cursor == s.limit:                    ##
                        r = False                              #
                    else:                                      #
                        r = s.chars[s.cursor - 1] not in _g_v  # negative grouping check
                    if r:                                      #
                        s.cursor -= 1                          ##
                    if r:
                        var39 = len(s) - s.cursor             ##
                        r = (s.cursor == s.limit)  # atlimit  #
                        if not r:                             # not
                            s.cursor = len(s) - var39         #
                        r = not r                             ##
                        if r:
                            r = s.set_range(self.left, self.right, u'i')  # <-
        return r
    
    def r_Step_2(self, s):
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
                    r = self.r_R1(s)  # routine call
                    if r:
                        if a_6 == 0:                                                        ##
                            r = s.set_range(self.left, self.right, u'tion')  # <-           #
                        if a_6 == 1:                                                        #
                            r = s.set_range(self.left, self.right, u'ence')  # <-           #
                        if a_6 == 2:                                                        #
                            r = s.set_range(self.left, self.right, u'ance')  # <-           #
                        if a_6 == 3:                                                        #
                            r = s.set_range(self.left, self.right, u'able')  # <-           #
                        if a_6 == 4:                                                        #
                            r = s.set_range(self.left, self.right, u'ent')  # <-            #
                        if a_6 == 5:                                                        #
                            r = s.set_range(self.left, self.right, u'ize')  # <-            #
                        if a_6 == 6:                                                        #
                            r = s.set_range(self.left, self.right, u'ate')  # <-            #
                        if a_6 == 7:                                                        #
                            r = s.set_range(self.left, self.right, u'al')  # <-             #
                        if a_6 == 8:                                                        #
                            r = s.set_range(self.left, self.right, u'ful')  # <-            #
                        if a_6 == 9:                                                        #
                            r = s.set_range(self.left, self.right, u'ous')  # <-            #
                        if a_6 == 10:                                                       # among
                            r = s.set_range(self.left, self.right, u'ive')  # <-            #
                        if a_6 == 11:                                                       #
                            r = s.set_range(self.left, self.right, u'ble')  # <-            #
                        if a_6 == 12:                                                       #
                            r = s.starts_with(u'l')  # character check                      #
                            if r:                                                           #
                                r = s.set_range(self.left, self.right, u'og')  # <-         #
                        if a_6 == 13:                                                       #
                            r = s.set_range(self.left, self.right, u'ful')  # <-            #
                        if a_6 == 14:                                                       #
                            r = s.set_range(self.left, self.right, u'less')  # <-           #
                        if a_6 == 15:                                                       #
                            if s.cursor == s.limit:                       ##                #
                                r = False                                 #                 #
                            else:                                         #                 #
                                r = s.chars[s.cursor - 1] in _g_valid_LI  # grouping check  #
                            if r:                                         #                 #
                                s.cursor -= 1                             ##                #
                            if r:                                                           #
                                r = s.set_range(self.left, self.right, u'')  # delete       ##
        return r
    
    def r_Step_3(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_7 = None                                          ##
            r = False                                           #
            var46 = s.cursor                                    #
            for var45, var49, var48 in _a_7:                    #
                if s.starts_with(var45):                        #
                    var47 = s.cursor                            #
                    r = (not var49) or getattr(self, var49)(s)  # substring
                    if r:                                       #
                      s.cursor = var47                          #
                      a_7 = var48                               #
                      break                                     #
                s.cursor = var46                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = self.r_R1(s)  # routine call
                    if r:
                        if a_7 == 0:                                                   ##
                            r = s.set_range(self.left, self.right, u'tion')  # <-      #
                        if a_7 == 1:                                                   #
                            r = s.set_range(self.left, self.right, u'ate')  # <-       #
                        if a_7 == 2:                                                   #
                            r = s.set_range(self.left, self.right, u'al')  # <-        #
                        if a_7 == 3:                                                   #
                            r = s.set_range(self.left, self.right, u'ic')  # <-        # among
                        if a_7 == 4:                                                   #
                            r = s.set_range(self.left, self.right, u'')  # delete      #
                        if a_7 == 5:                                                   #
                            r = self.r_R2(s)  # routine call                           #
                            if r:                                                      #
                                r = s.set_range(self.left, self.right, u'')  # delete  ##
        return r
    
    def r_Step_4(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_8 = None                                          ##
            r = False                                           #
            var51 = s.cursor                                    #
            for var50, var54, var53 in _a_8:                    #
                if s.starts_with(var50):                        #
                    var52 = s.cursor                            #
                    r = (not var54) or getattr(self, var54)(s)  # substring
                    if r:                                       #
                      s.cursor = var52                          #
                      a_8 = var53                               #
                      break                                     #
                s.cursor = var51                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = self.r_R2(s)  # routine call
                    if r:
                        if a_8 == 0:                                                   ##
                            r = s.set_range(self.left, self.right, u'')  # delete      #
                        if a_8 == 1:                                                   #
                            var55 = len(s) - s.cursor                       ##         #
                            r = s.starts_with(u's')  # character check      #          #
                            if not r:                                       # or       # among
                                s.cursor = len(s) - var55                   #          #
                                r = s.starts_with(u't')  # character check  ##         #
                            if r:                                                      #
                                r = s.set_range(self.left, self.right, u'')  # delete  ##
        return r
    
    def r_Step_5(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_9 = None                                          ##
            r = False                                           #
            var57 = s.cursor                                    #
            for var56, var60, var59 in _a_9:                    #
                if s.starts_with(var56):                        #
                    var58 = s.cursor                            #
                    r = (not var60) or getattr(self, var60)(s)  # substring
                    if r:                                       #
                      s.cursor = var58                          #
                      a_9 = var59                               #
                      break                                     #
                s.cursor = var57                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_9 == 0:                                                       ##
                        var62 = len(s) - s.cursor                            ##        #
                        r = self.r_R2(s)  # routine call                     #         #
                        if not r:                                            #         #
                            s.cursor = len(s) - var62                        #         #
                            r = self.r_R1(s)  # routine call                 #         #
                            if r:                                            # or      #
                                var61 = len(s) - s.cursor             ##     #         #
                                r = self.r_shortv(s)  # routine call  #      #         #
                                if not r:                             # not  #         #
                                    s.cursor = len(s) - var61         #      #         # among
                                r = not r                             ##     ##        #
                        if r:                                                          #
                            r = s.set_range(self.left, self.right, u'')  # delete      #
                    if a_9 == 1:                                                       #
                        r = self.r_R2(s)  # routine call                               #
                        if r:                                                          #
                            r = s.starts_with(u'l')  # character check                 #
                            if r:                                                      #
                                r = s.set_range(self.left, self.right, u'')  # delete  ##
        return r
    
    def r_exception2(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_10 = None                                         ##
            r = False                                           #
            var64 = s.cursor                                    #
            for var63, var67, var66 in _a_10:                   #
                if s.starts_with(var63):                        #
                    var65 = s.cursor                            #
                    r = (not var67) or getattr(self, var67)(s)  # substring
                    if r:                                       #
                      s.cursor = var65                          #
                      a_10 = var66                              #
                      break                                     #
                s.cursor = var64                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = (s.cursor == s.limit)  # atlimit
                    if r:
                        if a_10 == 0:  ##
                            r = True   ## among
        return r
    
    def r_exception1(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_11 = None                                         ##
            r = False                                           #
            var69 = s.cursor                                    #
            for var68, var72, var71 in _a_11:                   #
                if s.starts_with(var68):                        #
                    var70 = s.cursor                            #
                    r = (not var72) or getattr(self, var72)(s)  # substring
                    if r:                                       #
                      s.cursor = var70                          #
                      a_11 = var71                              #
                      break                                     #
                s.cursor = var69                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = (s.cursor == s.limit)  # atlimit
                    if r:
                        if a_11 == 0:                                               ##
                            r = s.set_range(self.left, self.right, u'ski')  # <-    #
                        if a_11 == 1:                                               #
                            r = s.set_range(self.left, self.right, u'sky')  # <-    #
                        if a_11 == 2:                                               #
                            r = s.set_range(self.left, self.right, u'die')  # <-    #
                        if a_11 == 3:                                               #
                            r = s.set_range(self.left, self.right, u'lie')  # <-    #
                        if a_11 == 4:                                               #
                            r = s.set_range(self.left, self.right, u'tie')  # <-    #
                        if a_11 == 5:                                               #
                            r = s.set_range(self.left, self.right, u'idl')  # <-    #
                        if a_11 == 6:                                               # among
                            r = s.set_range(self.left, self.right, u'gentl')  # <-  #
                        if a_11 == 7:                                               #
                            r = s.set_range(self.left, self.right, u'ugli')  # <-   #
                        if a_11 == 8:                                               #
                            r = s.set_range(self.left, self.right, u'earli')  # <-  #
                        if a_11 == 9:                                               #
                            r = s.set_range(self.left, self.right, u'onli')  # <-   #
                        if a_11 == 10:                                              #
                            r = s.set_range(self.left, self.right, u'singl')  # <-  #
                        if a_11 == 11:                                              #
                            r = True                                                ##
        return r
    
    def r_postlude(self, s):
        r = True
        r = self.b_Y_found  # boolean variable check
        if r:
            while True:                                                     ##
                var74 = s.cursor                                            #
                while True:                                         ##      #
                    var73 = s.cursor                                #       #
                    self.left = s.cursor  ##                        #       #
                    r = True              ## [                      #       #
                    if r:                                           #       #
                        r = s.starts_with(u'Y')  # character check  #       #
                        if r:                                       # goto  #
                            self.right = s.cursor  ##               #       #
                            r = True               ## ]             #       # repeat
                    if r or s.cursor == s.limit:                    #       #
                        s.cursor = var73                            #       #
                        break                                       #       #
                    s.cursor = var73 + 1                            ##      #
                if r:                                                       #
                    r = s.set_range(self.left, self.right, u'y')  # <-      #
                if not r:                                                   #
                    s.cursor = var74                                        #
                    break                                                   #
            r = True                                                        ##
        return r
    
    def r_stem(self, s):
        r = True
        var90 = s.cursor                                                                                       ##
        var76 = s.cursor                          ##                                                           #
        r = self.r_exception1(s)  # routine call  #                                                            #
        if not r:                                 #                                                            #
            s.cursor = var76                      #                                                            #
            var75 = s.cursor      ##              # or                                                         #
            r = s.hop(3)  # hop   #               #                                                            #
            if not r:             # not           #                                                            #
                s.cursor = var75  #               #                                                            #
            r = not r             ##              ##                                                           #
        if not r:                                                                                              #
            s.cursor = var90                                                                                   #
            var77 = s.cursor                       ##                                                          #
            r = self.r_prelude(s)  # routine call  #                                                           #
            s.cursor = var77                       # do                                                        #
            r = True                               ##                                                          #
            if r:                                                                                              #
                var78 = s.cursor                            ##                                                 #
                r = self.r_mark_regions(s)  # routine call  #                                                  #
                s.cursor = var78                            # do                                               #
                r = True                                    ##                                                 #
                if r:                                                                                          #
                    var87 = s.cursor                                                              ##           #
                    var88 = len(s) - s.limit                                                      #            #
                    s.direction *= -1                                                             #            #
                    s.cursor, s.limit = s.limit, s.cursor                                         #            #
                    var79 = len(s) - s.cursor              ##                                     #            #
                    r = self.r_Step_1a(s)  # routine call  #                                      #            #
                    s.cursor = len(s) - var79              # do                                   #            #
                    r = True                               ##                                     #            #
                    if r:                                                                         #            #
                        var86 = len(s) - s.cursor                                           ##    #            #
                        r = self.r_exception2(s)  # routine call                            #     #            #
                        if not r:                                                           #     #            #
                            s.cursor = len(s) - var86                                       #     #            #
                            var80 = len(s) - s.cursor              ##                       #     #            #
                            r = self.r_Step_1b(s)  # routine call  #                        #     #            # or
                            s.cursor = len(s) - var80              # do                     #     #            #
                            r = True                               ##                       #     #            #
                            if r:                                                           #     #            #
                                var81 = len(s) - s.cursor              ##                   #     #            #
                                r = self.r_Step_1c(s)  # routine call  #                    #     #            #
                                s.cursor = len(s) - var81              # do                 #     #            #
                                r = True                               ##                   #     #            #
                                if r:                                                       #     # backwards  #
                                    var82 = len(s) - s.cursor             ##                #     #            #
                                    r = self.r_Step_2(s)  # routine call  #                 #     #            #
                                    s.cursor = len(s) - var82             # do              # or  #            #
                                    r = True                              ##                #     #            #
                                    if r:                                                   #     #            #
                                        var83 = len(s) - s.cursor             ##            #     #            #
                                        r = self.r_Step_3(s)  # routine call  #             #     #            #
                                        s.cursor = len(s) - var83             # do          #     #            #
                                        r = True                              ##            #     #            #
                                        if r:                                               #     #            #
                                            var84 = len(s) - s.cursor             ##        #     #            #
                                            r = self.r_Step_4(s)  # routine call  #         #     #            #
                                            s.cursor = len(s) - var84             # do      #     #            #
                                            r = True                              ##        #     #            #
                                            if r:                                           #     #            #
                                                var85 = len(s) - s.cursor             ##    #     #            #
                                                r = self.r_Step_5(s)  # routine call  #     #     #            #
                                                s.cursor = len(s) - var85             # do  #     #            #
                                                r = True                              ##    ##    #            #
                    s.direction *= -1                                                             #            #
                    s.cursor = var87                                                              #            #
                    s.limit = len(s) - var88                                                      ##           #
                    if r:                                                                                      #
                        var89 = s.cursor                        ##                                             #
                        r = self.r_postlude(s)  # routine call  #                                              #
                        s.cursor = var89                        # do                                           #
                        r = True                                ##                                             ##
        return r
