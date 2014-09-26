# -*- coding: utf-8 -*-

""" WallpaperOptimizer::Core

wallpaperoptimizer core module.
"""

import sys
import os.path
import logging
#import subprocess
import time
import datetime
import glob

import WallpaperOptimizer

from WallpaperOptimizer.Config import Config
from WallpaperOptimizer.WorkSpace import WorkSpace
from WallpaperOptimizer.ChangerDir import ChangerDir
from WallpaperOptimizer.Imaging.ImgFile import ImgFile
from WallpaperOptimizer.Command.CommandFactory import CommandFactory


class Core(object):
    class CoreRuntimeError(Exception):
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)

    def _initializeConfig(self):
        """
        config instance set from configfile or instance default.
        """
        # config set from configfile
        self.configfile = os.path.join(
            WallpaperOptimizer.USERENVDIR,
            '.walloptrc')
        if os.path.exists(self.configfile):
            try:
                self.config = Config(self.configfile)
                logging.info('Config set from configfile.')
            except Config.FormatError, msg:
                logging.error('** FormatError: %s. ' % msg)
                raise Core.CoreRuntimeError(msg.value)
        else:
            self.config = Config()

        # config set/update from commandline option
        if (
            self.option.getLSize() is not None and
            self.option.getRSize() is not None
        ):
            self.config.lDisplay.toIntAsSizestring(self.option.getLSize())
            self.config.rDisplay.toIntAsSizestring(self.option.getRSize())
            logging.info('Config "display" update from commandline option.')

        if (
            self.option.getLSrcdir() != '' and
            self.option.getRSrcdir() != ''
        ):
            self.config.lDisplay.setSrcdir(self.option.getLSrcdir())
            self.config.rDisplay.setSrcdir(self.option.getRSrcdir())
            logging.info('Config "srcdir" update from commandline option.')

        if (
                not self.option.getWindow() and
                self.config.lDisplay.width == 0 and
                self.config.lDisplay.height == 0 and
                self.config.rDisplay.width == 0 and
                self.config.rDisplay.height == 0
        ):
            logging.error(
                '** Please setting left/right display size.' +
                '(Set --display option or .walloptrc file)')
            raise Core.CoreRuntimeError('No setting left/right display size.')

        if (
                self.option.getDaemonize() and
                not self.option.getWindow() and
                self.config.lDisplay.srcdir == '' and
                self.config.rDisplay.srcdir == ''
        ):
            logging.error('** Please setting srcdir in Daemonize mode.')
            raise Core.CoreRuntimeError(
                'No setting srcdir ind Daemonize mode.')

        logging.debug('%20s [%d,%d]'
                      % ('left display size',
                          self.config.lDisplay.width,
                          self.config.lDisplay.height))
        logging.debug('%20s [%d,%d]'
                      % ('right display size',
                          self.config.rDisplay.width,
                          self.config.rDisplay.height))
        logging.debug('%20s [%s,%s]'
                      % ('position',
                          self.config.lDisplay.posit,
                          self.config.rDisplay.posit))
        logging.debug('%20s [%s]'
                      % ('srcdir to left',
                          self.config.lDisplay.srcdir))
        logging.debug('%20s [%s]'
                      % ('srcdir to right',
                          self.config.rDisplay.srcdir))

    def _initializeWorkSpace(self):
        """
        WorkSpace instance initialize.
        """
        try:
            self.Ws = WorkSpace()
        except WorkSpace.WorkSpaceRuntimeError, msg:
            logging.error('** WorkSpaceRuntimeError: %s. ' % msg)
            raise Core.CoreRuntimeError(msg.value)

        logging.info('Current WorkSpace setting as.')
        logging.debug('%20s [%d,%d]'
                      % ('WorkSpace Size', self.Ws.Size.w, self.Ws.Size.h))
        logging.debug('%20s [%s]'
                      % ('WorkSpace depth', self.Ws.getDepth()))

    def _initializeScreen(self):
        """
        Screen(Rectangle) instance initialize and
            compared Screen size in WorkSpace instance.
        """
        logging.debug('Config Setting To Screens.')
                # Separate時は、.walloptrcをどう書いても反映されない。
        if not self.Ws.isSeparate():
            self.Ws.setScreenSize(
                (self.config.lDisplay.width, self.config.lDisplay.height),
                (self.config.rDisplay.width, self.config.rDisplay.height))
            if not self.Ws.compareToScreen():
                logging.error(
                    '** WorkSpace width[%d] < ' % (self.Ws.Size.w) +
                    'sum(left display size, right display size) [%d, %d].' % (
                        self.Ws.lScreen.Size.w,
                        self.Ws.rScreen.Size.w))
                raise Core.CoreRuntimeError(
                    'WorkSpace width over left/right display size summing')

        logging.debug('Current Screen Size.')
        logging.debug('%20s [%d,%d]' % (
            'Left  Screen Size',
            self.Ws.lScreen.Size.w,
            self.Ws.lScreen.Size.h))
        logging.debug('%20s [%d,%d]' % (
            'Right Screen Size',
            self.Ws.rScreen.Size.w,
            self.Ws.rScreen.Size.h))

        # ただし、妥当性だけは見られる
        self.Ws.setAttrScreenBool(
            self.config.lDisplay.getBool(),
            self.config.rDisplay.getBool())

        if (
                hasattr(self.Ws.lScreen.Size, 'islessThanWorkSpaceHeight') and
                self.Ws.lScreen.Size.islessThanWorkSpaceHeight
        ):
            logging.warning(
                '* WorkSpace height [%s] > left display height [%s].'
                % (self.Ws.Size.h, self.Ws.lScreen.Size.h))
        if (
                hasattr(self.Ws.rScreen.Size, 'islessThanWorkSpaceHeight') and
                self.Ws.rScreen.Size.islessThanWorkSpaceHeight
        ):
            logging.warning(
                '* WorkSpace height [%s] > right display height [%s].'
                % (self.Ws.Size.h, self.Ws.rScreen.Size.h))

        try:
            self.Ws.setAttrScreenType()
        except WorkSpace.WorkSpaceRuntimeError, msg:
            raise Core.CoreRuntimeError(msg.value)

        if (not hasattr(self.Ws.lScreen, 'displayType')):
            setattr(self.Ws.lScreen, 'displayType', 'undefined')
        tmpDisplayType1 = self.Ws.lScreen.displayType
        if (not hasattr(self.Ws.rScreen, 'displayType')):
            setattr(self.Ws.rScreen, 'displayType', 'undefined')
        tmpDisplayType2 = self.Ws.rScreen.displayType

        logging.debug('%20s [%s,%s]'
                      % ('display type', tmpDisplayType1, tmpDisplayType2))

        logging.info('Calculate center position to WorkSpace.')
        self.Ws.lScreen.calcCenter()
        self.Ws.rScreen.calcCenter()
        logging.debug('%20s [%d,%d]' % (
            'left screen',
            self.Ws.lScreen.center.x,
            self.Ws.lScreen.center.y))
        logging.debug('%20s [%d,%d]' % (
            'right screen',
            self.Ws.rScreen.center.x,
            self.Ws.rScreen.center.y))

    def _checkImgType(self, Ws, Img, line):
        """
        ImgFile square type decide by aspectratio.
        """
        logging.info('Checking imgType as Imgfile.')

        if (Img.Size.w < Ws.lScreen.Size.w or Img.Size.w < Ws.rScreen.Size.w):
            if Img.isDual():
                setattr(Img, 'imgType', 'dual')

        if Img.isSquare():
            setattr(Img, 'imgType', 'square')
        if Img.isWide():
            setattr(Img, 'imgType', 'wide')

        if not hasattr(Img, 'imgType'):
            setattr(Img, 'imgType', 'other')

        logging.debug('%20s%d [%s]' % ('imgType as Img', line, Img.imgType))

    def _bindingImgToScreen(self, Fixed, Img1, Img2):
        """
        ImgFile is binding to Screen instance.
        """
        #! 組み合わせバリエーションに対応しきれているか、見極められていない
        logging.info('Binding Img to Screen.')

        if Fixed:
            setattr(Img1, 'posit', 'left')
            logging.debug('%20s [%s]' % ('Img1 fixed binding', Img1.posit))
            setattr(Img2, 'posit', 'right')
            logging.debug('%20s [%s]' % ('Img2 fixed binding', Img2.posit))
        else:
            # アスペクト比見て、ディスプレイのタイプに応じて優先的に割り当てる
            if Img1.imgType == self.Ws.lScreen.displayType:
                setattr(Img1, 'posit', 'left')
                logging.debug('%20s [%s]' % ('Img1 binding', Img1.posit))
                setattr(Img2, 'posit', 'right')
                logging.debug('%20s [%s]' % ('Img2 binding', Img2.posit))
            elif Img1.imgType == self.Ws.rScreen.displayType:
                setattr(Img1, 'posit', 'right')
                logging.debug('%20s [%s]' % ('Img1 binding', Img1.posit))
                setattr(Img2, 'posit', 'left')
                logging.debug('%20s [%s]' % ('Img2 binding', Img2.posit))
            else:
                setattr(Img1, 'posit', 'left')
                logging.debug('%20s [%s]' % ('Img1 binding', Img1.posit))
                setattr(Img2, 'posit', 'right')
                logging.debug('%20s [%s]' % ('Img2 binding', Img2.posit))

    def _checkContain(self, Ws, Img, tmpMergin):
        """
        ImgFile check that contains Screen.
        """
        logging.info('Check Imgfile contain %s Screen.' % Img.posit)

        if Img.posit == 'left':
            # lScreenに、Imgがおさまる
            if (Ws.lScreen.containsPlusMergin(Img, tmpMergin)):
                return True
            else:
                return False
        elif Img.posit == 'right':
            # rScreenに、Imgがおさまる
            if (Ws.rScreen.containsPlusMergin(Img, tmpMergin)):
                return True
            else:
                return False

    def _downsizeImg(self, Ws, Img, tmpMergin):
        """
        ImgFile is fitting to Screen size.
        """
        if Img.posit == 'left':
            tmpScreen = Ws.lScreen
        elif Img.posit == 'right':
            tmpScreen = Ws.rScreen
        logging.info('Convert Imgfile with %s Screen.' % Img.posit)

        tmpMerginW = tmpMergin[0] + tmpMergin[1]
        logging.debug('%20s [%s]' % ('width mergin', tmpMerginW))
        tmpMerginH = tmpMergin[2] + tmpMergin[3]
        logging.debug('%20s [%s]' % ('height mergin', tmpMerginH))

        logging.debug('%20s [%d,]' % ('---tmpScreen size.w', tmpScreen.Size.w))
        if Img.Size.w > (tmpScreen.Size.w - tmpMerginW):
            Img.setSize(
                (tmpScreen.Size.w - tmpMerginW),
                int(max(
                    Img.Size.h *
                    (tmpScreen.Size.w - tmpMerginW)
                    / Img.Size.w, 1))
            )
        logging.debug('%20s [%d,%d]' % (
            '---set size',
            Img.Size.w,
            Img.Size.h))
        logging.debug('%20s [,%d]' % (
            '---tmpScreen size.h',
            tmpScreen.Size.h))
        if Img.Size.h > (tmpScreen.Size.h - tmpMerginH):
            Img.setSize(
                int(max(
                    Img.Size.w *
                    (tmpScreen.Size.h - tmpMerginH) /
                    Img.Size.h, 1)),
                (tmpScreen.Size.h - tmpMerginH)
            )
        logging.debug('%20s [%d,%d]' % ('---set size', Img.Size.w, Img.Size.h))

        Img.reSize(Img.Size.w, Img.Size.h)
        logging.debug('%20s [%d,%d]' % (
            'converted size',
            Img.Size.w,
            Img.Size.h))

    def _allocateCenter(self, Ws, Img, line):
        """
        ImgFile and Screen calculate center position.
        """
        logging.info('Calculate center position.')
        Img.calcCenter()
        logging.debug('%20s%d [%d,%d]' % (
            'Img',
            line,
            Img.center.x,
            Img.center.y))

    def _allocateImg(self, Option, Ws, Img):
        """
        ImgFile calculate allocate position.
        """
        if Img.posit == 'left':
            tmpScreen = Ws.lScreen
            tmpAlign = Option.getLAlign()
            tmpValign = Option.getLValign()
        elif Img.posit == 'right':
            tmpScreen = Ws.rScreen
            tmpAlign = Option.getRAlign()
            tmpValign = Option.getRValign()
        logging.info('Allocate Imgfile to %s Screen.' % Img.posit)

        # 画面中央と画像中央との距離をタプルで得る
        centerDistance = (abs(Img.center.distanceX(tmpScreen.center)),
                          abs(Img.center.distanceY(tmpScreen.center)))
        rightCornerDistance = (abs(Img.end.distanceX(tmpScreen.end)),
                               abs(Img.end.distanceY(tmpScreen.end)))

        # Imgはインスタンス化されたときに、x,y = 0,0 つまり align=left, valign=top
        if tmpAlign == 'center':
            if Img.center.x != tmpScreen.center.x:
                Img.start.x += centerDistance[0]
                Img.end.x += centerDistance[0]
        elif tmpAlign == 'right':
            if Img.end.x != tmpScreen.end.x:
                Img.start.x += rightCornerDistance[0]
                Img.end.x += rightCornerDistance[0]

        if tmpValign == 'middle':
            if Img.center.y != tmpScreen.center.y:
                Img.start.y += centerDistance[1]
                Img.end.y += centerDistance[1]
        elif tmpValign == 'bottom':
            if Img.end.y != tmpScreen.end.y:
                Img.start.y += rightCornerDistance[1]
                Img.end.y += rightCornerDistance[1]

        logging.debug('%20s [%d,%d]' % ('start', Img.start.x, Img.start.y))
        logging.debug('%20s [%d,%d]' % ('end', Img.end.x, Img.end.y))

    def _mergeWallpaper(self, Ws, bkImg, Img):
        """
        ImgFile paste to Wallpaper Img.
        """
        logging.info('Merge Imgfile to %s Screen.' % Img.posit)

        if Img.posit == 'right':
            Img.start.x += Ws.lScreen.Size.w
            Img.end.x += Ws.lScreen.Size.w
            # center.x
        bkImg.paste(Img, (Img.start.x, Img.start.y, Img.end.x, Img.end.y))

    def _optimizeWallpapers(self, Option, Config, Ws, Img1, Img2):
        """
        2 ImgFile allocate Wallpaper Img.
        """
        logging.info('Optimizing ... wallpapaers.')
        self._initializeScreen()
        self._checkImgType(Ws, Img1, 1)
        self._checkImgType(Ws, Img2, 2)

        self._bindingImgToScreen(Option.getFixed(), Img1, Img2)

        logging.info('Calculate mergin.')
        lMergin = (
            Option.getLMergin(),
            0,
            Option.getTopMergin(),
            Option.getBtmMergin())
        logging.debug('%20s [%d,%d,%d,%d]' % (
            'left Screen mergin',
            lMergin[0],
            lMergin[1],
            lMergin[2],
            lMergin[3]))
        rMergin = (
            0,
            Option.getRMergin(),
            Option.getTopMergin(),
            Option.getBtmMergin())
        logging.debug('%20s [%d,%d,%d,%d]' % (
            'right Screen mergin',
            rMergin[0],
            rMergin[1],
            rMergin[2],
            rMergin[3]))

        if not self._checkContain(Ws, Img1, lMergin):
            self._downsizeImg(Ws, Img1, lMergin)
        if not self._checkContain(Ws, Img2, rMergin):
            self._downsizeImg(Ws, Img2, rMergin)

        self._allocateCenter(Ws, Img1, 1)
        self._allocateCenter(Ws, Img2, 2)
        self._allocateImg(Option, Ws, Img1)
        self._allocateImg(Option, Ws, Img2)

        bkImg = ImgFile('', Option.getBgcolor(), Ws.Size.w, Ws.Size.h)

        self._mergeWallpaper(Ws, bkImg, Img1)
        self._mergeWallpaper(Ws, bkImg, Img2)
        return bkImg

    def _optimizeWallpaper(self, Option, Config, Ws, Img):
        """
        1 ImgFile allocate Wallpaper Img.
        """
        logging.info('Optimizing ... wallpapaer.')
        self._initializeScreen()
        self._checkImgType(Ws, Img, 1)

        #代  self._bindingImgToScreen(Option.getFixed(), Img1, Img2)
        setattr(Img, 'posit', 'left')

        logging.info('Calculate mergin.')
        Mergin = (
            Option.getLMergin(),
            Option.getRMergin(),
            Option.getTopMergin(),
            Option.getBtmMergin())
        logging.debug(
            '%20s [%d,%d,%d,%d]' % (
                'Screen mergin',
                Mergin[0],
                Mergin[1],
                Mergin[2],
                Mergin[3]))

        if not self._checkContain(Ws, Img, Mergin):
            self._downsizeImg(Ws, Img, Mergin)

        self._allocateCenter(Ws, Img, 1)
        self._allocateImg(Option, Ws, Img)

        bkImg = ImgFile(
            '',
            Option.getBgcolor(),
            Ws.lScreen.Size.w,
            Ws.lScreen.Size.h)

        self._mergeWallpaper(Ws, bkImg, Img)
        return bkImg

    def _setWall(self, bkImg, savePath=None):
        """
        Wallpaper Img set to GNOME wallpaper.
        """
        factory = CommandFactory()
        cmd = factory.create(WallpaperOptimizer.WINDOWMANAGER)

        # use Xfce4(4.10.1 later) only
        cmd.setOption(self.option)

        removePath = cmd.getWall()
        logging.debug('Current wallpaper [%s].' % removePath)
        if removePath.find('wallopt') < 0:
            removePath = None

        if savePath is None:
            savedPath = self._saveImgfile(bkImg, savePath)

        savedPath = os.path.abspath(savedPath)
        cmd.setWall(savedPath)
        cmd.setView()
        logging.info(
            'Change wallpaper to current Workspace [%s].' % (savedPath))

        if removePath is not None:
            if os.path.exists(removePath):
                os.remove(removePath)
                logging.debug('Delete wallpaper [%s].' % removePath)
            lstCleanFile = glob.glob(
                os.path.join(
                    WallpaperOptimizer.USERENVDIR,
                    'wallopt*.jpg'))
            if len(lstCleanFile) > 1:
                lstCleanFile.remove(savedPath)
                for x in lstCleanFile:
                    os.remove(x)
                    logging.debug('Cleanup old wallpapaer [%s].' % x)

    def _saveImgfile(self, bkImg, savePath):
        try:
            if savePath is None:
                savePath = os.path.join(
                    WallpaperOptimizer.USERENVDIR,
                    'wallopt' +
                    datetime.datetime.now().strftime('%Y%m%d-%H%M%S') +
                    '.jpg')
            bkImg.save(savePath)
            logging.info('Save optimized wallpaper [%s].' % savePath)
            return savePath
        except ImgFile.ImgFileIOError, msg:
            raise Core.CoreRuntimeError(msg.value)

    def _createBkImg(self):
        try:
            Img1 = ImgFile(self.LChangerDir.getImgfileRnd())
            Img2 = ImgFile(self.RChangerDir.getImgfileRnd())
        except ImgFile.ImgFileIOError, msg:
            raise Core.CoreRuntimeError(msg.value)

        if (
            WallpaperOptimizer.WINDOWMANAGER == 'Gnome3' or
            WallpaperOptimizer.WINDOWMANAGER == 'xfce40' or
            WallpaperOptimizer.WINDOWMANAGER == 'xfce41' or
            WallpaperOptimizer.WINDOWMANAGER == 'lxde'
        ):
            bkImg = self._optimizeWallpapers(
                self.option,
                self.config,
                self.Ws,
                Img1,
                Img2)
        elif WallpaperOptimizer.WINDOWMANAGER == 'Gnome2':
            bkImg = self._optimizeWallpaper(
                self.option,
                self.config,
                self.Ws,
                Img1)
        else:
            pass

        self._setWall(bkImg)

    def _setSrcdir(self, bRaise):
        try:
            self.LChangerDir = ChangerDir(self.config.lDisplay.srcdir)
            self.RChangerDir = ChangerDir(self.config.rDisplay.srcdir)
        except ChangerDir.FileCountZeroError, msg:
            if bRaise:
                raise Core.CoreRuntimeError(msg.value)
            else:
                logging.error('** %s.' % msg)
                sys.exit(2)

    def timerRun(self):
        self._setSrcdir(True)
        self._createBkImg()

    def background(self):
        self._setSrcdir(False)
        try:
            while (1):
                self._createBkImg()
                interval = self.option.getInterval()
                time.sleep(interval)
        except KeyboardInterrupt:
            sys.exit(0)

    def _loadImgFile(self, path):
        if path != '':
            try:
                Img = ImgFile(path)
            except ImgFile.ImgFileIOError, msg:
                raise Core.CoreRuntimeError(msg.value)
            logging.info('Load ImgFile. [%s]' % path)
            logging.debug('%20s [%d,%d]' % ('Img', Img.Size.w, Img.Size.h))
            return Img
        else:
            try:
                dummyImg = ImgFile('', self.option.getBgcolor())
            except ImgFile.ImgFileIOError, msg:
                raise Core.CoreRuntimeError(msg.value)
            logging.debug('Create Dummy Img object.')
            return dummyImg

    def singlerun(self):
        if (self.option.lengthArgs() == 2 or
                (
                    self.option.lengthArgs() == 1 and
                    not self.Ws.isSeparate())):
            Imgs = (
                self._loadImgFile(self.option.getLArg()),
                self._loadImgFile(self.option.getRArg()))
            bkImg = self._optimizeWallpapers(
                self.option,
                self.config,
                self.Ws,
                Imgs[0],
                Imgs[1])

        elif self.option.lengthArgs() == 1 and self.Ws.isSeparate():
            if self.option.getSetWall():
                if self.option.getLArg() != '':
                    Img = self._loadImgFile(self.option.getLArg())
                else:
                    Img = self._loadImgFile(self.option.getRArg())
            bkImg = self._optimizeWallpaper(
                self.option,
                self.config,
                self.Ws,
                Img)

        savePath = self.option.getSavePath()
        if savePath is not None:
            self._saveImgfile(bkImg, savePath)
        if self.option.getSetWall():
            self._setWall(bkImg, savePath)

    def __init__(self, Options):
        self.option = Options
        self._initializeConfig()
        self._initializeWorkSpace()
        self.LChangerDir = None
        self.RChangerDir = None
