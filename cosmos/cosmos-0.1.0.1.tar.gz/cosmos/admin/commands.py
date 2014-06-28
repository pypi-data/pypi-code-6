__author__ = 'Maruf Maniruzzaman'


import sys
import logging
import getpass

from cosmos.dataservice.objectservice import *
import settings


class CommandHandler():
    def __init__(self, *args, **kwargs):
        self.db = kwargs.get("db")

    def handle_command(self,command):
        if command == "new-admin":
            self.create_admin_user()
            return

        print "Unknown command"

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

