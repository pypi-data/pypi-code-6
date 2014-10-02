# rolne\support_library.py
#
# SUPPORT LIBRARY FOR ROLNE
#
    
import copy
import numbers

TNAME = 0
TVALUE = 1
TLIST = 2
TSEQ = 3

COPY_NS = -99

def _seq(self, seq=None, inc=1):
    # decide on a starting point (result)
    if seq:
        result = str(seq)
    else:
        result = str(self.NS[0])
        self.NS[0] += inc
    # now account for duplicates
    ext = 2
    if _seq_find_dup(self.ancestor, result):
        try_result = result+" ("+str(ext)+")"
        while _seq_find_dup(self.ancestor, try_result) and ext<100000:
            ext += 1
            try_result = result+" ("+str(ext)+")"
        result = try_result
    return result

def _seq_find_dup(data, seq):
    for item in data:
        if item[TSEQ]==seq:
            return True
        if item[TLIST]:
            if _seq_find_dup(item[TLIST], seq):
                return True
    return False
    
def mards(self, detail=False):
    # this is NOT, of course, a _real_ MARDS representation.
    # for example, it is possible for a 'rolne' name to be a string with spaces.
    #  but that is not possible in MARDS. Here, we simply put quotes around the name.
    #  Plus, MARDS only does strings. A rolne can do anything.
    #  Here, we add a equals sign to non-None scenarios.
    return _mards(self.data, detail)
    
def _mards(data, detail):
    result = u""
    # return repr(self.data)
    if data:
        for entry in data:
            if detail==True:
                result += u"[{}] ".format(unicode(entry[TSEQ]))
            result += poss_quotes(entry[TNAME])
            if entry[TVALUE] is None:
                result += u" is None"
            else:
                result += u" = "+poss_quotes(entry[TVALUE])
            result += u"\n"
            if entry[TLIST]:
                temp = _mards(entry[TLIST], detail)
                for line in temp.split(u"\n"):
                    if line:
                        result += u"    "+line
                        result += u"\n"
    else:
        result = u"%empty\n"
    return result

def poss_quotes(value):
    printable = unicode(value)
    quote_flag = False
    if len(printable)==0:
        quote_flag = True
    if '"' in printable:
        quote_flag = True
    if ' ' in printable:
        quote_flag = True
    if '=' in printable:
        quote_flag = True
    if len(printable) != len(printable.strip()):
        quote_flag = True
    if quote_flag:
        return u'"'+printable+u'"'
    return printable

def _extend(self, sublist, prefix, retain_seq):
    new_list = []
    for entry in sublist:
        (en, ev, el, es) = entry
        if retain_seq:
            seq = _seq(self, seq=prefix+es)
        else:
            seq = prefix+_seq(self)
        sub_list = _extend(self, el, prefix, retain_seq)
        tup = (en, ev, sub_list, seq)
        new_list.append(tup)
    return new_list
        

def _flattened_list(self, data, args, name, value, index, seq, grep=False):
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
        append_flag = False
        if arg_count==0:
            result.append(tup)
            append_flag = True
        if arg_count==1:
            if entry[TNAME]==args[0]:
                result.append(tup)
                append_flag = True
        if arg_count==2:
            if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                result.append(tup)
                append_flag = True
        if arg_count==3:
            if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                if ctr[(entry[TNAME], entry[TVALUE])]==args[2]:
                    result.append(tup)
                    append_flag = True
        if entry[TLIST]:
            # notice that the 'args' parameter does not get passed on recursion. That
            # is because the search only happen at layer one. (unless 'grep'=True)
            if grep:
                result.extend(_flattened_list(self, entry[TLIST], args, name, value, index, seq, grep=True) )
            else:
                if append_flag:
                    result.extend(_flattened_list(self, entry[TLIST], (), name, value, index, seq) )
    return result
    
def _serialize(self, data, name_prefix, value_prefix, index_prefix, explicit, path=None):
    result = []
    ctr = {}
    if path is None:
        path = name_prefix
    else:
        path += name_prefix
    for entry in data:
        # the counter function
        if (entry[TNAME], entry[TVALUE]) in ctr:
            ctr[(entry[TNAME], entry[TVALUE])] += 1
        else:
            ctr[(entry[TNAME], entry[TVALUE])] = 0
        # make the tuple
        idx = ctr[(entry[TNAME], entry[TVALUE])]
        if explicit:
            full_path = path+unicode(entry[TNAME])
            if entry[TVALUE] is None:
                full_path += value_prefix
            else:
                full_path += value_prefix+unicode(entry[TVALUE])
            full_path += index_prefix+str(idx)
        else:
            full_path = path+unicode(entry[TNAME])
            if idx>0 or entry[TVALUE] is not None:
                full_path += value_prefix+unicode(entry[TVALUE])
            if idx>0:
                full_path += index_prefix+str(idx)
        sub = []
        if entry[TLIST]:
            # notice that the 'args' parameter does not get passed on recursion. That
            # is because the search only happen at layer one.
            sub = _serialize(self, entry[TLIST], name_prefix, value_prefix, index_prefix, explicit, path=full_path)
        tup = (full_path, entry[TVALUE], [], entry[TSEQ])
        result.append(tup)
        result.extend(sub)
    return result

def _serialize_names(self, data, name_prefix, value_prefix, index_prefix, explicit, path=None):
    result = []
    ctr = {}
    if path is None:
        path = name_prefix
    else:
        path += name_prefix
    for entry in data:
        # the counter function
        if entry[TNAME] in ctr:
            ctr[entry[TNAME]] += 1
        else:
            ctr[entry[TNAME]] = 0
        # make the tuple
        idx = ctr[entry[TNAME]]
        if explicit:
            full_path = path+unicode(entry[TNAME])
            full_path += index_prefix+str(idx)
        else:
            full_path = path+unicode(entry[TNAME])
            if idx>0:
                full_path += index_prefix+str(idx)
        sub = []
        if entry[TLIST]:
            # notice that the 'args' parameter does not get passed on recursion. That
            # is because the search only happen at layer one.
            sub = _serialize_names(self, entry[TLIST], name_prefix, value_prefix, index_prefix, explicit, path=full_path)
        tup = (full_path, entry[TVALUE], [], entry[TSEQ])
        result.append(tup)
        result.extend(sub)
    return result

def _flatten(data, args):
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
        idx = ctr[(entry[TNAME], entry[TVALUE])]
        sub = []
        if entry[TLIST]:
            # notice that the 'args' parameter does not get passed on recursion. That
            # is because the search only happen at layer one.
            sub = _flatten(entry[TLIST], args)
        # insert as dictated by args given
        append_flag = False
        if arg_count==0:
            append_flag = True
        if arg_count==1:
            if entry[TNAME]==args[0]:
                append_flag = True
        if arg_count==2:
            if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                append_flag = True
        if arg_count==3:
            if entry[TNAME]==args[0] and entry[TVALUE]==args[1]:
                if ctr[(entry[TNAME], entry[TVALUE])]==args[2]:
                    append_flag = True
        if append_flag:
            tup = (entry[TNAME], entry[TVALUE], [], entry[TSEQ])
            result.append(tup)
        result.extend(sub)
    return result
   
def _renumber(self, data, increment, prefix, suffix):
    result = []
    for entry in data:
        seq = str(self.NS[0])
        if prefix:
            seq = prefix+seq
        if suffix:
            seq = seq+suffix
        self.NS[0] += increment
        # now account for duplicates
        if self.ref_seq is not None:  #am i a child (not the root)?
            ext = 2
            if _seq_find_dup(self.ancestor, seq):
                try_result = seq+" ("+str(ext)+")"
                while _seq_find_dup(self.ancestor, try_result) and ext<100000:
                    ext += 1
                    try_result = seq+" ("+str(ext)+")"
                seq = try_result
        if entry[TLIST]:
            sub = _renumber(self, entry[TLIST], increment, prefix, suffix)
        else:
            sub = []
        tup = (entry[TNAME], entry[TVALUE], sub, seq)
        result.append(tup)
    return result
    
def _dump(self, data):
    result = []
    for entry in data:
        tup = (entry[TNAME], entry[TVALUE], _dump(self, entry[TLIST]))
        result.append(tup)
    return result

# an internal routine to get self or an element based on flexible args
# returns (name, value, index, seq, list)
def ref_super_tuple(self, *args):
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
        super_tup = super_tuple_search_seq(self.ref_seq, self.ancestor)
        return super_tup
    else:
        for entry in self.data:
            (en, ev, el, es) = entry
            if en==name:
                if arglen==1:
                    return (en, ev, ctr, es, el)
                elif ev==value:
                    if ctr==index:
                        return (en, ev, ctr, es, el)
                    ctr += 1
    return (None, None, None, None, None)


def super_tuple_search_seq(seq, data):
    ctr = 0
    for entry in data:
        (en, ev, el, es) = entry
        if es==seq:
            target_name = en
            target_value = ev
            for (tn, tv, _, ts) in data:
                if target_name==tn and target_value==tv:
                    if ts==seq:
                        break
                    ctr += 1
            return (en, ev, ctr, es, el)
        if el:
            result = super_tuple_search_seq(seq, el)
            if result:
                return result
    return None


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
# TODO: delete this function; I strongly suspect that it is an unneeded later
def _point_ancestry(self):
    return rolne(in_tuple=(None, None, self.ancestor, None))
    
def ptr_to_seq(self, seq):
    # this is an interesting one: return a reference to
    # the direct tuple with this sequence. Use with care.
    (target_list, target_index) = list_ref_to_seq(self.ancestor, seq)
    if target_list is None:
        return None
    return target_list[target_index]

def _seq_lineage(data, seq):
    for index, entry in enumerate(data):
        (en, ev, el, es) = entry
        if es==seq:
           return [es]
        if el:
            result = _seq_lineage(el, seq)
            if result:
                return [es]+result
    return []
        

def list_ref_to_seq(orig_data, seq):
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
    return _list_ref_to_seq(orig_data, seq)

def _list_ref_to_seq(data, seq):
    result = (None, None)
    for index, entry in enumerate(data):
        (en, ev, el, es) = entry
        if es==seq:
           return (data, index)
        if el:
            result = _list_ref_to_seq(el, seq)
            if result[0] is not None:
                return result
    return (None, None)

def _copy_sublist_with_new_seq(self, source, prefix):
    dest = []
    for (ev, en, el, es) in source:
        new_seq = prefix+_seq(self) # called before next to make seq look logical
        new_list = _copy_sublist_with_new_seq(self, el, prefix)
        new_tup = (copy.copy(ev), copy.copy(en), new_list, new_seq)
        dest.append(new_tup)
    return dest

def _copy(self, seq_prefix, seq_suffix, data, renumber):
    global COPY_NS
    new_list = []
    for (ev, en, el, es) in data:
        if renumber:
            mid = str(COPY_NS)
        else:
            mid = es
        COPY_NS += 1
        sub = _copy(self, seq_prefix, seq_suffix, el, renumber)
        new_list.append((copy.copy(ev), copy.copy(en), sub, seq_prefix+mid+seq_suffix))
    return new_list

def dump_list(self, args, name=False, value=False, index=False, seq=False):
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

    
# the 'key_list' is very flexible:
#   exist_pull(item, "name")
#   exist_pull(item, ("name", "val"))
#   exist_pull(item, ["name1", "name2"])
#   exist_pull(item, [("name", "val"), ("name2", "val2")])
def exist_and_pull(tup, root_index, key_list):
    if isinstance(key_list, list):
        pass
    else:
        key_list = [key_list]
    ptr = [tup]
    for level, key in enumerate(key_list):
        en = ev = None
        ei = 0
        if isinstance(key, list) or isinstance(key, tuple):
            cl = len(key)
            if cl>0: en = key[0]
            if cl>1: ev = key[1]
            if cl>2: ei = key[2]
            if cl>3: cl=3
            if cl==1 and en is None:
                cl=0  # (None) and [] and [None] is the same as None: match everything
        else:
            en = key
            cl = 1
            if key is None:
                cl=0  # None means match everything. It is the same thing as () and []
        ctr = 0
        for i, item in enumerate(ptr):
            if cl==0:
                value = item[TVALUE]
                break
            elif cl==1:
                if en==item[TNAME]:
                    value = item[TVALUE]
                    break
            elif cl==2:
                if en==item[TNAME] and ev==item[TVALUE]:
                    value = item[TVALUE]
                    break
            elif cl==3:
                if en==item[TNAME] and ev==item[TVALUE]:
                    if level==0:
                        if ei==root_index:
                            value = item[TVALUE]
                            break
                    else:
                        if ei==ctr:
                            value = item[TVALUE]
                            break
                        ctr += 1
        else:
            return False, None
        ptr = ptr[i][TLIST]
    return True, value

