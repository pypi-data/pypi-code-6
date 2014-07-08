
class DockyardPlugin(object):

    def configureSuppliedParser(self, moduleSubparsers):

        parser = moduleSubparsers.add_parser('dockyard', help='Dockyard related operations')
        
        ## Module - Dockyard
        dockyardSubparsers = parser.add_subparsers(dest='operation', help='Docker operations help')

        parser = dockyardSubparsers.add_parser('init', help='Initialize Dockyard')
        parser = dockyardSubparsers.add_parser('list', help='List active Dockyards')

        # Dockyard - start
        parser = dockyardSubparsers.add_parser('start', help='Start dockyard(s)')
        parser.add_argument('dockyard', type=str, nargs='+', help='Dockyard container names')

        # Dockyard - stop
        parser = dockyardSubparsers.add_parser('stop', help='Stop dockyard(s)')
        parser.add_argument('dockyard', type=str, nargs='+', help='Dockyard name or id')

