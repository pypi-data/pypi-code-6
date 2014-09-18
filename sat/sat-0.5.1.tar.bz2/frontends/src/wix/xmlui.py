#!/usr/bin/python
# -*- coding: utf-8 -*-

# wix: a SAT frontend
# Copyright (C) 2009, 2010, 2011, 2012, 2013, 2014 Jérôme Poisson (goffi@goffi.org)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



from sat.core.i18n import _
import wx
from sat.core.log import getLogger
log = getLogger(__name__)
from sat_frontends.tools import xmlui
from sat_frontends.constants import Const as C


class EventWidget(object):
    """ Used to manage change event of  widgets """

    def _xmluiOnChange(self, callback):
        """ Call callback with widget as only argument """
        def change_cb(event):
            callback(self)
        self.Bind(self._xmlui_change_event, change_cb)


class WixWidget(object):
    _xmlui_proportion = 0


class ValueWidget(WixWidget):

    def _xmluiSetValue(self, value):
        self.SetValue(value)

    def _xmluiGetValue(self):
        return self.GetValue()


class EmptyWidget(WixWidget, xmlui.EmptyWidget, wx.Window):

    def __init__(self, _xmlui_parent):
        wx.Window.__init__(self, _xmlui_parent, -1)


class TextWidget(WixWidget, xmlui.TextWidget, wx.StaticText):

    def __init__(self, _xmlui_parent, value):
        wx.StaticText.__init__(self, _xmlui_parent, -1, value)


class LabelWidget(xmlui.LabelWidget, TextWidget):

    def __init__(self, _xmlui_parent, value):
        super(LabelWidget, self).__init__(_xmlui_parent, value+": ")


class JidWidget(xmlui.JidWidget, TextWidget):
    pass


class DividerWidget(WixWidget, xmlui.DividerWidget, wx.StaticLine):

    def __init__(self, _xmlui_parent, style='line'):
        wx.StaticLine.__init__(self, _xmlui_parent, -1)


class StringWidget(EventWidget, ValueWidget, xmlui.StringWidget, wx.TextCtrl):
    _xmlui_change_event = wx.EVT_TEXT

    def __init__(self, _xmlui_parent, value, read_only=False):
        style = wx.TE_READONLY if read_only else 0
        wx.TextCtrl.__init__(self, _xmlui_parent, -1, value, style=style)
        self._xmlui_proportion = 1


class PasswordWidget(EventWidget, ValueWidget, xmlui.PasswordWidget, wx.TextCtrl):
    _xmlui_change_event = wx.EVT_TEXT

    def __init__(self, _xmlui_parent, value, read_only=False):
        style = wx.TE_PASSWORD
        if read_only:
            style |= wx.TE_READONLY
        wx.TextCtrl.__init__(self, _xmlui_parent, -1, value, style=style)
        self._xmlui_proportion = 1


class TextBoxWidget(EventWidget, ValueWidget, xmlui.TextBoxWidget, wx.TextCtrl):
    _xmlui_change_event = wx.EVT_TEXT

    def __init__(self, _xmlui_parent, value, read_only=False):
        style = wx.TE_MULTILINE
        if read_only:
            style |= wx.TE_READONLY
        wx.TextCtrl.__init__(self, _xmlui_parent, -1, value, style=style)
        self._xmlui_proportion = 1


class BoolWidget(EventWidget, ValueWidget, xmlui.BoolWidget, wx.CheckBox):
    _xmlui_change_event = wx.EVT_CHECKBOX

    def __init__(self, _xmlui_parent, state, read_only=False):
        style = wx.CHK_2STATE
        if read_only:
            style |= wx.TE_READONLY
        wx.CheckBox.__init__(self, _xmlui_parent, -1, "", style=wx.CHK_2STATE)
        self.SetValue(state)
        self._xmlui_proportion = 1

    def _xmluiSetValue(self, value):
        self.SetValue(value == 'true')

    def _xmluiGetValue(self):
        return "true" if self.GetValue() else "false"


class ButtonWidget(EventWidget, WixWidget, xmlui.ButtonWidget, wx.Button):
    _xmlui_change_event = wx.EVT_BUTTON

    def __init__(self, _xmlui_parent, value, click_callback):
        wx.Button.__init__(self, _xmlui_parent, -1, value)
        self._xmlui_click_callback = click_callback
        _xmlui_parent.Bind(wx.EVT_BUTTON, lambda evt: click_callback(evt.GetEventObject()), self)
        self._xmlui_parent = _xmlui_parent

    def _xmluiOnClick(self, callback):
        self._xmlui_parent.Bind(wx.EVT_BUTTON, lambda evt: callback(evt.GetEventObject()), self)


class ListWidget(EventWidget, WixWidget, xmlui.ListWidget, wx.ListBox):
    _xmlui_change_event = wx.EVT_LISTBOX

    def __init__(self, _xmlui_parent, options, selected, flags):
        styles = wx.LB_MULTIPLE if not 'single' in flags else wx.LB_SINGLE
        wx.ListBox.__init__(self, _xmlui_parent, -1, choices=[option[1] for option in options], style=styles)
        self._xmlui_attr_map = {label: value for value, label in options}
        self._xmlui_proportion = 1
        self._xmluiSelectValues(selected)

    def _xmluiSelectValue(self, value):
        try:
            label = [label for label, _value in self._xmlui_attr_map.items() if _value == value][0]
        except IndexError:
            log.warning(_("Can't find value [%s] to select" % value))
            return
        for idx in xrange(self.GetCount()):
            self.SetSelection(idx, self.GetString(idx) == label)

    def _xmluiSelectValues(self, values):
        labels = [label for label, _value in self._xmlui_attr_map.items() if _value in values]
        for idx in xrange(self.GetCount()):
            self.SetSelection(idx, self.GetString(idx) in labels)

    def _xmluiGetSelectedValues(self):
        ret = []
        labels = [self.GetString(idx) for idx in self.GetSelections()]
        for label in labels:
            ret.append(self._xmlui_attr_map[label])
        return ret

    def _xmluiAddValues(self, values, select=True):
        selected = self._xmluiGetSelectedValues()
        for value in values:
            if value not in self._xmlui_attr_map.values():
                wx.ListBox.Append(self, value)
                self._xmlui_attr_map[value] = value
            if value not in selected:
                selected.append(value)
        self._xmluiSelectValues(selected)


class WixContainer(object):
    _xmlui_proportion = 1

    def _xmluiAppend(self, widget):
        self.sizer.Add(widget, self._xmlui_proportion, flag=wx.EXPAND)


class AdvancedListContainer(WixContainer, xmlui.AdvancedListContainer, wx.ScrolledWindow):

    def __init__(self, _xmlui_parent, columns, selectable='no'):
        wx.ScrolledWindow.__init__(self, _xmlui_parent)
        self._xmlui_selectable = selectable != 'no'
        if selectable:
            columns += 1
        self.sizer = wx.FlexGridSizer(cols=columns)
        self.SetSizer(self.sizer)
        self._xmlui_select_cb = None
        self._xmlui_select_idx = None
        self._xmlui_select_widgets = []

    def _xmluiAddRow(self, idx):
        # XXX: select_button is a Q&D way to implement row selection
        # FIXME: must be done properly
        if not self._xmlui_selectable:
            return
        select_button = wx.Button(self, wx.ID_OK, label=_("select"))
        self.sizer.Add(select_button)
        def click_cb(event, idx=idx):
            cb = self._xmlui_select_cb
            self._xmlui_select_idx = idx
            # TODO: fill self._xmlui_select_widgets
            if cb is not None:
                cb(self)
            event.Skip()
        self.Bind(wx.EVT_BUTTON, click_cb)

    def _xmluiGetSelectedWidgets(self):
        return self._xmlui_select_widgets

    def _xmluiGetSelectedIndex(self):
        return self._xmlui_select_idx

    def _xmluiOnSelect(self, callback):
        self._xmlui_select_cb = callback

class PairsContainer(WixContainer, xmlui.PairsContainer, wx.Panel):

    def __init__(self, _xmlui_parent):
        wx.Panel.__init__(self, _xmlui_parent)
        self.sizer = wx.FlexGridSizer(cols=2)
        self.sizer.AddGrowableCol(1) #The growable column need most of time to be the right one in pairs
        self.SetSizer(self.sizer)


class TabsContainer(WixContainer, xmlui.TabsContainer, wx.Notebook):

    def __init__(self, _xmlui_parent):
        wx.Notebook.__init__(self, _xmlui_parent, -1, style=wx.NB_LEFT if self._xmlui_main.type=='param' else 0)

    def _xmluiAddTab(self, label):
        tab_panel = wx.Panel(self, -1)
        tab_panel.sizer = wx.BoxSizer(wx.VERTICAL)
        tab_panel.SetSizer(tab_panel.sizer)
        self.AddPage(tab_panel, label)
        VerticalContainer._xmluiAdapt(tab_panel)
        return tab_panel


class VerticalContainer(WixContainer, xmlui.VerticalContainer, wx.Panel):

    def __init__(self, _xmlui_parent):
        wx.Panel.__init__(self, _xmlui_parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)


## Dialogs ##


class WixDialog(object):

    def __init__(self, _xmlui_parent, level):
        self.host = _xmlui_parent.host
        self.ok_cb = None
        self.cancel_cb = None
        if level == C.XMLUI_DATA_LVL_INFO:
            self.flags = wx.ICON_INFORMATION
        elif level == C.XMLUI_DATA_LVL_ERROR:
            self.flags = wx.ICON_ERROR
        else:
            self.flags = wx.ICON_INFORMATION
            log.warning(_("Unmanaged dialog level: %s") % level)

    def _xmluiShow(self):
        answer = self.ShowModal()
        if answer == wx.ID_YES or answer == wx.ID_OK:
            self._xmluiValidated()
        else:
            self._xmluiCancelled()

    def _xmluiClose(self):
        self.Destroy()


class MessageDialog(WixDialog, xmlui.MessageDialog, wx.MessageDialog):

    def __init__(self, _xmlui_parent, title, message, level):
        WixDialog.__init__(self, _xmlui_parent, level)
        xmlui.MessageDialog.__init__(self, _xmlui_parent)
        self.flags |= wx.OK
        wx.MessageDialog.__init__(self, _xmlui_parent.host, message, title, style = self.flags)


class NoteDialog(xmlui.NoteDialog, MessageDialog):
    # TODO: separate NoteDialog
    pass


class ConfirmDialog(WixDialog, xmlui.ConfirmDialog, wx.MessageDialog):

    def __init__(self, _xmlui_parent, title, message, level, buttons_set):
        WixDialog.__init__(self, _xmlui_parent, level)
        xmlui.ConfirmDialog.__init__(self, _xmlui_parent)
        if buttons_set == C.XMLUI_DATA_BTNS_SET_YESNO:
            self.flags |= wx.YES_NO
        else:
            self.flags |= wx.OK | wx.CANCEL
        wx.MessageDialog.__init__(self, _xmlui_parent.host, message, title, style = self.flags)


class FileDialog(WixDialog, xmlui.FileDialog, wx.FileDialog):

    def __init__(self, _xmlui_parent, title, message, level, filetype):
        # TODO: message and filetype are not managed yet
        WixDialog.__init__(self, _xmlui_parent, level)
        self.flags = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT # FIXME: use the legacy flags, but must manage cases like dir or open
        xmlui.FileDialog.__init__(self, _xmlui_parent)
        wx.FileDialog.__init__(self, _xmlui_parent.host, title, style = self.flags)

    def _xmluiShow(self):
        answer = self.ShowModal()
        if answer == wx.ID_OK:
            self._xmluiValidated({'path': self.GetPath()})
        else:
            self._xmluiCancelled()


class GenericFactory(object):

    def __getattr__(self, attr):
        if attr.startswith("create"):
            cls = globals()[attr[6:]]
            return cls


class WidgetFactory(GenericFactory):

    def __getattr__(self, attr):
        if attr.startswith("create"):
            cls = GenericFactory.__getattr__(self, attr)
            cls._xmlui_main = self._xmlui_main
            return cls


class XMLUIPanel(xmlui.XMLUIPanel, wx.Frame):
    """Create an user interface from a SàT XML"""
    widget_factory = WidgetFactory()

    def __init__(self, host, parsed_xml, title=None, flags = None,):
        self.widget_factory._xmlui_main = self
        xmlui.XMLUIPanel.__init__(self, host, parsed_xml, title, flags)

    def constructUI(self, parsed_dom):
        style = wx.DEFAULT_FRAME_STYLE & ~wx.CLOSE_BOX if 'NO_CANCEL' in self.flags else wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, None, style=style)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        def postTreat():
            if self.title:
                self.SetTitle(self.title)

            if self.type == 'form':
                dialogButtons = wx.StdDialogButtonSizer()
                submitButton = wx.Button(self.main_cont,wx.ID_OK, label=_("Submit"))
                dialogButtons.AddButton(submitButton)
                self.main_cont.Bind(wx.EVT_BUTTON, self.onFormSubmitted, submitButton)
                if not 'NO_CANCEL' in self.flags:
                    cancelButton = wx.Button(self.main_cont,wx.ID_CANCEL)
                    dialogButtons.AddButton(cancelButton)
                    self.main_cont.Bind(wx.EVT_BUTTON, self.onFormCancelled, cancelButton)
                dialogButtons.Realize()
                self.main_cont.sizer.Add(dialogButtons, flag=wx.ALIGN_CENTER_HORIZONTAL)

            self.sizer.Add(self.main_cont, 1, flag=wx.EXPAND)
            self.sizer.Fit(self)
            self.Show()

        super(XMLUIPanel, self).constructUI(parsed_dom, postTreat)
        if not 'NO_CANCEL' in self.flags:
            self.Bind(wx.EVT_CLOSE, self.onClose, self)
        self.MakeModal()

    def _xmluiClose(self):
        self.MakeModal(False)
        self.Destroy()

    ###events

    def onParamChange(self, ctrl):
        super(XMLUIPanel, self).onParamChange(ctrl)

    def onFormSubmitted(self, event):
        """Called when submit button is clicked"""
        button = event.GetEventObject()
        super(XMLUIPanel, self).onFormSubmitted(button)

    def onClose(self, event):
        """Close event: we have to send the form."""
        log.debug(_("close"))
        if self.type == 'param':
            self.onSaveParams()
        else:
            self._xmluiClose()
        event.Skip()


class XMLUIDialog(xmlui.XMLUIDialog):
    dialog_factory = WidgetFactory()


xmlui.registerClass(xmlui.CLASS_PANEL, XMLUIPanel)
xmlui.registerClass(xmlui.CLASS_DIALOG, XMLUIDialog)
create = xmlui.create
