import sys
import b2tool.commands
import komandr


def main():
    # _,params = args.parse(sys.argv[2:])
    # print "Start app"

    komandr.main.execute(sys.argv[1:3])