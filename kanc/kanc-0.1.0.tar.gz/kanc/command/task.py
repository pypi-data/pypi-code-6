from base import BaseCommand

class TaskCommand(BaseCommand):
    name = 'task'

    def __init__(self, client):
        super(TaskCommand, self).__init__(client)
    
    def help(self):
        print 'List of project subcommands'
        print '------------'
        print 'kanc task list {project_id} - list all tasks'
        print 'kanc task show {task_id} - show a task'
        print 'kanc task create - create new task'
        print 'kanc task edit {task_id} - edit a task'
        print 'kanc task move {task_id} up - move a task up on the board'
        print 'kanc task move {task_id} down - move a task down on the board'
        print 'kanc task move {task_id} {column} - move a task to other column'
        print ''
    
    def find_col(self, project_id, col_name):
        col = None
        cols = self.client.get_columns(project_id)
        for c in cols:
            if c['title'].startswith(unicode(col_name)):
                col = c
                break
        return col
    
    def action(self, args):
        if args[0] == 'list':
            project_id = int(args[1])
            tasks = self.client.get_all_tasks(project_id, 1)
            users = self.client.get_all_users()
            columns = self.client.get_columns(project_id)
            result = self.join_attr(tasks, 'owner_id', users, 'id', 
                    {'username':'assignee'})
            result = self.join_attr(result, 'column_id', columns, 'id', 
                    {'title':'column'})
            self.print_items(result, ['id', 'title', 'assignee', 'column'])

        elif args[0] == 'show':
            task_id = int(args[1])
            task = self.client.get_task(task_id)
            self.print_attr(task, ['id','title'])

        elif args[0] == 'create':
            task = self.client.create_empty_params('createTask')
            task = self.edit_attr(task, ['title', 'project_id'])
            if task is not None:
                self.client.create_task(**task)

        elif args[0] == 'edit':
            task_id = int(args[1])
            task = self.client.get_task(task_id)
            task = self.client.remove_unused_params('updateTask', task)
            update = self.edit_attr(task, ['id','title'])
            if update is not None:
                self.client.update_task(**update)

        elif args[0] == 'move':
            task_id = int(args[1])
            task = self.client.get_task(task_id)
            project_id = task['project_id']
            column_id = int(task['column_id'])
            position = int(task['position'])
            if args[2] == 'up':
                position -= 1
            elif args[2] == 'down':
                position += 1
            else:
                col_name = args[2]
                col = self.find_col(project_id, col_name)
                if col is None:
                    print 'Error: column {} not found'.format(col_name)
                    return False
                else:
                    position = 1
                    column_id = col['id']
            self.client.move_task_position(project_id=project_id,
                    task_id=task_id, column_id=column_id, position=position)

        elif args[0] == 'open':
            task_id = int(args[1])
            self.client.open_task(task_id)

        elif args[0] == 'close':
            task_id = int(args[1])
            self.client.close_task(task_id)

