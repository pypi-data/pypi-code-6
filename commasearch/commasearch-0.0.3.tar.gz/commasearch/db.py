import os
import re, json

from pickle_warehouse import Warehouse

home = os.path.expanduser('~')
indices = Warehouse(os.path.join(home, '.,', 'indices'))
errors = Warehouse(os.path.join(home, '.,', 'errors'))
def values(index):
    columns = json.dumps(index)
    subdirectory = columns if len(columns) <= 255 else str(hash(index))
    directory = os.path.join(home, '.,', 'values', re.sub(r'[\/]', '|', subdirectory))
    return Warehouse(directory)
