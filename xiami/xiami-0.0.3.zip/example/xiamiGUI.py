# -*- coding: utf-8 -*-

__author__ = 'rsj217'

import sys    
import wx
import time

class xiamiFrame(wx.Frame):
    '''
    创建一个Frame类
    '''
    def __init__(self, parent, id, title):
        super(xiamiFrame, self).__init__(parent, id, title, size=(600, 400),
                                          style=wx.STAY_ON_TOP|wx.DEFAULT_FRAME_STYLE)
        # 程序面板
        self.panel = wx.Panel(self)
        color = wx.Colour(236, 230, 217)
        self.panel.SetBackgroundColour(color)
        # 状态栏
        self.CreateStatusBar()
        self.SetStatusText('Welcome to xiami music download tool')
        menuBar = wx.MenuBar()
        # 菜单栏 文件
        menuFile = wx.Menu()
        exitItem = menuFile.Append(-1, '&Exit', 'Exit the xiami music download')
        menuBar.Append(menuFile, 'File')
        self.Bind(wx.EVT_MENU, self.OnCloseWindow, exitItem)
        # 菜单栏 关于
        menuAbout = wx.Menu()
        menuBar.Append(menuAbout, 'About')
        aboutItem = menuAbout.Append(-1, '&About', 'Exit the xiami music download')
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        # 设置菜单栏
        self.SetMenuBar(menuBar)
        # 欢迎标题
        welcome = wx.StaticText(self.panel, -1, label='XiamiMusic DownLoad v 0.01 ', pos=(130, 30), size=(200, 30))
        font = wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        welcome.SetFont(font)

        # url文本输入框
        self.textInput = wx.TextCtrl(self.panel, -1, 'Please Enter URL Of The Song', pos=(30, 80), size=(520, 30), style=wx.TE_NOHIDESEL)
        self.textInput.SetBackgroundColour('white')
        self.textInput.SetInsertionPoint(0)
        # 下载信息显示框
        self.textMessage = wx.TextCtrl(self.panel, -1, '---------Download Message--------- \n',
                                       pos=(30, 180), size=(520, 130),
                                       style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.textMessage.SetBackgroundColour('white')
        self.textMessage.SetInsertionPoint(0)

        # 重定向输入
        # redir = RedirectText(self.textMessage)
        # sys.stdout = redir

        # 下载按钮
        btnDownload = wx.Button(self.panel, label='start', pos=(300, 120), size=(120, 30))
        self.Bind(wx.EVT_BUTTON, self.OnDownload, btnDownload)
        # 重置按钮
        btnReset = wx.Button(self.panel, label='reset', pos=(430, 120), size=(120, 30))
        # 绑定事件
        self.Bind(wx.EVT_BUTTON, self.OnReset, btnReset)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)


    def OnDownload(self, event):

        def _schedule(downloaded_chunk_count, chunk_size, total_chunk_size):

            downloaded_size = downloaded_chunk_count * chunk_size

            if downloaded_chunk_count == 0:
                self.start_time = time.time()
                return

            # 下载所耗费的时间
            duration = time.time() - self.start_time
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

            download_message = 'Downloaded %0.2f of  %0.2f M , speed %d KB/s , %d seconds passed  ( %0.2f%% )\n\r' % (
                                                                    round(float(downloaded_size) / (1024 ** 2), 2),
                                                                    round(float(total_chunk_size) / (1024 ** 2), 2),
                                                                    speed,
                                                                    duration,
                                                                    percent)

            self.SetStatusText(download_message)

        from xiami import XiaMi
        song_info_url = self.textInput.GetValue()

        xiami = XiaMi(__file__)
        try:
            xiami.start(song_info_url)
        except Exception, e:
            dlg = wx.MessageBox(message='Url Error, Please Enter A Correct Url', caption='Warning', style=wx.OK)
            return

        self.textMessage.Clear()
        self.textMessage.AppendText('Download MP3 \n')
        download_mp3 = xiami.download_mp3(download_call=_schedule)
        if download_mp3:
            self.SetStatusText('MP3 Download Successfully')
            self.textMessage.AppendText('Download Successfully\n')

        self.textMessage.AppendText('Download Lyric \n')
        download_lyirc = xiami.download_lyric(download_call=_schedule)
        if download_lyirc:
            self.SetStatusText('Lyirc Download Successfully')
            self.textMessage.AppendText('Download Successfully\n')

        self.textMessage.AppendText('Download PIC\n')
        download_pic = xiami.download_pic(download_call=_schedule)
        if download_pic:
            self.SetStatusText('Pic Download Successfully')
            self.textMessage.AppendText('Download Successfully')
        self.SetStatusText('All Download Successfully')

    def OnReset(self, event):
        self.textInput.SetValue('')

    def OnCloseWindow(self, event):
        self.Destroy()

    def OnAbout(self, event):
        pass
              
class XiaMi(wx.App):
    '''
    创建一个App类
    '''
    def __init__(self, redirect=False, filename=None):
        super(XiaMi, self).__init__(redirect, filename)
        
    def OnInit(self):

        self.frame = xiamiFrame(parent=None,
                                id=-1,
                                title=u"xiami music download")
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
    
    def OnExit(self):
        pass

class RedirectText():

    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        self.out.WriteText(string)


def main():
    app = XiaMi()
    app.MainLoop()    
    
if __name__ == '__main__':
    main()    
        