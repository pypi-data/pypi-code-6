from zope.i18n import translate

from zettwerk.mailtemplates import mailtemplatesMessageFactory as _

from DateTime import DateTime
NULL_TIME = DateTime('2000/01/01')


class RegistrationReminder(object):

    def getTitle(self, request):
        return _(translate(
                u'Not logged on members',
                'zettwerk.mailtemplates',
                context=request)
                 )

    def filteredMembers(self, members):
        filtered = []
        for member in members:
            if member.getProperty('login_time') == NULL_TIME:
                filtered.append(member)
        return filtered
