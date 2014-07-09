from Crypto.Cipher import AES
from Crypto import Random

class Userpass:
    """A simple but not so secure object for username and password storage and retrieval"""

    def __init__ (self):
        self.length = dict()
        self.database = dict()
        self.current_user = ""
        self.mode = AES.MODE_CBC
        self.bs = 32
        self.key = Random.new().read(self.bs)
        self.iv = Random.new().read(16)

    def add_user_passwd (self, user, passwd):
        """add a username/password"""
        #set current_user if not set
        if self.current_user == "":
            self.current_user = user
        #track length of password per user
        self.length[user] = len(passwd)
        c = AES.new(self.key, self.mode, self.iv)
        self.database[user] = c.encrypt(passwd.ljust(self.bs))

    def user (self):
        """return current user"""
        return self.current_user

    def passwd (self, input_user="CURRENTUSER"):
        """return password for specified input_user or current user"""
        if input_user == "CURRENTUSER":
            user = self.current_user
        else:
            user = input_user
        length = self.length[user]
        c = AES.new(self.key, self.mode, self.iv)
        return c.decrypt(self.database[user])[0:length]

    def change_user(self, user):
        """switch current user"""
        if user in self.database:
            #only switch if user is already in the database
            self.current_user = user

    def load (self, filename):
        """read in yaml file for password database"""
        import yaml
        import sys
        if sys.platform == "linux2":
            import os,stat
            os.chmod(filename,stat.S_IRUSR|stat.S_IWUSR)
        with open(filename) as fh:
            yamldict = yaml.safe_load(fh)
        users = yamldict["users"]
        firstuser = ""
        for user in users:
            self.add_user_passwd(user,users[user])
        if yamldict.has_key("defaultuser"):
            #set default user from defaultuser key
            self.change_user( yamldict["defaultuser"] )

    def users(self):
        """alias --> self.keys()"""
        return self.keys()

    def keys(self):
        """get list of users"""
        return self.database.keys()

    def has_key(self, key):
        """return True of user exists, else return False"""
        return self.database.has_key(key)
