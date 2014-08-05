#!/usr/bin/env python
# vim:fileencoding=utf-8



# This file was auto-generated on 2014-08-05 20:04:09 using
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

_g_v = set(u'aeiouy\xe4\xf6\xfc')
_g_s_ending = set(u'bdfghklmnrt')
_g_st_ending = (_g_s_ending - set(u'r'))
_a_1 = ((u'Y', '', 0), (u'U', '', 1), (u'\xe4', '', 2), (u'\xf6', '', 3), (u'\xfc', '', 4), (u'', '', 5),)
_a_2 = ((u'ern', '', 0), (u'em', '', 0), (u'er', '', 0), (u'en', '', 1), (u'es', '', 1), (u'e', '', 1), (u's', '', 2),)
_a_3 = ((u'est', '', 0), (u'en', '', 0), (u'er', '', 0), (u'st', '', 1),)
_a_4 = ((u'isch', '', 1), (u'lich', '', 2), (u'heit', '', 2), (u'keit', '', 3), (u'end', '', 0), (u'ung', '', 0), (u'ig', '', 1), (u'ik', '', 1),)
_a_5 = ((u'lich', '', 0), (u'ig', '', 0),)

class _Program(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.i_p1 = 0
        self.i_p2 = 0
        self.i_x = 0

    def r_prelude(self, s):
        r = True
        var2 = s.cursor                                                                      ##
        while True:                                                                ##        #
            var1 = s.cursor                                                        #         #
            var0 = s.cursor                                                  ##    #         #
            self.left = s.cursor  ##                                         #     #         #
            r = True              ## [                                       #     #         #
            if r:                                                            #     #         #
                r = s.starts_with(u'\xdf')  # character check                #     #         #
                if r:                                                        #     #         #
                    self.right = s.cursor  ##                                # or  #         #
                    r = True               ## ]                              #     # repeat  # test
                    if r:                                                    #     #         #
                        r = s.set_range(self.left, self.right, u'ss')  # <-  #     #         #
            if not r:                                                        #     #         #
                s.cursor = var0                                              #     #         #
                r = s.hop(1)  # next                                         ##    #         #
            if not r:                                                              #         #
                s.cursor = var1                                                    #         #
                break                                                              #         #
        r = True                                                                   ##        #
        s.cursor = var2                                                                      ##
        if r:
            while True:                                                                                       ##
                var5 = s.cursor                                                                               #
                while True:                                                                           ##      #
                    var4 = s.cursor                                                                   #       #
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
                            var3 = s.cursor                                                     ##    #       #
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
                                s.cursor = var3                                                 #     #       #
                                r = s.starts_with(u'y')  # character check                      #     #       #
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
                                            r = s.set_range(self.left, self.right, u'Y')  # <-  ##    #       #
                    if r or s.cursor == s.limit:                                                      #       #
                        s.cursor = var4                                                               #       #
                        break                                                                         #       #
                    s.cursor = var4 + 1                                                               ##      #
                if not r:                                                                                     #
                    s.cursor = var5                                                                           #
                    break                                                                                     #
            r = True                                                                                          ##
        return r
    
    def r_mark_regions(self, s):
        r = True
        self.i_p1 = s.limit
        r = True
        if r:
            self.i_p2 = s.limit
            r = True
            if r:
                var6 = s.cursor                      ##
                r = s.hop(3)  # hop                  #
                if r:                                #
                    self.i_x = s.cursor  ##          # test
                    r = True             ## setmark  #
                s.cursor = var6                      ##
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
                                var7 = s.cursor                ##
                                r = self.i_p1 < self.i_x  # <  #
                                if r:                          #
                                    self.i_p1 = self.i_x       #
                                    r = True                   # try
                                if not r:                      #
                                    r = True                   #
                                    s.cursor = var7            ##
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
                          break                                     #                    #
                    s.cursor = var9                                 ##                   #
                if r:                                                                    #
                    self.right = s.cursor  ##                                            # repeat
                    r = True               ## ]                                          #
                    if r:                                                                #
                        if a_1 == 0:                                            ##       #
                            r = s.set_range(self.left, self.right, u'y')  # <-  #        #
                        if a_1 == 1:                                            #        #
                            r = s.set_range(self.left, self.right, u'u')  # <-  #        #
                        if a_1 == 2:                                            #        #
                            r = s.set_range(self.left, self.right, u'a')  # <-  #        #
                        if a_1 == 3:                                            # among  #
                            r = s.set_range(self.left, self.right, u'o')  # <-  #        #
                        if a_1 == 4:                                            #        #
                            r = s.set_range(self.left, self.right, u'u')  # <-  #        #
                        if a_1 == 5:                                            #        #
                            r = s.hop(1)  # next                                ##       #
            if not r:                                                                    #
                s.cursor = var13                                                         #
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
    
    def r_standard_suffix(self, s):
        r = True
        var20 = len(s) - s.cursor                                                                                      ##
        self.left = s.cursor  ##                                                                                       #
        r = True              ## [                                                                                     #
        if r:                                                                                                          #
            a_2 = None                                          ##                                                     #
            r = False                                           #                                                      #
            var15 = s.cursor                                    #                                                      #
            for var14, var18, var17 in _a_2:                    #                                                      #
                if s.starts_with(var14):                        #                                                      #
                    var16 = s.cursor                            #                                                      #
                    r = (not var18) or getattr(self, var18)(s)  # substring                                            #
                    if r:                                       #                                                      #
                      s.cursor = var16                          #                                                      #
                      a_2 = var17                               #                                                      #
                      break                                     #                                                      #
                s.cursor = var15                                ##                                                     #
            if r:                                                                                                      #
                self.right = s.cursor  ##                                                                              #
                r = True               ## ]                                                                            #
                if r:                                                                                                  #
                    r = self.r_R1(s)  # routine call                                                                   #
                    if r:                                                                                              #
                        if a_2 == 0:                                                                          ##       #
                            r = s.set_range(self.left, self.right, u'')  # delete                             #        #
                        if a_2 == 1:                                                                          #        #
                            r = s.set_range(self.left, self.right, u'')  # delete                             #        #
                            if r:                                                                             #        # do
                                var19 = len(s) - s.cursor                                              ##     #        #
                                self.left = s.cursor  ##                                               #      #        #
                                r = True              ## [                                             #      #        #
                                if r:                                                                  #      #        #
                                    r = s.starts_with(u's')  # character check                         #      #        #
                                    if r:                                                              #      #        #
                                        self.right = s.cursor  ##                                      #      #        #
                                        r = True               ## ]                                    # try  #        #
                                        if r:                                                          #      #        #
                                            r = s.starts_with(u'nis')  # character check               #      # among  #
                                            if r:                                                      #      #        #
                                                r = s.set_range(self.left, self.right, u'')  # delete  #      #        #
                                if not r:                                                              #      #        #
                                    r = True                                                           #      #        #
                                    s.cursor = len(s) - var19                                          ##     #        #
                        if a_2 == 2:                                                                          #        #
                            if s.cursor == s.limit:                       ##                                  #        #
                                r = False                                 #                                   #        #
                            else:                                         #                                   #        #
                                r = s.chars[s.cursor - 1] in _g_s_ending  # grouping check                    #        #
                            if r:                                         #                                   #        #
                                s.cursor -= 1                             ##                                  #        #
                            if r:                                                                             #        #
                                r = s.set_range(self.left, self.right, u'')  # delete                         ##       #
        s.cursor = len(s) - var20                                                                                      #
        r = True                                                                                                       ##
        if r:
            var26 = len(s) - s.cursor                                                                     ##
            self.left = s.cursor  ##                                                                      #
            r = True              ## [                                                                    #
            if r:                                                                                         #
                a_3 = None                                          ##                                    #
                r = False                                           #                                     #
                var22 = s.cursor                                    #                                     #
                for var21, var25, var24 in _a_3:                    #                                     #
                    if s.starts_with(var21):                        #                                     #
                        var23 = s.cursor                            #                                     #
                        r = (not var25) or getattr(self, var25)(s)  # substring                           #
                        if r:                                       #                                     #
                          s.cursor = var23                          #                                     #
                          a_3 = var24                               #                                     #
                          break                                     #                                     #
                    s.cursor = var22                                ##                                    #
                if r:                                                                                     #
                    self.right = s.cursor  ##                                                             #
                    r = True               ## ]                                                           # do
                    if r:                                                                                 #
                        r = self.r_R1(s)  # routine call                                                  #
                        if r:                                                                             #
                            if a_3 == 0:                                                         ##       #
                                r = s.set_range(self.left, self.right, u'')  # delete            #        #
                            if a_3 == 1:                                                         #        #
                                if s.cursor == s.limit:                        ##                #        #
                                    r = False                                  #                 #        #
                                else:                                          #                 #        #
                                    r = s.chars[s.cursor - 1] in _g_st_ending  # grouping check  # among  #
                                if r:                                          #                 #        #
                                    s.cursor -= 1                              ##                #        #
                                if r:                                                            #        #
                                    r = s.hop(3)  # hop                                          #        #
                                    if r:                                                        #        #
                                        r = s.set_range(self.left, self.right, u'')  # delete    ##       #
            s.cursor = len(s) - var26                                                                     #
            r = True                                                                                      ##
            if r:
                var43 = len(s) - s.cursor                                                                                                    ##
                self.left = s.cursor  ##                                                                                                     #
                r = True              ## [                                                                                                   #
                if r:                                                                                                                        #
                    a_4 = None                                          ##                                                                   #
                    r = False                                           #                                                                    #
                    var28 = s.cursor                                    #                                                                    #
                    for var27, var31, var30 in _a_4:                    #                                                                    #
                        if s.starts_with(var27):                        #                                                                    #
                            var29 = s.cursor                            #                                                                    #
                            r = (not var31) or getattr(self, var31)(s)  # substring                                                          #
                            if r:                                       #                                                                    #
                              s.cursor = var29                          #                                                                    #
                              a_4 = var30                               #                                                                    #
                              break                                     #                                                                    #
                        s.cursor = var28                                ##                                                                   #
                    if r:                                                                                                                    #
                        self.right = s.cursor  ##                                                                                            #
                        r = True               ## ]                                                                                          #
                        if r:                                                                                                                #
                            r = self.r_R2(s)  # routine call                                                                                 #
                            if r:                                                                                                            #
                                if a_4 == 0:                                                                                        ##       #
                                    r = s.set_range(self.left, self.right, u'')  # delete                                           #        #
                                    if r:                                                                                           #        #
                                        var33 = len(s) - s.cursor                                                  ##               #        #
                                        self.left = s.cursor  ##                                                   #                #        #
                                        r = True              ## [                                                 #                #        #
                                        if r:                                                                      #                #        #
                                            r = s.starts_with(u'ig')  # character check                            #                #        #
                                            if r:                                                                  #                #        #
                                                self.right = s.cursor  ##                                          #                #        #
                                                r = True               ## ]                                        #                #        #
                                                if r:                                                              #                #        #
                                                    var32 = len(s) - s.cursor                   ##                 #                #        #
                                                    r = s.starts_with(u'e')  # character check  #                  # try            #        #
                                                    if not r:                                   # not              #                #        #
                                                        s.cursor = len(s) - var32               #                  #                #        #
                                                    r = not r                                   ##                 #                #        #
                                                    if r:                                                          #                #        #
                                                        r = self.r_R2(s)  # routine call                           #                #        #
                                                        if r:                                                      #                #        #
                                                            r = s.set_range(self.left, self.right, u'')  # delete  #                #        #
                                        if not r:                                                                  #                #        #
                                            r = True                                                               #                #        #
                                            s.cursor = len(s) - var33                                              ##               #        #
                                if a_4 == 1:                                                                                        #        #
                                    var34 = len(s) - s.cursor                   ##                                                  #        #
                                    r = s.starts_with(u'e')  # character check  #                                                   #        #
                                    if not r:                                   # not                                               #        #
                                        s.cursor = len(s) - var34               #                                                   #        #
                                    r = not r                                   ##                                                  #        #
                                    if r:                                                                                           #        #
                                        r = s.set_range(self.left, self.right, u'')  # delete                                       #        #
                                if a_4 == 2:                                                                                        #        # do
                                    r = s.set_range(self.left, self.right, u'')  # delete                                           #        #
                                    if r:                                                                                           #        #
                                        var36 = len(s) - s.cursor                                              ##                   #        #
                                        self.left = s.cursor  ##                                               #                    #        #
                                        r = True              ## [                                             #                    #        #
                                        if r:                                                                  #                    #        #
                                            var35 = len(s) - s.cursor                        ##                #                    #        #
                                            r = s.starts_with(u'er')  # character check      #                 #                    #        #
                                            if not r:                                        # or              #                    #        #
                                                s.cursor = len(s) - var35                    #                 #                    # among  #
                                                r = s.starts_with(u'en')  # character check  ##                #                    #        #
                                            if r:                                                              # try                #        #
                                                self.right = s.cursor  ##                                      #                    #        #
                                                r = True               ## ]                                    #                    #        #
                                                if r:                                                          #                    #        #
                                                    r = self.r_R1(s)  # routine call                           #                    #        #
                                                    if r:                                                      #                    #        #
                                                        r = s.set_range(self.left, self.right, u'')  # delete  #                    #        #
                                        if not r:                                                              #                    #        #
                                            r = True                                                           #                    #        #
                                            s.cursor = len(s) - var36                                          ##                   #        #
                                if a_4 == 3:                                                                                        #        #
                                    r = s.set_range(self.left, self.right, u'')  # delete                                           #        #
                                    if r:                                                                                           #        #
                                        var42 = len(s) - s.cursor                                                            ##     #        #
                                        self.left = s.cursor  ##                                                             #      #        #
                                        r = True              ## [                                                           #      #        #
                                        if r:                                                                                #      #        #
                                            a_5 = None                                          ##                           #      #        #
                                            r = False                                           #                            #      #        #
                                            var38 = s.cursor                                    #                            #      #        #
                                            for var37, var41, var40 in _a_5:                    #                            #      #        #
                                                if s.starts_with(var37):                        #                            #      #        #
                                                    var39 = s.cursor                            #                            #      #        #
                                                    r = (not var41) or getattr(self, var41)(s)  # substring                  #      #        #
                                                    if r:                                       #                            #      #        #
                                                      s.cursor = var39                          #                            #      #        #
                                                      a_5 = var40                               #                            # try  #        #
                                                      break                                     #                            #      #        #
                                                s.cursor = var38                                ##                           #      #        #
                                            if r:                                                                            #      #        #
                                                self.right = s.cursor  ##                                                    #      #        #
                                                r = True               ## ]                                                  #      #        #
                                                if r:                                                                        #      #        #
                                                    r = self.r_R2(s)  # routine call                                         #      #        #
                                                    if r:                                                                    #      #        #
                                                        if a_5 == 0:                                               ##        #      #        #
                                                            r = s.set_range(self.left, self.right, u'')  # delete  ## among  #      #        #
                                        if not r:                                                                            #      #        #
                                            r = True                                                                         #      #        #
                                            s.cursor = len(s) - var42                                                        ##     ##       #
                s.cursor = len(s) - var43                                                                                                    #
                r = True                                                                                                                     ##
        return r
    
    def r_stem(self, s):
        r = True
        var44 = s.cursor                       ##
        r = self.r_prelude(s)  # routine call  #
        s.cursor = var44                       # do
        r = True                               ##
        if r:
            var45 = s.cursor                            ##
            r = self.r_mark_regions(s)  # routine call  #
            s.cursor = var45                            # do
            r = True                                    ##
            if r:
                var47 = s.cursor                                     ##
                var48 = len(s) - s.limit                             #
                s.direction *= -1                                    #
                s.cursor, s.limit = s.limit, s.cursor                #
                var46 = len(s) - s.cursor                      ##    #
                r = self.r_standard_suffix(s)  # routine call  #     # backwards
                s.cursor = len(s) - var46                      # do  #
                r = True                                       ##    #
                s.direction *= -1                                    #
                s.cursor = var47                                     #
                s.limit = len(s) - var48                             ##
                if r:
                    var49 = s.cursor                        ##
                    r = self.r_postlude(s)  # routine call  #
                    s.cursor = var49                        # do
                    r = True                                ##
        return r
