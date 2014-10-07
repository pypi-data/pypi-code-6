__author__    = 'Stojan Jovic <stojan.jovic@dmsgroup.rs>'
__contact__   = 'stojan.jovic@dmsgroup.rs'
__date__      = '12 December 2008'
__copyright__ = 'Copyright (c) 2008 DMS Group'


class Log4jProperties():
    """log4j additional properties"""
    
    def __init__(self, hostname='unknown', application='DEFAULT DOMAIN'):
        self.hostname = hostname
        self.application = application
    
    def get_hostname(self):
        return self.hostname
    
    def get_application(self):
        return self.application
    
    def set_hostname(self, hostname):
        self.hostname = hostname
    
    def set_application(self, application):
        self.application = application
