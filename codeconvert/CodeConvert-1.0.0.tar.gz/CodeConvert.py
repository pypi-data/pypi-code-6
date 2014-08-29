#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2014 HQM <qiminis0801@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# note:
# see http://docs.python.org/2/library/codecs.html#standard-encodings

import sys
import requests


class CodeConvert:
    def __init__(self):
        pass

    @staticmethod
    def Convert2Utf8(kw):
        if repr(kw).startswith('u'):
            # print repr(kw)[3:-1].split('\\')
            if repr(kw)[1:].strip('\'').strip('"').startswith('\\x'):  # 处理 u 内含 gbk、utf8 编码
                try:  # 处理 u 内含 utf8 编码
                    # kw.encode('latin1').decode('utf8')
                    # return kw.encode('latin1')
                    kw.encode('raw_unicode_escape').decode('utf8')  # 如果是 u 内含 gbk 编码，会出错进入 except
                    return kw.encode('raw_unicode_escape')
                except:  # 处理 u 内含 gbk 编码
                    # return kw.encode('latin1').decode('gbk').encode('utf8')
                    return kw.encode('raw_unicode_escape').decode('gbk').encode('utf8')
            # elif repr(kw)[1:].strip('\'').strip('"').startswith('\\u'):  # 处理 unicod 编码
            elif isinstance(kw, unicode):
                return kw.encode('utf8')
        else:
            if repr(kw).strip('\'').strip('"').startswith('\\x'):  # 处理 gbk、utf8 编码
                try:  # 处理 utf8 编码
                    kw.decode('utf8')
                    return kw
                except:  # 处理 gbk 编码
                    return kw.decode('gbk').encode('utf8')
            elif repr(kw).strip('\'').strip('"').startswith('\\\\u'):  # 处理无 u 的 unicode 编码
                return kw.decode('raw_unicode_escape').encode('utf8')
            else:
                return kw

    @staticmethod
    def Convert2Unicode(kw):
        if repr(kw).startswith('u'):
            # print repr(kw)[3:-1].split('\\')
            if repr(kw)[1:].strip('\'').strip('"').startswith('\\x'):  # 处理 u 内含 gbk、utf8 编码
                try:  # 处理 u 内含 utf8 编码
                    kw.encode('latin1').decode('utf8')
                    return kw.encode('latin1').decode('utf8')
                except:  # 处理 u 内含 gbk 编码
                    return kw.encode('latin1').decode('gbk')
            # elif repr(kw)[1:].strip('\'').strip('"').startswith('\\u'):  # 处理 unicode 编码
            elif isinstance(kw, unicode):
                return kw
        else:
            if repr(kw).strip('\'').strip('"').startswith('\\x'):  # 处理 gbk、utf8 编码
                try:  # 处理 utf8 编码
                    return kw.decode('utf8')
                except:  # 处理 gbk 编码
                    return kw.decode('gbk')
            elif repr(kw).strip('\'').strip('"').startswith('\\\\u'):  # 处理无 u 的 unicode 编码
                return kw.decode('raw_unicode_escape')
            else:
                return kw.decode('utf8')

    @staticmethod
    def Convert2Utf8_test(kw):
        if repr(kw).startswith('u'):
            if repr(kw)[1:].strip('\'').strip('"').startswith('\\x'):  # 处理 u 内含 gbk、utf8 编码
                try:  # 处理 u 内含 utf8 编码
                    kw.encode('raw_unicode_escape').decode('utf8')  # 如果是 u 内含 gbk 编码，会出错进入 except
                    print ">>> u 内含 utf8 编码: obj.encode('raw_unicode_escape')"
                    return kw.encode('raw_unicode_escape')
                except:  # 处理 u 内含 gbk 编码
                    print ">>> u 内含 gbk 编码: obj.encode('raw_unicode_escape').decode('gbk').encode('utf8')"
                    return kw.encode('raw_unicode_escape').decode('gbk').encode('utf8')
            elif isinstance(kw, unicode):  # 处理 unicod 编码
                print ">>> unicode 编码: obj.encode('utf8')"
                return kw.encode('utf8')
        else:
            if repr(kw).strip('\'').strip('"').startswith('\\x'):  # 处理 gbk、utf8 编码
                try:  # 处理 utf8 编码
                    kw.decode('utf8')
                    print ">>> utf8 编码: obj"
                    return kw
                except:  # 处理 gbk 编码
                    print ">>> gbk 编码: obj.decode('gbk').encode('utf8')"
                    return kw.decode('gbk').encode('utf8')
            elif repr(kw).strip('\'').strip('"').startswith('\\\\u'):  # 处理无 u 的 unicode 编码
                print ">>> 无 u 的 unicode 编码: obj.decode('raw_unicode_escape').encode('utf8')"
                return kw.decode('raw_unicode_escape').encode('utf8')
            else:
                print ">>> utf8 编码: obj"
                return kw

    @staticmethod
    def Convert2Unicode_test(kw):
        if repr(kw).startswith('u'):
            if repr(kw)[1:].strip('\'').strip('"').startswith('\\x'):  # 处理 u 内含 gbk、utf8 编码
                try:  # 处理 u 内含 utf8 编码
                    kw.encode('latin1').decode('utf8')
                    print ">>> u 内含 utf8 编码: obj.decode('utf8')"
                    return kw.encode('latin1').decode('utf8')
                except:  # 处理 u 内含 gbk 编码
                    print ">>> u 内含 gbk 编码: obj.encode('raw_unicode_escape').decode('gbk') or obj.encode('latin1').decode('gbk')"
                    return kw.encode('latin1').decode('gbk')
            elif isinstance(kw, unicode):  # 处理 unicode 编码
                print ">>> unicode 编码: obj"
                return kw
        else:
            if repr(kw).strip('\'').strip('"').startswith('\\x'):  # 处理 gbk、utf8 编码
                try:  # 处理 utf8 编码
                    kw.decode('utf8')
                    print ">>> unicode 编码: obj.decode('utf8')"
                    return kw.decode('utf8')
                except:  # 处理 gbk 编码
                    print ">>> unicode 编码: obj.decode('gbk')"
                    return kw.decode('gbk')
            elif repr(kw).strip('\'').strip('"').startswith('\\\\u'):  # 处理无 u 的 unicode 编码
                print ">>> 无 u 的 unicode 编码: obj.decode('raw_unicode_escape')"
                return kw.decode('raw_unicode_escape')
            else:
                print ">>> unicode 编码: obj.decode('utf8')"
                return kw.decode('utf8')


def utf8_test(obj):
    print '>>> 转化为 utf8 编码'
    cc = CodeConvert()
    obj = cc.Convert2Utf8_test(obj)
    print '>>>', obj, '<==>', repr(obj), '\n'


def unicode_test(obj):
    print '>>> 转化为 unicode 编码'
    obj = CodeConvert.Convert2Unicode_test(obj)
    print '>>>', obj, '<==>', repr(obj), '\n'


def _Convert2Utf8():

    # u 内含 gbk 编码字串, 先encode('latin1')为gbk编码，再decode('gbk')为unicode编码，再encode('utf8')为utf8编码
    utf8_test(u'\xd7\xee\xba\xf3\xd2\xbb\xb8\xf6\xce\xca\xcc\xe2')

    # u 内含 utf8 编码字串, 直接encode('latin1')为utf8编码
    utf8_test(u'\xe6\x9c\x80\xe5\x90\x8e\xe4\xb8\x80\xe4\xb8\xaa\xe9\x97\xae\xe9\xa2\x98')

    # unicode 编码字串, 直接encode('utf8')为utf8编码
    utf8_test(u'\u6700\u540e\u4e00\u4e2a\u95ee\u9898')

    # gbk 编码字串, 先encode('latin1')为gbk编码，再decode('gbk')为unicode编码，再encode('utf8')为utf8编码
    utf8_test('\xd7\xee\xba\xf3\xd2\xbb\xb8\xf6\xce\xca\xcc\xe2')

    # utf8 编码字串, 直接return
    utf8_test('\xe6\x9c\x80\xe5\x90\x8e\xe4\xb8\x80\xe4\xb8\xaa\xe9\x97\xae\xe9\xa2\x98')

    # 无 u 的 unicode 编码字串, 先decode('raw_unicode_escape')为unicode编码, 再encode('utf8')为utf8编码
    utf8_test('\u6700\u540e\u4e00\u4e2a\u95ee\u9898')

    # utf8 编码汉字
    utf8_test('最后一个问题')

    # unicode 编码汉字
    utf8_test(u'最后一个问题')

    # utf8 编码英文
    utf8_test('The last question')

    # unicode 编码英文
    utf8_test(u'The last question')


def _Convert2Unicode():

    # u 内含 gbk 编码字串, 先encode('latin1')为gbk编码，再decode('gbk')为unicode编码
    unicode_test(u'\xd7\xee\xba\xf3\xd2\xbb\xb8\xf6\xce\xca\xcc\xe2')

    # u 内含 utf8 编码字串, 直接encode('latin1')为utf8编码, 再decode('utf8')为unicode编码
    unicode_test(u'\xe6\x9c\x80\xe5\x90\x8e\xe4\xb8\x80\xe4\xb8\xaa\xe9\x97\xae\xe9\xa2\x98')

    # unicode 编码字串, 直接return
    unicode_test(u'\u6700\u540e\u4e00\u4e2a\u95ee\u9898')

    # gbk 编码字串, 直接decode('gbk')为unicode编码
    unicode_test('\xd7\xee\xba\xf3\xd2\xbb\xb8\xf6\xce\xca\xcc\xe2')

    # utf8 编码字串, 直接decode('utf8')为unicode编码
    unicode_test('\xe6\x9c\x80\xe5\x90\x8e\xe4\xb8\x80\xe4\xb8\xaa\xe9\x97\xae\xe9\xa2\x98')

    # 无 u 的 unicode 编码字串, 直接decode('raw_unicode_escape')为unicode编码
    unicode_test('\u6700\u540e\u4e00\u4e2a\u95ee\u9898')

    # utf8 编码汉字
    unicode_test('最后一个问题')

    # unicode 编码汉字
    unicode_test(u'最后一个问题')

    # utf8 编码英文
    unicode_test('The last question')

    # unicode 编码英文
    unicode_test(u'The last question')


def main():
    _Convert2Utf8()
    _Convert2Unicode()

if __name__ == '__main__':
    main()
