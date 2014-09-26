#!/usr/local/cpython-3.3/bin/python

'''
Provides a class that can wrap dict, treap, red_black_tree to
provide a dictionary-like-object supporting duplicate keys.
'''


class Dupdict(object):
    '''
    Class that can wrap dict, treap, red_black_tree to
    provide a dictionary-like-object supporting duplicate keys.
    '''
    def __init__(self, dict_like_object=None):
        self.num_elements = 0
        if dict_like_object is None:
            self.dict_like_object = {}
        else:
            self.dict_like_object = dict_like_object

    def __contains__(self, key):
        return key in self.dict_like_object

    def _slow_len(self):
        '''Compute the length of the dupdict in a slow but known-accurate way'''

        count = 0

        for element in self.values():
            dummy = element
            count += 1

        return count

    def __len__(self):
        return self.num_elements

    def __delitem__(self, key):
        self.num_elements -= 1
        del self.dict_like_object[key][0]

    def del_all(self, key):
        '''Delete all values under a given key'''
        self.num_elements -= len(self.dict_like_object[key])
        del self.dict_like_object[key]

    def __setitem__(self, key, value):
        self.num_elements += 1
        try:
            list_ = self.dict_like_object[key]
        except (IndexError, KeyError, ValueError):
            self.dict_like_object[key] = [value]
        else:
            list_.append(value)
        #if key in self.dict_like_object:
        #    self.dict_like_object[key].append(value)
        #else:
        #    self.dict_like_object[key] = [value]

    def __getitem__(self, key):
        return self.dict_like_object[key][0]

    def get_all(self, key):
        '''Get all values under a given key'''
        return self.dict_like_object[key]

    def __bool__(self):
        return bool(self.dict_like_object)

    __nonzero__ = __bool__

    def __iter__(self):
        for key, values in self.dict_like_object.items():
            for value in values:
                dummy = value
                yield key

    keys = __iter__
    iterator = __iter__

    def reverse_iterator(self):
        # pylint: disable=maybe-no-member
        # maybe-no-member: sometimes this is a dict, sometimes it's a tree that looks like a dict
        '''Reverse iterator'''
        if hasattr(self.dict_like_object, 'reverse_iterator'):
            for key in self.dict_like_object.reverse_iterator():
                # We repeat the key once for each value
                for value in self.dict_like_object[key]:
                    dummy = value
                    yield key
        else:
            # dict's, for example, do not have reverse_iterator.
            # We could enumerate their keys, sort in reverse order, and
            # yield that, but we don't :).
            raise NotImplementedError

    def items(self):
        '''Yield key, value pairs from the dictionary-like-object'''
        for key, values in self.dict_like_object.items():
            for value in values:
                yield (key, value)

    def all_items(self):
        '''Yield up keys with values as lists'''
        for key, values in self.dict_like_object.items():
            yield (key, values)

    def values(self):
        '''Yield each value in turn'''

        for values in self.dict_like_object.values():
            for value in values:
                yield value

    def find_min(self):
        '''
        Find the minimum key in the dict-like-object.
        If we are a treap or red-black tree, take advantage of how they do this.
        Otherwise, find the min of all keys in O(n) time.
        '''
        if hasattr(self.dict_like_object, 'find_min'):
            attr = getattr(self.dict_like_object, 'find_min')
            return attr()
        else:
            # Note that this is pretty slow
            keys = list(self.dict_like_object)
            return min(keys)

    def find_max(self):
        '''
        Find the maximum key in the dict-like-object.
        If we are a treap or red-black tree, take advantage of how they do this.
        Otherwise, find the max of all keys in O(n) time.
        '''
        if hasattr(self.dict_like_object, 'find_max'):
            attr = getattr(self.dict_like_object, 'find_max')
            return attr()
        else:
            # Note that this is pretty slow
            keys = list(self.dict_like_object)
            return max(keys)

    def remove_min(self):
        '''
        Remove the minimum key in the dict-like-object.
        If we are a treap or red-black tree, take advantage of how they do this.
        Otherwise, remove the min of all keys in O(n) time.
        '''
        if hasattr(self.dict_like_object, 'find_min'):
            attr = getattr(self.dict_like_object, 'find_min')
            min_key = attr()
        else:
            # Note that this is pretty slow
            min_key = min(self.dict_like_object)

        if len(self.dict_like_object[min_key]) > 1:
            # there is more than one of this key, so just pop one from the list
            value = self.dict_like_object[min_key].pop()
        else:
            # there's only one of this key, so delete the whole list
            value = self.dict_like_object[min_key][0]
            del self.dict_like_object[min_key]

        result = (min_key, value)

        self.num_elements -= 1

        return result

    def remove_max(self):
        '''
        Remove the maximum key in the dict-like-object.
        If we are a treap or red-black tree, take advantage of how they do this.
        Otherwise, remove the max of all keys in O(n) time.
        '''
        if hasattr(self.dict_like_object, 'find_max'):
            attr = getattr(self.dict_like_object, 'find_max')
            max_key = attr()
        else:
            # Note that this is pretty slow
            max_key = max(self.dict_like_object)

        if len(self.dict_like_object[max_key]) > 1:
            # there is more than one of this key, so just pop one from the list
            value = self.dict_like_object[max_key].pop()
        else:
            # there's only one of this key, so delete the whole list
            value = self.dict_like_object[max_key][0]
            del self.dict_like_object[max_key]

        result = (max_key, value)

        self.num_elements -= 1

        return result
