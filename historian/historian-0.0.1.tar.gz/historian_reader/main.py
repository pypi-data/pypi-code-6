import sys
import csv

import historian_reader.shell

def main():
    writer = csv.writer(sys.stdout)
    writer.writerow(('session','session_date','command_id','command_date','token'))
    try:
        for session in historian_reader.shell.historian():
            for token in session['tokens']:
                command_id, command_date, token_string = token
                writer.writerow((session['session'],
                                 session['session_date'].timestamp(),
                                 command_id,
                                 command_date.timestamp(),
                                 token_string))
    except KeyboardInterrupt:
        pass
    except BrokenPipeError:
        pass
