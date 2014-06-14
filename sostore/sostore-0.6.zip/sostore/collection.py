#    sostore - SQLite Object Store
#    Copyright (C) 2013, 2014 Jeffrey Armstrong 
#                            <jeffrey.armstrong@approximatrix.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import sqlite3
import warnings
import json
import collections
import random

from sostore.errors import RandomIdException, ConnectionException

# Need to check if Python 2.x because of Python 2.x's terrible
# string handling
import sys
_strtest = str
if sys.version_info[0] < 3:
    _strtest = basestring

_ID_COLUMN = '_id'
_DATA_COLUMN = '_data'

ID_KEY = _ID_COLUMN

ASCENDING  = 'ASC'
DESCENDING = 'DESC'

RANDOM_ATTEMPT_LIMIT = 1000

class Collection():
    def __init__(self, collection, connection=None, db=":memory:", randomized=False):
        """Initializes access to a collection
        
        Args:
            collection  The collection within the database to use
            
            connection  A valid sqlite3.Connection object, can be None
                        if db is specified
                        
            db          Database filename, unused if connection is
                        specified
                        
            randomized  If True, all ids in the collection will be randomly
                        generated.  If False, the ids are generated by SQLite
                        using its usual consecutive generation routine.
        """
        
        if collection is None:
            raise ValueError('A Collection name must be specified')
    
        if connection is not None:
            self._connection = connection
        else:
            self._connection = sqlite3.connect(db, isolation_level=None)
            
        self.collection = collection
        
        self.connection.execute("CREATE TABLE IF NOT EXISTS {0}({1} INTEGER PRIMARY KEY AUTOINCREMENT, {2} TEXT)".format(self.collection, _ID_COLUMN, _DATA_COLUMN))
        self.connection.commit()
        
        self.randomized = randomized
        
    @property
    def connection(self):
        if self._connection is None:
            raise ConnectionException(self.collection)
        else:
            try:
                test_cursor = self._connection.cursor()
                test_cursor.close()
            except sqlite3.ProgrammingError:
                self._connection = None
                raise ConnectionException(self.collection)
                
            return self._connection
        
    @property
    def count(self):
        """Returns the number of items in the collection"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT({0}) FROM {1}".format(_ID_COLUMN, self.collection))
        return cursor.fetchone()[0]
        
    def done(self):
        """Closes the connection to the Collection"""
        if self._connection is not None:
            self.connection.close()
        self._connection = None
        
    def get(self, id):
        """Retrieves a dictionary from the Collection
        
        Args:
            id  the id of the dictionary to retrieve
        """
        
        str = self.connection.execute("SELECT {0},{1} FROM {2} WHERE {0}=?".format(_ID_COLUMN, _DATA_COLUMN, self.collection), (id,)).fetchone()
        if str is None or len(str) != 2:
            return None

        d = json.loads(str[1])
        d[_ID_COLUMN] = id
        
        return d
        
    def get_many(self, ids, fields=None):
        """Retrieves multiple dictionaries as a list, possibly with only a subset of dictionary keys
        
        Args:
            ids     A list of database ids to retrieve
            
            fields  The keys from each dictionary to retrieve, 
                    defaults to None (all keys)
        """
        
        entries = []
        for id in ids:
            d = self.get(id)
            if fields is not None:
                removed_keys = [key for key in d.keys() if not key in fields]
                for k in removed_keys:
                    del d[k]
            entries.append(d)
            
        return entries
        
    def all(self, fields=None):
        """Retrieves all the dictionaries from the Collection
        
        Args:
            fields  The subset of keys to retrieve for each dictionary, 
                    defaults to None (all keys)
            
        """
        
        entries = []
        
        cursor = self.connection.cursor()
        for row in cursor.execute("SELECT {0},{1} FROM {2}".format(_ID_COLUMN, _DATA_COLUMN, self.collection)):
            toret = json.loads(row[1])
            toret[_ID_COLUMN] = row[0]
            if fields is not None:
                removed_keys = [key for key in toret.keys() if not key in fields]
                for k in removed_keys:
                    del toret[k]
            entries.append(toret)

        return entries    

    def _random_id(self):
        """Private random database id generator"""
        
        # The following causes our randomization to expand if
        # we're dealing with an extremely large number of 
        # entries (probably a bad idea for this db).
        topmost = max(1E+9, 10*self.count)
        
        # At this point, our random range should be at _least_ 10 times
        # larger than our current row count.  On average only one in 10
        # id's should be a duplicate, but we need to check
        attempts = 0
        while attempts < RANDOM_ATTEMPT_LIMIT:
            id = random.randint(1E+6, topmost)
            if self.get(id) is None:
                return id
            attempts += 1
            
        raise RandomIdException(self.collection)

    def insert(self, object):
        """Inserts a new dictionary into the Collection
        
        Args:
            object      A dictionary to insert into the Collection
            
        Throws:
            sostore.RandomIdException
                        This method may throw a RandomIdException in the unlikely event
                        that self.randomized is True and a unique id cannot be found in
                        a reasonable number of passes
                        
            ValueError  This method will throw a ValueError if an insert is attempted 
                        with an already-existant id
                        
        """
            
        if _ID_COLUMN in object:
            if object[_ID_COLUMN] is None:
                del object[_ID_COLUMN]
            else:
                raise ValueError("An object insert was attempted with a non-None id")
                
        str = json.dumps(object)
        cursor = self.connection.cursor()
        if not self.randomized:
            cursor.execute("INSERT INTO {0}({1}) VALUES(?)".format(self.collection, _DATA_COLUMN), (str,))
        else:
            id = self._random_id()
            cursor.execute("INSERT INTO {0}({1}, {2}) VALUES(?, ?)".format(self.collection, _ID_COLUMN, _DATA_COLUMN), (id, str,))
        self.connection.commit()
        
        object[_ID_COLUMN] = cursor.lastrowid
        return object
        
    def update(self, object):
        """Updates an existing dictionary in the Collection
        
        Args:
            object  A dictionary with a valid "_id" key, which will entirely
                    replace the existing dictionary associated with the id
                    
        Raises:
            ValueError  This method will throw a ValueError if an update is 
                        attempted and the dictionary does not include an 
                        already-existant id
        """
        
        if not _ID_COLUMN in object.keys():
            raise ValueError('Update called on a nonexistant db record')

        id = object[_ID_COLUMN]
        del object[_ID_COLUMN]
        
        str = json.dumps(object)
        
        self.connection.execute("UPDATE {0} SET {1}=? WHERE {2}=?".format(self.collection, _DATA_COLUMN, _ID_COLUMN), (str, id))
        self.connection.commit()
        
        object[_ID_COLUMN] = id
        
        return object
        
    def remove(self, object_or_id):
        """Removes a dictionary from the Collection
        
        Args:
            object_or_id    Either an object with a valid "_id" key 
                            or the object's id itself
        """
        
        deletion = object_or_id
        if isinstance(deletion, dict):
            deletion = object_or_id[_ID_COLUMN]

        self.connection.execute("DELETE FROM {0} WHERE {1}=?".format(self.collection, _ID_COLUMN), (deletion,))
        self.connection.commit()
        
    def find_one(self, field, value):
        """Finds a single dictionary in the Collection that has a matching value for a specified key (field).
        
        Args:
            field   The dictionary key being specified in the value
                    argument
                    
            value   The value to search for in the specified dictionary 
                    key
                    
        Notes:
            See Collection.find_field for more information on behavior
        """
        
        id = self.find(field, value)
        
        if len(id) == 0:
            return None
        else:
            return self.get(id[0])
    
    def random_entries(self, count=1):
        """Retrieve random dictionaries from the Collection
        
        Args:
            count   The number of random dictionaries to retrieve, defaults to 1
        """
        
        entries = []
        cursor = self.connection.cursor()
        for row in cursor.execute("SELECT * FROM {0} ORDER BY RANDOM() LIMIT {1};".format(self.collection, count)):
            toret = json.loads(row[1])
            toret[_ID_COLUMN] = row[0]
            entries.append(toret)

        return entries    
    
    def random_entry(self):
        """Retrieve a single random dictionary from the Collection"""
        
        entries = self.random_entries(1)
        if len(entries) == 1:
            return entries[0]
        
        return None
    
    def find_field(self, *args,**kwargs):
        """DEPRECATED - For compatibility with sostore < 0.4 only
        Please use Collection.find instead.  This method just calls
        it directly"""
        return self.find(*args, **kwargs)
    
    def find(self, field, value, compare_function=None):
        """Finds id's of dictionaries in the Collection that have a matching value for a specified key (field).
        
        Args:
            field   The dictionary key being specified in the value
                    argument
                    
            value   The value to search for in the specified dictionary 
                    key
                    
            compare_function    A function that accepts two values and returns
                                True if equal, False otherwise.  Defaults to
                                None to use ==
                    
        Notes:
            If the value of the field in the dictionary is a list, the routine
            will search each element of the list for a matching value.  If the
            value is specified as a string and the value in the dictionary is
            an integer, a conversion will be attempted during matching.
        """
        
        fieldsearch = self.all(fields=(_ID_COLUMN, field))
        matching = []
        for d in fieldsearch:
            
            if not field in d.keys():
                continue
                
            matched = False
            if isinstance(d[field], collections.Iterable) and not isinstance(d[field], _strtest):
                if compare_function is not None:
                    for stored_value in d[field]:                    
                        matched = matched or compare_function(value, stored_value)
                else:
                    matched = value in d[field]
                                        
            elif compare_function is not None:
                matched = compare_function(value, d[field])
            
            else:
                matched = (value == d[field])
                
            if matched:
                matching.append(d[ID_KEY])
                
        return matching
