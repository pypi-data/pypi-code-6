import cairo
import gtk
import os
import state
if os.name == "nt":
	from ctypes import windll

drawwin     = gtk.Window()
eventwin    = drawwin if os.name != "nt" else gtk.Window()
statusicon  = gtk.status_icon_new_from_stock(gtk.STOCK_GOTO_TOP)
drawcalls   = [lambda cr, c=state.color(): cr.set_source_rgb(*c)]
drawtrigger = 0

GWL_EXSTYLE      = -20
SW_HIDE          = 0
SW_SHOW          = 5
WS_EX_LAYERED    = 0x00080000
WS_EX_TOOLWINDOW = 0x00000080
LWA_ALPHA        = 0x00000002
LWA_COLORKEY     = 0x00000001
COLORREF_BLACK   = 0x00000000
MIN_ALPHA        = 1

def init():
	statusicon.connect("activate", on_status_clicked)
	eventwin.add_events(gtk.gdk.BUTTON_PRESS_MASK   |
	                    gtk.gdk.BUTTON_RELEASE_MASK |
	                    gtk.gdk.POINTER_MOTION_MASK)

	eventwin.connect("key-press-event", on_keypress)
	eventwin.connect("button-press-event", on_buttonpress)
	eventwin.connect("button-release-event", on_buttonrelease)
	eventwin.connect("motion-notify-event", on_motionnotify)
	eventwin.connect("delete-event", on_delete)
	if drawwin != eventwin:
		drawwin.connect("delete-event", on_delete)
	drawwin.connect("expose-event", on_expose)

	if os.name != "nt":
		drawwin.screen = drawwin.get_screen()
		colormap = drawwin.screen.get_rgba_colormap()
		if (colormap is not None and drawwin.screen.is_composited()):
			drawwin.set_colormap(colormap)
		else:
			print "Screen is not composited, transparency disabled!"

	drawwin.set_app_paintable(True)
	drawwin.maximize()
	drawwin.set_keep_above(True)
	drawwin.set_decorated(False)
	drawwin.show_all()
	if eventwin != drawwin:
		eventwin.maximize()
		eventwin.set_keep_above(True)
		eventwin.set_decorated(False)
		eventwin.show_all()
	eventwin.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSSHAIR))

	if os.name == "nt":
		hwnd  = eventwin.get_window().handle
		style = windll.user32.GetWindowLongA(hwnd, GWL_EXSTYLE)
		style = style | WS_EX_LAYERED | WS_EX_TOOLWINDOW
		windll.user32.ShowWindow(hwnd, SW_HIDE)
		windll.user32.SetWindowLongA(hwnd, GWL_EXSTYLE, style)
		windll.user32.SetLayeredWindowAttributes(hwnd, 0, MIN_ALPHA, LWA_ALPHA)
		windll.user32.ShowWindow(hwnd, SW_SHOW)

		hwnd  = drawwin.get_window().handle
		style = windll.user32.GetWindowLongA(hwnd, GWL_EXSTYLE)
		style = style | WS_EX_TOOLWINDOW
		if not state.opaque:
			style = style | WS_EX_LAYERED
		windll.user32.ShowWindow(hwnd, SW_HIDE)
		windll.user32.SetWindowLongA(hwnd, GWL_EXSTYLE, style)
		if not state.opaque:
			windll.user32.SetLayeredWindowAttributes(hwnd, COLORREF_BLACK, 0, LWA_COLORKEY)
		windll.user32.ShowWindow(hwnd, SW_SHOW)

	if state.minimized:
		statusicon.set_from_stock(gtk.STOCK_GOTO_BOTTOM)
		drawwin.iconify()
		if eventwin != drawwin:
			eventwin.iconify()

def on_keypress(window, event):
	global drawcalls

	if event.keyval == gtk.keysyms.q:
		gtk.main_quit()
	if event.keyval == gtk.keysyms.t:
		toggle_transparency()
	if event.keyval == gtk.keysyms.space:
		toggle()
	if event.keyval == gtk.keysyms.Delete:
		eventwin.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSSHAIR))
		drawcalls = [lambda cr, c=state.color(): cr.set_source_rgb(*c)]
		drawwin.queue_draw()
	if event.keyval == gtk.keysyms.e:
		eventwin.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.PIRATE))
		drawcalls.append(lambda cr: cr.stroke())
		drawcalls.append(lambda cr: cr.set_operator(cairo.OPERATOR_CLEAR))
		drawcalls.append(lambda cr: cr.set_line_width(50.0))
	if event.keyval in [gtk.keysyms.w, gtk.keysyms.r, gtk.keysyms.g, gtk.keysyms.b]:
		eventwin.get_window().set_cursor(gtk.gdk.Cursor(gtk.gdk.CROSSHAIR))
		if event.keyval == gtk.keysyms.w:
			state.white()
		if event.keyval == gtk.keysyms.r:
			state.red()
		if event.keyval == gtk.keysyms.g:
			state.green()
		if event.keyval == gtk.keysyms.b:
			state.blue()
		drawcalls.append(lambda cr: cr.stroke())
		drawcalls.append(lambda cr: cr.set_operator(cairo.OPERATOR_OVER))
		drawcalls.append(lambda cr: cr.set_line_width(2.0))
		drawcalls.append(lambda cr, c=state.color(): cr.set_source_rgb(*c))

def on_buttonpress(window, event):
	drawcalls.append(lambda cr, x=event.x, y=event.y: cr.move_to(x, y))

def on_buttonrelease(window, event):
	drawwin.queue_draw()

def on_motionnotify(window, event):
	if event.state & gtk.gdk.BUTTON1_MASK:
		drawcalls.append(lambda cr, x=event.x, y=event.y: cr.line_to(x, y))
		delayed_queue_draw()

def on_delete(window, event):
	toggle()
	return True

def on_expose(widget, event):
	cr = widget.get_window().cairo_create()
	cr.set_source_rgba(0, 0, 0, 1.0 if state.opaque else 0.0)
	cr.set_operator(cairo.OPERATOR_SOURCE)
	cr.paint()

	cr.set_operator(cairo.OPERATOR_OVER)
	if os.name == "nt" and not state.opaque:
		cr.set_antialias(cairo.ANTIALIAS_NONE)
	for drawcall in drawcalls:
		drawcall(cr)
	cr.stroke()
	return False

def on_status_clicked(status):
	toggle()

def toggle():
	if not state.minimized:
		statusicon.set_from_stock(gtk.STOCK_GOTO_BOTTOM)
		drawwin.hide()
		if eventwin != drawwin:
			eventwin.hide()
	else:
		statusicon.set_from_stock(gtk.STOCK_GOTO_TOP)
		drawwin.show()
		if eventwin != drawwin:
			eventwin.show()
	state.toggle_minimized()

def toggle_transparency():
	state.toggle_opaque()
	if os.name == "nt":
		hwnd  = drawwin.get_window().handle
		style = windll.user32.GetWindowLongA(hwnd, GWL_EXSTYLE)
		if state.opaque:
			windll.user32.SetWindowLongA(hwnd, GWL_EXSTYLE, style ^ WS_EX_LAYERED)
		else:
			windll.user32.SetWindowLongA(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED)
			windll.user32.SetLayeredWindowAttributes(hwnd, COLORREF_BLACK, 0, LWA_COLORKEY)
	drawwin.queue_draw()

def delayed_queue_draw():
	global drawtrigger
	# For performance reasons draw is queued every N-th time
	# from MOTION_NOTIFY event.
	N = 5
	if drawtrigger % N == 0:
		drawwin.queue_draw()
	drawtrigger += 1

def run():
	init()
	gtk.main()
