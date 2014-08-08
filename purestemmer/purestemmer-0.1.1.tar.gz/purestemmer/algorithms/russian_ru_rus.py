#!/usr/bin/env python
# vim:fileencoding=utf-8



# This file was auto-generated on 2014-08-05 20:04:18 using
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

_g_v = set(u'\u0430\u0435\u0438\u043e\u0443\u044b\u044d\u044e\u044f')
_a_1 = ((u'\u0438\u0432\u0448\u0438\u0441\u044c', '', 1), (u'\u044b\u0432\u0448\u0438\u0441\u044c', '', 1), (u'\u0432\u0448\u0438\u0441\u044c', '', 0), (u'\u0438\u0432\u0448\u0438', '', 1), (u'\u044b\u0432\u0448\u0438', '', 1), (u'\u0432\u0448\u0438', '', 0), (u'\u0438\u0432', '', 1), (u'\u044b\u0432', '', 1), (u'\u0432', '', 0),)
_a_2 = ((u'\u0438\u043c\u0438', '', 0), (u'\u044b\u043c\u0438', '', 0), (u'\u0435\u0433\u043e', '', 0), (u'\u043e\u0433\u043e', '', 0), (u'\u0435\u043c\u0443', '', 0), (u'\u043e\u043c\u0443', '', 0), (u'\u0435\u0435', '', 0), (u'\u0438\u0435', '', 0), (u'\u044b\u0435', '', 0), (u'\u043e\u0435', '', 0), (u'\u0435\u0439', '', 0), (u'\u0438\u0439', '', 0), (u'\u044b\u0439', '', 0), (u'\u043e\u0439', '', 0), (u'\u0435\u043c', '', 0), (u'\u0438\u043c', '', 0), (u'\u044b\u043c', '', 0), (u'\u043e\u043c', '', 0), (u'\u0438\u0445', '', 0), (u'\u044b\u0445', '', 0), (u'\u0443\u044e', '', 0), (u'\u044e\u044e', '', 0), (u'\u0430\u044f', '', 0), (u'\u044f\u044f', '', 0), (u'\u043e\u044e', '', 0), (u'\u0435\u044e', '', 0),)
_a_3 = ((u'\u0438\u0432\u0448', '', 1), (u'\u044b\u0432\u0448', '', 1), (u'\u0443\u044e\u0449', '', 1), (u'\u0435\u043c', '', 0), (u'\u043d\u043d', '', 0), (u'\u0432\u0448', '', 0), (u'\u044e\u0449', '', 0), (u'\u0449', '', 0),)
_a_4 = ((u'\u0441\u044f', '', 0), (u'\u0441\u044c', '', 0),)
_a_5 = ((u'\u0435\u0439\u0442\u0435', '', 1), (u'\u0443\u0439\u0442\u0435', '', 1), (u'\u0435\u0442\u0435', '', 0), (u'\u0439\u0442\u0435', '', 0), (u'\u0435\u0448\u044c', '', 0), (u'\u043d\u043d\u043e', '', 0), (u'\u0438\u043b\u0430', '', 1), (u'\u044b\u043b\u0430', '', 1), (u'\u0435\u043d\u0430', '', 1), (u'\u0438\u0442\u0435', '', 1), (u'\u0438\u043b\u0438', '', 1), (u'\u044b\u043b\u0438', '', 1), (u'\u0438\u043b\u043e', '', 1), (u'\u044b\u043b\u043e', '', 1), (u'\u0435\u043d\u043e', '', 1), (u'\u0443\u0435\u0442', '', 1), (u'\u0443\u044e\u0442', '', 1), (u'\u0435\u043d\u044b', '', 1), (u'\u0438\u0442\u044c', '', 1), (u'\u044b\u0442\u044c', '', 1), (u'\u0438\u0448\u044c', '', 1), (u'\u043b\u0430', '', 0), (u'\u043d\u0430', '', 0), (u'\u043b\u0438', '', 0), (u'\u0435\u043c', '', 0), (u'\u043b\u043e', '', 0), (u'\u043d\u043e', '', 0), (u'\u0435\u0442', '', 0), (u'\u044e\u0442', '', 0), (u'\u043d\u044b', '', 0), (u'\u0442\u044c', '', 0), (u'\u0435\u0439', '', 1), (u'\u0443\u0439', '', 1), (u'\u0438\u043b', '', 1), (u'\u044b\u043b', '', 1), (u'\u0438\u043c', '', 1), (u'\u044b\u043c', '', 1), (u'\u0435\u043d', '', 1), (u'\u044f\u0442', '', 1), (u'\u0438\u0442', '', 1), (u'\u044b\u0442', '', 1), (u'\u0443\u044e', '', 1), (u'\u0439', '', 0), (u'\u043b', '', 0), (u'\u043d', '', 0), (u'\u044e', '', 1),)
_a_6 = ((u'\u0438\u044f\u043c\u0438', '', 0), (u'\u044f\u043c\u0438', '', 0), (u'\u0430\u043c\u0438', '', 0), (u'\u0438\u0435\u0439', '', 0), (u'\u0438\u044f\u043c', '', 0), (u'\u0438\u0435\u043c', '', 0), (u'\u0438\u044f\u0445', '', 0), (u'\u0435\u0432', '', 0), (u'\u043e\u0432', '', 0), (u'\u0438\u0435', '', 0), (u'\u044c\u0435', '', 0), (u'\u0435\u0438', '', 0), (u'\u0438\u0438', '', 0), (u'\u0435\u0439', '', 0), (u'\u043e\u0439', '', 0), (u'\u0438\u0439', '', 0), (u'\u044f\u043c', '', 0), (u'\u0435\u043c', '', 0), (u'\u0430\u043c', '', 0), (u'\u043e\u043c', '', 0), (u'\u0430\u0445', '', 0), (u'\u044f\u0445', '', 0), (u'\u0438\u044e', '', 0), (u'\u044c\u044e', '', 0), (u'\u0438\u044f', '', 0), (u'\u044c\u044f', '', 0), (u'\u0430', '', 0), (u'\u0435', '', 0), (u'\u0438', '', 0), (u'\u0439', '', 0), (u'\u043e', '', 0), (u'\u0443', '', 0), (u'\u044b', '', 0), (u'\u044c', '', 0), (u'\u044e', '', 0), (u'\u044f', '', 0),)
_a_7 = ((u'\u043e\u0441\u0442\u044c', '', 0), (u'\u043e\u0441\u0442', '', 0),)
_a_8 = ((u'\u0435\u0439\u0448\u0435', '', 0), (u'\u0435\u0439\u0448', '', 0), (u'\u043d', '', 1), (u'\u044c', '', 2),)

class _Program(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.i_pV = 0
        self.i_p2 = 0

    def r_mark_regions(self, s):
        r = True
        self.i_pV = s.limit
        r = True
        if r:
            self.i_p2 = s.limit
            r = True
            if r:
                var0 = s.cursor                                                                                 ##
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
                    self.i_pV = s.cursor  ##                                                                    #
                    r = True              ## setmark                                                            #
                    if r:                                                                                       #
                        while True:                                                           ##                #
                            if s.cursor == s.limit:                ##                         #                 #
                                r = False                          #                          #                 #
                            else:                                  #                          #                 #
                                r = s.chars[s.cursor] not in _g_v  # negative grouping check  #                 #
                            if r:                                  #                          # gopast          #
                                s.cursor += 1                      ##                         #                 #
                            if r or s.cursor == s.limit:                                      #                 #
                                break                                                         #                 #
                            s.cursor += 1                                                     ##                #
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
                s.cursor = var0                                                                                 #
                r = True                                                                                        ##
        return r
    
    def r_R2(self, s):
        r = True
        r = self.i_p2 <= s.cursor  # <=
        return r
    
    def r_perfective_gerund(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_1 = None                                        ##
            r = False                                         #
            var2 = s.cursor                                   #
            for var1, var5, var4 in _a_1:                     #
                if s.starts_with(var1):                       #
                    var3 = s.cursor                           #
                    r = (not var5) or getattr(self, var5)(s)  # substring
                    if r:                                     #
                      s.cursor = var3                         #
                      a_1 = var4                              #
                      break                                   #
                s.cursor = var2                               ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_1 == 0:                                                   ##
                        var6 = len(s) - s.cursor                             ##    #
                        r = s.starts_with(u'\u0430')  # character check      #     #
                        if not r:                                            # or  #
                            s.cursor = len(s) - var6                         #     #
                            r = s.starts_with(u'\u044f')  # character check  ##    # among
                        if r:                                                      #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                    if a_1 == 1:                                                   #
                        r = s.set_range(self.left, self.right, u'')  # delete      ##
        return r
    
    def r_adjective(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_2 = None                                          ##
            r = False                                           #
            var8 = s.cursor                                     #
            for var7, var11, var10 in _a_2:                     #
                if s.starts_with(var7):                         #
                    var9 = s.cursor                             #
                    r = (not var11) or getattr(self, var11)(s)  # substring
                    if r:                                       #
                      s.cursor = var9                           #
                      a_2 = var10                               #
                      break                                     #
                s.cursor = var8                                 ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_2 == 0:                                               ##
                        r = s.set_range(self.left, self.right, u'')  # delete  ## among
        return r
    
    def r_adjectival(self, s):
        r = True
        r = self.r_adjective(s)  # routine call
        if r:
            var18 = len(s) - s.cursor                                                           ##
            self.left = s.cursor  ##                                                            #
            r = True              ## [                                                          #
            if r:                                                                               #
                a_3 = None                                          ##                          #
                r = False                                           #                           #
                var13 = s.cursor                                    #                           #
                for var12, var16, var15 in _a_3:                    #                           #
                    if s.starts_with(var12):                        #                           #
                        var14 = s.cursor                            #                           #
                        r = (not var16) or getattr(self, var16)(s)  # substring                 #
                        if r:                                       #                           #
                          s.cursor = var14                          #                           #
                          a_3 = var15                               #                           #
                          break                                     #                           #
                    s.cursor = var13                                ##                          #
                if r:                                                                           # try
                    self.right = s.cursor  ##                                                   #
                    r = True               ## ]                                                 #
                    if r:                                                                       #
                        if a_3 == 0:                                                   ##       #
                            var17 = len(s) - s.cursor                            ##    #        #
                            r = s.starts_with(u'\u0430')  # character check      #     #        #
                            if not r:                                            # or  #        #
                                s.cursor = len(s) - var17                        #     #        #
                                r = s.starts_with(u'\u044f')  # character check  ##    # among  #
                            if r:                                                      #        #
                                r = s.set_range(self.left, self.right, u'')  # delete  #        #
                        if a_3 == 1:                                                   #        #
                            r = s.set_range(self.left, self.right, u'')  # delete      ##       #
            if not r:                                                                           #
                r = True                                                                        #
                s.cursor = len(s) - var18                                                       ##
        return r
    
    def r_reflexive(self, s):
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
                    if a_4 == 0:                                               ##
                        r = s.set_range(self.left, self.right, u'')  # delete  ## among
        return r
    
    def r_verb(self, s):
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
                    if a_5 == 0:                                                   ##
                        var29 = len(s) - s.cursor                            ##    #
                        r = s.starts_with(u'\u0430')  # character check      #     #
                        if not r:                                            # or  #
                            s.cursor = len(s) - var29                        #     #
                            r = s.starts_with(u'\u044f')  # character check  ##    # among
                        if r:                                                      #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                    if a_5 == 1:                                                   #
                        r = s.set_range(self.left, self.right, u'')  # delete      ##
        return r
    
    def r_noun(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_6 = None                                          ##
            r = False                                           #
            var31 = s.cursor                                    #
            for var30, var34, var33 in _a_6:                    #
                if s.starts_with(var30):                        #
                    var32 = s.cursor                            #
                    r = (not var34) or getattr(self, var34)(s)  # substring
                    if r:                                       #
                      s.cursor = var32                          #
                      a_6 = var33                               #
                      break                                     #
                s.cursor = var31                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_6 == 0:                                               ##
                        r = s.set_range(self.left, self.right, u'')  # delete  ## among
        return r
    
    def r_derivational(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_7 = None                                          ##
            r = False                                           #
            var36 = s.cursor                                    #
            for var35, var39, var38 in _a_7:                    #
                if s.starts_with(var35):                        #
                    var37 = s.cursor                            #
                    r = (not var39) or getattr(self, var39)(s)  # substring
                    if r:                                       #
                      s.cursor = var37                          #
                      a_7 = var38                               #
                      break                                     #
                s.cursor = var36                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = self.r_R2(s)  # routine call
                    if r:
                        if a_7 == 0:                                               ##
                            r = s.set_range(self.left, self.right, u'')  # delete  ## among
        return r
    
    def r_tidy_up(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_8 = None                                          ##
            r = False                                           #
            var41 = s.cursor                                    #
            for var40, var44, var43 in _a_8:                    #
                if s.starts_with(var40):                        #
                    var42 = s.cursor                            #
                    r = (not var44) or getattr(self, var44)(s)  # substring
                    if r:                                       #
                      s.cursor = var42                          #
                      a_8 = var43                               #
                      break                                     #
                s.cursor = var41                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    if a_8 == 0:                                                                   ##
                        r = s.set_range(self.left, self.right, u'')  # delete                      #
                        if r:                                                                      #
                            self.left = s.cursor  ##                                               #
                            r = True              ## [                                             #
                            if r:                                                                  #
                                r = s.starts_with(u'\u043d')  # character check                    #
                                if r:                                                              #
                                    self.right = s.cursor  ##                                      #
                                    r = True               ## ]                                    #
                                    if r:                                                          # among
                                        r = s.starts_with(u'\u043d')  # character check            #
                                        if r:                                                      #
                                            r = s.set_range(self.left, self.right, u'')  # delete  #
                    if a_8 == 1:                                                                   #
                        r = s.starts_with(u'\u043d')  # character check                            #
                        if r:                                                                      #
                            r = s.set_range(self.left, self.right, u'')  # delete                  #
                    if a_8 == 2:                                                                   #
                        r = s.set_range(self.left, self.right, u'')  # delete                      ##
        return r
    
    def r_stem(self, s):
        r = True
        var45 = s.cursor                            ##
        r = self.r_mark_regions(s)  # routine call  #
        s.cursor = var45                            # do
        r = True                                    ##
        if r:
            var56 = s.cursor                                                                              ##
            var57 = len(s) - s.limit                                                                      #
            s.direction *= -1                                                                             #
            s.cursor, s.limit = s.limit, s.cursor                                                         #
            var54 = len(s) - s.cursor                                                         ##          #
            var55 = s.limit                                                                   #           #
            r = s.to_mark(self.i_pV)  # tomark                                                #           #
            if r:                                                                             #           #
                s.limit = s.cursor                                                            #           #
                s.cursor = len(s) - var54                                                     #           #
                var50 = len(s) - s.cursor                                           ##        #           #
                var49 = len(s) - s.cursor                                     ##    #         #           #
                r = self.r_perfective_gerund(s)  # routine call               #     #         #           #
                if not r:                                                     #     #         #           #
                    s.cursor = len(s) - var49                                 #     #         #           #
                    var46 = len(s) - s.cursor                ##               #     #         #           #
                    r = self.r_reflexive(s)  # routine call  #                #     #         #           #
                    if not r:                                # try            #     #         #           #
                        r = True                             #                #     #         #           #
                        s.cursor = len(s) - var46            ##               #     #         #           #
                    if r:                                                     # or  #         #           #
                        var48 = len(s) - s.cursor                       ##    #     # do      #           #
                        var47 = len(s) - s.cursor                 ##    #     #     #         #           #
                        r = self.r_adjectival(s)  # routine call  #     #     #     #         #           #
                        if not r:                                 # or  #     #     #         #           #
                            s.cursor = len(s) - var47             #     # or  #     #         #           #
                            r = self.r_verb(s)  # routine call    ##    #     #     #         #           #
                        if not r:                                       #     #     #         #           #
                            s.cursor = len(s) - var48                   #     #     #         #           #
                            r = self.r_noun(s)  # routine call          ##    ##    #         #           #
                s.cursor = len(s) - var50                                           #         # setlimit  # backwards
                r = True                                                            ##        #           #
                if r:                                                                         #           #
                    var51 = len(s) - s.cursor                                          ##     #           #
                    self.left = s.cursor  ##                                           #      #           #
                    r = True              ## [                                         #      #           #
                    if r:                                                              #      #           #
                        r = s.starts_with(u'\u0438')  # character check                #      #           #
                        if r:                                                          #      #           #
                            self.right = s.cursor  ##                                  # try  #           #
                            r = True               ## ]                                #      #           #
                            if r:                                                      #      #           #
                                r = s.set_range(self.left, self.right, u'')  # delete  #      #           #
                    if not r:                                                          #      #           #
                        r = True                                                       #      #           #
                        s.cursor = len(s) - var51                                      ##     #           #
                    if r:                                                                     #           #
                        var52 = len(s) - s.cursor                   ##                        #           #
                        r = self.r_derivational(s)  # routine call  #                         #           #
                        s.cursor = len(s) - var52                   # do                      #           #
                        r = True                                    ##                        #           #
                        if r:                                                                 #           #
                            var53 = len(s) - s.cursor              ##                         #           #
                            r = self.r_tidy_up(s)  # routine call  #                          #           #
                            s.cursor = len(s) - var53              # do                       #           #
                            r = True                               ##                         #           #
                s.limit = var55                                                               ##          #
            s.direction *= -1                                                                             #
            s.cursor = var56                                                                              #
            s.limit = len(s) - var57                                                                      ##
        return r
