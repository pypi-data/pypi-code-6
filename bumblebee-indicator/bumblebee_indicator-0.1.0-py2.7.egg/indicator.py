
import config
import logging
import sys
import gtk
import appindicator
import os.path
from logic import Optimus

class BumblebeeIndicator:
	
	BUMBLEBEE_ICON = config.get_resource('bumblebee-icon.png')
	BUMBLEBEE_ICON_ACTIVE = config.get_resource('bumblebee-icon-active.png')
	BUMBLEBEE_ICON_DUAL = config.get_resource('bumblebee-icon-dual.png')
	
	def __init__(self):
		self.__ind = appindicator.Indicator("bumblebee-indicator", "", appindicator.CATEGORY_APPLICATION_STATUS)
		self.__ind.set_status(appindicator.STATUS_ACTIVE)
		self.__ind.set_icon(BumblebeeIndicator.BUMBLEBEE_ICON)
		self.__ind.set_attention_icon(BumblebeeIndicator.BUMBLEBEE_ICON_ACTIVE)

		self.__menu = self.__menu_setup()
		self.__ind.set_menu(self.__menu)
		
		self.__optimus = Optimus()

	def __menu_setup(self):
		menu = gtk.Menu()
		
		item = gtk.CheckMenuItem("Nvidia Optimus")
		item.show()
		item.set_active(False)
		item.set_sensitive(False)
		menu.append(item)
		self.__optimus_item = item
		
		item = gtk.CheckMenuItem("Dual monitor")
		item.show()
		item.set_active(False)
		menu.append(item)
		self.__dual_item = item

		item = gtk.MenuItem("Quit")
		item.connect("activate", self.quit)
		item.show()
		menu.append(item)
		return menu
		
	def __update_dual(self, dual):
		curr = dual.is_active()
		displ = self.__dual_item.get_active()
		if curr != displ:
			self.__dual_item.set_active(curr)
		icon = self.__ind.get_attention_icon()
		if curr and icon != BumblebeeIndicator.BUMBLEBEE_ICON_DUAL:
			self.__ind.set_attention_icon(BumblebeeIndicator.BUMBLEBEE_ICON_DUAL)
		if not curr and icon == BumblebeeIndicator.BUMBLEBEE_ICON_DUAL:
			self.__ind.set_attention_icon(BumblebeeIndicator.BUMBLEBEE_ICON_ACTIVE)
		
	def __check_status(self):
		displ = self.__optimus_item.get_active()
		curr = self.__optimus.is_active()
		
		if curr != displ:
			self.__optimus_item.set_active(curr)
			if curr:
				dual = self.__optimus.dual_monitor()
				self.__update_dual(dual)
				self.__ind.set_status(appindicator.STATUS_ATTENTION)
			else:
				self.__ind.set_status(appindicator.STATUS_ACTIVE)
		return True

	def main(self):
		gtk.timeout_add(config.PING_FREQUENCY, self.__check_status)
		try:
			gtk.main()
		except KeyboardInterrupt:
			sys.exit(0)
		except Exception, ex:
			logging.error("Error: %s" % ex)
			sys.exit(1)
	def quit(self, widget):
		sys.exit(0)
