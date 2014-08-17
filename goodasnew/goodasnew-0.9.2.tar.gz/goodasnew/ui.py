# Copyright (c) 2012, Wide Open Technologies. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer. Redistributions in
# binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution. THIS SOFTWARE IS
# PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import wx
import wx.lib.sized_controls as sc

class DownloadProgressDialog(sc.SizedDialog):
    def __init__(self, title, message, maximum=100, parent=None, style=wx.PD_AUTO_HIDE|wx.PD_APP_MODAL):
        super(DownloadProgressDialog, self).__init__(parent, -1, title, style=wx.DEFAULT_DIALOG_STYLE)
        
        panel = self.GetContentsPane()
        self.disabler = wx.WindowDisabler(self)
        self.message = wx.StaticText(panel, -1, message)
        self.keep_going = True
        self.finished = False
        self.maximum = maximum
        
        self.gauge = wx.Gauge(panel, -1, maximum)
        self.gauge.SetSizerProps(expand=True)
        
        self.btn_sizer = self.CreateStdDialogButtonSizer(wx.CANCEL)
        self.GetSizer().Add(self.btn_sizer, 0, wx.EXPAND | wx.BOTTOM | wx.RIGHT, self.GetDialogBorder())
        cancel_btn = self.FindWindowById(wx.ID_CANCEL)
        cancel_btn.Bind(wx.EVT_BUTTON, self.OnCancel)
            
        self.Fit()
        self.Show()
        
    def SetRange(self, range):
        self.gauge.SetRange(range)
        
    def OnCancel(self, event):
        if not self.finished:
            self.keep_going = False
        else:
            self.SetReturnCode(wx.ID_CANCEL)
            self.Hide()
        
    def Update(self, value, newmsg = None):
        if newmsg:
            self.message.Label = newmsg
            
        self.gauge.SetValue(value)
        if value == self.maximum:
            self.finished = True
            cancel_btn = self.FindWindowById(wx.ID_CANCEL)
            cancel_btn.Label = "Install and Restart"
            self.message.SetLabel("Download complete. Ready to install.")
            self.btn_sizer.RecalcSizes()
            self.btn_sizer.Layout()
            self.Layout()
            self.Refresh()
            
        wx.Yield()
        return self.keep_going, False
