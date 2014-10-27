from base import BaseCommand
from base import CommandError
import json

class UserCommand(BaseCommand):
    name = 'user'

    def __init__(self, client, rcfile):
        super(UserCommand, self).__init__(client, rcfile)
        self.param_order = ['id', 'user_id', 'username', 'name']

    def help(self):
        print 'List of user subcommands'
        print '------------'
        print 'kanc user list - list all users'
        print 'kanc user show {user_id} - show user'
        print 'kanc user create - create new user'
        print 'kanc user edit {user_id} - edit a user'
        print 'kanc user remove {user_id_1} {user_id_2} ... - remove users'
        print ''
    
    def action(self, subcmd, args):
        if subcmd is None:
            raise CommandError('Subcommand not specified')

        if subcmd == 'help':
            self.help()

        if subcmd == 'list':
            self.print_items(self.client.get_all_users(), 
                    ['id', 'username', 'name'])

        elif subcmd == 'show':
            if len(args) < 1:
                raise CommandError("Needs to specify user_id")
            user_id = int(args[0])
            user = self.client.get_user(user_id)
            primary_fields = ['id', 'username', 'name']
            self.print_attr(user, primary_fields)

        elif subcmd == 'create':
            user = self.client.create_empty_params('createUser')
            user = self.edit_attr(user, ['username'])
            if user is not None:
                self.client.create_user(**user)

        elif subcmd == 'edit':
            if len(args) < 1:
                raise CommandError("Needs to specify user_id")
            user_id = int(args[0])
            user = self.client.get_user(user_id)
            user = self.client.remove_unused_params('updateUser', user)
            update = self.edit_attr(user, ['id', 'username'])
            if update is not None:
                self.client.update_user(**update)
        
        elif subcmd == 'remove':
            if len(args) < 1:
                raise CommandError('user_id not specified')
            for u in args[0:]:
                user_id = int(u)
                if not self.client.remove_user(user_id):
                    raise CommandError('could not delete user')
        else:
            raise CommandError("Unknown subcommand")


