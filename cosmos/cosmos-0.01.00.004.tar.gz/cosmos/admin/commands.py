__author__ = 'Maruf Maniruzzaman'

import os
import sys
import logging
import getpass
import createproject

from cosmos.dataservice.objectservice import *

class CommandHandler():
    def __init__(self, *args, **kwargs):
        self.db = kwargs.get("db", None)

    def handle_command(self, *args, **kwarg):
        current_directory = args[0]
        command = args[1]
        print command

        if command == "new-admin":
            self.create_admin_user()
            return
        elif command == "new-project":
            createproject.new_project(current_directory)
            sys.exit(0)
        else:
            print "Unknown command"
            sys.exit(0)

    def get_input(self, prompt):
        input = None
        while not input or len(input)==0:
            input = raw_input(prompt).strip()

        return input

    def _admin_user_created(self, result, error):
        if error:
            logging.error("Admin user creation failed.")
            logging.error(error)
        else:
            logging.info("Admin user was created successfully.")

        sys.exit(0)

    def create_admin_user(self):
        username = self.get_input('Enter admin username: ')
        password = getpass.getpass('Enter admin password: ')
        password_re = getpass.getpass('Repeat admin password: ')
        if password != password_re:
            print "Password mismatch"
            sys.exit(1)

        email = self.get_input('Enter admin email: ')
        data = {"username":username, "password":password, "email":email, "roles":[ADMIN_USER_ROLE_SID]}
        object_service = ObjectService()
        object_service.save(SYSTEM_USER, self.db, COSMOS_USERS_OBJECT_NAME, data, self._admin_user_created)



def admin_main():
    current_directory = os.getcwd()
    if len(sys.argv) < 1:
        print "Command required"
        return
    else:
        command = sys.argv[1].strip()
        handler = CommandHandler()
        handler.handle_command(current_directory, command)

    tornado.ioloop.IOLoop.instance().start()
