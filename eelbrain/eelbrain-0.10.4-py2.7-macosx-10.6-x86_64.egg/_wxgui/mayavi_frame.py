# Author: Christian Brodbeck <christianbrodbeck@nyu.edu>
import wx


class MayaviFrame(wx.Frame):
    def __init__(self, parent=None, id=wx.ID_ANY):
        wx.Frame.__init__(self, parent, id, 'Mayavi in Wx')
        self.visualization = Visualization()
        self.control = self.visualization.edit_traits(parent=self,
                                kind='subpanel').control
        self.Show()
