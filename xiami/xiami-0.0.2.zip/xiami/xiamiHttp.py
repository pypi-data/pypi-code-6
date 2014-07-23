# -*- coding: utf-8 -*-

""" 网络处理模块，发送请求json数据请求和发送下载请求下载文件
"""

__author__ = 'rsj217'

import json
import sys
import time
import urllib
import urllib2


class XiamiHttp(object):
    """ 网络处理类，发送请求json数据请求和发送下载请求下载文件
    """

    @staticmethod
    def send_request(url, timeout=10):
        """  发送http请求
        Args:
            :param  url: 请求的`url`
            :param  timeout: 网络请求超时限制，默认为10秒
        Return:
            返回 http response，包含请求响应的信息
        Exception:
            URLError 网络异常，远程主机无应答
            HTTPError 请求异常，返回异常数据
        """
        # headers信息
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        }
        # 装配请求
        req = urllib2.Request(
            url = url,
            headers = headers
        )
        # 发送请求
        try:
            res = urllib2.urlopen(req, timeout=timeout)
        except urllib2.URLError, e:
            raise e
        except urllib2.HTTPError, e:
            raise e
        else:
            return res

    @staticmethod
    def get_res_json(res):
        """ 解析请求，获得 json，并转换成python字典
        Args:
            :param res: 网络请求的响应
        Return:
            响应内容字典
        """
        d = json.load(res)
        return d

    @staticmethod
    def _schedule(downloaded_chunk_count, chunk_size, total_chunk_size):
        """ 显示下载进度条的函数
        Args:
            :param downloaded_chunk: 已经下载的数据库块（chunk）
            :param chunk_size: 数据块的大小
            :param total_chunk_size: 数据块的总大小
        """
        # 定义下载开始时间
        global start_time
        if downloaded_chunk_count == 0:
            start_time = time.time()
            return
        # 已下载总大小
        downloaded_size = downloaded_chunk_count * chunk_size
        # 下载所耗费的时间
        duration = time.time() - start_time
        try:
            # 下载的平均速度
            speed = downloaded_size / (1024 * duration)
        except Exception, e:
            return
        # 计算已经下载的百分比
        percent = 100 * float(downloaded_chunk_count) * chunk_size / total_chunk_size
        # 百分比修正
        if percent > 100:
            percent = 100
        sys.stdout.write('Downloaded %0.2f of  %0.2f M , speed %d KB/s , %d seconds passed  ( %0.2f%% )\n\r' % (
                                                                    float(downloaded_size) / (1024 ** 2),
                                                                    float(total_chunk_size) / (1024 ** 2),
                                                                    speed,
                                                                    duration,
                                                                    percent))
    @staticmethod
    def save(file_url, file_name):
        """ 使用 `urllib.urlretrieve` 下载文件
        Args:
            :param file_url: 下载文件的`url`地址
            :param file_name: 保存在本地的文件名
        """
        urllib.urlretrieve(file_url, file_name, XiamiHttp._schedule)

if __name__ == '__main__':

    url = 'http://www.xiami.com/song/playlist/id/1773346501/object_name/default/object_id/0/cat/json'
    res = XiamiHttp.send_request(url)
    print res
    d = XiamiHttp.get_res_json(res)
    print d
