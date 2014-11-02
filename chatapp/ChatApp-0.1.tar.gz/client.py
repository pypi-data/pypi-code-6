#!/usr/bin/python3

import socket
import threading
from gi.repository import Gtk


class Client(Gtk.Window):
	"""This class is client class"""
	
	def __init__(self,):
		Gtk.Window.__init__(self,)
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ui/gui.glade")
		self.window = self.builder.get_object("window")
		self.entry = self.builder.get_object("entry")
		self.label = self.builder.get_object("label2")
		self.treeView = self.builder.get_object("treeview")
		self.listStore = Gtk.ListStore(str)
		self.treeView.set_model(self.listStore)
		
		self.configure = self.builder.get_object("configure")
		self.about = self.builder.get_object("about")
		
		self.configure.connect("activate", self.configueIt)
		self.about.connect("activate", self.aboutIt)
		
		self.window.connect("delete-event", Gtk.main_quit)
		
		self.window.show_all()
	
	def process(self, username='User', hostname='127.0.0.1', port=4096):
		self.username = username
		self.hostname = hostname
		self.port = port
		
		self.column_text = Gtk.TreeViewColumn(self.username,Gtk.CellRendererText(), text=0)
		self.treeView.append_column(self.column_text)
		
		self.theSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
		    self.theSocket.connect((self.hostname, int(self.port)))
		except ConnectionRefusedError:
		    self.label.set_text("Not Connected")
		else:
		    self.label.set_text("Connected")
		    self.reciveThread = threading.Thread(target=self.recive_message, args=())
		    self.reciveThread.start()
		    self.entry.connect("activate", self.send_message)
		

	def recive_message(self,):
		while True:
			message=self.theSocket.recv(2048)
			if not message:
				break
			self.listStore.append([str(message)[2:-1]])


	def send_message(self, widget):
		self.theSocket.send(bytes(self.username + ': ' + str(widget.get_text()),'utf-8'))
		widget.set_text('')

	def configueIt(self, widget):
		dialog = conf()
	
	def aboutIt(self, widget):
		aboutit = about()
	


class conf(Gtk.Dialog):
	def __init__(self,):
		Gtk.Dialog.__init__(self,)
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ui/dialog.glade")
		self.dialog = self.builder.get_object("configuration")
		self.connectButton = self.builder.get_object('connectButton')
		self.cancalButton = self.builder.get_object('cancalButton')
		self.username = self.builder.get_object('username')
		self.hostname = self.builder.get_object('hostname')
		self.port = self.builder.get_object('port')
		
		self.connectButton.connect('activate', self.send_conf)
		self.connectButton.connect('clicked', self.send_conf)
		self.cancalButton.connect('clicked', self.close)
		
		self.dialog.show_all()
	
	def send_conf(self, widget):
		clientObj.process(self.username.get_text(), self.hostname.get_text(), self.port.get_text())
		self.dialog.destroy()
	
	def close(self, widget):
		self.dialog.destroy()

class about(Gtk.AboutDialog):
	def __init__(self,):
		Gtk.AboutDialog.__init__(self,)
		self.builder = Gtk.Builder()
		self.builder.add_from_file("ui/about.glade")
		self.aboutDialog = self.builder.get_object("aboutdialog")
		self.aboutDialog.show_all()
	


clientObj = Client()
Gtk.main()