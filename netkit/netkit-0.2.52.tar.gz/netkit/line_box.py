# -*- coding: utf-8 -*-
"""
以\n为每个包的结束
"""

import json

END_STR = '\n'


class LineBox(object):
    """
    LineBox 打包解包
    """

    # 如果调用unpack成功的话，会置为True
    _unpack_done = None

    _body = None

    def __init__(self, buf=None):
        self.reset()

        # 为了简写代码
        if buf:
            self.unpack(buf)

    @property
    def unpack_done(self):
        return self._unpack_done

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        if value.endswith(END_STR):
            self._body = value
        else:
            self._body = value + END_STR

        if isinstance(self._body, unicode):
            self._body = self._body.encode('utf-8')

    def reset(self):
        self._unpack_done = False

        self.body = ''

    def pack(self):
        """
        打包
        """
        return self.body

    def unpack(self, buf, save=True):
        """
        解析buf，并赋值

        :param buf:     输入buf
        :param save:    是否赋值
        :return:
            >0: 成功生成obj，返回了使用的长度，即剩余的部分buf要存起来
            <0: 报错
            0: 继续收
        """

        found_idx = buf.find(END_STR)
        if found_idx < 0:
            # 说明没有\n
            return 0

        packet_len = found_idx + 1

        if not save:
            # 如果不需要保存的话，就直接返回好了
            return packet_len

        self.body = buf[:packet_len]

        self._unpack_done = True

        return packet_len

    def check(self, buf):
        """
        仅检查buf是否合法

        :param buf:     输入buf
        :return:
            >0: 成功生成obj，返回了使用的长度，即剩余的部分buf要存起来
            <0: 报错
            0: 继续收
        """
        return self.unpack(buf, save=False)

    def get_json(self):
        """
        解析为json格式
        用函数而不是属性的原因参考requests、flask.request
        :return:
        """
        if not self.body:
            return None
        return json.loads(self.body)

    def set_json(self, value):
        """
        打包为json格式
        :return:
        """
        if not value:
            self.body = ''
            return
        self.body = json.dumps(value)

    def __repr__(self):
        return repr(self.body)
