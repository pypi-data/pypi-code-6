from dippy import Container

class Girl(object):

    instance_dependencies = dict(context='context')
    constructor_dependencies = dict(partner='kissable', name='girl_name')

    def __init__(self, partner=None, name='', *args, **kwds):
        self.partner = partner
        self.name = name
    
    def give_kiss(self):
        print "GIRL(in %s, named %s) SAYS: Mwah!" % (self.context, self.name)
        self.partner.receive_kiss()

class ProgrammerGirl(Girl):
    constructor_dependencies = dict(programming_language='programming_language')

    def __init__(self, programming_language, *args, **kwds):
        super(ProgrammerGirl, self).__init__(*args, **kwds)
        self.programming_language = programming_language

    def give_kiss(self):
        print "PROGRAMMER GIRL SAYS: do you want to write some %s code?" % self.programming_language
        super(ProgrammerGirl, self).give_kiss()

class Kissable(object):
    pass

class Boy(Kissable):
    def receive_kiss(self):
        print "BOY SAYS: Mwwwahhh!"

container = Container()
container.register_singleton('kissable', Boy)
container.register_service_factory('girl', ProgrammerGirl)
container.register_instance('girl_name', 'Rebecca')
container.register_instance('context', 'hawaii')
container.register_instance('programming_language', 'Python')
g = container.girl()
g.give_kiss()
