# -*- extra stuff goes here -*-
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('ityou.qrcode')


INSTANCE_PATH   = '/'.join(INSTANCE_HOME.split('/')[:-2])
QRCODE_LOCATION = INSTANCE_PATH + "/src/ityou.qrcode/src/ityou/qrcode/qr_codes"
QRCODE_RESOURCE = "++resource++ityou.qrcodes"

BOXSIZE = 10 # Pixel
OFFSET  = 4 # Boxes
BOXCOLOR = '#596069' # grau


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
