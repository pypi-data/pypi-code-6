# -*- coding: utf-8 -*-

import sys
from WallpaperOptimizer.Core import Core


class Starter(object):
    def _putlogOption(self, option, logging):
        """
        option instance dump.
        """
        logging.debug('Command line option as.')
        logging.debug('%20s [%s,%s].'
                      % ('align', option.getLAlign(), option.getRAlign()))
        logging.debug('%20s [%s,%s].'
                      % ('valign', option.getLValign(), option.getRValign()))
        logging.debug('%20s [%d,%d,%d,%d]'
                      % ('mergin',
                          option.getLMergin(), option.getRMergin(),
                          option.getTopMergin(), option.getBtmMergin()))
        logging.debug('%20s [%s]'
                      % ('fixed', option.getFixed()))
        logging.debug('%20s [%s,%s]'
                      % ('display', option.getLSize(), option.getRSize()))
        logging.debug('%20s [%s]'
                      % ('bgcolor', option.getBgcolor()))
        logging.debug('%20s [%s,%s]'
                      % ('srcdir', option.getLSrcdir(), option.getRSrcdir()))
        logging.debug('%20s [%s]'
                      % ('setWall', option.getSetWall()))
        logging.debug('%20s [%s]'
                      % ('savepath', option.getSavePath()))
        logging.debug('%20s [%s]'
                      % ('daemon', option.getDaemonize()))
        logging.debug('%20s [%s]'
                      % ('interval', option.getInterval()))

    def _runConsoleSide(self, option, logging):
        if option.getVerbose():
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(name)-12s: %(levelname)-8s %(message)s')
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)
            self._putlogOption(option, logging)

        if option.getDaemonize():
            core = Core(option)
            logging.debug('Running ... daemonize mode.')
            try:
                core.background()
            except Core.CoreRuntimeError, msg:
                logging.error('** CoreRuntimeError: %s. ' % msg.value)
                sys.exit(2)
        else:
            core = Core(option)
            logging.debug('Running ... singlerun mode.')
            try:
                core.singlerun()
            except Core.CoreRuntimeError, msg:
                logging.error('** CoreRuntimeError: %s. ' % msg.value)
                sys.exit(2)

    def start(self):
        pass
