#!/usr/bin/env python
# vim:fileencoding=utf-8



# This file was auto-generated on 2014-08-05 20:04:04 using
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

_g_AEI = set(u'a\xe4ei')
_g_V1 = set(u'aeiouy\xe4\xf6')
_g_V2 = set(u'aeiou\xe4\xf6')
_g_particle_end = (_g_V1 | set(u'nt'))
_a_1 = ((u'kaan', '', 0), (u'k\xe4\xe4n', '', 0), (u'kin', '', 0), (u'han', '', 0), (u'h\xe4n', '', 0), (u'sti', '', 1), (u'ko', '', 0), (u'k\xf6', '', 0), (u'pa', '', 0), (u'p\xe4', '', 0),)
_a_2 = ((u'nsa', '', 2), (u'ns\xe4', '', 2), (u'mme', '', 2), (u'nne', '', 2), (u'si', '', 0), (u'ni', '', 1), (u'an', '', 3), (u'\xe4n', '', 4), (u'en', '', 5),)
_a_3 = ((u'ssa', '', 0), (u'sta', '', 0), (u'lla', '', 0), (u'lta', '', 0), (u'ta', '', 0), (u'na', '', 0),)
_a_4 = ((u'ss\xe4', '', 0), (u'st\xe4', '', 0), (u'll\xe4', '', 0), (u'lt\xe4', '', 0), (u't\xe4', '', 0), (u'n\xe4', '', 0),)
_a_5 = ((u'lle', '', 0), (u'ine', '', 0),)
_a_6 = ((u'aa', '', 0), (u'ee', '', 0), (u'ii', '', 0), (u'oo', '', 0), (u'uu', '', 0), (u'\xe4\xe4', '', 0), (u'\xf6\xf6', '', 0),)
_a_7 = ((u'siin', 'r_VI', 6), (u'seen', 'r_LONG', 6), (u'tten', 'r_VI', 6), (u'han', '', 0), (u'hen', '', 1), (u'hin', '', 2), (u'hon', '', 3), (u'h\xe4n', '', 4), (u'h\xf6n', '', 5), (u'den', 'r_VI', 6), (u'tta', '', 9), (u'tt\xe4', '', 9), (u'ssa', '', 10), (u'ss\xe4', '', 10), (u'sta', '', 10), (u'st\xe4', '', 10), (u'lla', '', 10), (u'll\xe4', '', 10), (u'lta', '', 10), (u'lt\xe4', '', 10), (u'lle', '', 10), (u'ksi', '', 10), (u'ine', '', 10), (u'ta', '', 10), (u't\xe4', '', 10), (u'na', '', 10), (u'n\xe4', '', 10), (u'n', '', 7), (u'a', '', 8), (u'\xe4', '', 8),)
_a_8 = ((u'impi', '', 1), (u'impa', '', 1), (u'imp\xe4', '', 1), (u'immi', '', 1), (u'imma', '', 1), (u'imm\xe4', '', 1), (u'mpi', '', 0), (u'mpa', '', 0), (u'mp\xe4', '', 0), (u'mmi', '', 0), (u'mma', '', 0), (u'mm\xe4', '', 0), (u'eja', '', 1), (u'ej\xe4', '', 1),)
_a_9 = ((u'i', '', 0), (u'j', '', 0),)
_a_10 = ((u'imma', '', 1), (u'mma', '', 0),)

class _Program(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.i_p1 = 0
        self.i_p2 = 0
        self.s_x = _String('')
        self.b_ending_removed = True

    def r_mark_regions(self, s):
        r = True
        self.i_p1 = s.limit
        r = True
        if r:
            self.i_p2 = s.limit
            r = True
            if r:
                while True:                                               ##
                    var0 = s.cursor                                       #
                    if s.cursor == s.limit:             ##                #
                        r = False                       #                 #
                    else:                               #                 #
                        r = s.chars[s.cursor] in _g_V1  # grouping check  #
                    if r:                               #                 # goto
                        s.cursor += 1                   ##                #
                    if r or s.cursor == s.limit:                          #
                        s.cursor = var0                                   #
                        break                                             #
                    s.cursor = var0 + 1                                   ##
                if r:
                    while True:                                                            ##
                        if s.cursor == s.limit:                 ##                         #
                            r = False                           #                          #
                        else:                                   #                          #
                            r = s.chars[s.cursor] not in _g_V1  # negative grouping check  #
                        if r:                                   #                          # gopast
                            s.cursor += 1                       ##                         #
                        if r or s.cursor == s.limit:                                       #
                            break                                                          #
                        s.cursor += 1                                                      ##
                    if r:
                        self.i_p1 = s.cursor  ##
                        r = True              ## setmark
                        if r:
                            while True:                                               ##
                                var1 = s.cursor                                       #
                                if s.cursor == s.limit:             ##                #
                                    r = False                       #                 #
                                else:                               #                 #
                                    r = s.chars[s.cursor] in _g_V1  # grouping check  #
                                if r:                               #                 # goto
                                    s.cursor += 1                   ##                #
                                if r or s.cursor == s.limit:                          #
                                    s.cursor = var1                                   #
                                    break                                             #
                                s.cursor = var1 + 1                                   ##
                            if r:
                                while True:                                                            ##
                                    if s.cursor == s.limit:                 ##                         #
                                        r = False                           #                          #
                                    else:                                   #                          #
                                        r = s.chars[s.cursor] not in _g_V1  # negative grouping check  #
                                    if r:                                   #                          # gopast
                                        s.cursor += 1                       ##                         #
                                    if r or s.cursor == s.limit:                                       #
                                        break                                                          #
                                    s.cursor += 1                                                      ##
                                if r:
                                    self.i_p2 = s.cursor  ##
                                    r = True              ## setmark
        return r
    
    def r_R2(self, s):
        r = True
        r = self.i_p2 <= s.cursor  # <=
        return r
    
    def r_particle_etc(self, s):
        r = True
        var7 = len(s) - s.cursor                                               ##
        var8 = s.limit                                                         #
        r = s.to_mark(self.i_p1)  # tomark                                     #
        if r:                                                                  #
            s.limit = s.cursor                                                 #
            s.cursor = len(s) - var7                                           #
            self.left = s.cursor  ##                                           #
            r = True              ## [                                         #
            if r:                                                              #
                a_1 = None                                        ##           #
                r = False                                         #            #
                var3 = s.cursor                                   #            #
                for var2, var6, var5 in _a_1:                     #            # setlimit
                    if s.starts_with(var2):                       #            #
                        var4 = s.cursor                           #            #
                        r = (not var6) or getattr(self, var6)(s)  # substring  #
                        if r:                                     #            #
                          s.cursor = var4                         #            #
                          a_1 = var5                              #            #
                          break                                   #            #
                    s.cursor = var3                               ##           #
                if r:                                                          #
                    self.right = s.cursor  ##                                  #
                    r = True               ## ]                                #
            s.limit = var8                                                     ##
        if r:
            if a_1 == 0:                                                            ##
                if s.cursor == s.limit:                           ##                #
                    r = False                                     #                 #
                else:                                             #                 #
                    r = s.chars[s.cursor - 1] in _g_particle_end  # grouping check  # among
                if r:                                             #                 #
                    s.cursor -= 1                                 ##                #
            if a_1 == 1:                                                            #
                r = self.r_R2(s)  # routine call                                    ##
            if r:
                r = s.set_range(self.left, self.right, u'')  # delete
        return r
    
    def r_possessive(self, s):
        r = True
        var14 = len(s) - s.cursor                                                ##
        var15 = s.limit                                                          #
        r = s.to_mark(self.i_p1)  # tomark                                       #
        if r:                                                                    #
            s.limit = s.cursor                                                   #
            s.cursor = len(s) - var14                                            #
            self.left = s.cursor  ##                                             #
            r = True              ## [                                           #
            if r:                                                                #
                a_2 = None                                          ##           #
                r = False                                           #            #
                var10 = s.cursor                                    #            #
                for var9, var13, var12 in _a_2:                     #            # setlimit
                    if s.starts_with(var9):                         #            #
                        var11 = s.cursor                            #            #
                        r = (not var13) or getattr(self, var13)(s)  # substring  #
                        if r:                                       #            #
                          s.cursor = var11                          #            #
                          a_2 = var12                               #            #
                          break                                     #            #
                    s.cursor = var10                                ##           #
                if r:                                                            #
                    self.right = s.cursor  ##                                    #
                    r = True               ## ]                                  #
            s.limit = var15                                                      ##
        if r:
            if a_2 == 0:                                                              ##
                var16 = len(s) - s.cursor                   ##                        #
                r = s.starts_with(u'k')  # character check  #                         #
                if not r:                                   # not                     #
                    s.cursor = len(s) - var16               #                         #
                r = not r                                   ##                        #
                if r:                                                                 #
                    r = s.set_range(self.left, self.right, u'')  # delete             #
            if a_2 == 1:                                                              #
                r = s.set_range(self.left, self.right, u'')  # delete                 #
                if r:                                                                 #
                    self.left = s.cursor  ##                                          #
                    r = True              ## [                                        #
                    if r:                                                             #
                        r = s.starts_with(u'kse')  # character check                  #
                        if r:                                                         #
                            self.right = s.cursor  ##                                 #
                            r = True               ## ]                               #
                            if r:                                                     #
                                r = s.set_range(self.left, self.right, u'ksi')  # <-  #
            if a_2 == 2:                                                              #
                r = s.set_range(self.left, self.right, u'')  # delete                 #
            if a_2 == 3:                                                              #
                a_3 = None                                          ##                #
                r = False                                           #                 #
                var18 = s.cursor                                    #                 #
                for var17, var21, var20 in _a_3:                    #                 #
                    if s.starts_with(var17):                        #                 #
                        var19 = s.cursor                            #                 #
                        r = (not var21) or getattr(self, var21)(s)  #                 #
                        if r:                                       # among           #
                          s.cursor = var19                          #                 #
                          a_3 = var20                               #                 #
                          break                                     #                 #
                    s.cursor = var18                                #                 #
                if r:                                               #                 #
                    if a_3 == 0:                                    #                 #
                        r = True                                    ##                #
                if r:                                                                 # among
                    r = s.set_range(self.left, self.right, u'')  # delete             #
            if a_2 == 4:                                                              #
                a_4 = None                                          ##                #
                r = False                                           #                 #
                var23 = s.cursor                                    #                 #
                for var22, var26, var25 in _a_4:                    #                 #
                    if s.starts_with(var22):                        #                 #
                        var24 = s.cursor                            #                 #
                        r = (not var26) or getattr(self, var26)(s)  #                 #
                        if r:                                       # among           #
                          s.cursor = var24                          #                 #
                          a_4 = var25                               #                 #
                          break                                     #                 #
                    s.cursor = var23                                #                 #
                if r:                                               #                 #
                    if a_4 == 0:                                    #                 #
                        r = True                                    ##                #
                if r:                                                                 #
                    r = s.set_range(self.left, self.right, u'')  # delete             #
            if a_2 == 5:                                                              #
                a_5 = None                                          ##                #
                r = False                                           #                 #
                var28 = s.cursor                                    #                 #
                for var27, var31, var30 in _a_5:                    #                 #
                    if s.starts_with(var27):                        #                 #
                        var29 = s.cursor                            #                 #
                        r = (not var31) or getattr(self, var31)(s)  #                 #
                        if r:                                       # among           #
                          s.cursor = var29                          #                 #
                          a_5 = var30                               #                 #
                          break                                     #                 #
                    s.cursor = var28                                #                 #
                if r:                                               #                 #
                    if a_5 == 0:                                    #                 #
                        r = True                                    ##                #
                if r:                                                                 #
                    r = s.set_range(self.left, self.right, u'')  # delete             ##
        return r
    
    def r_LONG(self, s):
        r = True
        a_6 = None                                          ##
        r = False                                           #
        var33 = s.cursor                                    #
        for var32, var36, var35 in _a_6:                    #
            if s.starts_with(var32):                        #
                var34 = s.cursor                            #
                r = (not var36) or getattr(self, var36)(s)  #
                if r:                                       # among
                  s.cursor = var34                          #
                  a_6 = var35                               #
                  break                                     #
            s.cursor = var33                                #
        if r:                                               #
            if a_6 == 0:                                    #
                r = True                                    ##
        return r
    
    def r_VI(self, s):
        r = True
        r = s.starts_with(u'i')  # character check
        if r:
            if s.cursor == s.limit:                 ##
                r = False                           #
            else:                                   #
                r = s.chars[s.cursor - 1] in _g_V2  # grouping check
            if r:                                   #
                s.cursor -= 1                       ##
        return r
    
    def r_case_ending(self, s):
        r = True
        var42 = len(s) - s.cursor                                                ##
        var43 = s.limit                                                          #
        r = s.to_mark(self.i_p1)  # tomark                                       #
        if r:                                                                    #
            s.limit = s.cursor                                                   #
            s.cursor = len(s) - var42                                            #
            self.left = s.cursor  ##                                             #
            r = True              ## [                                           #
            if r:                                                                #
                a_7 = None                                          ##           #
                r = False                                           #            #
                var38 = s.cursor                                    #            #
                for var37, var41, var40 in _a_7:                    #            # setlimit
                    if s.starts_with(var37):                        #            #
                        var39 = s.cursor                            #            #
                        r = (not var41) or getattr(self, var41)(s)  # substring  #
                        if r:                                       #            #
                          s.cursor = var39                          #            #
                          a_7 = var40                               #            #
                          break                                     #            #
                    s.cursor = var38                                ##           #
                if r:                                                            #
                    self.right = s.cursor  ##                                    #
                    r = True               ## ]                                  #
            s.limit = var43                                                      ##
        if r:
            if a_7 == 0:                                                                   ##
                r = s.starts_with(u'a')  # character check                                 #
            if a_7 == 1:                                                                   #
                r = s.starts_with(u'e')  # character check                                 #
            if a_7 == 2:                                                                   #
                r = s.starts_with(u'i')  # character check                                 #
            if a_7 == 3:                                                                   #
                r = s.starts_with(u'o')  # character check                                 #
            if a_7 == 4:                                                                   #
                r = s.starts_with(u'\xe4')  # character check                              #
            if a_7 == 5:                                                                   #
                r = s.starts_with(u'\xf6')  # character check                              #
            if a_7 == 6:                                                                   #
                pass                                                                       #
            if a_7 == 7:                                                                   #
                var46 = len(s) - s.cursor                                     ##           #
                var45 = len(s) - s.cursor                              ##     #            #
                var44 = len(s) - s.cursor                        ##    #      #            #
                r = self.r_LONG(s)  # routine call               #     #      #            #
                if not r:                                        # or  #      #            #
                    s.cursor = len(s) - var44                    #     # and  #            #
                    r = s.starts_with(u'ie')  # character check  ##    #      #            #
                if r:                                                  #      #            #
                    s.cursor = len(s) - var45                          #      # try        #
                    r = s.hop(1)  # next                               ##     #            # among
                if r:                                                         #            #
                    self.right = s.cursor  ##                                 #            #
                    r = True               ## ]                               #            #
                if not r:                                                     #            #
                    r = True                                                  #            #
                    s.cursor = len(s) - var46                                 ##           #
            if a_7 == 8:                                                                   #
                if s.cursor == s.limit:                 ##                                 #
                    r = False                           #                                  #
                else:                                   #                                  #
                    r = s.chars[s.cursor - 1] in _g_V1  # grouping check                   #
                if r:                                   #                                  #
                    s.cursor -= 1                       ##                                 #
                if r:                                                                      #
                    if s.cursor == s.limit:                     ##                         #
                        r = False                               #                          #
                    else:                                       #                          #
                        r = s.chars[s.cursor - 1] not in _g_V1  # negative grouping check  #
                    if r:                                       #                          #
                        s.cursor -= 1                           ##                         #
            if a_7 == 9:                                                                   #
                r = s.starts_with(u'e')  # character check                                 #
            if a_7 == 10:                                                                  #
                r = True                                                                   ##
            if r:
                r = s.set_range(self.left, self.right, u'')  # delete
                if r:
                    self.b_ending_removed = True  ##
                    r = True                      ## set
        return r
    
    def r_other_endings(self, s):
        r = True
        var52 = len(s) - s.cursor                                                ##
        var53 = s.limit                                                          #
        r = s.to_mark(self.i_p2)  # tomark                                       #
        if r:                                                                    #
            s.limit = s.cursor                                                   #
            s.cursor = len(s) - var52                                            #
            self.left = s.cursor  ##                                             #
            r = True              ## [                                           #
            if r:                                                                #
                a_8 = None                                          ##           #
                r = False                                           #            #
                var48 = s.cursor                                    #            #
                for var47, var51, var50 in _a_8:                    #            # setlimit
                    if s.starts_with(var47):                        #            #
                        var49 = s.cursor                            #            #
                        r = (not var51) or getattr(self, var51)(s)  # substring  #
                        if r:                                       #            #
                          s.cursor = var49                          #            #
                          a_8 = var50                               #            #
                          break                                     #            #
                    s.cursor = var48                                ##           #
                if r:                                                            #
                    self.right = s.cursor  ##                                    #
                    r = True               ## ]                                  #
            s.limit = var53                                                      ##
        if r:
            if a_8 == 0:                                            ##
                var54 = len(s) - s.cursor                    ##     #
                r = s.starts_with(u'po')  # character check  #      #
                if not r:                                    # not  #
                    s.cursor = len(s) - var54                #      # among
                r = not r                                    ##     #
            if a_8 == 1:                                            #
                r = True                                            ##
            if r:
                r = s.set_range(self.left, self.right, u'')  # delete
        return r
    
    def r_i_plural(self, s):
        r = True
        var60 = len(s) - s.cursor                                                ##
        var61 = s.limit                                                          #
        r = s.to_mark(self.i_p1)  # tomark                                       #
        if r:                                                                    #
            s.limit = s.cursor                                                   #
            s.cursor = len(s) - var60                                            #
            self.left = s.cursor  ##                                             #
            r = True              ## [                                           #
            if r:                                                                #
                a_9 = None                                          ##           #
                r = False                                           #            #
                var56 = s.cursor                                    #            #
                for var55, var59, var58 in _a_9:                    #            # setlimit
                    if s.starts_with(var55):                        #            #
                        var57 = s.cursor                            #            #
                        r = (not var59) or getattr(self, var59)(s)  # substring  #
                        if r:                                       #            #
                          s.cursor = var57                          #            #
                          a_9 = var58                               #            #
                          break                                     #            #
                    s.cursor = var56                                ##           #
                if r:                                                            #
                    self.right = s.cursor  ##                                    #
                    r = True               ## ]                                  #
            s.limit = var61                                                      ##
        if r:
            if a_9 == 0:  ##
                r = True  ## among
            if r:
                r = s.set_range(self.left, self.right, u'')  # delete
        return r
    
    def r_t_plural(self, s):
        r = True
        var63 = len(s) - s.cursor                                                         ##
        var64 = s.limit                                                                   #
        r = s.to_mark(self.i_p1)  # tomark                                                #
        if r:                                                                             #
            s.limit = s.cursor                                                            #
            s.cursor = len(s) - var63                                                     #
            self.left = s.cursor  ##                                                      #
            r = True              ## [                                                    #
            if r:                                                                         #
                r = s.starts_with(u't')  # character check                                #
                if r:                                                                     #
                    self.right = s.cursor  ##                                             #
                    r = True               ## ]                                           # setlimit
                    if r:                                                                 #
                        var62 = len(s) - s.cursor                                 ##      #
                        if s.cursor == s.limit:                 ##                #       #
                            r = False                           #                 #       #
                        else:                                   #                 #       #
                            r = s.chars[s.cursor - 1] in _g_V1  # grouping check  # test  #
                        if r:                                   #                 #       #
                            s.cursor -= 1                       ##                #       #
                        s.cursor = len(s) - var62                                 ##      #
                        if r:                                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete         #
            s.limit = var64                                                               ##
        if r:
            var70 = len(s) - s.cursor                                                ##
            var71 = s.limit                                                          #
            r = s.to_mark(self.i_p2)  # tomark                                       #
            if r:                                                                    #
                s.limit = s.cursor                                                   #
                s.cursor = len(s) - var70                                            #
                self.left = s.cursor  ##                                             #
                r = True              ## [                                           #
                if r:                                                                #
                    a_10 = None                                         ##           #
                    r = False                                           #            #
                    var66 = s.cursor                                    #            #
                    for var65, var69, var68 in _a_10:                   #            # setlimit
                        if s.starts_with(var65):                        #            #
                            var67 = s.cursor                            #            #
                            r = (not var69) or getattr(self, var69)(s)  # substring  #
                            if r:                                       #            #
                              s.cursor = var67                          #            #
                              a_10 = var68                              #            #
                              break                                     #            #
                        s.cursor = var66                                ##           #
                    if r:                                                            #
                        self.right = s.cursor  ##                                    #
                        r = True               ## ]                                  #
                s.limit = var71                                                      ##
            if r:
                if a_10 == 0:                                           ##
                    var72 = len(s) - s.cursor                    ##     #
                    r = s.starts_with(u'po')  # character check  #      #
                    if not r:                                    # not  #
                        s.cursor = len(s) - var72                #      # among
                    r = not r                                    ##     #
                if a_10 == 1:                                           #
                    r = True                                            ##
                if r:
                    r = s.set_range(self.left, self.right, u'')  # delete
        return r
    
    def r_tidy(self, s):
        r = True
        var79 = len(s) - s.cursor                                                                        ##
        var80 = s.limit                                                                                  #
        r = s.to_mark(self.i_p1)  # tomark                                                               #
        if r:                                                                                            #
            s.limit = s.cursor                                                                           #
            s.cursor = len(s) - var79                                                                    #
            var74 = len(s) - s.cursor                                                     ##             #
            var73 = len(s) - s.cursor                                              ##     #              #
            r = self.r_LONG(s)  # routine call                                     #      #              #
            if r:                                                                  #      #              #
                s.cursor = len(s) - var73                                          #      #              #
                self.left = s.cursor  ##                                           #      #              #
                r = True              ## [                                         #      #              #
                if r:                                                              # and  #              #
                    r = s.hop(1)  # next                                           #      # do           #
                    if r:                                                          #      #              #
                        self.right = s.cursor  ##                                  #      #              #
                        r = True               ## ]                                #      #              #
                        if r:                                                      #      #              #
                            r = s.set_range(self.left, self.right, u'')  # delete  ##     #              #
            s.cursor = len(s) - var74                                                     #              #
            r = True                                                                      ##             #
            if r:                                                                                        #
                var75 = len(s) - s.cursor                                                          ##    #
                self.left = s.cursor  ##                                                           #     #
                r = True              ## [                                                         #     #
                if r:                                                                              #     #
                    if s.cursor == s.limit:                  ##                                    #     #
                        r = False                            #                                     #     #
                    else:                                    #                                     #     #
                        r = s.chars[s.cursor - 1] in _g_AEI  # grouping check                      #     #
                    if r:                                    #                                     #     #
                        s.cursor -= 1                        ##                                    #     #
                    if r:                                                                          #     #
                        self.right = s.cursor  ##                                                  #     #
                        r = True               ## ]                                                # do  #
                        if r:                                                                      #     #
                            if s.cursor == s.limit:                     ##                         #     #
                                r = False                               #                          #     #
                            else:                                       #                          #     #
                                r = s.chars[s.cursor - 1] not in _g_V1  # negative grouping check  #     #
                            if r:                                       #                          #     # setlimit
                                s.cursor -= 1                           ##                         #     #
                            if r:                                                                  #     #
                                r = s.set_range(self.left, self.right, u'')  # delete              #     #
                s.cursor = len(s) - var75                                                          #     #
                r = True                                                                           ##    #
                if r:                                                                                    #
                    var77 = len(s) - s.cursor                                              ##            #
                    self.left = s.cursor  ##                                               #             #
                    r = True              ## [                                             #             #
                    if r:                                                                  #             #
                        r = s.starts_with(u'j')  # character check                         #             #
                        if r:                                                              #             #
                            self.right = s.cursor  ##                                      #             #
                            r = True               ## ]                                    #             #
                            if r:                                                          #             #
                                var76 = len(s) - s.cursor                       ##         # do          #
                                r = s.starts_with(u'o')  # character check      #          #             #
                                if not r:                                       # or       #             #
                                    s.cursor = len(s) - var76                   #          #             #
                                    r = s.starts_with(u'u')  # character check  ##         #             #
                                if r:                                                      #             #
                                    r = s.set_range(self.left, self.right, u'')  # delete  #             #
                    s.cursor = len(s) - var77                                              #             #
                    r = True                                                               ##            #
                    if r:                                                                                #
                        var78 = len(s) - s.cursor                                              ##        #
                        self.left = s.cursor  ##                                               #         #
                        r = True              ## [                                             #         #
                        if r:                                                                  #         #
                            r = s.starts_with(u'o')  # character check                         #         #
                            if r:                                                              #         #
                                self.right = s.cursor  ##                                      #         #
                                r = True               ## ]                                    # do      #
                                if r:                                                          #         #
                                    r = s.starts_with(u'j')  # character check                 #         #
                                    if r:                                                      #         #
                                        r = s.set_range(self.left, self.right, u'')  # delete  #         #
                        s.cursor = len(s) - var78                                              #         #
                        r = True                                                               ##        #
            s.limit = var80                                                                              ##
        if r:
            while True:                                                                ##
                var81 = len(s) - s.cursor                                              #
                if s.cursor == s.limit:                     ##                         #
                    r = False                               #                          #
                else:                                       #                          #
                    r = s.chars[s.cursor - 1] not in _g_V1  # negative grouping check  #
                if r:                                       #                          # goto
                    s.cursor -= 1                           ##                         #
                if r or s.cursor == s.limit:                                           #
                    s.cursor = len(s) - var81                                          #
                    break                                                              #
                s.cursor = len(s) - var81 - 1                                          ##
            if r:
                self.left = s.cursor  ##
                r = True              ## [
                if r:
                    r = s.hop(1)  # next
                    if r:
                        self.right = s.cursor  ##
                        r = True               ## ]
                        if r:
                            r = self.s_x.set_chars(s.get_range(self.left, self.right))  # ->
                            if r:
                                r = s.starts_with(self.s_x.chars)  # character check
                                if r:
                                    r = s.set_range(self.left, self.right, u'')  # delete
        return r
    
    def r_stem(self, s):
        r = True
        var82 = s.cursor                            ##
        r = self.r_mark_regions(s)  # routine call  #
        s.cursor = var82                            # do
        r = True                                    ##
        if r:
            self.b_ending_removed = False  ##
            r = True                       ## unset
            if r:
                var91 = s.cursor                                                           ##
                var92 = len(s) - s.limit                                                   #
                s.direction *= -1                                                          #
                s.cursor, s.limit = s.limit, s.cursor                                      #
                var83 = len(s) - s.cursor                   ##                             #
                r = self.r_particle_etc(s)  # routine call  #                              #
                s.cursor = len(s) - var83                   # do                           #
                r = True                                    ##                             #
                if r:                                                                      #
                    var84 = len(s) - s.cursor                 ##                           #
                    r = self.r_possessive(s)  # routine call  #                            #
                    s.cursor = len(s) - var84                 # do                         #
                    r = True                                  ##                           #
                    if r:                                                                  #
                        var85 = len(s) - s.cursor                  ##                      #
                        r = self.r_case_ending(s)  # routine call  #                       #
                        s.cursor = len(s) - var85                  # do                    #
                        r = True                                   ##                      #
                        if r:                                                              #
                            var86 = len(s) - s.cursor                    ##                #
                            r = self.r_other_endings(s)  # routine call  #                 #
                            s.cursor = len(s) - var86                    # do              #
                            r = True                                     ##                # backwards
                            if r:                                                          #
                                var89 = len(s) - s.cursor                            ##    #
                                r = self.b_ending_removed  # boolean variable check  #     #
                                if r:                                                #     #
                                    var87 = len(s) - s.cursor               ##       #     #
                                    r = self.r_i_plural(s)  # routine call  #        #     #
                                    s.cursor = len(s) - var87               # do     #     #
                                    r = True                                ##       # or  #
                                if not r:                                            #     #
                                    s.cursor = len(s) - var89                        #     #
                                    var88 = len(s) - s.cursor               ##       #     #
                                    r = self.r_t_plural(s)  # routine call  #        #     #
                                    s.cursor = len(s) - var88               # do     #     #
                                    r = True                                ##       ##    #
                                if r:                                                      #
                                    var90 = len(s) - s.cursor           ##                 #
                                    r = self.r_tidy(s)  # routine call  #                  #
                                    s.cursor = len(s) - var90           # do               #
                                    r = True                            ##                 #
                s.direction *= -1                                                          #
                s.cursor = var91                                                           #
                s.limit = len(s) - var92                                                   ##
        return r
