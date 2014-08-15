# -*- coding: utf-8 -*-
from helga.plugins import command


_chars = u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!()_[]{}\\\',<>./?'
_flip = u'ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz∀qƆpƎℲפHIſʞ˥WNOԀQɹS┴∩ΛMX⅄ZƖᄅƐㄣϛ9ㄥ860¡)(‾][}{/,\'><˙\\¿'

MAP = dict((c, _flip[i]) for i, c in enumerate(_chars))


@command('flip', help='Flip words. Useage: helga flip [WORDS]')
def flip(client, channel, nick, message, cmd, args):
    words = u' '.join(args)
    output = u'(╯°□°）╯︵ '

    for c in words[::-1]:
        output += MAP.get(c, c)

    return output
