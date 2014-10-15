import cmd
from .main import cli
from hyperdns.vendor.core import import_driver

class VendorShell(cmd.Cmd):
    """Provides an interactive shell interface to the vendor utilities.
    """ 
    def __init__(self,configuration):
        """Create an instance of the shell - this is built by the 'shell'
        command in VendorCommands (see VendorCommands::run_shell in get_commands).
        The configuration is only available at the last minute, which is why
        we create this vendor shell at the last minute.
        
        Also note that self.vkey is set during class construction in VendorCommands,
        since the actuall class that is created is not VendorShell, but a
        dynamically created subclass VendorShell_<vkey>.  This malarky has to do
        with tricking the cmd.Cmd system into finding the class-attached do_<cmd>
        methods and associating the do_<cmd> method __doc__ strings, which are
        sensitive <vkey> (or rather, to the driver class loaded via <vkey>)
        """
        cmd.Cmd.__init__(self)
        self.dclass=import_driver(self.vkey)
        self.prompt="%s>> " % self.dclass.name
        self.intro="Welcome to the HAPI %s vendor shell" % self.dclass.name
        #self.completekey='\t'
        
    def _tokenize(self,cmd,line):
        """Create the equivalent of sys.argv from the command and the interactive
        shell line.  We have to
        
        :param str cmd: this is the command to be executed by click.
        :param str line: this is the rest of the command line from cmd.Cmd
        """
        args=line.split(' ')
        args.insert(0,cmd)
        args.insert(0,self.vkey)
        args=[x for x in args if x!='']
        #args.insert(0,PROGNAME)
        return args

    def _invoke(self,cmd,line):
        """Parse the command line and invoke the click.Command equivalent
        of the command.  Note - cmd matches the do_<cmd> method that was
        invoked - so it needs to be 're-added' to the line in the tokenization
        process.
        
        :param str cmd: this is the command to be executed by click.
        :param str line: this is the rest of the command line from cmd.Cmd
        """
        try:
            args=self._tokenize(cmd,line)
            cli.main(args=args)
        except SystemExit:
            pass
        except Exception as E:
            print("Error:%s" % E)
            raise

    def do_exit(self,line):
        """Exit the shell"""
        return True
        
    def emptyline(self):
        """This line will make an empty line (just hitting return)
        do nothing - the default being to re-issue the previous command.
        """
        pass

#