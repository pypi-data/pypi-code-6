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
from sat_frontends.wix.constants import Const as C
from sat_frontends.quick_frontend.quick_chat_list import QuickChatList
from sat_frontends.quick_frontend.quick_app import QuickApp
import wx
from sat_frontends.wix.contact_list import ContactList
from sat_frontends.wix.chat import Chat
from sat_frontends.wix import xmlui
from sat_frontends.wix.profile import Profile
from sat_frontends.wix.profile_manager import ProfileManager
import os.path
from sat_frontends.tools.jid  import JID
from sat.core.log import getLogger
log = getLogger(__name__)
from sat_frontends.wix.constants import Const

idCONNECT,\
idDISCONNECT,\
idEXIT,\
idABOUT,\
idPARAM,\
idSHOW_PROFILE,\
idJOIN_ROOM,\
 = range(7)

class ChatList(QuickChatList):
    """This class manage the list of chat windows"""

    def createChat(self, target):
        return Chat(target, self.host)

class MainWindow(wx.Frame, QuickApp):
    """main app window"""

    def __init__(self):
        QuickApp.__init__(self)
        wx.Frame.__init__(self,None, title="SàT Wix", size=(350,500))

        #sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        #Frame elements
        self.contact_list = ContactList(self, self)
        self.contact_list.registerActivatedCB(self.onContactActivated)
        self.contact_list.Hide()
        self.sizer.Add(self.contact_list, 1, flag=wx.EXPAND)

        self.chat_wins=ChatList(self)
        self.CreateStatusBar()

        #ToolBar
        self.tools=self.CreateToolBar()
        self.statusBox = wx.ComboBox(self.tools, -1, "Online", choices=[status[1] for status in Const.PRESENCE],
                                      style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.tools.AddControl(self.statusBox)
        self.tools.AddSeparator()
        self.statusTxt = wx.TextCtrl(self.tools, -1, style=wx.TE_PROCESS_ENTER)
        self.tools.AddControl(self.statusTxt)
        self.Bind(wx.EVT_COMBOBOX, self.onStatusChange, self.statusBox)
        self.Bind(wx.EVT_TEXT_ENTER, self.onStatusChange, self.statusTxt)
        self.tools.Disable()

        #tray icon
        ticon = wx.Icon(os.path.join(self.media_dir, 'icons/crystal/32/tray_icon.xpm'), wx.BITMAP_TYPE_XPM)
        self.tray_icon = wx.TaskBarIcon()
        self.tray_icon.SetIcon(ticon, _("Wix jabber client"))
        wx.EVT_TASKBAR_LEFT_UP(self.tray_icon, self.onTrayClick)


        #events
        self.Bind(wx.EVT_CLOSE, self.onClose, self)


        #profile panel
        self.profile_pan = ProfileManager(self)
        self.sizer.Add(self.profile_pan, 1, flag=wx.EXPAND)

        self.postInit()

        self.Show()

    def plug_profile_1(self, profile_key='@DEFAULT@'):
        """Hide profile panel then plug profile"""
        log.debug (_('plugin profile %s' % profile_key))
        self.profile_pan.Hide()
        self.contact_list.Show()
        self.sizer.Layout()
        super(MainWindow, self).plug_profile_1(profile_key)
        #menus
        self.createMenus()

    def addMenus(self, menubar, type_, menu_data=None):
        """Add cached menus to instance
        @param menu: wx.MenuBar instance
        @param type_: menu type like is sat.core.sat_main.importMenu
        @param menu_data: data to send with these menus

        """
        menus = self.profiles[self.profile]['menus'].get(type_,[])
        for id_, path, path_i18n  in menus:
            if len(path) != 2:
                raise NotImplementedError("Menu with a path != 2 are not implemented yet")
            category = path_i18n[0] # TODO: manage path with more than 2 levels
            name = path_i18n[1]
            menu_idx = menubar.FindMenu(category)
            current_menu = None
            if menu_idx == wx.NOT_FOUND:
                #the menu is new, we create it
                current_menu = wx.Menu()
                menubar.Append(current_menu, category)
            else:
                current_menu = menubar.GetMenu(menu_idx)
            assert(current_menu != None)
            item_id = wx.NewId()
            help_string = self.bridge.getMenuHelp(id_, '')
            current_menu.Append(item_id, name, help=help_string)
            #now we register the event
            def event_answer(e, id_=id_):
                self.launchAction(id_, menu_data, profile_key = self.profile)

            wx.EVT_MENU(menubar.Parent, item_id, event_answer)

    def createMenus(self):
        log.info(_("Creating menus"))
        connectMenu = wx.Menu()
        connectMenu.Append(idCONNECT, _("&Connect	CTRL-c"),_(" Connect to the server"))
        connectMenu.Append(idDISCONNECT, _("&Disconnect	CTRL-d"),_(" Disconnect from the server"))
        connectMenu.Append(idPARAM,_("&Parameters"),_(" Configure the program"))
        connectMenu.AppendSeparator()
        connectMenu.Append(idABOUT, _("A&bout"), _(" About %s") % Const.APP_NAME)
        connectMenu.Append(idEXIT,_("E&xit"),_(" Terminate the program"))
        contactMenu = wx.Menu()
        communicationMenu = wx.Menu()
        communicationMenu.Append(idJOIN_ROOM, _("&Join Room"),_(" Join a Multi-User Chat room"))
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(connectMenu,_("&General"))
        self.menuBar.Append(contactMenu,_("&Contacts"))
        self.menuBar.Append(communicationMenu,_("&Communication"))
        self.SetMenuBar(self.menuBar)

        #additionals menus
        #FIXME: do this in a more generic way (in quickapp)
        self.addMenus(self.menuBar, C.MENU_GLOBAL)

        # menu items that should be displayed after the automatically added ones
        contactMenu.AppendSeparator()
        contactMenu.Append(idSHOW_PROFILE, _("&Show profile"), _(" Show contact's profile"))

        #events
        wx.EVT_MENU(self, idCONNECT, self.onConnectRequest)
        wx.EVT_MENU(self, idDISCONNECT, self.onDisconnectRequest)
        wx.EVT_MENU(self, idPARAM, self.onParam)
        wx.EVT_MENU(self, idABOUT, self.onAbout)
        wx.EVT_MENU(self, idEXIT, self.onExit)
        wx.EVT_MENU(self, idSHOW_PROFILE, self.onShowProfile)
        wx.EVT_MENU(self, idJOIN_ROOM, self.onJoinRoom)

    def newMessageHandler(self, from_jid, to_jid, msg, _type, extra, profile):
        QuickApp.newMessageHandler(self, from_jid, to_jid, msg, _type, extra, profile)

    def showAlert(self, message):
        # TODO: place this in a separate class
        popup=wx.PopupWindow(self)
        ### following code come from wxpython demo
        popup.SetBackgroundColour("CADET BLUE")
        st = wx.StaticText(popup, -1, message, pos=(10,10))
        sz = st.GetBestSize()
        popup.SetSize( (sz.width+20, sz.height+20) )
        x=(wx.DisplaySize()[0]-popup.GetSize()[0])/2
        popup.SetPosition((x,0))
        popup.Show()
        wx.CallLater(5000,popup.Destroy)

    def showDialog(self, message, title="", type_="info", answer_cb = None, answer_data = None):
        if type_ == 'info':
            flags = wx.OK | wx.ICON_INFORMATION
        elif type_ == 'error':
            flags = wx.OK | wx.ICON_ERROR
        elif type_ == 'yes/no':
            flags = wx.YES_NO | wx.ICON_QUESTION
        else:
            flags = wx.OK | wx.ICON_INFORMATION
            log.error(_('unmanaged dialog type: %s'), type_)
        dlg = wx.MessageDialog(self, message, title, flags)
        answer = dlg.ShowModal()
        dlg.Destroy()
        if answer_cb:
            data = [answer_data] if answer_data else []
            answer_cb(True if (answer == wx.ID_YES or answer == wx.ID_OK) else False, *data)

    def setStatusOnline(self, online=True, show="", statuses={}):
        """enable/disable controls, must be called when local user online status change"""
        if online:
            self.SetStatusText(Const.msgONLINE)
            self.tools.Enable()
            try:
                presence = [x for x in Const.PRESENCE if x[0] == show][0][1]
                self.statusBox.SetValue(presence)
            except (TypeError, IndexError):
                pass
            try:
                self.statusTxt.SetValue(statuses['default'])
            except (TypeError, KeyError):
                pass
        else:
            self.SetStatusText(Const.msgOFFLINE)
            self.tools.Disable()
        return

    def launchAction(self, callback_id, data=None, profile_key="@NONE@"):
        """ Launch a dynamic action
        @param callback_id: id of the action to launch
        @param data: data needed only for certain actions
        @param profile_key: %(doc_profile_key)s

        """
        if data is None:
            data = dict()
        def action_cb(data):
            if not data:
                # action was a one shot, nothing to do
                pass
            elif "xmlui" in data:
                log.debug (_("XML user interface received"))
                ui = xmlui.create(self, xml_data = data['xmlui'])
                ui.show()
            elif "authenticated_profile" in data:
                assert("caller" in data)
                if data["caller"] == "profile_manager":
                    assert(self.profile_pan.IsShown())
                    self.profile_pan.getXMPPParams(data['authenticated_profile'])
                elif data["caller"] == "plug_profile":
                    self.plug_profile_1(data['authenticated_profile'])
                else:
                    raise NotImplementedError
            else:
                dlg = wx.MessageDialog(self, _(u"Unmanaged action result"),
                                       _('Error'),
                                       wx.OK | wx.ICON_ERROR
                                      )
                dlg.ShowModal()
                dlg.Destroy()
        def action_eb(failure):
            dlg = wx.MessageDialog(self, failure.message,
                                   failure.fullname,
                                   wx.OK | wx.ICON_ERROR
                                  )
            dlg.ShowModal()
            dlg.Destroy()

        self.bridge.launchAction(callback_id, data, profile_key, callback=action_cb, errback=action_eb)

    def askConfirmationHandler(self, confirmation_id, confirmation_type, data, profile):
        #TODO: refactor this in QuickApp
        if not self.check_profile(profile):
            return
        log.debug (_("Confirmation asked"))
        answer_data={}
        if confirmation_type == "FILE_TRANSFER":
            log.debug (_("File transfer confirmation asked"))
            dlg = wx.MessageDialog(self, _("The contact %(jid)s wants to send you the file %(filename)s\nDo you accept ?") % {'jid':data["from"], 'filename':data["filename"]},
                                   _('File Request'),
                                   wx.YES_NO | wx.ICON_QUESTION
                                  )
            answer=dlg.ShowModal()
            if answer==wx.ID_YES:
                filename = wx.FileSelector(_("Where do you want to save the file ?"), flags = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if filename:
                    answer_data["dest_path"] = filename
                    self.bridge.confirmationAnswer(confirmation_id, True, answer_data, profile)
                    self.waitProgress(confirmation_id, _("File Transfer"), _("Copying %s") % os.path.basename(filename), profile)
                else:
                    answer = wx.ID_NO
            if answer==wx.ID_NO:
                    self.bridge.confirmationAnswer(confirmation_id, False, answer_data, profile)

            dlg.Destroy()

        elif confirmation_type == "YES/NO":
            log.debug (_("Yes/No confirmation asked"))
            dlg = wx.MessageDialog(self, data["message"],
                                   _('Confirmation'),
                                   wx.YES_NO | wx.ICON_QUESTION
                                  )
            answer=dlg.ShowModal()
            if answer==wx.ID_YES:
                self.bridge.confirmationAnswer(confirmation_id, True, {}, profile)
            if answer==wx.ID_NO:
                self.bridge.confirmationAnswer(confirmation_id, False, {}, profile)

            dlg.Destroy()

    def actionResultHandler(self, type_, id_, data, profile):
        if not self.check_profile(profile):
            return
        log.debug (_("actionResult: type_ = [%(type_)s] id_ = [%(id_)s] data = [%(data)s]") % {'type_':type_, 'id_':id_, 'data':data})
        if not id_ in self.current_action_ids:
            log.debug (_('unknown id_, ignoring'))
            return
        if type_ == "SUPPRESS":
            self.current_action_ids.remove(id_)
        elif type_ == "SUCCESS":
            self.current_action_ids.remove(id_)
            dlg = wx.MessageDialog(self, data["message"],
                                   _('Success'),
                                   wx.OK | wx.ICON_INFORMATION
                                  )
            dlg.ShowModal()
            dlg.Destroy()
        elif type_ == "ERROR":
            self.current_action_ids.remove(id_)
            dlg = wx.MessageDialog(self, data["message"],
                                   _('Error'),
                                   wx.OK | wx.ICON_ERROR
                                  )
            dlg.ShowModal()
            dlg.Destroy()
        elif type_ == "XMLUI":
            self.current_action_ids.remove(id_)
            log.debug (_("XML user interface received"))
            misc = {}
            #FIXME FIXME FIXME: must clean all this crap !
            title = _('Form')
            if data['type_'] == _('registration'):
                title = _('Registration')
                misc['target'] = data['target']
                misc['action_back'] = self.bridge.gatewayRegister
            xmlui.create(self, title=title, xml_data = data['xml'], misc = misc)
        elif type_ == "RESULT":
            self.current_action_ids.remove(id_)
            if self.current_action_ids_cb.has_key(id_):
                callback = self.current_action_ids_cb[id_]
                del self.current_action_ids_cb[id_]
                callback(data)
        elif type_ == "DICT_DICT":
            self.current_action_ids.remove(id_)
            if self.current_action_ids_cb.has_key(id_):
                callback = self.current_action_ids_cb[id_]
                del self.current_action_ids_cb[id_]
                callback(data)
        else:
            log.error (_("FIXME FIXME FIXME: type_ [%s] not implemented") % type_)
            raise NotImplementedError



    def progressCB(self, progress_id, title, message, profile):
        data = self.bridge.getProgress(progress_id, profile)
        if data:
            if not self.pbar:
                #first answer, we must construct the bar
                self.pbar = wx.ProgressDialog(title, message, float(data['size']), None,
                    wx.PD_SMOOTH | wx.PD_ELAPSED_TIME | wx.PD_ESTIMATED_TIME | wx.PD_REMAINING_TIME)
                self.pbar.finish_value = float(data['size'])

            self.pbar.Update(int(data['position']))
        elif self.pbar:
            self.pbar.Update(self.pbar.finish_value)
            return

        wx.CallLater(10, self.progressCB, progress_id, title, message, profile)

    def waitProgress (self, progress_id, title, message, profile):
        self.pbar = None
        wx.CallLater(10, self.progressCB, progress_id, title, message, profile)



    ### events ###

    def onContactActivated(self, jid):
        log.debug (_("onContactActivated: %s"), jid)
        if self.chat_wins[jid.bare].IsShown():
            self.chat_wins[jid.bare].Hide()
        else:
            self.chat_wins[jid.bare].Show()

    def onConnectRequest(self, e):
        QuickApp.asyncConnect(self, self.profile)

    def onDisconnectRequest(self, e):
        self.bridge.disconnect(self.profile)

    def __updateStatus(self):
        show = [x for x in Const.PRESENCE if x[1] == self.statusBox.GetValue()][0][0]
        status = self.statusTxt.GetValue()
        self.bridge.setPresence(show=show, statuses={'default': status}, profile_key=self.profile)  #FIXME: manage multilingual statuses

    def onStatusChange(self, e):
        log.debug(_("Status change request"))
        self.__updateStatus()

    def onParam(self, e):
        log.debug(_("Param request"))
        def success(params):
            xmlui.create(self, xml_data=params, title=_("Configuration"))

        def failure(error):
            dlg = wx.MessageDialog(self, error.message,
                                   error.fullname,
                                   wx.OK | wx.ICON_ERROR
                                  )
            dlg.ShowModal()
            dlg.Destroy()
        self.bridge.getParamsUI(app=Const.APP_NAME, profile_key=self.profile, callback=success, errback=failure)

    def onAbout(self, e):
        about = wx.AboutDialogInfo()
        about.SetName(Const.APP_NAME)
        about.SetVersion (unicode(self.bridge.getVersion()))
        about.SetCopyright(u"(C) 2009, 2010, 2011, 2012, 2013, 2014 Jérôme Poisson aka Goffi")
        about.SetDescription( _(u"%(name)s is a SàT (Salut à Toi) frontend\n"+
        u"%(name)s is based on WxPython, and is the standard graphic interface of SàT") % {'name': Const.APP_NAME})
        about.SetWebSite(("http://www.goffi.org", "Goffi's non-hebdo (french)"))
        about.SetDevelopers([ "Goffi (Jérôme Poisson)"])
        try:
            with open(Const.LICENCE_PATH, "r") as licence:
                about.SetLicence(''.join(licence.readlines()))
        except:
            pass

        wx.AboutBox(about)

    def onExit(self, e):
        self.Close()

    def onShowProfile(self, e):
        log.debug(_("Show contact's profile request"))
        target = self.contact_list.getSelection()
        if not target:
            dlg = wx.MessageDialog(self, _("You haven't selected any contact !"),
                                   _('Error'),
                                   wx.OK | wx.ICON_ERROR
                                  )
            dlg.ShowModal()
            dlg.Destroy()
            return
        _id = self.bridge.getCard(target.bare, self.profile)
        self.current_action_ids.add(_id)
        self.current_action_ids_cb[_id] = self.onProfileReceived

    def onProfileReceived(self, data):
        """Called when a profile is received"""
        log.debug (_('Profile received: [%s]') % data)
        Profile(self, data)

    def onJoinRoom(self, e):
        log.warning('FIXME: temporary menu, must be improved')
        #TODO: a proper MUC room joining dialog with nickname etc
        dlg = wx.TextEntryDialog(
                self, _("Please enter MUC's JID"),
                #_('Entering a MUC room'), 'test@conference.necton2.int')
                _('Entering a MUC room'), 'room@muc_service.server.tld')
        if dlg.ShowModal() == wx.ID_OK:
            room_jid=JID(dlg.GetValue())
            if room_jid.is_valid():
                self.bridge.joinMUC(room_jid, self.profiles[self.profile]['whoami'].node, {}, self.profile)
            else:
                log.error (_("'%s' is an invalid JID !"), room_jid)

    def onClose(self, e):
        QuickApp.onExit(self)
        log.info(_("Exiting..."))
        for win in self.chat_wins:
            self.chat_wins[win].Destroy()
        self.tray_icon.Destroy()
        e.Skip()

    def onTrayClick(self, e):
        log.debug(_("Tray Click"))
        if self.IsShown():
            self.Hide()
        else:
            self.Show()
            self.Raise()
        e.Skip()
