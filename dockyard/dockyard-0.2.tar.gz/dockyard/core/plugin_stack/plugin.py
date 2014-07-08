
class StackPlugin(object):

    def configureSuppliedParser(self, moduleSubparsers):

        parser = moduleSubparsers.add_parser('stack', help='Stack related commands, can combine vagrant + docker commands into a single command')
        
        ## Module - Stack
        stackSubparsers = parser.add_subparsers(dest='operation', help='Stack operations')

        # Stack - up
        parser = stackSubparsers.add_parser('up', help='Create Vagrant VM, build Docker containers')

        # Stack - down
        parser = stackSubparsers.add_parser('down', help='Destroy Vagrant VM')

        # Stack - 
        parser = stackSubparsers.add_parser('start', help='Start a dock configuration')
        parser.add_argument('configuration', type=str, nargs='+', help='Dock configuration')

        parser = stackSubparsers.add_parser('stop', help='Stop a dock configuration')
        parser.add_argument('configuration', type=str, nargs='+', help='Dock configuration')

