
class DockerPlugin(object):

    def configureSuppliedParser(self, moduleSubparsers):

        parser = moduleSubparsers.add_parser('docker', help='Execute Docker related tasks from the host')

        ## Module - Docker
        dockerSubparsers = parser.add_subparsers(dest='operation', help='Docker operations help')

        # Exec
        parser = dockerSubparsers.add_parser('command', help='Execute command')
        parser.add_argument('arg', type=str, nargs='+', help='Execution arguments')

        # Docker - build
        parser = dockerSubparsers.add_parser('build', help='Build Docker containers')
        parser.add_argument('docker', type=str, nargs='+', help='Docker container names')

        # Docker - images
        parser = dockerSubparsers.add_parser('image', help='Image operations')
        subparser = parser.add_subparsers(dest='action', help='Image operations')
        parser = subparser.add_parser('list', help='List images')
        parser = subparser.add_parser('remove', help='Remove image(s)')
        parser.add_argument('image', type=str, nargs='+', help='Image name, \'all\' for all')
        parser = subparser.add_parser('create', help='Create image(s)')
        parser.add_argument('image', type=str, nargs='+', help='Image name, \'all\' for all')
        parser = subparser.add_parser('run', help='Run image(s)')
        parser.add_argument('image', type=str, nargs='+', help='Image name, \'all\' for all')
        parser = subparser.add_parser('history', help='Kill container(s)')

        parser = dockerSubparsers.add_parser('container', help='Container operations')
        subparser = parser.add_subparsers(dest='action', help='Container operations')
        parser = subparser.add_parser('list', help='List container(s)')
        parser = subparser.add_parser('kill', help='Kill container(s)')
        parser.add_argument('hash', type=str, nargs='+', help='Container hash, \'all\' for all')