from base import BaseCommand
from base import CommandError

class ProjectCommand(BaseCommand):
    name = 'project'

    def __init__(self, client, rcfile):
        super(ProjectCommand, self).__init__(client, rcfile)
        
    def help(self):
        print 'List of project subcommands'
        print '------------'
        print 'kanc project list - list all projects'
        print 'kanc project current - show current project'
        print 'kanc project swtich {project_id} - switch project'
        print 'kanc project show {project_id} - show a proejct'
        print 'kanc project create - create new project'
        print 'kanc project edit {project_id} - edit a project'
        print 'kanc project remove {project_id} {project_id} - remove projects'
        print ''
    
    def action(self, subcmd, args):
        if subcmd == 0:
            raise CommandError('Subcommand not specified')

        if subcmd == 'list':
            self.print_items(self.client.get_all_projects(), ['id', 'name'])

        elif subcmd == 'current':
            project_id = int(self.rcfile.get('currentProject'))
            project = self.client.get_project_by_id(project_id)
            if project is None:
                raise CommandError('Project not found')
            print '* Current Project: {0}.{1}'.format(project_id, project['name'])
        
        elif subcmd == 'switch':
            if len(args) < 1:
                raise CommandError('project_id not specified')
            project_id = int(args[0])
            project = self.client.get_project_by_id(project_id)
            if project is None:
                raise CommandError('Project not found')
            self.rcfile.set('currentProject', project_id)
            self.rcfile.save()
            print '* Switch project to: {0}.{1}'.format(project_id, project['name'])

        elif subcmd == 'show':
            if len(args) < 1:
                raise CommandError('project_id not specified')
            project_id = int(args[0])
            self.print_attr(self.client.get_project_by_id(project_id))

        elif subcmd == 'create':
            project = self.client.create_empty_params('createProject')
            project = self.edit_attr(project, ['name'])
            if project is not None:
                self.client.create_project(**project)

        elif subcmd == 'edit':
            if len(args) < 1:
                raise CommandError('project_id not specified')
            project_id = int(args[0])
            project = self.client.get_project_by_id(project_id)
            project = self.client.remove_unused_params('updateProject', project)
            update = self.edit_attr(project, ['id', 'name'])
            if update is not None:
                self.client.update_project(**update)
        
        elif subcmd == 'remove':
            if len(args) < 1:
                raise CommandError('project_id not specified')
            for p in args:
                project_id = int(p)
                if not self.client.remove_project(project_id):
                    raise CommandError('could not delete project')
        
        else:
            raise CommandError('Unknown subcommand')

