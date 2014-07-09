import cmd2
from termcolor import colored

class ConsoleBase(cmd2.Cmd):

    section    = 'console'
    configFile = 'console.cfg'
    prompt     = colored('(console) ', 'green')
    intro      = colored('Console de Base', 'grey')
    config     = ''

    LIST_VARIABLE = { }
    
    def __init__(self, config):
        self.config = config
        self.read_config()
        cmd2.Cmd.__init__(self)

    def read_config(self):
        self.config.read(self.configFile)
        for variable in self.LIST_VARIABLE.keys():
            try:
                setattr(self, variable, self.config.get(self.section, variable))
            except Exception as e:
                print e
                print colored("Variable %s undefined in cfg file %s section %s" % (variable,self.configFile, self.section), 'red')

    # config
    def do_config(self, line):
        for (variable, description) in self.LIST_VARIABLE.iteritems():
            print "%25s : %s" % (description, colored(getattr(self, variable),'green'))
    
    def help_config(self):
        print '\n'.join([ 'config',
                          'show configuration'
                        ])

    # GET
    def do_get(self, variable):
        if variable not in self.LIST_VARIABLE.keys():
            print colored('Variable not found','red')
        else:
            print "%s : %s" % (variable,getattr(self, variable))

    def help_get(self):
        print '\n'.join([ 'get [variable]',
                        ' show variable value'
                        ])

    def complete_get(self, text, line, begids, endidx):
        if not text:
            completions = self.LIST_VARIABLE.keys()[:]
        else:
            completions = [ f
                    for f in self.LIST_VARIABLE.keys()
                    if f.startswith(text)
                    ]
        return completions

    # SET
    def do_set(self, arg):
        (variable, value) = arg.split(' ')
        setattr(self, variable, value)

    def help_set(self):
        print '\n'.join([ 'set [variable] [value]',
                          'set variable with value'
                        ])

    def complete_set(self, text, line, begidx, endidx):
        return self.complete_get(text, line, begidx, endidx)


    # Save
    def do_save(self, line):
        for variable in self.LIST_VARIABLE.keys():
            self.config.set(self.section,variable,getattr(self,variable))
        with open(self.configFile,'wb') as configfile:
            self.config.write(configfile)

    def help_save(self):
        print '\n'.join([ 'save',
                          'save config'
                          ])

