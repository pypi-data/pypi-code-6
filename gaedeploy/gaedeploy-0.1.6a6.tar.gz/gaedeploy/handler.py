from watchdog.events import FileSystemEventHandler
# from subprocess import call
# import string
# import os

class DeployEventHandler(FileSystemEventHandler):
    def __init__(self, command):
    # def __init__(self, path, command):
        # self.path = path
        # self.commands = string.split(command, " ")
        self.command = command

    def _run_build_tools(self):
        self.command.execute()
        # os.chdir(self.path)
        # call(self.commands)

    def on_moved(self, event):
        self._run_build_tools()

    def on_created(self, event):
        self._run_build_tools()

    def on_deleted(self, event):
        self._run_build_tools()

    def on_modified(self, event):
        self._run_build_tools()
