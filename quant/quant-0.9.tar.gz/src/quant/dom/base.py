from dm.dom.stateful import *

# todo: Rename PersonExtn as Person
# todo: Rename Person as User
class PersonExtn(DatedStatefulObject):

    realname = String()
    email = String('')
    user = HasA('Person', isRequired=False, default=None)

    searchAttributeNames = ['realname']
    startsWithAttributeName = 'realname'

    def getLabelValue(self):
        return self.realname or self.id

