from base import BaseCommand
from base import CommandError

class TaskCommand(BaseCommand):
    name = 'task'

    def __init__(self, client, rcfile):
        super(TaskCommand, self).__init__(client, rcfile)
    
    def help(self):
        print 'List of project subcommands'
        print '------------'
        print 'kanc task list - list all tasks in current project'
        print 'kanc task show {task_id} - show a task'
        print 'kanc task create - create new task'
        print 'kanc task edit {task_id} - edit a task'
        print 'kanc task remove {task_id} {task_id} - remove tasks'
        print 'kanc task move {task_id} up - move a task up on the board'
        print 'kanc task move {task_id} down - move a task down on the board'
        print 'kanc task move {task_id} {column} - move a task to other column'
        print 'kanc task open {task_id} - open a task'
        print 'kanc task close {task_id} - close a task'
        print ''
    
    def find_col(self, project_id, col_name):
        col = None
        cols = self.client.get_columns(project_id)
        for c in cols:
            if c['title'].startswith(unicode(col_name)):
                col = c
                break
        return col
    
    def action(self, subcmd, args):
        if subcmd is None:
            raise CommandError('Subcommand not specified')

        if subcmd == 'list':
            project_id = int(self.rcfile.get('currentProject'))
            tasks = self.client.get_all_tasks(project_id, 1)
            users = self.client.get_all_users()
            columns = self.client.get_columns(project_id)
            result = self.join_attr(tasks, 'owner_id', users, 'id', 
                    {'username':'assignee'})
            result = self.join_attr(result, 'column_id', columns, 'id', 
                    {'title':'column'})
            self.print_items(result, ['id', 'title', 'assignee', 'column'])

        elif subcmd == 'show':
            if len(args) < 1:
                raise CommandError('task_id not specified')
            task_id = int(args[0])
            task = self.client.get_task(task_id)
            self.print_attr(task, ['id','title'])

        elif subcmd == 'create':
            task = self.client.create_empty_params('createTask')
            task = self.edit_attr(task, ['title', 'project_id'])
            if task is not None:
                self.client.create_task(**task)

        elif subcmd == 'edit':
            if len(args) < 1:
                raise CommandError('task_id not specified')
            task_id = int(args[0])
            task = self.client.get_task(task_id)
            task = self.client.remove_unused_params('updateTask', task)
            update = self.edit_attr(task, ['id','title'])
            if update is not None:
                self.client.update_task(**update)

        elif subcmd == 'remove':
            if len(args) < 1:
                raise CommandError('task_id not specified')
            for t in args[1:]:
                task_id = int(t)
                if not self.client.remove_task(task_id):
                    raise CommandError('could not delete task')

        elif subcmd == 'move':
            if len(args) < 1:
                raise CommandError('task_id not specified')
            if len(args) < 2:
                raise CommandError('move destination not specified')
            task_id = int(args[0])
            task = self.client.get_task(task_id)
            project_id = task['project_id']
            column_id = int(task['column_id'])
            position = int(task['position'])
            if args[1] == 'up':
                position -= 1
            elif args[1] == 'down':
                position += 1
            else:
                col_name = args[1]
                col = self.find_col(project_id, col_name)
                if col is None:
                    print 'Error: column {} not found'.format(col_name)
                    return False
                else:
                    position = 1
                    column_id = col['id']
            self.client.move_task_position(project_id=project_id,
                    task_id=task_id, column_id=column_id, position=position)

        elif subcmd == 'open':
            if len(args) < 1:
                raise CommandError('task_id not specified')
            task_id = int(args[0])
            self.client.open_task(task_id)

        elif subcmd == 'close':
            if len(args) < 1:
                raise CommandError('task_id not specified')
            task_id = int(args[0])
            self.client.close_task(task_id)
        else:
            raise CommandError('Unknown subcommand specified')

