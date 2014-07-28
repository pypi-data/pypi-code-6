# rolne\__init__.py
#
# rolne datatype class: Recursive Ordered List of Named Elements
#
# Version 0.1.0
    
import copy

TNAME = 0
TVALUE = 1
TLIST = 2

class rolne(object):

    def __init__(self, in_list=[]):
        self.data = in_list

    def __str__(self):
        result = "<rolne datatype object\n"
        result += self.mards()
        result += ">"
        return result

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
            for entry in self.data:
                if entry[0]==name:
                    if entry[1]==value:
                        if start_ctr==index:
                            return(rolne(entry[2]))
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

    def append(self, name, value=None):
        new_tuple = (name, value, [])
        self.data.append(new_tuple)
        return True

    def upsert(self, name, value=None):
        new_tuple = (name, value, [])
        for entry in self.data:
            if entry[TNAME]==name:
                if entry[TVALUE]==value:
                    return False
        self.data.append(new_tuple)
        return True


    def get_list(self, name):
        result = []
        for entry in self.data:
            if entry[TNAME]==name:
                result.append(entry[TVALUE])
        return result

    def value(self, name):
        for (en, ev, el) in self.data:
            if en==name:
                return ev
        return None

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
        my_var["item", "broom"].upsert("size", "7")
        my_var["item", "broom"].upsert("title", 'The "big" thing')
        my_var.upsert("zoom_flag")
        my_var.upsert("code_seq")
        my_var["code_seq", None].append("*", "r9")
        my_var["code_seq", None].append("*", "r3")
        my_var["code_seq", None].append("*", "r2")
        my_var["code_seq", None].append("*", "r3")
        my_var.upsert("system_title", "hello")

        print "a", my_var
        #print "aa", my_var["zoom_flag"]
        print "b", my_var["code_seq"]
        print "bb", my_var.find("code_seq")
        #print "c", my_var.get_list("item")
        my_var["code_seq"]["*", "r9"] = 'zings'
        print "d", my_var
        #print "e", my_var["item", "bam"].value("size")
        #my_var["item", "zing"].reset_value("color", "white")
        #print "f", my_var

    else:
        print "==================================="
        print
        import doctest
        print "Testing begins. Errors found:"
