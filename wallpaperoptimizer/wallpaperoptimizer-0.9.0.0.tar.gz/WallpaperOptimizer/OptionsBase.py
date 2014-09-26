# -*- coding: utf-8 -*-


class OptionsBase(object):
    def getLAlign(self):
        return self.opts.align[0]

    def getRAlign(self):
        return self.opts.align[1]

    def getLValign(self):
        return self.opts.valign[0]

    def getRValign(self):
        return self.opts.valign[1]

    def getLMergin(self):
        return int(self.opts.mergin[0])

    def getRMergin(self):
        return int(self.opts.mergin[1])

    def getTopMergin(self):
        return int(self.opts.mergin[2])

    def getBtmMergin(self):
        return int(self.opts.mergin[3])

    def getFixed(self):
        return self.opts.fixed

    def getLSize(self):
        return self.opts.size[0]

    def getRSize(self):
        return self.opts.size[1]

    def getBgcolor(self):
        return self.opts.bgcolor

    def getLSrcdir(self):
        return self.opts.srcdir[0]

    def getRSrcdir(self):
        return self.opts.srcdir[1]

    def getVerbose(self):
        return self.opts.verbose

    def getWindow(self):
        return False

    def getSavePath(self):
        return self.opts.save

    def getSetWall(self):
        return self.opts.setWall

    def getDaemonize(self):
        return self.opts.daemonize

    def getInterval(self):
        return self.opts.interval

    def getLArg(self):
        return self.args[0]

    def getRArg(self):
        return self.args[1]

    def getArgs(self):
        return self.args

    def lengthArgs(self):
        return len(self.args) - self.args.count('')

    def getCombine(self):
        if hasattr(self.opts, 'combine'):
            return self.opts.combine
        else:
            return True
