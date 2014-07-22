# -*- coding: utf-8 -*-

__author__ = 'rsj217'


import os
import os.path
import re
import sys
import stat
from xiamiHttp import XiamiHttp
from xiamiParse import XiamiParser

# TODO GUI界面
# TODO 分离配置文件
# TODO 多线程下载
# TODO 下载专辑
class XiaMi(object):
    """  下载主要入口，处理用户输入，提供开发者api接口

    """

    def __init__(self, file):
        """ 初始化下载类型
        """
        self.category = {
            'mp3': ('song_url', 'mp3'),
            'lyric': ('lyric', 'Irc'),
            'picture': ('pic', 'jpg')
        }

        self._curdir = os.path.dirname(file)
        self._downdir = os.path.join(self._curdir, 'download')

    def start(self):
        """ 下载入口
        """
        # 处理用户输入，提取歌曲id
        self.song_id = self._get_song_id_from_input()
        # 通过歌曲id，获取请求json数据的url
        self.request_url = self._get_song_request_url(self.song_id)
        # 通过请求json的url地址，得到json数据
        self.song_json = self._get_song_json(self.request_url)
        # 解析json数据，获得歌曲信息
        self.song_info = self._get_song_info(self.song_json)

        # 开始下载
        # 下载音频
        sys.stdout.write('####### start download mp3 ####### \r')
        self._download('mp3')
        sys.stdout.write('####### download completed ####### \r')
        # 下载歌词
        sys.stdout.write('####### start download lyric ####### \r')
        self._download('lyric')
        sys.stdout.write('####### download completed ####### \r')
        # 下载专辑图片
        sys.stdout.write('####### start download pic ####### \r')
        self._download('picture')
        sys.stdout.write('####### download completed ####### \r')

    def _get_song_id_from_input(self):
        """  处理用户输入，提取歌曲id
        Return:
            song_id: 歌曲id
        """
        song_url = raw_input("Please enter the song url: ", )
        pattren = re.compile(r'/(\d+)\?')
        song_id = re.search(pattren, song_url).group(1)
        return song_id

    def _get_song_request_url(self, song_id):
        """  获取请求json数据的url
        Args:
            :param song_id: 歌曲的id
        Return:
            url: 请求json数据的url
        """
        url = ('http://www.xiami.com/'
               'song/playlist/id/{song_id}/'
               'object_name/default/object_id/0/cat/json').format(song_id=song_id)
        return url

    def _get_song_json(self, url):
        """  获取json数据
        Args:
            :param url: 请求json数据的url
        Return:
            j: 返回的json数据
        """
        res = XiamiHttp.send_request(url)
        j = XiamiHttp.get_res_json(res)
        return j

    def _get_song_info(self, data):
        """ 获取歌曲的信息
        Args:
            :param data: json数据
        Return:
            返回歌曲信息
        """
        return XiamiParser.get_song_info(data)

    def _checkout_directory(self, directory_name):
        """ 检查下载目录是否存在
        Args:
            :param directory_name: 下载的终极目录名
        """
        # 检查目录是否存在，如果不存在则新建
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
            # 目录权限 针对 *nix系统 mode:777
            os.chmod(directory_name, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)

    def _download(self, type='mp3'):
        """ 下载入口
        Args:
            :param type: 下载类型，默认为下载 mp3 音频
        """
        # 文件名
        file_name = self.song_id
        entry = self.category.get(type)
        # 文件扩展名
        extension_name = entry[1]
        req_url = self.song_info.get(entry[0])
        # 目录名
        download_directory = os.path.join(self._downdir, file_name)
        # 检查新建目录
        self._checkout_directory(download_directory)
        filename = os.path.join(download_directory, file_name)

        # 保存的文件完整路径
        file_name = '{filename}.{extension_name}'.\
            format(filename=filename, extension_name=extension_name)

        # 下载并保存文件
        XiamiHttp.save(req_url, file_name)

if __name__ == '__main__':
    url = 'http://www.xiami.com/song/1773346501?spm=a1z1s.3521865.23309997.1.254APJ'
    app = XiaMi()
    app.start()
