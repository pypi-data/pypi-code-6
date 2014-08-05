import os


def load_serc511_log_file():
    module_path = os.pathdirname(__file__)
    return open(os.path.join(module_path, 'data', 'iris.csv'), 'r')
