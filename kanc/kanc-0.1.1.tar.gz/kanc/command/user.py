from base import BaseCommand
from base import CommandError
import json

class UserCommand(BaseCommand):
    name = 'user'

    def __init__(self, client):
        super(UserCommand, self).__init__(client)
        self.param_order = ['id', 'user_id', 'username', 'name']

    def help(self):
        print 'List of user subcommands'
        print '------------'
        print 'kanc user list - list all users'
        print 'kanc user show {user_id} - show user'
        print 'kanc user create - create new user'
        print 'kanc user edit {user_id} - edit a user'
        print ''
    
    def action(self, args):
        if len(args) == 0:
            raise CommandError('Subcommand not specified')

        if args[0] == 'help':
            self.help()
        if args[0] == 'list':
            self.print_items(self.client.get_all_users(), 
                    ['id', 'username', 'name'])
        elif args[0] == 'show':
            if len(args) < 2:
                raise CommandError("Needs to specify user_id")
            user_id = int(args[1])
            user = self.client.get_user(user_id)
            primary_fields = ['id', 'username', 'name']
            self.print_attr(user, primary_fields)
        elif args[0] == 'create':
            user = self.client.create_empty_params('createUser')
            user = self.edit_attr(user, ['username'])
            if user is not None:
                self.client.create_user(**user)
        elif args[0] == 'edit':
            if len(args) < 2:
                raise CommandError("Needs to specify user_id")
            user_id = int(args[1])
            user = self.client.get_user(user_id)
            user = self.client.remove_unused_params('updateUser', user)
            update = self.edit_attr(user, ['id', 'username'])
            if update is not None:
                self.client.update_user(**update)
        else:
            raise CommandError("Unknown subcommand")


