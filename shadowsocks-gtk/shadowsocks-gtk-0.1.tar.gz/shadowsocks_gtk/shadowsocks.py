#!/usr/bin/env python

# Copyright (c) 2014 apporc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import pygtk
pygtk.require('2.0')
import gtk
import vte
import subprocess
import gettext
from pkg_resources import resource_filename
from shadowsocks_gtk.encrypt import method_supported
from shadowsocks_gtk.utils import get_config, save_config


DEFAULT_LOGLEVEL = 'info'
WINDOW_HEIGHT = 260
WINDOW_WIDTH = 450
VTE_HEIGHT = 200
LINE_HEIGHT = 25
LINE_HEADER_WIDTH = 120
ADDRESS_WIDTH = 180
PORT_WIDTH = 50
LOGO_FILE = 'shadowsocks.png'
DEFAULT_SERVER = ['209.141.36.62', '8348', '$#HAL9000!', 'aes-256-cfb']
DEFAULT_LOCAL = ['127.0.0.1', '1080']
DEFAULT_TIMEOUT = 600


gettext.bindtextdomain('shadowsocks_gtk', resource_filename(__name__, 'locale'))
gettext.textdomain('shadowsocks_gtk')
_ = gettext.gettext


class ShadowSocks(object):
    command = ['/usr/bin/env', 'python', 'local.py']

    def __init__(self, window=None):
        self.supported_methods = method_supported.keys()
        self.config = get_config()
        server_ip = self.config.get('server', None)
        server_port = self.config.get('server_port', None)
        self.servers = self.config.get('servers', [DEFAULT_SERVER])
        if server_ip and server_port:
            self.server_ip = str(server_ip)
            self.server_port = str(server_port)
            self.password = self.config.get('password')
            method = self.config.get('method')
        else:
            self.server_ip = DEFAULT_SERVER[0]
            self.server_port = DEFAULT_SERVER[1]
            self.password = DEFAULT_SERVER[2]
            method = DEFAULT_SERVER[3]

        self.method = self.supported_methods.index(method) if (method in self.supported_methods) else 0
        self.local_ip = self.config.get('local_address', DEFAULT_LOCAL[0])
        self.local_port = str(self.config.get('local_port', DEFAULT_LOCAL[1]))
        self.timeout = str(self.config.get('timeout', DEFAULT_TIMEOUT))
        self.status = 'disconnected'
        self.childpid = None
        self.childexited = True

        self.window = window
        self.labels = {}
        self.entrys = {}
        self.buttons = {}
        if not self.window:
            self.create_window()
        self.create_trayicon()
        self.create_menu()
        self.fill_window()

    def create_window(self):
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('ShadowSocks')
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_border_width(10)
        self.window.connect('window-state-event', self.state_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_size_request(WINDOW_WIDTH, WINDOW_HEIGHT)
        logo = resource_filename(__name__, LOGO_FILE)
        self.window.set_icon_from_file(logo)
        self.window.show()

    def create_trayicon(self):
        self.trayicon = gtk.StatusIcon()
        logo = resource_filename(__name__, LOGO_FILE)
        self.trayicon.set_from_file(logo)
        self.trayicon.connect('popup-menu', self.show_menu)
        self.trayicon.connect('activate', self.toggle_showhide_item)
        self.trayicon.set_tooltip('ShadowSocks')
        self.trayicon.set_visible(True)

    def show_menu(self, statusicon, button, activation_time):
        self.menu.popup(None, None, gtk.status_icon_position_menu, button, activation_time, self.trayicon)

    def create_menu(self):
        self.menu = gtk.Menu()
        self.showhide_item = gtk.MenuItem(_('Hide'))
        self.showhide_item.connect('activate', self.toggle_showhide_item)
        self.connect_item = gtk.MenuItem(_('Connect'))
        self.connect_item.connect('activate', self.toggle_connect)
        self.quit_item = gtk.MenuItem(_('Quit'))
        self.quit_item.connect('activate', self.destroy)
        self.menu.append(self.connect_item)
        self.menu.append(self.showhide_item)
        self.menu.append(self.quit_item)
        self.menu.show_all()

    def add_line(self, labelname='Default Label :', elements=None):
        #create HBox
        hbox = gtk.HBox(False, 0)
        self.vbox.pack_start(hbox, False, False, 0)
        #create label header
        label = gtk.Label(_(labelname) + ' :')
        label.set_size_request(LINE_HEADER_WIDTH, LINE_HEIGHT)
        label.set_properties(xalign=1)
        hbox.pack_start(label, False, False, 10)
        label.show()
        label_name = labelname.lower()
        self.labels[label_name] = label

        if elements:
            for e in elements:
                hbox.pack_start(e[0], e[1], e[1], e[2])
        return hbox

    def check_port(self, entry):
        port = entry.get_text()
        if not port.isdigit():
            entry.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("red"))
        else:
            entry.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))

    def update_server(self, box):
        t = box.get_active_text()
        if ':' in t:
            t = t.split(':')
            box.child.set_text(t[0])
            self.entrys['server_port'].set_text(t[1])

    def fill_window(self):
        self.vbox = gtk.VBox(False, 10)
        self.window.add(self.vbox)
        #Server Line
        liststore = gtk.ListStore(str)
        self.entrys['server_ip'] = gtk.ComboBoxEntry(liststore, 0)
        for server in self.servers:
            self.entrys['server_ip'].append_text(server[0] + ':' + server[1])
        self.entrys['server_ip'].child.set_text(self.server_ip)
        self.entrys['server_ip'].connect('changed', self.update_server)
        self.entrys['server_ip'].set_size_request(ADDRESS_WIDTH, LINE_HEIGHT)
        self.labels['server_colon'] = gtk.Label(':')
        self.labels['server_colon'].set_properties(xalign=0.5)
        self.entrys['server_port'] = gtk.Entry()
        self.entrys['server_port'].set_size_request(PORT_WIDTH, LINE_HEIGHT)
        self.entrys['server_port'].set_text(self.server_port)
        elements = [(self.entrys['server_ip'], True, 0),
                    (self.labels['server_colon'], False, 0),
                    (self.entrys['server_port'], False, 0)]
        self.server_hbox = self.add_line('Server Address', elements)
        self.entrys['server_port'].connect('changed', self.check_port)

        #Local Line
        self.entrys['local_ip'] = gtk.Entry()
        self.entrys['local_ip'].set_size_request(ADDRESS_WIDTH, LINE_HEIGHT)
        self.entrys['local_ip'].set_text(self.local_ip)
        self.labels['local_colon'] = gtk.Label(':')
        self.labels['local_colon'].set_properties(xalign=0.5)
        self.entrys['local_port'] = gtk.Entry()
        self.entrys['local_port'].set_size_request(PORT_WIDTH, LINE_HEIGHT)
        self.entrys['local_port'].set_text(self.local_port)
        elements = [(self.entrys['local_ip'], True, 0),
                    (self.labels['local_colon'], False, 0),
                    (self.entrys['local_port'], False, 0)]
        self.local_hbox = self.add_line('Local Listening', elements)

        #Password Line
        self.entrys['password'] = gtk.Entry()
        self.entrys['password'].set_visibility(False)
        if self.password:
            self.entrys['password'].set_text(self.password)
        elements = [(self.entrys['password'], True, 0)]
        self.pass_hbox = self.add_line('Password', elements)

        #Encryption Method Line
        self.entrys['encrypt_method'] = gtk.combo_box_new_text()
        for method in self.supported_methods:
            self.entrys['encrypt_method'].append_text(method)
        self.entrys['encrypt_method'].set_active(self.method)
        elements = [(self.entrys['encrypt_method'], True, 0)]
        self.encrypt_hbox = self.add_line('Encryption Method', elements)

        #Timeout Line
        self.entrys['timeout'] = gtk.Entry()
        self.entrys['timeout'].set_text(self.timeout)
        elements = [(self.entrys['timeout'], True, 0)]
        self.timeout_hbox = self.add_line('Timeout in Second', elements)

        #Status Line
        self.labels['current_status'] = gtk.Label(_(self.status))
        self.labels['current_status'].set_properties(xalign=0)
        self.labels['current_status'].show()
        self.buttons['detail'] = gtk.Button(_('show detail'))
        self.buttons['detail'].set_size_request(80, LINE_HEIGHT)
        self.buttons['detail'].connect("clicked", self.toggle_detail_button, None)
        elements = [(self.labels['current_status'], True, 0),
                    (self.buttons['detail'], False, 0)]
        self.status_hbox = self.add_line('Current Status', elements)

        #Add buttonbox
        self.add_buttonbox()

        #Terminal Window
        self.terminal = vte.Terminal()
        self.terminal.set_size_request(380, 180)
        self.vbox.pack_start(self.terminal, True, True, 0)

        #Show them
        self.server_hbox.show_all()
        self.local_hbox.show_all()
        self.pass_hbox.show_all()
        self.encrypt_hbox.show_all()
        self.timeout_hbox.show_all()
        self.status_hbox.show()
        self.buttonbox.show_all()
        self.vbox.show()

    def add_buttonbox(self):
        #HButtonBox
        self.buttonbox = gtk.HButtonBox()
        self.buttonbox.set_layout(gtk.BUTTONBOX_END)
        self.buttons['connect'] = gtk.Button(_('Connect'))
        self.buttons['close'] = gtk.Button(stock=gtk.STOCK_CLOSE)
        self.buttonbox.add(self.buttons['connect'])
        self.buttonbox.add(self.buttons['close'])
        self.buttons['close'].set_size_request(60, LINE_HEIGHT)
        self.buttons['close'].connect_object("clicked", self.destroy, self.window)
        self.buttons['connect'].set_size_request(60, LINE_HEIGHT)
        self.buttons['connect'].connect("clicked", self.toggle_connect)
        self.vbox.pack_start(self.buttonbox, False, False, 0)

    def show_vte(self):
        self.window.resize(WINDOW_WIDTH, WINDOW_HEIGHT + VTE_HEIGHT)
        self.terminal.show()

    def hide_vte(self):
        self.window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.terminal.hide()

    def on_child_exited(self, term):
        self.childexited = True
        self.update_status(False)
        self.hide_vte()
        self.hide_detail_button()

    def update_status(self, connect):
        if connect:
            self.status = 'connected'
            self.buttons['connect'].set_label(_('Disconnect'))
            self.connect_item.set_label(_('Disconnect'))
            self.labels['current_status'].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("green"))
            self.labels['current_status'].set_text('%s %s' %
                                                   (_(self.status + ' to'), self.entrys['server_ip'].child.get_text()))
        else:
            self.status = 'disconnected'
            self.buttons['connect'].set_label(_('Connect'))
            self.connect_item.set_label(_('Connect'))
            self.labels['current_status'].modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse("black"))
            self.labels['current_status'].set_text(_(self.status))

    def toggle_showhide_item(self, widget=None):
        if self.showhide_item.get_label() == _('Show'):
            self.window.deiconify()
            self.window.show()
            self.showhide_item.set_label(_('Hide'))
        else:
            self.window.iconify()

    def save(self):
        self.server_ip = self.entrys['server_ip'].child.get_text()
        self.server_port = self.entrys['server_port'].get_text()
        self.local_ip = self.entrys['local_ip'].get_text()
        self.local_port = self.entrys['local_port'].get_text()
        self.password = self.entrys['password'].get_text()
        self.timeout = self.entrys['timeout'].get_text()
        self.method = self.entrys['encrypt_method'].get_active()
        method = self.supported_methods[self.method]
        server = [self.server_ip, self.server_port, self.password, method]
        if server not in self.servers:
            self.servers.append(server)

        self.config['servers'] = self.servers
        self.config['server'] = self.server_ip
        self.config['server_port'] = int(self.server_port)
        self.config['local_address'] = self.local_ip
        self.config['local_port'] = int(self.local_port)
        self.config['password'] = self.password
        self.config['timeout'] = int(self.timeout)
        self.config['level'] = DEFAULT_LOGLEVEL
        self.config['method'] = method
        save_config(self.config)

    def toggle_detail_button(self, widget, data=None):
        if self.buttons['detail'].get_label() == _('show detail'):
            self.buttons['detail'].set_label(_('hide detail'))
            self.show_vte()
        else:
            self.buttons['detail'].set_label(_('show detail'))
            self.hide_vte()

    def show_detail_button(self):
        if self.status == 'connected':
            self.buttons['detail'].set_label(_('show detail'))
        else:
            self.buttons['detail'].set_label(_('hide detail'))
        self.buttons['detail'].show()

    def hide_detail_button(self):
        self.buttons['detail'].hide()

    def run(self):
        if self.childexited:
            self.childpid = self.terminal.fork_command(self.command[0], self.command, os.getcwd())
            if self.childpid > 0:
                self.childexited = False
                self.terminal.connect('child-exited', self.on_child_exited)
            else:
                self.childexited = False

    def stop(self):
        if not self.childexited:
            code0 = subprocess.call(['kill', str(self.childpid)])
            if code0 != 0:
                subprocess.call(['kill', '-9', str(self.childpid)])
            self.childexited = True

    def toggle_connect(self, widget=None):
        if self.status == 'disconnected':
            self.save()
            self.run()
            self.update_status(True)
            self.show_detail_button()
        else:
            self.stop()

    def destroy(self, widget, data=None):
        self.stop()
        gtk.main_quit()

    def state_event(self, window, event):
        if event.changed_mask & gtk.gdk.WINDOW_STATE_ICONIFIED\
                and event.new_window_state & gtk.gdk.WINDOW_STATE_ICONIFIED:
            self.showhide_item.set_label(_('Show'))
            self.window.hide()

    def main(self):
        gtk.main()


def main():
    path = os.path.abspath(__file__)
    if os.path.islink(path):
        path = getattr(os, 'readlink', lambda x: x)(path)
    os.chdir(os.path.dirname(os.path.abspath(path)))

    shadowsocks = ShadowSocks()
    shadowsocks.main()


if __name__ == "__main__":
    main()
