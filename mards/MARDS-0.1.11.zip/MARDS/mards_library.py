# -*- coding: iso-8859-1 -*-
# MARDS\mards_library.py
#
# INTERNAL SUPPORT ROUTINES
#

from rolne import rolne
import string


# Core priciple: if strict=False and there is no schema, there will NEVER
# be an error.
def MARDS_to_rolne(doc=None, schema=None, context="doc", strict=False, key_open=False, prefix="", schema_dir=None, suppress_schema=False):
    result = rolne()
    error_list = []
    if doc is None:
        return result, error_list
    if suppress_schema:
        schema = rolne()
    else:
        schema, schema_errors = SCHEMA_to_rolne(schema, prefix="", schema_dir=schema_dir)
        error_list.extend(schema_errors)
    current = 0
    tab_list = [0]
    pointer_list = range(50)
    pointer_list[0]=result
    last_spot = pointer_list[0]
    last_nvi = range(50)
    for ctr, line in enumerate(doc.split("\n")):
        (indent, key, value, error) = parse_line(line, tab_list, strict=strict, key_open=key_open)
        if error:
            t = ("[error]", context, ctr, error)
            error_list.append(t)
        else:
            if key:
                if indent<current:
                    current = indent
                elif indent==current:
                    pass # do nothing, the operational default works
                elif indent==(current+1):
                    pointer_list[indent] = last_spot
                    current = indent
                else:
                    if strict:
                        t = ("[error]", context, ctr, "tab stop jumped ahead too far")
                        error_list.append(t)
                        break
                    else:
                        indent = current+1
                        pointer_list[indent] = last_spot
                        current = indent
                index = pointer_list[indent].append_index(key, value, seq=prefix+str(ctr))
                last_spot = pointer_list[indent][key, value, index]
                last_nvi[indent]=(key, value, index)
    if not suppress_schema:
        result, schema_errors = schema_rolne_check(result, schema)
        error_list.extend(schema_errors)
    return result, error_list

# if strict==False, there should NEVER be an error returned.   
def parse_line(line, tab_list, strict=False, key_open=False):
    indent = None
    key = None
    value = None
    error = None
    space_ctr = 0
    if len(line.strip())==0: #skip completely whitespace lines
        return (indent, key, value, error)
    # mode: 0=beginning, 1=key, 2=pre-value, 3=value
    mode = 0 # beginning
    for c in line:
        if mode==0: # beginning
            if c==" ":
                space_ctr += 1
            elif c=="\n":
                return (indent, key, value, error) # skip line if all whitespaces
            elif c=="#" and key_open==False:
                return (indent, key, value, error) # skip line if starts with # comment symbol
            elif len(c.strip())==0 and strict:
                return (indent, key, value, "non-space whitespace character found before key")
            elif c=="\t":
                space_ctr += 4
            elif c in string.whitespace:
                space_ctr += 1
            else:
                key=c
                mode = 1 # key
        elif mode==1: # key
            if c==" ":
                mode = 2 # pre-value
            elif len(c.strip())==0 and strict:
                return (indent, key, value, "non-space whitespace character found inside key")
            elif c in string.whitespace:
                mode = 2 #pre-value
            else:
                key += c
        elif mode==2: # pre-value
            if c==" ":
                pass
            else:
                value=c
                mode = 3 # value
        elif mode==3: # value
            value += c
        else:
            raise
    if value is not None:
        value = value.strip()
        if len(value)>=2:
            if value[0]==value[-1]=='"':
                value=value.rstrip()[1:-1]
            elif value[0]==value[-1]=="'":
                value=value.rstrip()[1:-1]
    #
    # calculate indent
    #
    if strict:
        indent = int(space_ctr / 4)
        if space_ctr % 4 != 0:
            snap = line.strip()[:20]
            return (indent, key, value, "indent found that is not a multiple of 4 spaces: '{}'".format(snap))
    else:
        indent = 0
        #print key, value, space_ctr, repr(tab_list)
        match_found = False
        for spot, x in enumerate(tab_list):
            if space_ctr<x:
                # spot found, but at a new 'tab'. aka the 'slide to the left'
                indent = spot
                break
            elif space_ctr==x:
                indent = spot
                match_found = True
                break
            elif space_ctr>x:
                indent = spot
        else:
            # new 'biggest' number found
            tab_list.append(space_ctr)
            indent += 1
            match_found = True
        #print indent, match_found
        if not match_found:
            tab_list[indent] = space_ctr
        if len(tab_list)>(indent+1):
            del tab_list[indent+1:]
    #
    # done
    #
    return (indent, key, value, error)

def rolne_to_dict(rolne):
    d = {}
    for entry in rolne:
        (key, value, new_rolne) = entry
        if new_rolne:
            if key in d:
                d[key].append(rolne_to_dict(new_rolne))
            else:
                d[key] = [rolne_to_dict(new_rolne)]
        if value is not None:
            if key in d:
                d[key].append(value)
            else:
                d[key] = [value]
    return d

def render_mards_target(target, indent=0, quote_method='all'):
    result = ""
    if type(target) is dict:
        for key in target:
            # turn everything back into list of things
            if type(target[key]) is list:
                value_list = target[key]
            elif type(target[key]) is dict:
                value_list = [None]
            else:
                value_list = [target[key]]
            for value in value_list:
                result += " "*(indent*4)
                result += str(key)
                if value:
                    result += value_output(value, quote_method=quote_method)
                result += "\n"
            if type(target[key]) is dict:
                result += render_mards_target(target[key], indent=indent+1, quote_method=quote_method)
    return result
    
def delist(target):
    ''' for any "list" found, replace with a single entry if the list has exactly one entry '''
    result = target
    if type(target) is dict:
        for key in target:
            target[key] = delist(target[key])
    if type(target) is list:
        if len(target)==0:
            result = None
        elif len(target)==1:
            result = delist(target[0])
        else:
            result = [delist(e) for e in target]
    return result

def value_output(value, quote_method='all', none_handle='strict'):
    '''
    Format types:
    'all'.
       (default) everything is embraced with quotes
    'needed'.
       Quote only if needed. Values are on placed in quotes if:
       a. the value contains a quote
       b. there is whitespace at the beginning or end of string
    'none'.
       Quote nothing.
    '''
    p = str(value)
    if value is None:
        if none_handle=='strict':
            return ""
        elif none_handle=='empty':
            return ' ""'
        elif none_handle=='None':
            p = "None"
        else:
            raise "none handler "+str(none_handle)+" not recognized"
    if quote_method=='all':
        return ' "'+p+'"'
    elif quote_method=='by_need':
        if len(p)!=len(p.strip()):
            return ' "'+p+'"'
        if '"' in p:
            return ' "'+p+'"'
        return " "+p
    elif quote_method=='none':
        return " "+p
    else:
        raise "quote method "+str(quote_method)+" not recognized"
    return

    
def SCHEMA_to_rolne(doc=None, prefix=None, schema_dir=None):
    # print "a"
    if prefix is None:
        prefix = ""
    ################################
    # CONVERT TO A ROLNE
    ################################
    schema, error_list = MARDS_to_rolne(doc, context="schema", strict=True, key_open=True, prefix=prefix, suppress_schema=True)
    ################################
    #  FIRST PASS SYNTAX CHECKING
    #
    # build a list of names from the document and their corresponding locations
    # mark as False if the key is seen twice
    # also do basic syntax checking
    ################################
    for key in schema.grep():
        (en, ev, ei, es) = key
        if en in ["name", "template"]:
            pass
        elif en in ["#!MARDS_schema_en_1.0", "import", "local", "exclusive"]:
            pass
        elif en in ["##"]:
            schema.seq_delete(es)
        elif en in ["limit"]:
            # TODO: check that parent is 'recurse'
            parent_es = schema.seq_parent(es)
            if schema.at_seq(parent_es).name!='recurse':
                error_list.append( ("[error]", "schema", es, "the 'limit' element may only be applied to a 'recurse'") )
                schema.seq_delete(es)
            else:
                if ev.isdigit():
                    if int(ev)<1 or int(ev)>20:
                        error_list.append( ("[error]", "schema", es, "the 'limit' should have a integer value between 1 and 20") )
                        schema.seq_delete(es)
                else:
                    error_list.append( ("[error]", "schema", es, "the 'limit' should have a integer value between 1 and 20") )
                    schema.seq_delete(es)
        elif en in ["treatment", "value", "required", "default", "ordered"]:
            pass
        elif en in ["insert", "recurse", "extend", "from"]:
            pass
        elif en in ["describe", "title", "abstract", "body", "reference", "author", 'title', 'url', 'journal', 'book', 'date_written', 'date_retreived', 'pages', 'paragraphs', 'copyright_message', 'publisher']:
            pass
        elif en in ["match", "search", "match_else"]:
            pass
        elif en in ["raise_error", "raise_warning", "raise_log"]:
            pass
        elif en in ["type", "choice", "search", "min"]:  ## TODO: Type stuff
            pass
        elif en in ["define_type", "unit", "*"]:  ## TODO: schema type stuff
            pass
        else:
            t = ("[error]", "schema", es, "'{}' not a recognized schema element name".format(en))
            error_list.append(t)
            schema.seq_delete(es)
    # print "b"
    ##################################
    #
    # IMPLEMENT Header and imports
    #
    #################################
    schema_list = schema.list_tuples("#!MARDS_schema_en_1.0")
    for (ev, en, ei, es) in schema_list:
        header = schema.at_seq(es)
        import_list = header.list_tuples("import")
        for (ien, iev, iei, ies) in import_list:
            i = header.at_seq(ies)
            if iev:
                prx = iev+"/"
            else:
                prx = "./"
            if i.get_name("local"):
                file_loc = i.get_value("local")
                if file_loc is None:
                    file_loc = iev+".MARDS-schema"
                    try:
                        with open(file_loc, 'r') as file:
                            subdata = file.read()
                    except: 
                        file_loc = schema_dir+"/"+iev+".MARDS-schema"
                        try:
                            with open(file_loc, 'r') as file:
                                subdata = file.read()
                        except IOError, e: 
                            error_list.append ( ("[error]", "schema", ies, str(e)) )
                            subdata = None
                else:
                    try:
                        with open(file_loc, 'r') as file:
                            subdata = file.read()
                    except IOError, e: 
                        file_loc = schema_dir+"/"+file_loc
                        try:
                            with open(file_loc, 'r') as file:
                                subdata = file.read()
                        except IOError, e: 
                            error_list.append ( ("[error]", "schema", ies, str(e)) )
                            subdata = None
                if subdata:
                    if prefix:
                        prx = prefix+prx
                    sr,e = SCHEMA_to_rolne(subdata, prefix=prx, schema_dir=schema_dir)
                    schema.extend(sr, retain_seq=True)
                    error_list.extend(e)
            else:
                error_list.append( ("[error]", "schema", ies, "unable to locate import method for '{}'".format(iev)) )
    # print "c"
    #################################
    #
    # MAKE A COPY AND BUILD INDEX
    #
    # copy used by other functions for internal insertions, etc.
    #################################
    copy = schema.copy(seq_prefix="", seq_suffix="")
    name_seq = {}
    name_seq[""] = {}
    for key in schema.grep():
        (en, ev, _, es) = key
        if en in ["name", "template"]:
            if es.startswith(prefix):
                es = es[len(prefix):]
            levels = es.split("/")
            if levels==1:
                subidx = levels[0]
                subimport = ""
            else:
                subidx = levels[-1]
                subimport = "/".join(levels[0:-1])
            if subimport not in name_seq:
                name_seq[subimport] = {}
            if ev in name_seq[subimport]:
                name_seq[subimport][ev]=False
            else:
                name_seq[subimport][ev]=es
    # print "d"
    #################################
    # IMPLEMENT 'template'
    #
    # This is done oddly: now that 'copy' has been made, we simply
    # delete the templates from the  active rolne and rename 'template' to
    # 'name' in the copy.
    #################################

    schema_list = schema.grep("template")
    for (ev, _, _, es) in schema_list:
        if not prefix:
            schema.seq_delete(es)
        copy.at_seq(es).name="name"
    #print "jschema",prefix,schema
    #print "jcopy",copy
    #################################
    #
    # IMPLEMENT 'insert'
    #
    #################################
    schema_list = schema.grep("insert")
    safety_ctr=0
    while schema_list and safety_ctr<20:
        for (_, ev, _, es) in schema_list:
            item = schema.at_seq(es)
            sub_doc = item.get_value('from') or ""
            if sub_doc in name_seq:
                if ev in name_seq[sub_doc]:
                    if name_seq[sub_doc][ev] is False:
                        t = ("[error]", "schema", es, "'name {}' found in schema multiple times".format(ev))
                        error_list.append(t)
                        schema.seq_delete(es)
                    else:
                        src = prefix+name_seq[sub_doc][ev]
                        depth_desired = 1
                        line = schema.seq_lineage(es)
                        new_depth = len(line) 
                        prx = src+"."
                        if name_seq[sub_doc][ev] in line:
                            error_list.append(("[error]", "schema", es, "'insert {}' ends up forming a loop. See lines {}. ".format(ev, ",".join(line))))
                            schema.seq_delete(es)
                        else:
                            schema.seq_replace(es, copy.at_seq(src), prx)
                else:
                    if sub_doc:
                        t = ("[error]", "schema", es, "on insert, a name or template for '{}' not found in schema '{}'".format(ev, sub_doc))
                    else:
                        t = ("[error]", "schema", es, "on insert, a name or template for '{}' not found in local schema".format(ev))
                    error_list.append(t)
                    schema.seq_delete(es)
            else:
                t = ("[error]", "schema", es, "an import for '{}' not found in schema".format(sub_doc))
                error_list.append(t)
                schema.seq_delete(es)
        schema_list = schema.grep("insert")
        safety_ctr += 1
    #################################
    #
    # IMPLEMENT 'extend'
    #
    #################################
    schema_list = schema.grep("extend")
    safety_ctr=0
    while schema_list and safety_ctr<20:
        for (_, ev, _, es) in schema_list:
            item = schema.at_seq(es)
            sub_doc = item.get_value('from') or ""
            if sub_doc in name_seq:
                if ev in name_seq[sub_doc]:
                    if name_seq[sub_doc][ev] is False:
                        t = ("[error]", "schema", es, "'name {}' found in schema multiple times".format(ev))
                        error_list.append(t)
                        schema.seq_delete(es)
                    else:
                        src = prefix+name_seq[sub_doc][ev]
                        depth_desired = 1
                        line = schema.seq_lineage(es)
                        new_depth = len(line) 
                        prx = src+"."
                        if name_seq[sub_doc][ev] in line:
                            error_list.append(("[error]", "schema", es, "'extend {}' ends up forming a loop. See lines {}. ".format(ev, ",".join(line))))
                            schema.seq_delete(es)
                        else:
                            parent = schema.at_seq(schema.seq_parent(es))
                            children = copy.at_seq(src)
                            if children:
                                children = children.copy(seq_prefix="", seq_suffix="")
                                if children.has('value'):
                                    del children['value']
                                parent.extend(children, prefix=prx)
                            else:
                                error_list.append(("[error]", "schema", es, "internal empty child error src='{}'. ".format(src)))
                            schema.seq_delete(es)
                else:
                    if sub_doc:
                        t = ("[error]", "schema", es, "on extend, a name or template for '{}' not found in schema '{}'".format(ev, sub_doc))
                    else:
                        t = ("[error]", "schema", es, "on extend, a name or template for '{}' not found in local schema".format(ev))
                    error_list.append(t)
                    schema.seq_delete(es)
            else:
                print prefix
                for s in name_seq:
                    print "   ",s
                t = ("[error]", "schema", es, "an import for '{}' not found in schema".format(sub_doc))
                error_list.append(t)
                schema.seq_delete(es)
        schema_list = schema.grep("extend")
        safety_ctr += 1
    #################################
    #
    # IMPLEMENT 'resurse' recursion
    #
    #################################
    schema_list = schema.grep("recurse")
    safety_ctr=0
    while schema_list and safety_ctr<20:
        for (_, ev, _, es) in schema_list:
            item = schema.at_seq(es)
            sub_doc = item.get_value('from') or ""
            if sub_doc in name_seq:
                if ev in name_seq[sub_doc]:
                    if name_seq[sub_doc][ev] is False:
                        t = ("[error]", "schema", es, "'name {}' found in schema multiple times".format(ev))
                        error_list.append(t)
                        schema.seq_delete(es)
                    else:
                        src = prefix+name_seq[sub_doc][ev]
                        depth_desired = item.get_value("limit")
                        if depth_desired is None:
                            depth_desired = 2
                        else:
                            try:
                                depth_desired = abs(int(depth_desired))
                            except:
                                depth_desired = 2
                                error_list.append(("[error]", "schema", es, "recurse limit is not a positive integer."))
                        line = schema.seq_lineage(es)
                        new_depth = safety_ctr+1
                        prx = src+".r"+str(new_depth)+"."
                        if name_seq[sub_doc][ev] in line:
                            if new_depth<=depth_desired:
                                schema.seq_replace(es, copy.at_seq(src), prx)
                            else:
                                schema.seq_delete(es)
                        else:
                            error_list.append(("[error]", "schema", es, "'recurse {}' is not recursive".format(ev)))
                            schema.seq_delete(es)
                else:
                    if sub_doc:
                        t = ("[error]", "schema", es, "on recurse, a name or template for '{}' not found in schema '{}'".format(ev, sub_doc))
                    else:
                        t = ("[error]", "schema", es, "on recurse, a name or template for '{}' not found in local schema".format(ev))
                    error_list.append(t)
                    schema.seq_delete(es)
            else:
                t = ("[error]", "schema", es, "an import for '{}' not found in schema".format(sub_doc))
                error_list.append(t)
                schema.seq_delete(es)
        schema_list = schema.grep("recurse")
        safety_ctr += 1
    # print "e"
    #################################
    #
    # LOCATE Missing VALUE and TYPE
    #
    #################################
    for (en, ev, ei, es) in schema.grep("name"):
        item = schema.at_seq(es)
        if item.has("value"):
            if not item["value"].has("type"):
                item["value"].append("type", "string", seq=es+".auto_type")
        else:
            item.append("value", None, seq=es+".auto_val")
            item["value", None].append("type", "string", seq=es+".auto_val.auto_type")
    
    #################################
    #
    # REMOVE ALL BUT TOP #!MARDS_schema_en_1.0
    #
    #################################
    head_list = schema.list_seq("#!MARDS_schema_en_1.0")
    if head_list:
        # keep the first one, but remove any 'import' references
        import_list = schema["#!MARDS_schema_en_1.0"].list_seq("import")
        for seq in import_list:
            schema.seq_delete(seq)
        # delete the rest
        del head_list[0]
        for seq in head_list:
            schema.seq_delete(seq)
    ########################
    #   DONE
    ########################
    # print "f"
    return schema, error_list
    
def schema_rolne_check(doc, schema):
    '''
    CHECK THE DOCUMENT AGAINST IT'S SCHEMA
    
    returns: cleaned-up-document, error_list
    '''
    import standard_types as st
    error_list = []
    #
    # PASS ONE: FORWARD CHECK OF DOC
    #
    # this pass verifies that each entry in the document
    # has a corresponding entry in the schema
    #
    exclusive_flag = True
    if schema.list_names("#!MARDS_schema_en_1.0"):
        if schema["#!MARDS_schema_en_1.0"].get_value("exclusive")=="false":
            exclusive_flag = False
    if exclusive_flag:
        # print "jj", schema
        el = check_schema_coverage(doc, schema)
        error_list.extend(el)
    #
    # PASS TWO: REQUIREMENTS CHECK OF SCHEMA
    #
    # this pass verifies that any 'required' entries in the
    # schema are met. It auto-inserts if allowed. Otherwise,
    # it adds an error.
    el = sub_schema_requirements(doc, schema)
    error_list.extend(el)
    #
    # PASS THREE: TREATMENT CHECKS
    #
    el = sub_schema_treatments(doc, schema)
    error_list.extend(el)
    #
    # PASS FOUR: TYPE CHECKS AND NORMALIZATION
    #
    el = st.apply_schema_types(doc, schema)
    error_list.extend(el)
    #
    #
    # PASS FIVE: RAISE_ERROR CHECKS
    #
    el = sub_schema_raises(doc, schema)
    error_list.extend(el)
    #
    return doc, error_list

def check_schema_coverage(doc, schema):
    '''
    FORWARD CHECK OF DOCUMENT
    
    This routine looks at each element in the doc, and makes sure there
    is a matching 'name' in the schema at that level.
    '''
    error_list = []
    to_delete = []
    for entry in doc.list_tuples():
        (name, value, index, seq) = entry
        temp_schema = schema_match_up(doc, schema)
        if not name in temp_schema.list_values("name"):
            error_list.append( ("[error]", "doc", seq, "a name of '{}' not found in schema".format(name)) )
            to_delete.append(seq)
        else:
            # check subs
            el = check_schema_coverage(doc[name, value, index], temp_schema["name", name])
            error_list.extend(el)
    for seq in to_delete:
        doc.seq_delete(seq)
    return error_list

def schema_match_up(doc, schema):
    '''
    SCHEMA mini-recompile for:

      each SEARCH then MATCH function
      each TYPE then CHOICE function
    
    given the doc, it returns a schema copy that implements the match
    '''
    copy = schema.copy(seq_prefix="", seq_suffix="")
    copy = _schema_match_up_search(doc, copy)
    copy = _schema_match_up_type_choice(doc, copy)
    return copy

def _schema_match_up_search(doc, copy):
    search_list = copy.list_keys("search")
    while search_list:
        for skey in search_list:
            (_, target, _) = skey
            doc_value = doc.get_value(target)
            match_list = copy[skey].list_values("match")
            if doc_value in match_list:
                copy.extend(copy[skey]["match", doc_value], prefix="match.")
                # del copy[skey]
                # copy = _schema_match_up_search(doc, copy)
            else:
                if copy[skey].has("match_else"):
                    copy.extend(copy[skey]["match_else"], prefix="match.")
                    # copy = _schema_match_up_search(doc, copy)
            del copy[skey]
        search_list = copy.list_keys("search")
    return copy

def _schema_match_up_type_choice(doc, copy):
    choices = copy.only([("name",),("value",),("type",),("choice",)])
    for item in choices:
        target = item.value
        doc_value = doc.get_value(target)
        choice_list = item["value"]["type"].list_tuples("choice")
        seq = None
        for (en, ev, ei, es) in choice_list:
            if doc_value==ev:
                seq = es
                break
        if seq:
            copy["name", target].extend(copy.at_seq(seq), prefix="choice.")
    return copy

    
def sub_schema_treatments(doc, orig_schema):
    schema = schema_match_up(doc, orig_schema)
    error_list = []
    to_delete = []
    for target in schema.list_values("name"):
        pointer = schema["name", target]
        treatment = pointer.get_value("treatment")
        if not treatment:
            treatment = "list"
        if treatment=="list":
            pass # there are no checks needed for list
        elif treatment=="unique":
            first_line = {}
            delete_list=[]
            for entry in doc.list_tuples(target):
                (en, ev, ei, es) = entry
                if ei==0:
                    first_line[ev] = es
                else:
                    delete_list.append((en, ev, ei))
                    error_list.append( ("[error]", "doc", es, "'{}' entries should be unique, but this line is a duplicate of line {}.".format(target, first_line[ev])) )
                    to_delete.append(es)
            for tup in reversed(delete_list):  # the items must be deleted in reverse to avoid index numbering problems
                del doc[tup]
        elif treatment=="sum":
            pass
        elif treatment=="average":
            pass
        elif treatment=="one":
            entry_list = doc.list_tuples(target)
            if len(entry_list)>1:
                first_line = entry_list[0][3]
                del entry_list[0]
                for (en, ev, ei, es) in entry_list:
                    #print doc
                    #exit()
                    error_list.append( ("[error]", "doc", es, "only one '{}' entry should exist, but this line is in addition to line {}.".format(target, first_line)) )
                    to_delete.append(es)
                for (en, ev, ei, es) in reversed(entry_list):
                    del doc[en, ev, ei]
        else:
            pass
        # check subs
        for key in doc.list_keys(target):
            el = sub_schema_treatments(doc[key],schema["name", target])
            error_list.extend(el)
    for seq in to_delete:
        doc.seq_delete(seq)
    return error_list

req_ctr = 0

def sub_schema_requirements(doc, orig_schema):
    schema = schema_match_up(doc, orig_schema)
    global req_ctr
    error_list = []
    for name_rule in schema.only("name"):
        # check/insert if a required name
        target_name = name_rule.value
        if name_rule.has("required"):
            if not doc.has(target_name):
                if name_rule.has("value"):
                    newseq = doc.append(target_name, name_rule["value"].get_value("default"), seq='auto'+str(req_ctr))
                else:
                    newseq = doc.append(target_name, None, seq="auto"+str(req_ctr))
                error_list.append( ("[warning]", "doc", newseq, "an entry for '{}' is required so it was automaticaly inserted.".format(target_name)) )
                req_ctr += 1
        # check 'value' (if exists)
        if name_rule.has("value"):
            value_parms = name_rule["value"]
            if value_parms.has("required"):
                for item in doc.only((target_name, None)):
                    if value_parms.has("default"):
                        item.value = value_parms.get_value("default")
                        error_list.append( ("[warning]", "doc", item.seq, "value was required for '{}' so the default value of '{}' was used.".format(target_name, str(value_parms.get_value("default")))) )
                    else:
                        error_list.append( ("[error]", "doc", item.seq, "value is required for '{}' and there is not default value.".format(target_name)) )
        # check subs
        for item in doc.only(target_name):
            el = sub_schema_requirements(item, name_rule)
            error_list.extend(el)
    return error_list

def sub_schema_raises(doc, schema):
    '''
    Look for "raise_error", "raise_warning", and "raise_log"
    
    '''
    error_list = []
    temp_schema = schema_match_up(doc, schema)
    for msg in temp_schema.list_values("raise_error"):
        error_list.append( ("[error]", "doc", doc.seq, "'{}'".format(msg)) )
    for msg in temp_schema.list_values("raise_warning"):
        error_list.append( ("[warning]", "doc", doc.seq, "'{}'".format(msg)) )
    for msg in temp_schema.list_values("raise_log"):
        error_list.append( ("[log]", "doc", doc.seq, "'{}'".format(msg)) )
    for entry in doc:
        if temp_schema.has(("name", entry.name)):
            el = sub_schema_raises(entry, temp_schema["name", entry.name])
            error_list.extend(el)
    return error_list
    
    
    
    
def sub_convert_python(doc, schema):
    #print "jj", doc, schema
    if schema.get_value("ordered")=="False":
        name_ordered_flag = False
    else:
        name_ordered_flag = True
    # create the 'structure' whatever it is
    if name_ordered_flag:
        result = []
    else:
        result = {}
    delete_list = {}
    # parse each entry
    for entry in doc.list_tuples():
        (en, ev, ei, es) = entry
        treatment = schema["name", en].get_value("treatment")
        if schema["name", en].get_value("ordered")=="False":
            value_ordered_flag = False
        else:
            value_ordered_flag = True
        if schema["name", en].list_values("name"):
            has_subs = True
        else:
            has_subs = False
        name_count = len(doc.list_values(en))
        sub_list = sub_convert_python(doc[en, ev, ei], schema["name", en])
        # create an item for the structure
        if name_ordered_flag:
            if value_ordered_flag:
                if has_subs:
                    item = (en, ev, sub_list)
                else:
                    item = (en, ev)
            else:
                if has_subs:
                    item = (en, ev, sub_list)
                else:
                    item = (en, ev)
            result.append(item)
        else:
            if value_ordered_flag:
                if has_subs:
                    if ev:
                        item = (ev, sub_list)
                    else:
                        item = sub_list
                else:
                    item = ev
            else:
                if has_subs:
                    item = {ev: sub_list}
                else:
                    item = ev
            if treatment=='one':
                if not en in result:
                    result[en] = item # only set if the first found
            elif treatment=='sum':
                if value_ordered_flag:
                    if not en in result:
                        result[en] = (ev, sub_list)
                    else:
                        result[en] = (type_aware_sum_value(result[en][0], ev), type_aware_sum_sub(result[en][1], sub_list))
                else:
                    #print "jj", en
                    if not en in result:
                        result[en] = {ev: sub_list}
                        if not en in delete_list:
                            delete_list[en] = [ev]
                    else:
                        dv = delete_list[en][-1]
                        delete_list[en].append(ev)
                        new_key = type_aware_sum_value(dv, ev)
                        #print "new_key", new_key
                        result[en][new_key] = type_aware_sum_sub(result[en][dv], sub_list)
            else: #anything else is a list
                if not en in result:
                    result[en] = []
                result[en].append(item)
        # cleanup of deleted keys from sub operation
        for name in delete_list:
            print "del", name, delete_list[name]
            # TODO: leave this in here or handle summing in rolne?
    return result


def type_aware_sum_sub(item_a, item_b, item_type=None):
    if type(item_a) is list:
        result = item_a
        if type(item_b) is list:
            result.extend(item_b)
        else:
            result.append(item_b)
    elif type(item_a) is dict:
        result = {}
        for key in item_a:
            if key in item_b:
                if type(item_a[key]) is list:
                    value = item_a[key] + item_b[key]
                else:
                    value = str(item_a[key])+str(item_b[key])
                result[key] = value
            else:
                result[key] = item_a[key] 
        #dict(item_a.items() + item_b.items())
    else:
        result = "fail"
    return result

def type_aware_sum_value(item_a, item_b, item_type=None):
    if item_a is None:
        if item_b is None:
            result = None
        else:
            result = item_b
    else:
        if item_b is None:
            result = item_a
        else:
            result = str(item_a)+str(item_b)
    return result


    
    
# eof: MARDS\mards_library.py
