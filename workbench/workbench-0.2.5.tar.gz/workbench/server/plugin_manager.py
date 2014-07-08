
''' A simple plugin manager. Rolling my own for three reasons:
    1) Environmental scan did not give me quite what I wanted.
    2) The super simple examples didn't support automatic/dynamic loading.
    3) I kinda wanted to understand the process :)
'''

import os, sys
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import inspect

class PluginManager(FileSystemEventHandler):
    ''' Plugin Manager for Workbench '''

    def __init__(self, plugin_callback, plugin_dir = 'workers'):
        ''' Initialize the Plugin Manager for Workbench '''

        # Set the callback
        self.plugin_callback = plugin_callback

        # First go through the existing python files in the plugin directory
        self.plugin_path = os.path.realpath(plugin_dir)
        sys.path.append(plugin_dir)
        for f in [os.path.join(plugin_dir, child) for child in os.listdir(plugin_dir)]:

            # Skip certain files
            if '.DS_Store' in f or '__init__.py' in f: 
                continue

            # Add the plugin
            self.add_plugin(f)

        # Now setup dynamic monitoring of the plugins directory
        observer = Observer()
        observer.schedule(self, path=self.plugin_path)
        observer.start()

    def on_created(self, event):
        ''' Watcher callback '''
        self.add_plugin(event.src_path)
    def on_modified(self, event):
        ''' Watcher callback '''
        self.add_plugin(event.src_path)

    def add_plugin(self, f):
        ''' Adding and verifying plugin '''
        if f.endswith('.py'):

            # Just the basename without extension
            plugin_name = os.path.splitext(os.path.basename(f))[0]

            # It's possible the plugin has been modified and needs to be reloaded
            if plugin_name in sys.modules:
                try:
                    handler = reload(sys.modules[plugin_name])
                except ImportError, error:
                    print 'Failed to import plugin: %s (%s)' % (plugin_name, error)
                    return
            else:
                # Not already loaded so try to import it
                try:
                    handler = __import__(plugin_name, globals(), locals(), [], -1)
                except ImportError, error:
                    print 'Failed to import plugin: %s (%s)' % (plugin_name, error)
                    return

            # Run the handler through plugin validation
            plugin = self.validate(handler)
            if plugin:

                # Okay must be successfully loaded so capture the plugin meta-data,
                # modification time and register the plugin through the callback
                plugin['name'] = plugin_name
                plugin['dependencies'] = plugin['class'].dependencies
                mod_time = datetime.utcfromtimestamp(os.path.getmtime(f))
                self.plugin_callback(plugin, mod_time)

    def validate(self, handler):
        ''' Validate the plugin, each plugin must have the following:
            1) The worker class must have an execute method: execute(self, input_data)
            2) The worker class must have a dependencies list (even if it's empty)
            3) The file must have a top level test() method
        '''

        # Check for the test method first
        test_method = self.plugin_test_validation(handler)
        if not test_method:
            return None

        # Here we iterate through the classes found in the module and pick
        # the first one that satisfies the validation
        for name, plugin_class in inspect.getmembers(handler, inspect.isclass):
            if self.plugin_class_validation(plugin_class):
                return {'class':plugin_class, 'test':test_method}

        # If we're here the plugin didn't pass validation
        print 'Failure for plugin: %s' % (handler.__name__)
        print 'Validation Error: Worker class is required to have a dependencies list and an execute method'
        return None

    def plugin_test_validation(self, handler):
        ''' Plugin validation
            - Every workbench plugin must have top level test method
        '''
        methods = {name:func for name, func in inspect.getmembers(handler, callable)}
        if 'test' not in methods.keys():
            print 'Failure for plugin: %s' % (handler.__name__)
            print 'Validation Error: The file must have a top level test() method'
            return None
        else:
            return methods['test']

    def plugin_class_validation(self, plugin_class):
        ''' Plugin validation 
            - Every workbench plugin must have a dependencies list (even if it's empty)
            - Every workbench plugin must have an execute method.
        '''

        try:
            getattr(plugin_class, 'dependencies')
            getattr(plugin_class, 'execute')
        except AttributeError:
            return False

        return True


# Just create the class and run it for a test
def test():
    ''' -- plugin_manager.py test -- '''

    # This test actually does more than it appears. The workers
    # directory will get scanned and stuff will get loaded, etworkbench.
    def new_plugin(plugin, mod_time):
        ''' new plugin callback '''
        print '%s %s' % (plugin, mod_time)

    # Create Plugin Manager
    plugin_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'workers')
    PluginManager(new_plugin, plugin_dir=plugin_dir)

if __name__ == "__main__":
    test()
