import os
import traceback
import shlex
from subprocess import Popen, PIPE
import npyscreen


# We override ActionForm to provide us Login & Refresh buttons (Login is the OK button, Refresh is the Cancel button)
class MainForm(npyscreen.ActionForm):
    OK_BUTTON_TEXT = ' Login '
    CANCEL_BUTTON_TEXT = ' Refresh '
    CANCEL_BUTTON_BR_OFFSET = (2, 16)

    def __init__(self, *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)
        self.prefix_errors = []

    def on_ok(self):
        error = self.parentApp.login()
        # If we reached here it means we failed to execute the login program.
        self.prefix_errors = ["Failed to execute login program:"] + error
        self.parentApp.switchForm("MAIN")

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")

    def beforeEditing(self):
        status, lines = self.parentApp.get_form_data(self.prefix_errors)
        self.prefix_errors = []

        status_widget = self.get_widget('status')
        status_widget.entry_widget.color = 'GOOD' if status else 'DANGER'
        status_widget.value = 'OK' if status else 'ERROR'

        log_widget = self.get_widget('log')
        log_widget.hidden = status
        log_widget.values = lines


class Greeter(npyscreen.NPSAppManaged):
    def __init__(self, product_name, version, log_file_path, status_program, login_program):
        super(Greeter, self).__init__()
        self.product_name = product_name
        self.version = version
        self.log_file_path = log_file_path
        self.status_program = status_program
        self.login_program = login_program

    def load_log(self):
        """returns list of log lines"""
        try:
            with open(self.log_file_path, 'r') as f:
                return [s.rstrip() for s in f.readlines()]
        except:
            return traceback.format_exc().split("\n")

    def get_status(self):
        """returns (bool, list of error lines)"""
        try:
            args = shlex.split(self.status_program)
            with open(os.devnull, 'w') as devnull:
                p = Popen(args, stdin=devnull, stdout=PIPE, stderr=PIPE, close_fds=True, shell=False)
                stdout, stderr = p.communicate()
                exitcode = p.wait()
            return exitcode == 0, ["Status command: " + repr(args), "Status stdout:"] + stdout.split("\n") + ["Status stderr:"] + stderr.split("\n")
        except:
            return False, ["Error executing status program:"] + traceback.format_exc().split("\n")

    def clear_and_restore_terminal(self):
        # We want to clear the screen and restore the terminal mode before execing the login program
        import curses
        self.getForm('MAIN').erase()
        curses.curs_set(1)
        curses.reset_shell_mode()

    def close_fds(self):
        import glob
        import sys
        fd_paths = glob.glob("/proc/{}/fd/*".format(str(os.getpid())))
        fds = set(int(os.path.basename(p)) for p in fd_paths)
        exclude_fds = set(f.fileno() for f in (sys.stdin, sys.stdout, sys.stderr))
        for fd in (fds - exclude_fds):
            try:
                os.close(fd)
            except:
                pass

    def login(self):
        """this method should never return, but if it does it returns a list of error lines"""
        try:
            self.clear_and_restore_terminal()
            parts = shlex.split(self.login_program)
            self.close_fds()
            os.execv(parts[0], parts)
        except:
            return traceback.format_exc().split("\n")

    def create_form(self):
        f = MainForm(name="MAIN", framed=False, parentApp=self)
        f.add(npyscreen.FixedText, value=self.product_name + ' ' + self.version, editable=False)
        f.add(npyscreen.FixedText, value='', editable=False)  #  spacer
        f.add(npyscreen.TitleText, w_id='status', name='Service Status:', labelColor='DEFAULT', editable=False, use_two_lines=False)
        f.add(npyscreen.FixedText, value='', editable=False)  #  spacer
        f.add(npyscreen.BoxTitle, w_id='log', name='Status & Log Output', color='DEFAULT', scroll_exit=True)
        return f

    def get_form_data(self, prefix_errors=[]):
        status, status_output = self.get_status()
        lines = prefix_errors + status_output + ([ "", "Log file:"] + self.load_log() if not status else [])
        return status, lines

    def onStart(self):
        form = self.create_form()
        self.registerForm("MAIN", form)

