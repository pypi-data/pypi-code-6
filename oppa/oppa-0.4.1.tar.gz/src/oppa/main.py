import argparse
import gui
import state

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-o", "--opaque",    dest="opaque",    action="store_true", help="start in opaque mode")
	parser.add_argument("-z", "--minimized", dest="minimized", action="store_true", help="start minimized")
	args = parser.parse_args()

	if args.opaque:
		state.toggle_opaque()
	if args.minimized:
		state.toggle_minimized()

	gui.run()
