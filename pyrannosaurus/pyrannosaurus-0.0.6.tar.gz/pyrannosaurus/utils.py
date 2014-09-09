import base64
from datetime import datetime
from lxml import etree
import os
import zipfile

from pyrannosaurus.lib.metadata import Metadata
from pyrannosaurus.clients.apex import ApexClient 

NS = "http://soap.sforce.com/2006/04/metadata"
NS_FULL = "{http://soap.sforce.com/2006/04/metadata}"
NAMESPACES = {"sf": NS}
METADATA_TYPE = {'object': 'CustomObject'}
METADATA_DICTIONARY = {'objects' : 'Custom Object', 'triggers' : 'Apex Trigger', 'classes' : 'Apex Class'}

def package_to_dict(file_path):
    parser = etree.XMLParser(remove_blank_text=True)
    meta_types = {}
    pkg_manifest = etree.parse(file_path,parser)
    root = pkg_manifest.getroot()
    #loop through each type node in the package
    for item in root.xpath("sf:types",namespaces=NAMESPACES):
        #get the meta name and create it in  the new package if it doesn't exist, using asterisk wildcard
        meta_name = item.xpath("sf:name/text()", namespaces=NAMESPACES)[0]
        meta_types[meta_name] = []
        for mem in item.xpath("sf:members/text()", namespaces=NAMESPACES):
            meta_types[meta_name].append(mem)

    return meta_types

def zip(src):
    zf = zipfile.ZipFile("deploy.zip" , "w")
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname)
            zf.write(absname, arcname)
    zf.close()

def salesforce_datetime_format(dt):
    return dt.strftime("%Y-%m-%dT%H:%m:%SZ")

def convert_soap_datetime(dt):
    return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")

def set_debug_log(target_id, client=None, exp_dt=None,all_lvl=None, **kwargs):
    _valid_debug_levels = ['Debug']
    if client == None:
        #handle here by creating new client
        pass
    tf = client.create_object('TraceFlag')
    all_lvl = all_lvl if all_lvl else 'Debug'
    if all_lvl not in _valid_debug_levels:
        print "Provided debug level was not a valid option."
    else:
        tf.ApexCode = all_lvl
        tf.ApexProfiling = all_lvl
        tf.Callout = all_lvl
        tf.Database = all_lvl
        tf.Validation = all_lvl
        tf.System = all_lvl
        tf.Visualforce = all_lvl
        tf.Workflow = all_lvl
        if kwargs:
            for k, v in kwargs.iteritems():
                if k in tf.__keylist__:
                    tf.__setattr__(k, v)

        tf.TracedEntityId = target_id
        tf.ExpirationDate = salesforce_datetime_format(exp_dt)
        res = client.create(tf)

        return res

def binary_to_zip(zip_response):
    ''' Handle the SF Metadata API checkRetrieveStatus zip file response '''

    decoded_file = base64.b64decode(zip_response)
    zip_file = open('retrieve.zip', 'w')
    zip_file.write(decoded_file)
    zip_file.close()

def zip_to_binary(file_path):
    #TODO: make this absolute
    zip_file = open(file_path)
    zip_contents = zip_file.read()
    encoded_file = base64.b64encode(zip_contents)
    zip_file.close()
    return encoded_file

def get_object(file_name='Account.object'):
    parser = etree.XMLParser(remove_blank_text=True)
    x = etree.parse(file_name).getroot()
    primary_nodes = []
    name = file_name.split(".", 1)[0]
    obj_type = file_name.split(".", 1)[1]
    meta = Metadata(name=file_name, obj_type=obj_type)

    for node in x.getchildren():
        node_tag = node.tag.replace(NS_FULL,"")
        if node_tag not in primary_nodes:
            meta.add_child(node_tag)
            primary_nodes.append(node_tag)

    for node in primary_nodes:
        for child_node in x.xpath("sf:" + node, namespaces=NAMESPACES):
            if not child_node.getchildren():
                meta.add_property(child_node.tag.replace(NS_FULL, ""), child_node.text)
            else:
                cm = Metadata(name=child_node.tag.replace(NS_FULL, ""))
                for pr in child_node.getchildren():
                    if not pr.getchildren():
                        cm.add_property(pr.tag.replace(NS_FULL, ""), pr.text)
                    else:
                        name, sub_meta = get_child_node(pr)
                        cm.add_child(pr.tag.replace(NS_FULL, ""), value=sub_meta)

                (meta.__dict__[node]).append(cm)

    return meta

def get_child_node(node):
    sub_meta = []
    name = ""
    for pr in node.getchildren():
        name = pr.tag.replace(NS_FULL, "")
        sm = Metadata()
        has_children = False
        for check_children in pr.getchildren():
            if check_children.getchildren():
                has_children = True
                break

        if pr.getchildren() and has_children:
            r_name, r_meta = get_child_node(pr)
            sm.add_child(name, value=r_meta)
        elif pr.getchildren and not has_children:
            for sv in pr.getchildren():
                sm.add_property(sv.tag.replace(NS_FULL, ""), sv.text)
        else:
            sm.add_property(sv.tag.replace(NS_FULL, ""), sv.text)

        sub_meta.append(sm)

    return name, sub_meta

def meta_dir_to_type(type):
    return METADATA_DICTIONARY.get(type, None)

def array_to_soql_string(arr):
    try:
        #get the 0 index as a sample
        s = arr[0]
        #check if the array is strings, then keep the quotes
        if isinstance(s, str):
            return '(\'' + '\', \''.join(arr) + '\')'
        #otherwise create the string 'array' and remove the quotes
        else:
            print "string"
            soql_array = '(' + ', '.join(str(v) for v in arr) + ')'
            return soql_array
    except:
        print "array to soql string recieved an empty array"
        return arr

### useful set of functionality for unscheduling/rescheduling apex ###
### depends on the schedule apex name = class name ###################

class ScheduledJob:

    def __init__(self, name, cron_exp, id):
        self.name = name[0]
        self.cron_exp = cron_exp
        self.id = id

def unschedule_apex(un, pw, token):
    client = ApexClient()
    client.login(un, pw, token, is_production=False)
    scheduled_jobs = []
    
    cjds = client.query('SELECT Id,Name,JobType FROM CronJobDetail WHERE JobType = \'7\'')
    try:
        cjd_ids = []
        cjd_names = {}
        for cjd in cjds.records:
            cjd_ids.append(cjd.Id[0])
            cjd_names[cjd.Id[0]] = cjd.Name

        scheduled_jobs = []
        #TODO:make a array to string for soql utility
        cjd_ids_filter = array_to_soql_string(cjd_ids)
        print cjd_ids_filter
        cts = client.query("SELECT CronExpression,CronJobDetailId,Id FROM CronTrigger WHERE CronJobDetailId IN %s" % cjd_ids_filter)
        for ct in cts.records:
            scheduled_jobs.append(ScheduledJob(cjd_names.get(ct.CronJobDetailId[0]), ct.CronExpression[0], ct.Id[0]))

        apex_str = "system.abortjob('%s'); \n"
        exec_str = ''
        #TODO: refactor to single api exec anon call
        for sj in scheduled_jobs:
            exec_str = exec_str + apex_str  % sj.id

        client.execute_anonymous(exec_str)
    finally:
        return scheduled_jobs

def reschedule_apex(un, pw, token, scheduled_jobs):
    client = ApexClient()
    client.login(un, pw, token, is_production=False)
    apex_str = "%s x = new %s(); String cron_exp = '%s'; system.schedule('%s', cron_exp, x); \n"
    exec_str = ''
    for sj in scheduled_jobs:
        exec_str = exec_str + apex_str % (sj.name, sj.name, sj.cron_exp, sj.name)

    resp = client.execute_anonymous(exec_str)