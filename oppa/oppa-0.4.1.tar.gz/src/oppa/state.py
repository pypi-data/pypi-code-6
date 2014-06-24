minimized = False
opaque    = False

def toggle_minimized():
	global minimized
	minimized = not minimized

def toggle_opaque():
	global opaque
	opaque = not opaque

class Color:
	WHITE = "w"
	RED   = "r"
	GREEN = "g"
	BLUE  = "b"
current_color = Color.WHITE

def color():
	global current_color
	rgb = {Color.WHITE : [1.0, 1.0, 1.0],
	       Color.RED   : [1.0, 0.0, 0.0],
	       Color.GREEN : [0.0, 1.0, 0.0],
	       Color.BLUE  : [0.0, 0.0, 1.0]}
	return rgb[current_color]

def set_color(c):
	global current_color
	current_color = c

def white():
	set_color(Color.WHITE)
def red():
	set_color(Color.RED)
def green():
	set_color(Color.GREEN)
def blue():
	set_color(Color.BLUE)
