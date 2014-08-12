# rolne\__init__.py
#
# rolne datatype class: Recursive Ordered List of Named Elements
#
# Version 0.1.4
    
import copy

TNAME = 0
TVALUE = 1
TLIST = 2

class rolne(object):

    def __init__(self, in_list=None):
        if in_list is None:
            self.data = []
        else:
            self.data = in_list

    def __str__(self):
        result = "<rolne datatype object\n"
        result += self.mards()
        result += ">"
        return result

    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, tup):
        if isinstance(tup, slice):
            (start_name, start_value, start_index) = (None, None, 0)
            if tup.start:
                if len(tup.start)>0:
                    start_name = tup.start[0]
                if len(tup.start)>1:
                    start_value = tup.start[1]
                if len(tup.start)>2:
                    start_index = tup.start[2]
            (stop_name, stop_value, stop_index) = (None, None, 0)
            if tup.stop:
                if len(tup.stop)>0:
                    stop_name = tup.stop[0]
                if len(tup.stop)>1:
                    stop_value = tup.stop[1]
                if len(tup.stop)>2:
                    stop_index = tup.stop[2]
            if tup.step:
                if tup.step==0:
                    raise KeyError, "Step cannot be zero"
                step = int(tup.step)
            else:
                step = 1
            #
            if tup.start:
                start_flag = False
            else:
                start_flag = True
            start_ctr = 0
            step_ctr = 0
            new_list = []
            for entry in self.data:
                if start_flag:
                    if tup.stop and stop_name==entry[TNAME] and stop_value==entry[TVALUE]:
                        break
                    if (step_ctr % step)==0:
                        new_list.append(entry)
                    step_ctr += 1
                else:
                    if start_name==entry[TNAME] and start_value==entry[TVALUE]:
                        if start_ctr==start_index:
                            start_flag = True
                            new_list.append(entry)
                            step_ctr += 1
                        else:
                            start_ctr += 1
            else:
                if start_flag:
                    if tup.stop:
                        raise KeyError, repr(tup.stop)+" not found"
                else:
                    raise KeyError, repr(tup.start)+" not found"
            return rolne(in_list=new_list)
        else:
            if not isinstance(tup, tuple):
                tup = (tup, None)
            (name, value, index) = (None, None, 0)
            if len(tup)>0:
                name = tup[0]
            if len(tup)>1:
                value = tup[1]
            if len(tup)>2:
                index = tup[2]
            start_ctr = 0
            if index<0:
                search_data = reversed(list(enumerate(self.data)))
                index = -index - 1
            else:
                search_data = enumerate(self.data)
            for i, entry in search_data:
                if entry[0]==name:
                    if entry[1]==value:
                        if start_ctr==index:
                            return(rolne(self.data[i][2]))
                        else:
                            start_ctr += 1
        raise KeyError, repr(tup)+" not found"
        return None

    def __setitem__(self, tup, value):
        if not isinstance(tup, tuple):
            tup = (tup, None)
        (name, cur_value, index) = (None, None, 0)
        index_flag = False
        if len(tup)>0:
            name = tup[0]
        if len(tup)>1:
            cur_value = tup[1]
        if len(tup)>2:
            index = tup[2]
            index_flag = True
        start_ctr = 0
        for i,(entry_name, entry_value, entry_list) in enumerate(self.data):
            if entry_name==name:
                if entry_value==cur_value:
                    if start_ctr==index:
                        new_tuple = (entry_name, value, entry_list)
                        self.data[i] = new_tuple
                        return True
                    else:
                        start_ctr += 1
        if index_flag:
            raise KeyError, repr(tup)+" not found"
        else:
            self.upsert(name, value)
        return True

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
            x = rolne([entry])
            yield x

    def find(self, *argv):
        return self.__getitem__(argv)

    def mards(self):
        result = ""
        # return repr(self.data)
        if self.data:
            for entry in self.data:
                result += entry[0]
                if entry[1] is not None:
                    printable = str(entry[1])
                    quote_flag = False
                    if '"' in printable:
                        quote_flag = True
                    if len(printable) != len(printable.strip()):
                        quote_flag = True
                    if quote_flag:
                        result += " "+'"'+str(entry[1])+'"'
                    else:
                        result += " "+str(entry[1])
                result += "\n"
                if entry[2]:
                    # result += "*"
                    temp = rolne(entry[2]).mards()
                    for line in temp.split("\n"):
                        if line:
                            result += "    "+line
                            result += "\n"
        else:
            result = "None\n"
        return result

    def append(self, name, value=None, sublist=None):
        if sublist is None:
            sublist = []
        new_tuple = (name, value, sublist)
        self.data.append(new_tuple)
        return True

    def append_index(self, name, value=None, sublist=None):
        if sublist is None:
            sublist = []
        new_tuple = (name, value, sublist)
        self.data.append(new_tuple)
        index = len(self.get_list(name, value)) - 1
        return index


    def upsert(self, name, value=None):
        new_tuple = (name, value, [])
        for entry in self.data:
            if entry[TNAME]==name:
                if entry[TVALUE]==value:
                    return False
        self.data.append(new_tuple)
        return True

    def get_list(self, *args):
        #         name=None):
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

    def get_names(self):
        result = []
        for entry in self.data:
            result.append(entry[TNAME])
        return result

    def get_tuples(self, name=None):
        result = []
        for entry in self.data:
            if (entry[TNAME]==name) or (name is None):
                result.append((entry[TNAME], entry[TVALUE]))
        return result
        
    def value(self, name):
        for (en, ev, el) in self.data:
            if en==name:
                return ev
        return None

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
        for (en, ev, el) in self.data:
            if en==name:
                if value_missing or ev==value:
                    value_list.append(ev)
                    summary.append((en, ev, el))
        return (name, value_list, rolne(in_list = summary))

    def filter(self, *argv):
        return self.summarize(*argv)[2]


    def reset_value(self, name, value):
        for (en, ev, el) in self.data:
            if en==name:
                return self.__setitem__((en, ev), value)
        return False
    
if __name__ == "__main__":

    if True:

        my_var = rolne()
        my_var.upsert("item", "zing")
        my_var["item", "zing"].upsert("size", "4")
        my_var["item", "zing"].upsert("color", "red")
        my_var["item", "zing"]["color", "red"].upsert("intensity", "44%")
        my_var["item", "zing"].upsert("color", "yellow")
        my_var.upsert("item", "womp")
        my_var["item", "womp"].upsert("size", "5")
        my_var["item", "womp"].upsert("color", "blue")
        my_var.upsert("item", "bam")
        my_var.upsert("item", "broom")
        my_var["item", "broom", -1].upsert("size", "1")
        my_var["item", "broom", -1].upsert("title", 'The "big" thing')
        my_var.append("item", "broom")
        my_var["item", "broom", -1].upsert("size", "2")
        my_var["item", "broom", -1].upsert("title", 'The "big" thing')
        my_var.append("item", "broom")
        my_var["item", "broom", -1].upsert("size", "3")
        my_var["item", "broom", -1].upsert("title", 'The "big" thing')
        my_var.upsert("zoom_flag")
        my_var.upsert("code_seq")
        my_var["code_seq", None].append("*", "r9")
        my_var["code_seq", None].append("*", "r3")
        my_var["code_seq", None].append("*", "r2")
        my_var["code_seq", None].append("*", "r3")
        my_var.upsert("system_title", "hello")

        print "a", my_var
        #print "aa", my_var["zoom_flag"]
        #print "b", my_var["code_seq"]
        #print "bb", my_var.find("code_seq")
        print "c1", my_var.get_list()
        print "c2", my_var.get_list("item")
        print "c3", my_var.get_list("item", "broom")
        print "c4", my_var.get_list("item", "broom", 2)
        print "c5", my_var.get_list("item", "broom", 9)
        #my_var["code_seq"]["*", "r9"] = 'zings'
        #print "d", my_var
        #print "e", my_var["item", "bam"].value("size")
        #my_var["item", "zing"].reset_value("color", "white")
        #print "f", my_var
        #print "g", my_var["item", "broom", -1]
        print my_var.append_index("item", "broom")
        print my_var

    else:
        print "==================================="
        print
        import doctest
        print "Testing begins. Errors found:"
