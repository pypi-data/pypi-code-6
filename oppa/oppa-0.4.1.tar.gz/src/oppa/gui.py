import cairo
import gtk
import state

class Gui(gtk.Window):
	def __init__(self):
		super(Gui, self).__init__()

		self.statusicon = gtk.status_icon_new_from_stock(gtk.STOCK_GOTO_TOP)
		self.statusicon.connect("activate", self.on_status_clicked)

		self.add_events(gtk.gdk.BUTTON_PRESS_MASK   |
		                gtk.gdk.BUTTON_RELEASE_MASK |
		                gtk.gdk.POINTER_MOTION_MASK)

		self.connect("key-press-event", self.on_keypress)
		self.connect("button-press-event", self.on_buttonpress)
		self.connect("button-release-event", self.on_buttonrelease)
		self.connect("motion-notify-event", self.on_motionnotify)
		self.connect("delete-event", self.on_delete)
		self.connect("expose-event", self.on_expose)

		self.screen = self.get_screen()
		colormap = self.screen.get_rgba_colormap()
		if (colormap is not None and self.screen.is_composited()):
			self.set_colormap(colormap)
		else:
			print "Screen is not composited, transparency disabled!"

		self.set_app_paintable(True)
		self.maximize()
		self.set_keep_above(True)
		self.set_decorated(False)
		self.show_all()
		self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSSHAIR))

		self.drawcalls   = [lambda cr, c=state.color(): cr.set_source_rgb(*c)]
		self.drawtrigger = 0

		if state.minimized:
			self.statusicon.set_from_stock(gtk.STOCK_GOTO_BOTTOM)
			self.iconify()

	def on_keypress(self, window, event):
		if event.keyval == gtk.keysyms.q:
			gtk.main_quit()
		if event.keyval == gtk.keysyms.t:
			state.toggle_opaque()
			self.queue_draw()
		if event.keyval == gtk.keysyms.space:
			self.toggle()
		if event.keyval == gtk.keysyms.Delete:
			self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSSHAIR))
			self.drawcalls = [lambda cr, c=state.color(): cr.set_source_rgb(*c)]
			self.queue_draw()
		if event.keyval == gtk.keysyms.e:
			self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.PIRATE))
			self.drawcalls.append(lambda cr: cr.stroke())
			self.drawcalls.append(lambda cr: cr.set_operator(cairo.OPERATOR_CLEAR))
			self.drawcalls.append(lambda cr: cr.set_line_width(50.0))
		if event.keyval in [gtk.keysyms.w, gtk.keysyms.r, gtk.keysyms.g, gtk.keysyms.b]:
			self.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSSHAIR))
			if event.keyval == gtk.keysyms.w:
				state.white()
			if event.keyval == gtk.keysyms.r:
				state.red()
			if event.keyval == gtk.keysyms.g:
				state.green()
			if event.keyval == gtk.keysyms.b:
				state.blue()
			self.drawcalls.append(lambda cr: cr.stroke())
			self.drawcalls.append(lambda cr: cr.set_operator(cairo.OPERATOR_OVER))
			self.drawcalls.append(lambda cr: cr.set_line_width(2.0))
			self.drawcalls.append(lambda cr, c=state.color(): cr.set_source_rgb(*c))

	def on_buttonpress(self, window, event):
		self.drawcalls.append(lambda cr, x=event.x, y=event.y: cr.move_to(x, y))

	def on_buttonrelease(self, window, event):
		self.queue_draw()

	def on_motionnotify(self, window, event):
		if event.state & gtk.gdk.BUTTON1_MASK:
			self.drawcalls.append(lambda cr, x=event.x, y=event.y: cr.line_to(x, y))
			self.delayed_queue_draw()

	def on_delete(self, window, event):
		self.toggle()
		return True

	def on_expose(self, widget, event):
		cr = widget.get_window().cairo_create()
		cr.set_source_rgba(0, 0, 0, 1.0 if state.opaque else 0.0)
		cr.set_operator(cairo.OPERATOR_SOURCE)
		cr.paint()

		cr.set_operator(cairo.OPERATOR_OVER)
		for drawcall in self.drawcalls:
			drawcall(cr)
		cr.stroke()
		return False

	def on_status_clicked(self, status):
		self.toggle()

	def toggle(self):
		if not state.minimized:
			self.statusicon.set_from_stock(gtk.STOCK_GOTO_BOTTOM)
			self.iconify()
		else:
			self.statusicon.set_from_stock(gtk.STOCK_GOTO_TOP)
			self.deiconify()
		state.toggle_minimized()

	def delayed_queue_draw(self):
		# For performance reasons draw is queued every N-th time
		# from MOTION_NOTIFY event.
		N = 5
		if self.drawtrigger % N == 0:
			self.queue_draw()
		self.drawtrigger += 1

def run():
	Gui()
	gtk.main()
