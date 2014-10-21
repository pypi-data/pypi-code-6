from base import BaseCommand
from base import CommandError

class ProjectCommand(BaseCommand):
    name = 'project'

    def __init__(self, client):
        super(ProjectCommand, self).__init__(client)
        
    def help(self):
        print 'List of project subcommands'
        print '------------'
        print 'kanc project list - list all projects'
        print 'kanc project show {project_id} - show a proejct'
        print 'kanc project create - create new project'
        print 'kanc project edit {project_id} - edit a project'
        print 'kanc project remove {project_id} {project_id} - remove projects'
        print ''
    
    def action(self, args):
        if len(args) == 0:
            raise CommandError('Subcommand not specified')

        if args[0] == 'list':
            self.print_items(self.client.get_all_projects(), ['id', 'name'])

        elif args[0] == 'show':
            if len(args) < 2:
                raise CommandError('project_id not specified')
            project_id = int(args[1])
            self.print_attr(self.client.get_project_by_id(project_id))

        elif args[0] == 'create':
            project = self.client.create_empty_params('createProject')
            project = self.edit_attr(project, ['name'])
            if project is not None:
                self.client.create_project(**project)

        elif args[0] == 'edit':
            if len(args) < 2:
                raise CommandError('project_id not specified')
            project_id = int(args[1])
            project = self.client.get_project_by_id(project_id)
            project = self.client.remove_unused_params('updateProject', project)
            update = self.edit_attr(project, ['id', 'name'])
            if update is not None:
                self.client.update_project(**update)
        
        elif args[0] == 'remove':
            if len(args) < 2:
                raise CommandError('project_id not specified')
            for p in args[1:]:
                project_id = int(p)
                if not self.client.remove_project(project_id):
                    raise CommandError('could not delete project')
        
        else:
            raise CommandError('Unknown subcommand')

