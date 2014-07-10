from .controller import connect, get_config
import tempfile
import os
import sys
import configparser

class Snippet(object):
    """
    Class for working with snippets
    """
    def __init__(self, category=None, name=None, content=None):
        """
        init for snippets
        """
        self.category = category
        self.name = name
        self.content = content

    def commit(self):
        """
        save your snippet to redis
        """
        r = connect()
        if self.category and self.name:
            r.set('%s:%s' % (self.category, self.name), self.content)
        else:
            print('ERROR: Category or Name is  empty... exiting')
            sys.exit(1)

    def exists(self):
        """
        check if the snippet already exists
        """
        r = connect()
        if r.get("%s:%s" % (self.category, self.name)):
            return True
        else:
            return False

    def get(self):
        """
        get the content of a snippet
        """
        r = connect()
        try:
            return r.get('%s:%s' % (self.category, self.name)).decode()
        except AttributeError:
            print("ERROR: cannot find your snippet"),
            exit(1)

    def rename(self, newname):
        """
        rename a snippet, but not the category
        """
        r = connect()
        r.rename('%s:%s' % (self.category, self.name), '%s:%s' \
                 % (self.category, newname))

    def edit(self):
        """
        edit your snippet
        """
        if get_config():
            configfile = get_config()
            config = configparser.ConfigParser()
            config.read(configfile)
            editor = config['GLOBAL']['editor']
        else:
            editor = 'vim'
        fh = tempfile.NamedTemporaryFile(delete=False)
        fh.write(self.get().encode('UTF-8'))
        fh.flush()
        openeditor = '%s %s' % (editor, fh.name)
        os.system(openeditor)
        if os.path.getsize(fh.name) > 0:
            self.content = open(fh.name).read()
            self.commit()
        else:
            print("Your snippet is empty... exiting")
            sys.exit(1)

    def delete(self):
        """
        delete your snippet
        """
        r = connect()
        r.delete('%s:%s' % (self.category, self.name))
