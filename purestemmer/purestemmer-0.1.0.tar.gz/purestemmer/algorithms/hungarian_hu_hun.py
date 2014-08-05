#!/usr/bin/env python
# vim:fileencoding=utf-8



# This file was auto-generated on 2014-08-05 20:04:11 using
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

_g_v = set(u'aeiou\xe1\xe9\xed\xf3\xf6\xf5\xfa\xfc\xfb')
_a_1 = ((u'dzs', '', 0), (u'cs', '', 0), (u'gy', '', 0), (u'ly', '', 0), (u'ny', '', 0), (u'sz', '', 0), (u'ty', '', 0), (u'zs', '', 0),)
_a_2 = ((u'\xe1', '', 0), (u'\xe9', '', 1),)
_a_3 = ((u'ccs', '', 0), (u'ggy', '', 0), (u'lly', '', 0), (u'nny', '', 0), (u'ssz', '', 0), (u'tty', '', 0), (u'zzs', '', 0), (u'bb', '', 0), (u'cc', '', 0), (u'dd', '', 0), (u'ff', '', 0), (u'gg', '', 0), (u'jj', '', 0), (u'kk', '', 0), (u'll', '', 0), (u'mm', '', 0), (u'nn', '', 0), (u'pp', '', 0), (u'rr', '', 0), (u'ss', '', 0), (u'tt', '', 0), (u'vv', '', 0), (u'zz', '', 0),)
_a_4 = ((u'al', '', 0), (u'el', '', 1),)
_a_5 = ((u'k\xe9ppen', '', 0), (u'onk\xe9nt', '', 0), (u'enk\xe9nt', '', 0), (u'ank\xe9nt', '', 0), (u'k\xe9pp', '', 0), (u'k\xe9nt', '', 0), (u'ban', '', 0), (u'ben', '', 0), (u'nak', '', 0), (u'nek', '', 0), (u'val', '', 0), (u'vel', '', 0), (u't\xf3l', '', 0), (u't\xf5l', '', 0), (u'r\xf3l', '', 0), (u'r\xf5l', '', 0), (u'b\xf3l', '', 0), (u'b\xf5l', '', 0), (u'hoz', '', 0), (u'hez', '', 0), (u'h\xf6z', '', 0), (u'n\xe1l', '', 0), (u'n\xe9l', '', 0), (u'\xe9rt', '', 0), (u'kor', '', 0), (u'ba', '', 0), (u'be', '', 0), (u'ra', '', 0), (u're', '', 0), (u'ig', '', 0), (u'at', '', 0), (u'et', '', 0), (u'ot', '', 0), (u'\xf6t', '', 0), (u'ul', '', 0), (u'\xfcl', '', 0), (u'v\xe1', '', 0), (u'v\xe9', '', 0), (u'en', '', 0), (u'on', '', 0), (u'an', '', 0), (u'\xf6n', '', 0), (u'n', '', 0), (u't', '', 0),)
_a_6 = ((u'\xe1nk\xe9nt', '', 2), (u'\xe9n', '', 0), (u'\xe1n', '', 1),)
_a_7 = ((u'astul', '', 0), (u'est\xfcl', '', 0), (u'\xe1stul', '', 2), (u'\xe9st\xfcl', '', 3), (u'stul', '', 1), (u'st\xfcl', '', 1),)
_a_8 = ((u'\xe1', '', 0), (u'\xe9', '', 1),)
_a_9 = ((u'\xe1k', '', 0), (u'\xe9k', '', 1), (u'\xf6k', '', 2), (u'ak', '', 3), (u'ok', '', 4), (u'ek', '', 5), (u'k', '', 6),)
_a_10 = ((u'ok\xe9', '', 0), (u'\xf6k\xe9', '', 0), (u'ak\xe9', '', 0), (u'ek\xe9', '', 0), (u'\xe9k\xe9', '', 1), (u'\xe1k\xe9', '', 2), (u'\xe9\xe9i', '', 4), (u'\xe1\xe9i', '', 5), (u'k\xe9', '', 3), (u'\xe9i', '', 6), (u'\xe9\xe9', '', 7), (u'\xe9', '', 8),)
_a_11 = ((u'\xe1juk', '', 4), (u'\xe9j\xfck', '', 5), (u'\xfcnk', '', 0), (u'unk', '', 0), (u'\xe1nk', '', 1), (u'\xe9nk', '', 2), (u'juk', '', 6), (u'j\xfck', '', 6), (u'nk', '', 3), (u'uk', '', 7), (u'\xfck', '', 7), (u'em', '', 8), (u'om', '', 8), (u'am', '', 8), (u'\xe1m', '', 9), (u'\xe9m', '', 10), (u'od', '', 12), (u'ed', '', 12), (u'ad', '', 12), (u'\xf6d', '', 12), (u'\xe1d', '', 13), (u'\xe9d', '', 14), (u'ja', '', 16), (u'je', '', 16), (u'm', '', 11), (u'd', '', 15), (u'a', '', 17), (u'e', '', 17), (u'o', '', 17), (u'\xe1', '', 18), (u'\xe9', '', 19),)
_a_12 = ((u'jaitok', '', 19), (u'jeitek', '', 19), (u'jaink', '', 15), (u'jeink', '', 15), (u'aitok', '', 20), (u'eitek', '', 20), (u'\xe1itok', '', 21), (u'\xe9itek', '', 22), (u'jaim', '', 0), (u'jeim', '', 0), (u'jaid', '', 5), (u'jeid', '', 5), (u'eink', '', 16), (u'aink', '', 16), (u'\xe1ink', '', 17), (u'\xe9ink', '', 18), (u'itek', '', 23), (u'jeik', '', 24), (u'jaik', '', 24), (u'\xe1im', '', 1), (u'\xe9im', '', 2), (u'aim', '', 3), (u'eim', '', 3), (u'\xe1id', '', 6), (u'\xe9id', '', 7), (u'aid', '', 8), (u'eid', '', 8), (u'jai', '', 10), (u'jei', '', 10), (u'ink', '', 19), (u'aik', '', 25), (u'eik', '', 25), (u'\xe1ik', '', 26), (u'\xe9ik', '', 27), (u'im', '', 4), (u'id', '', 9), (u'\xe1i', '', 11), (u'\xe9i', '', 12), (u'ai', '', 13), (u'ei', '', 13), (u'ik', '', 28), (u'i', '', 14),)

class _Program(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.i_p1 = 0

    def r_mark_regions(self, s):
        r = True
        self.i_p1 = s.limit
        r = True
        if r:
            var7 = s.cursor                                                                   ##
            if s.cursor == s.limit:            ##                                             #
                r = False                      #                                              #
            else:                              #                                              #
                r = s.chars[s.cursor] in _g_v  # grouping check                               #
            if r:                              #                                              #
                s.cursor += 1                  ##                                             #
            if r:                                                                             #
                while True:                                                           ##      #
                    var0 = s.cursor                                                   #       #
                    if s.cursor == s.limit:                ##                         #       #
                        r = False                          #                          #       #
                    else:                                  #                          #       #
                        r = s.chars[s.cursor] not in _g_v  # negative grouping check  #       #
                    if r:                                  #                          # goto  #
                        s.cursor += 1                      ##                         #       #
                    if r or s.cursor == s.limit:                                      #       #
                        s.cursor = var0                                               #       #
                        break                                                         #       #
                    s.cursor = var0 + 1                                               ##      #
                if r:                                                                         #
                    var6 = s.cursor                                            ##             #
                    a_1 = None                                        ##       #              #
                    r = False                                         #        #              #
                    var2 = s.cursor                                   #        #              #
                    for var1, var5, var4 in _a_1:                     #        #              #
                        if s.starts_with(var1):                       #        #              #
                            var3 = s.cursor                           #        #              #
                            r = (not var5) or getattr(self, var5)(s)  #        #              #
                            if r:                                     # among  #              #
                              s.cursor = var3                         #        # or           #
                              a_1 = var4                              #        #              #
                              break                                   #        #              # or
                        s.cursor = var2                               #        #              #
                    if r:                                             #        #              #
                        if a_1 == 0:                                  #        #              #
                            r = True                                  ##       #              #
                    if not r:                                                  #              #
                        s.cursor = var6                                        #              #
                        r = s.hop(1)  # next                                   ##             #
                    if r:                                                                     #
                        self.i_p1 = s.cursor  ##                                              #
                        r = True              ## setmark                                      #
            if not r:                                                                         #
                s.cursor = var7                                                               #
                if s.cursor == s.limit:                ##                                     #
                    r = False                          #                                      #
                else:                                  #                                      #
                    r = s.chars[s.cursor] not in _g_v  # negative grouping check              #
                if r:                                  #                                      #
                    s.cursor += 1                      ##                                     #
                if r:                                                                         #
                    while True:                                              ##               #
                        if s.cursor == s.limit:            ##                #                #
                            r = False                      #                 #                #
                        else:                              #                 #                #
                            r = s.chars[s.cursor] in _g_v  # grouping check  #                #
                        if r:                              #                 # gopast         #
                            s.cursor += 1                  ##                #                #
                        if r or s.cursor == s.limit:                         #                #
                            break                                            #                #
                        s.cursor += 1                                        ##               #
                    if r:                                                                     #
                        self.i_p1 = s.cursor  ##                                              #
                        r = True              ## setmark                                      ##
        return r
    
    def r_R1(self, s):
        r = True
        r = self.i_p1 <= s.cursor  # <=
        return r
    
    def r_v_ending(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_2 = None                                          ##
            r = False                                           #
            var9 = s.cursor                                     #
            for var8, var12, var11 in _a_2:                     #
                if s.starts_with(var8):                         #
                    var10 = s.cursor                            #
                    r = (not var12) or getattr(self, var12)(s)  # substring
                    if r:                                       #
                      s.cursor = var10                          #
                      a_2 = var11                               #
                      break                                     #
                s.cursor = var9                                 ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = self.r_R1(s)  # routine call
                    if r:
                        if a_2 == 0:                                            ##
                            r = s.set_range(self.left, self.right, u'a')  # <-  #
                        if a_2 == 1:                                            # among
                            r = s.set_range(self.left, self.right, u'e')  # <-  ##
        return r
    
    def r_double(self, s):
        r = True
        var18 = len(s) - s.cursor                                    ##
        a_3 = None                                          ##       #
        r = False                                           #        #
        var14 = s.cursor                                    #        #
        for var13, var17, var16 in _a_3:                    #        #
            if s.starts_with(var13):                        #        #
                var15 = s.cursor                            #        #
                r = (not var17) or getattr(self, var17)(s)  #        #
                if r:                                       # among  # test
                  s.cursor = var15                          #        #
                  a_3 = var16                               #        #
                  break                                     #        #
            s.cursor = var14                                #        #
        if r:                                               #        #
            if a_3 == 0:                                    #        #
                r = True                                    ##       #
        s.cursor = len(s) - var18                                    ##
        return r
    
    def r_undouble(self, s):
        r = True
        r = s.hop(1)  # next
        if r:
            self.left = s.cursor  ##
            r = True              ## [
            if r:
                r = s.hop(1)  # hop
                if r:
                    self.right = s.cursor  ##
                    r = True               ## ]
                    if r:
                        r = s.set_range(self.left, self.right, u'')  # delete
        return r
    
    def r_instrum(self, s):
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
                        if a_4 == 0:                              ##
                            r = self.r_double(s)  # routine call  #
                        if a_4 == 1:                              # among
                            r = self.r_double(s)  # routine call  ##
                        if r:
                            r = s.set_range(self.left, self.right, u'')  # delete
                            if r:
                                r = self.r_undouble(s)  # routine call
        return r
    
    def r_case(self, s):
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
                        if a_5 == 0:  ##
                            r = True  ## among
                        if r:
                            r = s.set_range(self.left, self.right, u'')  # delete
                            if r:
                                r = self.r_v_ending(s)  # routine call
        return r
    
    def r_case_special(self, s):
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
                    r = self.r_R1(s)  # routine call
                    if r:
                        if a_6 == 0:                                            ##
                            r = s.set_range(self.left, self.right, u'e')  # <-  #
                        if a_6 == 1:                                            #
                            r = s.set_range(self.left, self.right, u'a')  # <-  # among
                        if a_6 == 2:                                            #
                            r = s.set_range(self.left, self.right, u'a')  # <-  ##
        return r
    
    def r_case_other(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_7 = None                                          ##
            r = False                                           #
            var35 = s.cursor                                    #
            for var34, var38, var37 in _a_7:                    #
                if s.starts_with(var34):                        #
                    var36 = s.cursor                            #
                    r = (not var38) or getattr(self, var38)(s)  # substring
                    if r:                                       #
                      s.cursor = var36                          #
                      a_7 = var37                               #
                      break                                     #
                s.cursor = var35                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = self.r_R1(s)  # routine call
                    if r:
                        if a_7 == 0:                                               ##
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_7 == 1:                                               #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_7 == 2:                                               # among
                            r = s.set_range(self.left, self.right, u'a')  # <-     #
                        if a_7 == 3:                                               #
                            r = s.set_range(self.left, self.right, u'e')  # <-     ##
        return r
    
    def r_factive(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_8 = None                                          ##
            r = False                                           #
            var40 = s.cursor                                    #
            for var39, var43, var42 in _a_8:                    #
                if s.starts_with(var39):                        #
                    var41 = s.cursor                            #
                    r = (not var43) or getattr(self, var43)(s)  # substring
                    if r:                                       #
                      s.cursor = var41                          #
                      a_8 = var42                               #
                      break                                     #
                s.cursor = var40                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = self.r_R1(s)  # routine call
                    if r:
                        if a_8 == 0:                              ##
                            r = self.r_double(s)  # routine call  #
                        if a_8 == 1:                              # among
                            r = self.r_double(s)  # routine call  ##
                        if r:
                            r = s.set_range(self.left, self.right, u'')  # delete
                            if r:
                                r = self.r_undouble(s)  # routine call
        return r
    
    def r_plural(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_9 = None                                          ##
            r = False                                           #
            var45 = s.cursor                                    #
            for var44, var48, var47 in _a_9:                    #
                if s.starts_with(var44):                        #
                    var46 = s.cursor                            #
                    r = (not var48) or getattr(self, var48)(s)  # substring
                    if r:                                       #
                      s.cursor = var46                          #
                      a_9 = var47                               #
                      break                                     #
                s.cursor = var45                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = self.r_R1(s)  # routine call
                    if r:
                        if a_9 == 0:                                               ##
                            r = s.set_range(self.left, self.right, u'a')  # <-     #
                        if a_9 == 1:                                               #
                            r = s.set_range(self.left, self.right, u'e')  # <-     #
                        if a_9 == 2:                                               #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_9 == 3:                                               #
                            r = s.set_range(self.left, self.right, u'')  # delete  # among
                        if a_9 == 4:                                               #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_9 == 5:                                               #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_9 == 6:                                               #
                            r = s.set_range(self.left, self.right, u'')  # delete  ##
        return r
    
    def r_owned(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_10 = None                                         ##
            r = False                                           #
            var50 = s.cursor                                    #
            for var49, var53, var52 in _a_10:                   #
                if s.starts_with(var49):                        #
                    var51 = s.cursor                            #
                    r = (not var53) or getattr(self, var53)(s)  # substring
                    if r:                                       #
                      s.cursor = var51                          #
                      a_10 = var52                              #
                      break                                     #
                s.cursor = var50                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = self.r_R1(s)  # routine call
                    if r:
                        if a_10 == 0:                                              ##
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_10 == 1:                                              #
                            r = s.set_range(self.left, self.right, u'e')  # <-     #
                        if a_10 == 2:                                              #
                            r = s.set_range(self.left, self.right, u'a')  # <-     #
                        if a_10 == 3:                                              #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_10 == 4:                                              #
                            r = s.set_range(self.left, self.right, u'e')  # <-     # among
                        if a_10 == 5:                                              #
                            r = s.set_range(self.left, self.right, u'a')  # <-     #
                        if a_10 == 6:                                              #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_10 == 7:                                              #
                            r = s.set_range(self.left, self.right, u'e')  # <-     #
                        if a_10 == 8:                                              #
                            r = s.set_range(self.left, self.right, u'')  # delete  ##
        return r
    
    def r_sing_owner(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_11 = None                                         ##
            r = False                                           #
            var55 = s.cursor                                    #
            for var54, var58, var57 in _a_11:                   #
                if s.starts_with(var54):                        #
                    var56 = s.cursor                            #
                    r = (not var58) or getattr(self, var58)(s)  # substring
                    if r:                                       #
                      s.cursor = var56                          #
                      a_11 = var57                              #
                      break                                     #
                s.cursor = var55                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = self.r_R1(s)  # routine call
                    if r:
                        if a_11 == 0:                                              ##
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_11 == 1:                                              #
                            r = s.set_range(self.left, self.right, u'a')  # <-     #
                        if a_11 == 2:                                              #
                            r = s.set_range(self.left, self.right, u'e')  # <-     #
                        if a_11 == 3:                                              #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_11 == 4:                                              #
                            r = s.set_range(self.left, self.right, u'a')  # <-     #
                        if a_11 == 5:                                              #
                            r = s.set_range(self.left, self.right, u'e')  # <-     #
                        if a_11 == 6:                                              #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_11 == 7:                                              #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_11 == 8:                                              #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_11 == 9:                                              #
                            r = s.set_range(self.left, self.right, u'a')  # <-     #
                        if a_11 == 10:                                             # among
                            r = s.set_range(self.left, self.right, u'e')  # <-     #
                        if a_11 == 11:                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_11 == 12:                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_11 == 13:                                             #
                            r = s.set_range(self.left, self.right, u'a')  # <-     #
                        if a_11 == 14:                                             #
                            r = s.set_range(self.left, self.right, u'e')  # <-     #
                        if a_11 == 15:                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_11 == 16:                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_11 == 17:                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_11 == 18:                                             #
                            r = s.set_range(self.left, self.right, u'a')  # <-     #
                        if a_11 == 19:                                             #
                            r = s.set_range(self.left, self.right, u'e')  # <-     ##
        return r
    
    def r_plur_owner(self, s):
        r = True
        self.left = s.cursor  ##
        r = True              ## [
        if r:
            a_12 = None                                         ##
            r = False                                           #
            var60 = s.cursor                                    #
            for var59, var63, var62 in _a_12:                   #
                if s.starts_with(var59):                        #
                    var61 = s.cursor                            #
                    r = (not var63) or getattr(self, var63)(s)  # substring
                    if r:                                       #
                      s.cursor = var61                          #
                      a_12 = var62                              #
                      break                                     #
                s.cursor = var60                                ##
            if r:
                self.right = s.cursor  ##
                r = True               ## ]
                if r:
                    r = self.r_R1(s)  # routine call
                    if r:
                        if a_12 == 0:                                              ##
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_12 == 1:                                              #
                            r = s.set_range(self.left, self.right, u'a')  # <-     #
                        if a_12 == 2:                                              #
                            r = s.set_range(self.left, self.right, u'e')  # <-     #
                        if a_12 == 3:                                              #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_12 == 4:                                              #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_12 == 5:                                              #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_12 == 6:                                              #
                            r = s.set_range(self.left, self.right, u'a')  # <-     #
                        if a_12 == 7:                                              #
                            r = s.set_range(self.left, self.right, u'e')  # <-     #
                        if a_12 == 8:                                              #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_12 == 9:                                              #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_12 == 10:                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_12 == 11:                                             #
                            r = s.set_range(self.left, self.right, u'a')  # <-     #
                        if a_12 == 12:                                             #
                            r = s.set_range(self.left, self.right, u'e')  # <-     #
                        if a_12 == 13:                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_12 == 14:                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete  # among
                        if a_12 == 15:                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_12 == 16:                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_12 == 17:                                             #
                            r = s.set_range(self.left, self.right, u'a')  # <-     #
                        if a_12 == 18:                                             #
                            r = s.set_range(self.left, self.right, u'e')  # <-     #
                        if a_12 == 19:                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_12 == 20:                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_12 == 21:                                             #
                            r = s.set_range(self.left, self.right, u'a')  # <-     #
                        if a_12 == 22:                                             #
                            r = s.set_range(self.left, self.right, u'e')  # <-     #
                        if a_12 == 23:                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_12 == 24:                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_12 == 25:                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete  #
                        if a_12 == 26:                                             #
                            r = s.set_range(self.left, self.right, u'a')  # <-     #
                        if a_12 == 27:                                             #
                            r = s.set_range(self.left, self.right, u'e')  # <-     #
                        if a_12 == 28:                                             #
                            r = s.set_range(self.left, self.right, u'')  # delete  ##
        return r
    
    def r_stem(self, s):
        r = True
        var64 = s.cursor                            ##
        r = self.r_mark_regions(s)  # routine call  #
        s.cursor = var64                            # do
        r = True                                    ##
        if r:
            var74 = s.cursor                                                            ##
            var75 = len(s) - s.limit                                                    #
            s.direction *= -1                                                           #
            s.cursor, s.limit = s.limit, s.cursor                                       #
            var65 = len(s) - s.cursor              ##                                   #
            r = self.r_instrum(s)  # routine call  #                                    #
            s.cursor = len(s) - var65              # do                                 #
            r = True                               ##                                   #
            if r:                                                                       #
                var66 = len(s) - s.cursor           ##                                  #
                r = self.r_case(s)  # routine call  #                                   #
                s.cursor = len(s) - var66           # do                                #
                r = True                            ##                                  #
                if r:                                                                   #
                    var67 = len(s) - s.cursor                   ##                      #
                    r = self.r_case_special(s)  # routine call  #                       #
                    s.cursor = len(s) - var67                   # do                    #
                    r = True                                    ##                      #
                    if r:                                                               #
                        var68 = len(s) - s.cursor                 ##                    #
                        r = self.r_case_other(s)  # routine call  #                     #
                        s.cursor = len(s) - var68                 # do                  #
                        r = True                                  ##                    #
                        if r:                                                           #
                            var69 = len(s) - s.cursor              ##                   #
                            r = self.r_factive(s)  # routine call  #                    # backwards
                            s.cursor = len(s) - var69              # do                 #
                            r = True                               ##                   #
                            if r:                                                       #
                                var70 = len(s) - s.cursor            ##                 #
                                r = self.r_owned(s)  # routine call  #                  #
                                s.cursor = len(s) - var70            # do               #
                                r = True                             ##                 #
                                if r:                                                   #
                                    var71 = len(s) - s.cursor                 ##        #
                                    r = self.r_sing_owner(s)  # routine call  #         #
                                    s.cursor = len(s) - var71                 # do      #
                                    r = True                                  ##        #
                                    if r:                                               #
                                        var72 = len(s) - s.cursor                 ##    #
                                        r = self.r_plur_owner(s)  # routine call  #     #
                                        s.cursor = len(s) - var72                 # do  #
                                        r = True                                  ##    #
                                        if r:                                           #
                                            var73 = len(s) - s.cursor             ##    #
                                            r = self.r_plural(s)  # routine call  #     #
                                            s.cursor = len(s) - var73             # do  #
                                            r = True                              ##    #
            s.direction *= -1                                                           #
            s.cursor = var74                                                            #
            s.limit = len(s) - var75                                                    ##
        return r
