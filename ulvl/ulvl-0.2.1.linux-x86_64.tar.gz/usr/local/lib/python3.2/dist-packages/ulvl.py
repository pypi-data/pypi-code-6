# ulvl - Universal Level Formats
# Copyright (c) 2014 Julian Marchant <onpon4@riseup.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This library reads and writes universal level formats.  These level
formats are generic enough to be used by any 2-D game.  Their purpose is
to unify level editing.
"""

__version__ = "0.2.1"


import json
import warnings


__all__ = ["ASCL", "JSL", "LevelObject"]


class ASCL(object):

    """
    This class loads, stores, and saves ASCII Level (ASCL) files.  This
    format is based on a grid of plain text characters and generally has
    one of the following extensions: ".ascl", ".asc", ".txt".

    An ASCL file contains two main components: the meta variable
    definitions and the level object grid.

    Meta variables are defined simply at the top of the file: each line
    indicates the value of a different meta variable, always a string.
    Any number of meta variables can be defined.

    Everything after the first blank line in the ASCL file is considered
    to be part of the level object grid. Here, ASCII characters are used
    to represent level objects.  Any ASCII character can be used to
    represent an object except for ``" "``, which represents an empty
    tile.

    .. attribute:: meta

       A list of the level's meta variables.

    .. attribute:: objects

       A list of objects in the level as :class:`jsl.LevelObject`
       objects.  They must have single-character strings as types.
    """

    def __init__(self):
        self.meta = []
        self.objects = []

    @classmethod
    def load(cls, fname):
        """
        Load the indicated file and return a :class:`ulvl.ASCL` object.
        """
        self = cls()

        data = f.read()

        grid = False
        y = 0
        for line in data.splitlines():
            if grid:
                for x in range(len(line)):
                    char = line[x]
                    if char != " ":
                        obj = LevelObject(char, x, y)
                        self.objects.append(obj)
                y += 1
            elif line:
                self.meta.append(line)
            else:
                grid = True

        return self

    def save(self, f):
        """Save the object to the indicated file."""
        objects = []

        for obj in self.objects:
            T = str(obj.type)
            if len(T) == 1:
                x = int(round(obj.x))
                y = int(round(obj.y))
                while y >= len(objects):
                    objects.append([])
                while x >= len(objects[y]):
                    objects[y].append(" ")

                objects[y][x] = T
            else:
                raise ValueError("Object type must be a single character.")

        meta_data = [str(i) for i in self.meta]
        obj_data = [''.join(i) for i in objects]

        meta_text = '\n'.join(meta_data)
        obj_text = '\n'.join(obj_data)
        text = '\n\n'.join([meta_text, obj_text])

        f.write(text)


class JSL(object):

    """
    This class loads, stores, and saves JavaScript Level (JSL) files.
    This format is based on JSON and generally has one of the following
    extensions: ".jsl", ".json".

    A JSL file contains a top-level object with two keys:

    - ``"meta"``: an object indicating the level's meta variables.
      These can be any kind of value.
    - ``"objects"``: an object with the level's object IDs as keys. Each
      value is an array of objects in the level with the corresponding
      key, as an array with the following values:

      - The horizontal position of the object in the level.
      - The vertical position of the object in the level.
      - (Optional) An extra option for the object.  Can be any value.

    .. attribute:: meta

       A dictionary of all of the level's meta variables.

    .. attribute:: objects

       A list of objects in the level as :class:`jsl.LevelObject`
       objects.
    """

    def __init__(self):
        self.meta = {}
        self.objects = []

    @classmethod
    def load(cls, f):
        """
        Load the indicated file and return a :class:`ulvl.JSL` object.
        """
        self = cls()

        data = json.load(f)

        self.meta = data.get("meta", {})

        for t in data.setdefault("objects", {}):
            for o in data["objects"][t]:
                obj = LevelObject(t, *o)
                self.objects.append(obj)

        return self

    def save(self, f):
        """Save the object to the indicated file."""
        data = {"meta": self.meta, "objects": {}}

        for obj in self.objects:
            data["objects"].setdefault(obj.type, [])

            obj_list = [obj.x, obj.y]
            if obj.option is not None:
                obj_list.append(obj.option)

            data["objects"][obj.type].append(obj_list)

        json.dump(data, f, indent=4)


class LevelObject(object):

    """
    This class stores level objects.

    .. attribute:: type

       The type of object this is.  Can be any arbitrary value.

    .. attribute:: x

       The horizontal position of the object in the level.  The unit of
       measurement used is arbitrary; pixels or tiles is recommended.

    .. attribute:: y

       The vertical position of the object in the level.  The unit of
       measurement used is arbitrary; pixels or tiles is recommended.

    .. attribute:: option

       The option of the object; default is :const:`None`.  The meaning
       of this value is completely arbitrary; use it for any special
       variations level objects have.
    """

    def __init__(self, type_, x, y, option=None):
        self.type = type_
        self.x = x
        self.y = y
        self.option = option
