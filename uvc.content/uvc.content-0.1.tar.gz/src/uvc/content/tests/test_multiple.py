"""
Multiple schemas example
========================

Sonja The Red is a famous Hero and a Barbarian. She has a certain killing
standard but, all things considered, she's not a savage and she likes fancy
outfits. Two schemas can summarize her killing and fashion tendencies :

  >>> sonja = FemaleBarbarian()
  >>> IBarbarian.providedBy(sonja)
  True
  >>> IFemaleHero.providedBy(sonja)
  True

Sonja is maybe a barbarian, but her Redhair is one of her most priced assets.
So, if defined at the class level, the attribute will not be overriden and
the given value will be used.

  >>> sonja.nickname
  u'The Red'

The other attributes of our hero are still set to default.

  >>> sonja.armor
  u'metal bikini'

"""
from uvc.content import schema
from zope.interface import Interface
from zope.schema import TextLine, Int, Choice


class IFemaleHero(Interface):
    """A female hero, noticeable by her armor.
    """
    armor = Choice(
        title=u"Armor",
        values=[u'metal bikini', u'leather bikini'],
        default=u'metal bikini')


class IBarbarian(Interface):
    """A barbarian. Usually only wearing a leather underpants.
    """
    kills = Int(
        title=u"Kills !",
        default=100)

    nickname = TextLine(
        title=u"Nickname",
        default=u"The Barbarian")


class FemaleBarbarian(object):
    """A sexy barbarian content
    """
    schema(IFemaleHero, IBarbarian)
    nickname = u"The Red"
