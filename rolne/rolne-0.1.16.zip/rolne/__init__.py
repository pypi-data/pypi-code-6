# rolne\__init__.py
#
# rolne datatype class: Recursive Ordered List of Named Elements
#
# Version 0.1.16
    
import copy

TNAME = 0
TVALUE = 1
TLIST = 2
TSEQ = 3
NS = 101

'''
Internal Notes:

    self.data is the actual place where the rolne data is stored.
    It is a list of tuples, where each tuple is:
    
          (name, value, list, seq)
          
    where:
    
        name is a string; part of the name/value pair being stored
        value is a string; part of the name/value pair being stored
        list is any subtending data under the name/value pair. Essentially
            is is another list of tuples.
        seq is a tracking string for historic and diagnostic data

    There are 4 globals in the doc: TNAME, TVALUE, TLIST, TSEQ to make the
    numeric index of each of these tuple elements easier to read.
        
'''

class rolne(object):

    def __init__(self, in_list=None, in_tuple=None, ancestor=None):
        self.ref_name = None
        self.ref_value = None
        self.ref_seq = None
        if in_list is None:
            if in_tuple is None:
                self.data = []
            else:
                (self.ref_name, self.ref_value, self.data, self.ref_seq) = in_tuple
        else:
            self.data = in_list
        if ancestor is None:
            self.ancestor = self.data
        else:
            self.ancestor = ancestor

    def __str__(self, detail=False):
        result = ""
        if detail:
            result += "<rolne datatype object:\n"
        else:
            result += "%rolne:\n"
        result += self.mards(detail=detail)
        if detail:
            result += ">"
        return result

    def _explicit(self):
        return self.__str__(detail=True)


    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, tup):
        if isinstance(tup, slice):
            ###################
            # handle a 'slice'
            ###################
            (start_name, start_value, start_index) = (None, None, 0)
            startlen = 0
            if tup.start:
                if not isinstance(tup.start, tuple):
                    tup_start = (tup.start,)
                else:
                    tup_start = tup.start
                startlen = len(tup_start)
                if startlen>0:
                    start_name = tup_start[0]
                if startlen>1:
                    start_value = tup_start[1]
                if startlen>2:
                    start_index = tup_start[2]
            (stop_name, stop_value, stop_index) = (None, None, 0)
            stoplen = 0
            if tup.stop:
                if not isinstance(tup.stop, tuple):
                    tup_stop = (tup.stop,)
                else:
                    tup_stop = tup.stop
                stoplen = len(tup_stop)
                if stoplen>0:
                    stop_name = tup_stop[0]
                if stoplen>1:
                    stop_value = tup_stop[1]
                if stoplen>2:
                    stop_index = tup_stop[2]
            if tup.step:
                if tup.step<1:
                    raise KeyError, "Step cannot be less than 1"
                step = int(tup.step)
            else:
                step = 1
            #
            if tup.start:
                start_flag = False
            else:
                start_flag = True
            start_ctr = 0
            stop_ctr = 0
            step_ctr = 0
            new_list = []
            for entry in self.data:
                if start_flag:
                    if stoplen==1 and stop_name==entry[TNAME]:
                        break
                    if stoplen==2 and stop_name==entry[TNAME] and stop_value==entry[TVALUE]:
                        break
                    if stoplen==3 and stop_name==entry[TNAME] and stop_value==entry[TVALUE] and stop_index==stop_ctr:
                        break
                    if (step_ctr % step)==0:
                        new_list.append(entry)
                    step_ctr += 1
                else:
                    if startlen==1 and start_name==entry[TNAME]:
                        start_flag = True
                        new_list.append(entry)
                        step_ctr += 1
                    if startlen==2 and start_name==entry[TNAME] and start_value==entry[TVALUE]:
                        start_flag = True
                        new_list.append(entry)
                        step_ctr += 1
                    if startlen==3 and start_name==entry[TNAME] and start_value==entry[TVALUE] and start_index==start_ctr:
                        start_flag = True
                        new_list.append(entry)
                        step_ctr += 1
                # do the counters seperately
                if startlen==3 and start_name==entry[TNAME] and start_value==entry[TVALUE]:
                    start_ctr += 1
                if stoplen==3 and stop_name==entry[TNAME] and stop_value==entry[TVALUE]:
                    stop_ctr += 1
            else:
                if start_flag:
                    if tup.stop:
                        raise KeyError, repr(tup.stop)+" not found"
                else:
                    raise KeyError, repr(tup.start)+" not found"
            return rolne(in_tuple = (self.ref_name, self.ref_value, new_list, self.ref_seq), ancestor=self.ancestor)
        else:
            ###################
            # handle a tuple (non-slice)
            ###################
            if not isinstance(tup, tuple):
                tup = (tup,)
            arglen = len(tup)
            (name, value, index) = (None, None, 0)
            if arglen>0:
                name = tup[0]
            if arglen>1:
                value = tup[1]
            if arglen>2:
                index = tup[2]
            start_ctr = 0
            if index<0:
                search_data = reversed(list(enumerate(self.data)))
                index = -index - 1
            else:
                search_data = enumerate(self.data)
            for i, entry in search_data:
                if entry[TNAME]==name:
                    if arglen==1 or entry[TVALUE]==value:
                        if start_ctr==index:
                            return rolne(in_tuple = self.data[i], ancestor=self.ancestor)
                        else:
                            start_ctr += 1
        raise KeyError, repr(tup)+" not found"
        return None

    def __setitem__(self, tup, value):
        if not isinstance(tup, tuple):
            tup = tuple([tup])
        arglen = len(tup)
        (name, cur_value, index) = (None, None, 0)
        index_flag = False
        if arglen==1:
            name = tup[TNAME]
        elif arglen==2:
            name = tup[TNAME]
            cur_value = tup[TVALUE]
        elif arglen==3:
            name = tup[TNAME]
            cur_value = tup[TVALUE]
            index = tup[2]
        elif arglen==0:
            raise KeyError, repr(tup)+" is empty"
        else:
            raise KeyError, repr(tup)+" has too many items"
        start_ctr = 0
        for i,(entry_name, entry_value, entry_list, entry_seq) in enumerate(self.data):
            if entry_name==name:
                if entry_value==cur_value or arglen==1:
                    if start_ctr==index:
                        new_tuple = (entry_name, value, entry_list, entry_seq)
                        self.data[i] = new_tuple
                        return True
                    else:
                        start_ctr += 1
        if arglen==3:
            raise KeyError, repr(tup)+" not found"
        else:
            self.append(name, value)
        return True

    def __delitem__(self, tup):
        if not isinstance(tup, tuple):
            tup = tuple([tup])
        arglen = len(tup)
        (name, value, index) = (None, None, 0)
        index_flag = False
        if arglen==1:
            name = tup[TNAME]
        elif arglen==2:
            name = tup[TNAME]
            value = tup[TVALUE]
        elif arglen==3:
            name = tup[TNAME]
            value = tup[TVALUE]
            index = tup[2]
        elif arglen==0:
            raise KeyError, repr(tup)+" is empty"
        else:
            raise KeyError, repr(tup)+" has too many items"
        start_ctr = 0
        for i,(entry_name, entry_value, entry_list, entry_seq) in enumerate(self.data):
            if entry_name==name:
                if entry_value==value or arglen==1:
                    if start_ctr==index:
                        del self.data[i]
                        return
                    else:
                        start_ctr += 1
        raise KeyError, repr(tup)+" not found"


    def __contains__(self, target):
        target_value_missing = True
        target_name = target
        target_index = 0
        if isinstance(target, tuple):
            if len(target)>0:
                target_name = target[0]
            if len(target)>1:
                target_value = target[1]
                target_value_missing = False
            if len(target)>2:
                target_index = target[2]
        ctr = 0
        for i,(entry_name, entry_value, entry_list) in enumerate(self.data):
                if (entry_name==target_name):
                    if target_value_missing:
                        return True
                    else:
                        if entry_value==target_value:
                            if ctr==target_index:
                                return True
                            else:
                                ctr += 1
        return False

    def __iter__(self):
        for entry in self.data:
            x = rolne(in_tuple = entry, ancestor=self.ancestor)
            #x = rolne([entry])
            yield x

    def _seq(self, seq=None):
        global NS
        if seq:
            result = str(seq)
        else:
            result = str(NS)
            NS += 1
        return result

    def find(self, *argv):
        """Locate a single rolne entry.

        This function is very similar to simply doing a dictionary-style
        lookup. For example:

            new_rolne = my_var.find("test", "zoom", 4)

        is effectively the same as:

            new_rolne = my_var["test", "zoom", 4]

        The biggest difference is that if entry at ["test", "zoom", 4] does
        not exist, the dictionary-style lookup generates a key error. Whereas
        this method simply returns None.

        Example of use:

        >>> # setup an example rolne first
        >>> my_var = rolne()
        >>> my_var.append("item", "zing")
        >>> my_var["item", "zing"].append("size", "4")
        >>> my_var["item", "zing"].append("color", "red")
        >>> my_var["item", "zing"]["color", "red"].append("intensity", "44%")
        >>> my_var["item", "zing"].append("reverse", None)
        >>> my_var.append("item", "broom")
        >>> my_var["item", "broom", -1].append("size", "1")
        >>> my_var["item", "broom", -1].append("title", 'The "big" thing')
        >>> my_var.append("item", "broom")
        >>> my_var["item", "broom", -1].append("size", "2")
        >>> my_var["item", "broom", -1].append("title", 'Other thing')
        >>> my_var.append("code_seq")
        >>> my_var["code_seq", None].append("*", "r9")
        >>> my_var["code_seq", None].append("*", "r3")
        >>> my_var["code_seq", None].append("*", "r2")
        >>> my_var["code_seq", None].append("*", "r3")
        >>> my_var.append("system_title", "hello")
        >>> #
        >>> print my_var.find("item","broom",1)
        %rolne:
        size 2
        title Other thing
        <BLANKLINE>
        >>> print my_var.find("item","broom",2)
        None
        >>> print my_var["code_seq", None].find("*","r3")
        %rolne:
        %empty
        <BLANKLINE>

        .. versionadded:: 0.1.2
        
        :param name:
           The key name of the name/value pair.
        :param value:
           The key value of the name/value pair. If not passed, then the value
           is assumed to be empty (None).
        :param index:
           The index of the name/value pair. if not passed, then the index is
           assumed to be 0.
        :returns:
           Returns either a rolne that points to the located entry or None if
           that entry is not found.
        """
        try:
            return self.__getitem__(argv)
        except KeyError:
            return None
        return None

    def mards(self, detail=False):
        result = ""
        # return repr(self.data)
        if self.data:
            for entry in self.data:
                if detail==True:
                    result += "[{}] ".format(str(entry[TSEQ]))
                result += str(entry[TNAME])
                if entry[TVALUE] is not None:
                    printable = str(entry[TVALUE])
                    quote_flag = False
                    if '"' in printable:
                        quote_flag = True
                    if len(printable) != len(printable.strip()):
                        quote_flag = True
                    if quote_flag:
                        result += " "+'"'+str(entry[TVALUE])+'"'
                    else:
                        result += " "+str(entry[TVALUE])
                result += "\n"
                if entry[TLIST]:
                    temp = rolne(in_tuple = entry, ancestor=self.ancestor).mards(detail=detail)
                    for line in temp.split("\n"):
                        if line:
                            result += "    "+line
                            result += "\n"
        else:
            result = "%empty\n"
        return result

    def append(self, name, value=None, sublist=None, seq=None):
        """Add one name/value entry to the main context of the rolne.

        Example of use:

        >>> # setup an example rolne first
        >>> my_var = rolne()
        >>> my_var.append("item", "zing")
        >>> my_var["item", "zing", -1].append("size", "4")
        >>> my_var["item", "zing", -1].append("color", "red")
        >>> print my_var
        %rolne:
        item zing
            size 4
            color red
        <BLANKLINE>
        >>> my_var.append("item", "zing")
        >>> my_var["item", "zing", -1].append("size", "2")
        >>> my_var["item", "zing", -1].append("color", "blue")
        >>> print my_var
        %rolne:
        item zing
            size 4
            color red
        item zing
            size 2
            color blue
        <BLANKLINE>

        .. versionadded:: 0.1.1
        
        :param name:
           The key name of the name/value pair.
        :param value:
           The key value of the name/value pair. If not passed, then the value
           is assumed to be None.
        :param sublist:
           An optional parameter that also appends a subtending list of entries.
           It is not recommended that this parameter be used.
        """
        if sublist is None:
            sublist = []
        new_tuple = (name, value, sublist, self._seq(seq))
        self.data.append(new_tuple)

    def append_index(self, name, value=None, sublist=None, seq=None):
        """Add one name/value entry to the main context of the rolne and
        return the index number for the new entry.

        Example of use:

        >>> # setup an example rolne first
        >>> my_var = rolne()
        >>> index = my_var.append_index("item", "zing")
        >>> print index
        0
        >>> my_var["item", "zing", index].append("size", "4")
        >>> my_var["item", "zing", index].append("color", "red")
        >>> print my_var
        %rolne:
        item zing
            size 4
            color red
        <BLANKLINE>
        >>> index = my_var.append_index("item", "zing")
        >>> print index
        1
        >>> my_var["item", "zing", index].append("size", "2")
        >>> my_var["item", "zing", index].append("color", "blue")
        >>> print my_var
        %rolne:
        item zing
            size 4
            color red
        item zing
            size 2
            color blue
        <BLANKLINE>

        .. versionadded:: 0.1.4
        
        :param name:
           The key name of the name/value pair.
        :param value:
           The key value of the name/value pair. If not passed, then the value
           is assumed to be None.
        :param sublist:
           An optional parameter that also appends a subtending list of entries.
           It is not recommended that this parameter be used.
        :returns:
           An integer representing the index of the newly inserted name/pair.
        """
        if sublist is None:
            sublist = []
        new_tuple = (name, value, sublist, self._seq(seq))
        self.data.append(new_tuple)
        index = len(self.list_values(name, value)) - 1
        return index

    def upsert(self, name, value=None, seq=None):
        """Add one name/value entry to the main context of the rolne, but
        only if an entry with that name does not already exist.

        If the an entry with name exists, then the first entry found has it's
        value changed.

        NOTE: the upsert only updates the FIRST entry with the name found.

        The method returns True if an insertion occurs, otherwise False.

        Example of use:

        >>> # setup an example rolne first
        >>> my_var = rolne()
        >>> my_var.upsert("item", "zing")
        True
        >>> my_var["item", "zing"].append("color", "blue")
        >>> print my_var
        %rolne:
        item zing
            color blue
        <BLANKLINE>
        >>> my_var.upsert("item", "zing")
        False
        >>> print my_var
        %rolne:
        item zing
            color blue
        <BLANKLINE>
        >>> my_var.upsert("item", "broom")
        False
        >>> print my_var
        %rolne:
        item broom
            color blue
        <BLANKLINE>

        .. versionadded:: 0.1.1
        
        :param name:
           The key name of the name/value pair.
        :param value:
           The key value of the name/value pair. If not passed, then the value
           is assumed to be None.
        :returns:
           Returns True if the name/value was newly inserted. Otherwise, it
           returns False indicated that an update was done instead.
        """
        for ctr, entry in enumerate(self.data):
            if entry[TNAME]==name:
                new_tuple = (name, value, entry[TLIST], entry[TSEQ])
                self.data[ctr]=new_tuple
                return False
        new_tuple = (name, value, [], self._seq(seq))
        self.data.append(new_tuple)
        return True

    def extend(self, new_rolne, prefix=""):
        for child in new_rolne:
            new_list = []
            new_list = self._extend(child.rlist(), prefix)
            tup = (child.name(), child.value(), new_list, prefix+self._seq())
            self.data.append(tup)
        return

    def _extend(self, sublist, prefix):
        new_list = []
        for entry in sublist:
            (en, ev, el, es) = entry
            sub_list = self._extend(el, prefix)
            tup = (en, ev, sub_list, prefix+self._seq())
            new_list.append(tup)
        return new_list
        
        
    def get_tuples(self, *args):
        arg_count = len(args)
        result = []
        ctr = 0
        for entry in self.data:
            if arg_count==0:
                result.append((entry[TNAME], entry[TVALUE]))
            if arg_count==1:
                if entry[TNAME]==args[0]:
                    result.append((entry[TNAME], entry[TVALUE]))
            if arg_count==2:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    result.append((entry[TNAME], entry[TVALUE]))
            if arg_count==3:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    if ctr==args[2]:
                        result.append((entry[TNAME], entry[TVALUE]))
                    ctr += 1
        return result

    def keys(self, *args):
        return self.dump_list(args, name=True, value=True, index=True)

    def dump_list(self, args, name=False, value=True, index=False, seq=False):
        if not isinstance(args, tuple):
            args = tuple([args])
        arg_count = len(args)
        result = []
        ctr = {}
        for entry in self.data:
            # the counter function
            if (entry[TNAME], entry[TVALUE]) in ctr:
                ctr[(entry[TNAME], entry[TVALUE])] += 1
            else:
                ctr[(entry[TNAME], entry[TVALUE])] = 0
            # make the tuple
            items = []
            if name:
                items.append(entry[TNAME])
            if value:
                items.append(entry[TVALUE])
            if index:
                items.append(ctr[(entry[TNAME], entry[TVALUE])])
            if seq:
                items.append(entry[TSEQ])
            tup = tuple(items)
            # insert as dictated by args given
            if arg_count==0:
                result.append(tup)
            if arg_count==1:
                if entry[TNAME]==args[0]:
                    result.append(tup)
            if arg_count==2:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    result.append(tup)
            if arg_count==3:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    if ctr[(entry[TNAME], entry[TVALUE])]==args[2]:
                        result.append(tup)
        return result

        
    def flattened_list(self, args, name=False, value=True, index=False, seq=False):
        if not isinstance(args, tuple):
            args = tuple([args])
        return self._flattened_list(self.data, args, name=name, value=value, index=index, seq=seq)

    def _flattened_list(self, data, args, name, value, index, seq):
        arg_count = len(args)
        result = []
        ctr = {}
        for entry in data:
            # the counter function
            if (entry[TNAME], entry[TVALUE]) in ctr:
                ctr[(entry[TNAME], entry[TVALUE])] += 1
            else:
                ctr[(entry[TNAME], entry[TVALUE])] = 0
            # make the tuple
            items = []
            if name:
                items.append(entry[TNAME])
            if value:
                items.append(entry[TVALUE])
            if index:
                items.append(ctr[(entry[TNAME], entry[TVALUE])])
            if seq:
                items.append(entry[TSEQ])
            tup = tuple(items)
            # insert as dictated by args given
            if arg_count==0:
                result.append(tup)
            if arg_count==1:
                if entry[TNAME]==args[0]:
                    result.append(tup)
            if arg_count==2:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    result.append(tup)
            if arg_count==3:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    if ctr[(entry[TNAME], entry[TVALUE])]==args[2]:
                        result.append(tup)
            if entry[TLIST]:
                result.extend(self._flattened_list( entry[TLIST], args, name, value, index, seq) )
        return result
        
    def dump(self):
        return self._dump(self.data)

    def _dump(self, data):
        result = []
        for entry in data:
            tup = (entry[TNAME], entry[TVALUE], self._dump(entry[TLIST]))
            result.append(tup)
        return result

    #
    #
    #   GET name/value/list/seq SECTION
    #
    #
        
    # if called as x.name(), it returns it's own name
    # if called as x.name(name), it returns the name of the first name entry
    #    IF found (otherwise None)
    def name(self, *args):
        (name, _, _, _) = self._ref_tuple(*args)
        return name
    
    # if called as x.value(), it returns it's own value
    # if called as x.value(name), it returns the value of the first name entry
    #    found (otherwise None)
    def value(self, *args):
        (_, value, _, _) = self._ref_tuple(*args)
        return value

    # TODO: not sure if this should be allowed
    def rlist(self, *args):
        (_, _, rlist, _) = self._ref_tuple(*args)
        return rlist

    # if called as x.seq(), it returns it's own sequence id
    # if called as x.seq(name, value, index), it returns the value of the first name entry
    #    found (otherwise None)
    #def seq(self, name, value, index=None):
    def seq(self, *args):
        (_, _, _, seq) = self._ref_tuple(*args)
        return seq


    # an internal routine to get self or an element based on flexible args
    def _ref_tuple(self, *args):
        arglen = len(args)
        (name, value, index) = (None, None, 0)
        if arglen>0:
            name = args[0]
        if arglen>1:
            value = args[1]
        if arglen>2:
            index = args[2]
        ctr = 0
        if arglen==0:
            return (self.ref_name, self.ref_value, self.data, self.ref_seq)
        else:
            for entry in self.data:
                (en, ev, el, es) = entry
                if en==name:
                    if arglen==1 or ev==value:
                        if ctr==index:
                            return entry
                        ctr += 1
        return (None, None, None, None)


    #
    #
    # SET name/value/list/seq SECTION
    #
    #
    def set_name(self, new_parm, *args):
        index = self._ref_index(*args)
        if index is None:
            return False
        if index==-1:
            # set the name of the SELF
            # which, to make globally true, requires access
            # to ancestry
            if self.ref_seq is None:
                # you can't change the name of SELF at the very
                # top of the tree. (doing so breaks a lot of stuff)
                return False
            else:
                rtemp = self._point_ancestry()
                (list_ptr, index) = rtemp.list_ref_to_seq(self.ref_seq)
                if index is None:
                    return False
                else:
                    (en, ev, el, es) = list_ptr[index]
                    list_ptr[index] = (new_parm, ev, el, es)
                self.ref_name = new_parm
                return True
        # set the name of a child
        (en, ev, el, es) = self.data[index]
        self.data[index] = (new_parm, ev, el, es)
        return True

    def set_value(self, new_parm, *args):
        index = self._ref_index(*args)
        if index is None:
            return False
        if index==-1:
            # set the name of the SELF
            # which, to make globally true, requires access
            # to ancestry
            if self.ref_seq is None:
                # you can't change the name of SELF at the very
                # top of the tree. (doing so breaks a lot of stuff)
                return False
            else:
                rtemp = self._point_ancestry()
                (list_ptr, index) = rtemp.list_ref_to_seq(self.ref_seq)
                if index is None:
                    return False
                else:
                    (en, ev, el, es) = list_ptr[index]
                    list_ptr[index] = (en, new_parm, el, es)
                self.ref_name = new_parm
                return True
        # set the name of a child
        (en, ev, el, es) = self.data[index]
        self.data[index] = (en, new_parm, el, es)
        return True
    
    # FOR NOW, we are not going to permit the 'setting' of an internal tuple-list
    #def set_rlist(self, *args):
    #    return False

    def set_seq(self, new_parm, *args):
        index = self._ref_index(*args)
        if index is None:
            return False
        if index==-1:
            # set the name of the SELF
            # which, to make globally true, requires access
            # to ancestry
            if self.ref_seq is None:
                # you can't change the name of SELF at the very
                # top of the tree. (doing so breaks a lot of stuff)
                return False
            else:
                rtemp = self._point_ancestry()
                (list_ptr, index) = rtemp.list_ref_to_seq(self.ref_seq)
                if index is None:
                    return False
                else:
                    (en, ev, el, es) = list_ptr[index]
                    list_ptr[index] = (en, ev, el, new_parm)
                self.ref_name = new_parm
                return True
        # set the name of a child
        (en, ev, el, es) = self.data[index]
        self.data[index] = (en, ev, el, new_parm)
        return True

    # an internal routine to get data index based on flexible args
    #   -1 = self
    #   None = not found
    #   else returns index number
    def _ref_index(self, *args):
        arglen = len(args)
        (name, value, index) = (None, None, 0)
        if arglen>0:
            name = args[0]
        if arglen>1:
            value = args[1]
        if arglen>2:
            index = args[2]
        ctr = 0
        if arglen==0:
            return -1
        else:
            for i, entry in enumerate(self.data):
                (en, ev, el, es) = entry
                if en==name:
                    if arglen==1 or ev==value:
                        if ctr==index:
                            return i
                        ctr += 1
        return None

    # this routine creates a 'temporary' rolne that points to the
    # 'top-level' rolne list.
    # Any changes to self.ref_seq, ref_name, or ref_value are bogus
    # and are lost when the rolne is garbage collected. But changes
    # to children in TLIST survive.
    def _point_ancestry(self):
        return rolne(in_tuple=(None, None, self.ancestor, None))


    #
    #
    #   LIST name/value/list/seq SECTION
    #
    #

    def get_list(self, *args):
        raise NameError("Command 'get_list' deprecated. Use 'list_values'.")

    def list_values(self, *args):
        arg_count = len(args)
        result = []
        ctr = 0
        for entry in self.data:
            if arg_count==0:
                result.append(entry[TVALUE])
            if arg_count==1:
                if entry[TNAME]==args[0]:
                    result.append(entry[TVALUE])
            if arg_count==2:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    result.append(entry[TVALUE])
            if arg_count==3:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    if ctr==args[2]:
                        result.append(entry[TVALUE])
                    ctr += 1
        return result

    def get_names(self, *args):
        raise NameError("Command 'get_names' deprecated. Use 'list_names'.")
    
    def list_names(self, *args):
        arg_count = len(args)
        result = []
        ctr = 0
        for entry in self.data:
            if arg_count==0:
                result.append(entry[TNAME])
            if arg_count==1:
                if entry[TNAME]==args[0]:
                    result.append(entry[TNAME])
            if arg_count==2:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    result.append(entry[TNAME])
            if arg_count==3:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    if ctr==args[2]:
                        result.append(entry[TNAME])
                    ctr += 1
        return result

    def list_seq(self, *args):
        arg_count = len(args)
        result = []
        ctr = 0
        for entry in self.data:
            if arg_count==0:
                result.append(entry[TSEQ])
            if arg_count==1:
                if entry[TNAME]==args[0]:
                    result.append(entry[TSEQ])
            if arg_count==2:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    result.append(entry[TSEQ])
            if arg_count==3:
                if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                    if ctr==args[2]:
                        result.append(entry[TSEQ])
                    ctr += 1
        return result


    #
    #
    #   SEQUENCE ANCESTRY SUPPORT
    #
    #


    # TODO: remove this function
    def summarize(self, name, *args):
        # we are using *args for 'value' because None is a valid value parameter that
        # must be distinquished from a _missing_ parameter.
        if args:
            value = args[0]
            value_missing = False
        else:
            value = None
            value_missing = True
        value_list = []
        summary = []
        for (en, ev, el, es) in self.data:
            if en==name:
                if value_missing or ev==value:
                    value_list.append(ev)
                    summary.append((en, ev, el, es))
        return (name, value_list, rolne(in_list = summary))

    # TODO: remove this function
    def filter(self, *argv):
        return self.summarize(*argv)[2]

    def at_seq(self, seq=None):
        # return the rolne located with the seq
        tup = self.ptr_to_seq(seq)
        if tup is None:
            return None
        return rolne(in_tuple=tup, ancestor=self.ancestor)
        
    def ptr_to_seq(self, seq):
        # this is an interesting one: return a reference to
        # the direct tuple with this sequence. Use with care.
        (target_list, target_index) = self.list_ref_to_seq(seq)
        if target_list is None:
            return None
        return target_list[target_index]

    def list_ref_to_seq(self, seq):
        # this one REALLY jumps down the rabbit hole.
        #
        # returns a tuple containing the original list containing the
        # sequence and the index pointing to the entry that
        # has the sequence.
        #
        # (list, index)
        #
        # this is useful for for routines that, in turn, modify
        # an entry. One cannot "change" a tuple. So a pointer
        # to a tuple has no value. This combo allows true change
        # because lists are mutable.
        #
        return self._list_ref_to_seq(self.data, seq)

    def _list_ref_to_seq(self, data, seq):
        result = (None, None)
        for index, entry in enumerate(data):
            (en, ev, el, es) = entry
            if es==seq:
               return (data, index)
            if el:
                result = self._list_ref_to_seq(el, seq)
                if result[0] is not None:
                    return result
        return (None, None)

    def seq_replace(self, seq, src, prefix="rep"):
        # locating the entry with 'seq', replace the contents
        # of seq with a COPY of the entry seen at src.
        # If src is a string, the it is a sequence id of the data
        #  in the same rolne.
        # if src is a tuple, then it is a tuple of the new actual data.
        # the original entry retains it's seq string, but the
        # name, value, and subtending list all change.
        # the subtending entries get new seq ids
        # returns True is successful, else False
        dest_ref = self.list_ref_to_seq(seq)
        if dest_ref[0] is None:
            return False
        (dest_list, dest_index) = dest_ref
        ro_dest_tup = dest_list[dest_index]
        if type(src) is tuple:
            src_tup = src
        else:
            src_tup = self.ptr_to_seq(src)
        if src_tup is None:
            return False
        new_sub_list = self._copy_sublist_with_new_seq(src_tup[TLIST], prefix)
        new_tup = (copy.deepcopy(src_tup[TNAME]), copy.deepcopy(src_tup[TVALUE]), new_sub_list, ro_dest_tup[TSEQ])
        dest_list[dest_index] = new_tup
        return True

    def _copy_sublist_with_new_seq(self, source, prefix):
        dest = []
        for (ev, en, el, es) in source:
            new_seq = prefix+self._seq() # called before next to make seq look logical
            new_list = self._copy_sublist_with_new_seq(el, prefix)
            new_tup = (copy.copy(ev), copy.copy(en), new_list, new_seq)
            dest.append(new_tup)
        return dest

    def seq_lineage(self, seq):
        # return a parental list of seq that are represented by a seq
        # TODO add a param to return keys rather than seq
        return self._seq_lineage(self.data, seq)

    def _seq_lineage(self, data, seq):
        for index, entry in enumerate(data):
            (en, ev, el, es) = entry
            if es==seq:
               return [es]
            if el:
                result = self._seq_lineage(el, seq)
                if result:
                    return [es]+result
        return []
        
    def seq_parent(self, seq):
        # seq of immediate parent
        the_line = self.seq_lineage(seq)
        if len(the_line)>1:
            return the_line[-2]
        return None

    def seq_progenitor(self, seq):
        # seq of top ancestor
        the_line = self.seq_lineage(seq)
        if the_line:
            return the_line[0]
        return None

    def seq_delete(self, seq):
        # delete the entry pointed to by the sequence
        ref = self.list_ref_to_seq(seq)
        if ref[0] is None:
            return None
        (rl, ri) = ref
        del rl[ri]
        return seq

    def copy(self, seq_prefix="copy_", seq_suffix=""):
        seq_prefix = str(seq_prefix)
        seq_suffix = str(seq_suffix)
        return rolne(in_tuple=(None, None, self._copy(seq_prefix, seq_suffix, self.data), None))

    def _copy(self, seq_prefix, seq_suffix, data):
        new_list = []
        for (ev, en, el, es) in data:
            sub = self._copy(seq_prefix, seq_suffix, el)
            new_list.append((copy.copy(ev), copy.copy(en), sub, seq_prefix+es+seq_suffix))
        return new_list
        
if __name__ == "__main__":

    if True:

        my_var = rolne()
        my_var.append("item", "zing")
        my_var["item", "zing"].upsert("size", "4")
        my_var["item", "zing"].upsert("color", "red")
        my_var["item", "zing"]["color", "red"].upsert("intensity", "44%")
        my_var["item", "zing"].upsert("color", "yellow")
        my_var.append("item", "womp")
        my_var["item", "womp"].upsert("size", "5")
        my_var["item", "womp"].upsert("color", "blue")
        my_var.append("item", "bam")
        my_var.append("item", "broom")
        my_var["item", "broom", -1].upsert("size", "1")
        my_var["item", "broom", -1].upsert("title", 'The "big" thing')
        my_var.append("item", "broom")
        my_var["item", "broom", -1].upsert("size", "2")
        my_var["item", "broom", -1].upsert("title", 'The "big" thing')
        my_var.append("item", "broom")
        my_var["item", "broom", -1].upsert("size", "3")
        my_var["item", "broom", -1].upsert("title", 'The "big" thing')
        my_var.upsert("zoom_flag")
        my_var.upsert("code_seq", seq="ln1")
        my_var["code_seq", None].append("*", "r9", seq="ln2")
        my_var["code_seq", None].append("*", "r3")
        my_var["code_seq", None].append("*", "r2")
        my_var["code_seq", None].append("*", "r3")
        my_var.upsert("system_title", "hello")

        x_var = rolne()
        x_var.append("item", "zingo")
        x_var["item", "zingo"].upsert("size", "4b")
        x_var["item", "zingo"].upsert("color", "redb")
        x_var["item", "zingo"]["color", "redb"].upsert("intensity", "44%b")
        x_var["item", "zingo"].upsert("color", "yellowb")


        print "a", my_var._explicit()
        print "a2", x_var._explicit()
        #print "aa", my_var["zoom_flag"]
        #c_var = my_var.copy()
        #print "b", my_var["code_seq"]
        #print "bb", my_var.find("code_seq")
        #print "c1", my_var.dump_list( ( ), name=True, value=True, index=True, seq=True)
        #print "cz", my_var.flattened_list( ("title"), name=True, value=True, index=True, seq=True)
        #print "c2", my_var.get( ("item"), name=True, value=True, index=True, seq=True)
        #print "c3", my_var.get( ("item", "broom"), name=True, value=True, index=True, seq=True)
        #print "c4", my_var.get( ("item", "broom", 2), name=True, value=True, index=True, seq=True)
        #print "c5", my_var.get( ("item", "broom", 9), name=True, value=True, index=True, seq=True)
        #print "c6", my_var.keys("item", "broom")
        #my_var["code_seq"]["*", None] = 'zings'
        #print "d", my_var._explicit()
        #print "e", my_var["item", "zing"].value("size")
        #print "f", my_var
        #print "g", my_var["item", "broom", -1]
        #seq = "120"
        #new_var = my_var.at_seq("ln1")
        #if new_var is not None:
        #    print "h2", new_var._explicit()
        #    print "h2b", new_var.name()
        #    print "h2c", new_var.value()
        #    print "h2d", new_var.value("*")
        #    print "h2e", new_var.list_names()
        #    print "h2f1", new_var.list_values()
        #    print "h2f2", my_var["code_seq"].list_values("*")
        #    print "h2f2", my_var["code_seq"].get_list("*")
        #    print "h2g", new_var.list_seq()
        #else:
        #    print "h2", None
        #new_tup = c_var.ptr_to_seq("copy_ln1")
        #print "h3", new_tup
        #new_ptr = my_var.list_ref_to_seq(seq)
        #print "h4", new_ptr
        #print "h5",my_var.seq_replace(seq, c_var.ptr_to_seq("copy_ln1"), "xx")
        #print "k1 line",my_var.seq_lineage(seq)
        #print "k2 prnt",my_var.seq_parent(seq)
        #print "k3 prog",my_var.seq_progenitor(seq)
        #print "k4  del",my_var.seq_delete(seq)
        #print my_var.append_index("item", "broom")
        #print "mn1", my_var.name()
        #print "mn2", my_var.name("system_title")
        #print "mn3", my_var["system_title"].name()
        #print "mn4", my_var["item", "broom"].name("size")
        #print "mv1", my_var.value()
        #print "mv2", my_var.value("system_title")
        #print "mv3", my_var["system_title"].value()
        #print "mv4", my_var["item", "broom"].value("size")
        #print "mr1", my_var.rlist()
        #print "mr2", my_var.rlist("system_title")
        #print "mr3", my_var["system_title"].rlist()
        #print "mr4", my_var["item", "broom"].rlist("size")
        #print "ms1", my_var.seq()
        #print "ms2", my_var.seq("system_title")
        #print "ms3", my_var["system_title"].seq()
        #print "ms4", my_var["item", "broom"].seq("size")
        #print "ms5", my_var["code_seq"].seq()
        #print "ms5", my_var["code_seq"].seq("*", "r3")
        #print "ms5", my_var["code_seq"].seq("*", "r3", 1)
        #print "nn1", my_var.set_name("zip")
        #print "nn2", my_var.set_name("new_title", "system_title")
        #print "nn3", my_var["zoom_flag"].set_name("new_flag")
        #print "nn4",  my_var["item", "broom"].set_name("new_size", "size")
        #print "nn4b", my_var["item", "broom"].set_name("new_size", "size")
        #print "nv1", my_var.set_value("zip")
        #print "nv2", my_var.set_value("spook", "new_title")
        #print "nv3", my_var["new_flag"].set_value("True")
        #print "nv4",  my_var["item", "broom"].set_value("1000", "new_size")
        #print "ns1", my_var.set_seq("2000")
        #print "ns2", my_var.set_seq("3000", "new_title")
        #print "ns3", my_var["new_flag"].set_seq("4000")
        #print "ns4",  my_var["item", "broom"].set_seq("5000", "new_size")
        #print "ns4b", my_var["item", "broom"]["new_size"].name()
        #print "ns4c", my_var["item", "broom"]["new_size"].value()
        #print "ns4d", my_var["item", "broom"]["new_size"].seq()
        #print "o",my_var[("item", "zing") : ("item", "broom", 2)]
        #print "o2",my_var[("zoom_flag") : ("system_title") : 1]
        #print "o3",my_var[ : : 2]
        my_var.extend(x_var, prefix="blah")
        
        print "z",my_var._explicit()
        #print "z1", c_var._explicit()
        #print "z2",my_var.dump()
        print "z3",x_var._explicit()

        #TODO: add '.del_decendants()'
        #TODO: add '.del_ancestral_branch()'
        #TODO: add '.change_name()'

    else:
        print "==================================="
        print
        import doctest
        print "Testing begins. Errors found:"
        print doctest.run_docstring_examples(rolne.find, None)
        print doctest.run_docstring_examples(rolne.append, None)
        print doctest.run_docstring_examples(rolne.append_index, None)
        print doctest.run_docstring_examples(rolne.upsert, None)
        
