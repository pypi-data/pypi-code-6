#!/usr/bin/env python
import uuid
import os
from boxes import Safe, FileBox

if __name__ == "__main__":
    box = Safe(FileBox('test'))
    for item in os.listdir('.'):
        if os.path.isfile(item):
            name = uuid.uuid4()
            box[name] = open(item)

    print box
    print box.items()
    print box.keys()
    del(box[box.keys()[1]])
    print box.items()
