# -*- coding: utf-8 -*-

import os.path
import re

from optparse import Option, OptionGroup, OptionParser, OptionValueError
from WallpaperOptimizer.OptionsBase import OptionsBase


class Options(OptionsBase):
    def getWindow(self):
        return self.opts.window

    def getIID(self):
        return self.opts.iid

    def getFD(self):
        return self.opts.fd

    def __init__(self):
        OptionsBase.__init__(self)

        class MultiargOption(Option):
            ACTIONS = Option.ACTIONS + (
                "multistore", "quatrostore", "doublestore", )
            STORE_ACTIONS = Option.STORE_ACTIONS + (
                "multistore", "quatrostore", "doublestore", )
            TYPED_ACTIONS = Option.TYPED_ACTIONS + (
                "multistore", "quatrostore", "doublestore", )
            ALWAYS_TYPED_ACTIONS = Option.ALWAYS_TYPED_ACTIONS + (
                "multistore", "quatrostore", "doublestore", )

            def take_action(self, action, dest, opt, value, values, parser):
                def exchangeValue(lvalue, dest, values):
                    for idx, m in enumerate(lvalue):
                        if m != "":
                            vals = getattr(values, dest)
                            vals[idx] = lvalue[idx]
                            setattr(values, dest, vals)

                if action == "multistore":
                    lvalue = value.split(",")
                    if (len(lvalue) > 1 and len(lvalue) <= 2):
                        exchangeValue(lvalue, dest, values)
                    else:
                        raise OptionValueError(
                            "option: %s to 2 values." % dest)
                elif action == "quatrostore":
                    lvalue = value.split(",")
                    if (len(lvalue) > 1 and len(lvalue) <= 4):
                        exchangeValue(lvalue, dest, values)
                    else:
                        raise OptionValueError(
                            "option: %s to 2 values." % dest)
                elif action == "doublestore":
                    lvalue = value.split(",")
                    if (
                        len(lvalue) == 2 and
                        lvalue[0] != "" and
                        lvalue[1] != ""
                    ):
                        exchangeValue(lvalue, dest, values)
                    else:
                        raise OptionValueError(
                            "option: %s necessary 2 values." % dest)
                else:
                    Option.take_action(
                        self, action, dest, opt, value, values, parser)

        parser = OptionParser(
            usage="%prog [options] imgfile1 imgfile2",
            version="%prog 0.1.0.0",
            option_class=MultiargOption)
        parser.set_defaults(
            align=["center", "center"],
            valign=["middle", "middle"],
            mergin=[0, 0, 0, 0],
            fixed=False,
            size=[None, None],
            bgcolor="black",
            srcdir=['', ''],
            verbose=False,
            window=False,
            save=None,
            setWall=False,
            daemonize=False,
            interval=60,
            iid=None,
            fd=None)

        viewgroup = OptionGroup(parser, 'View Options')
        viewgroup.add_option(
            "-a", "--align", dest="align", action="multistore",
            metavar="left,center,right",
            help="horizontal alignment (left, center, right)")
        viewgroup.add_option(
            "-v", "--valign", dest="valign", action="multistore",
            metavar="top,middle,bottom",
            help="vertical alignment (top, middle, bottom)")
        viewgroup.add_option(
            "-m", "--mergin", dest="mergin", action="quatrostore",
            metavar="pixel,pixel,pixel,pixel",
            help="left/right/top/bottom mergin for WorkSpace")
        viewgroup.add_option(
            "-f", "--fixed", dest="fixed", action="store_true",
            help="fixed imgfile allocation (nothing: Optimize)")
        viewgroup.add_option(
            "-d", "--display", dest="size", action="doublestore",
            metavar="pixel x pixel,pixel x pixel",
            help="left/right Display size")
        viewgroup.add_option(
            "-b", "--bgcolor", dest="bgcolor", action="store", type="string",
            metavar="color, 0xRRGGBB",
            help="Wallpaper base color (default: black)")
        viewgroup.add_option(
            "-s", "--srcdir",
            dest="srcdir",
            action="doublestore",
            type="string",
            metavar="PATH,PATH",
            help="wallpaper src dir")

        actiongroup = OptionGroup(parser, 'Action Options')
        actiongroup.add_option(
            "-V", "--verbose", dest="verbose", action="store_true",
            help="verbose")
        actiongroup.add_option(
            "-W", "--window", dest="window", action="store_true",
            help="window mode")
        actiongroup.add_option(
            "-S", "--save", dest="save", action="store",
            metavar="PATH",
            help="Save Wallpaper to PATH")
        actiongroup.add_option(
            "-C", "--change", dest="setWall", action="store_true",
            help="Created wallpaper set to current WorkSpace")
        actiongroup.add_option(
            "-D", "--daemonize", dest="daemonize", action="store_true",
            help="daemonize (default: False)")
        actiongroup.add_option(
            "-i", "--interval", dest="interval", action="store", type="int",
            metavar="sec",
            help="change wallpaper interval (default: 60sec)")

        appletgroup = OptionGroup(parser, 'Applet Use Options')
        appletgroup.add_option("--oaf-activate-iid", dest="iid")
        appletgroup.add_option("--oaf-ior-fd", dest="fd")

        parser.add_option_group(viewgroup)
        parser.add_option_group(actiongroup)
        parser.add_option_group(appletgroup)

        (self.opts, self.args) = parser.parse_args()

        if not self.opts.window:
            if (len(self.args) == 1 and self.opts.save is not None):
                parser.error("Please set imgfile2 parameter.")

            for m_align in self.opts.align:
                if m_align in ("left", "center", "right"):
                    break
                raise OptionValueError("align invalid")

            for m_valign in self.opts.valign:
                if m_valign in ("top", "middle", "bottom"):
                    break
                raise OptionValueError("valign invalid")

            if (self.opts.srcdir[0] != '' and self.opts.srcdir[1] != ''):
                for i in range(0, 1):
                    if not os.path.exists(self.opts.srcdir[i]):
                        raise OptionValueError(
                            'No such srcdir [%s]' % self.opts.srcdir[i])

            ptn = re.compile('^0x(.+)$')
            if ptn.match(self.opts.bgcolor):
                subStr = ptn.split(self.opts.bgcolor)
                self.opts.bgcolor = '#%s' % subStr[1]
