
import json
import sys
from StringIO import StringIO
import time

import pandas as pd
import requests
from yhat import df_to_json

def log_to_user(status,msg):
    print json.dumps({"status":status,"msg":msg,"time":time.strftime("%Y:%m:%d %H:%M:%S",time.gmtime())})
    sys.stdout.flush()
    if status == "ERROR":
        sys.exit(2)

def make_pred(lines,header, response_header, endpoint, auth, out_file):
    csv_string = header + ''.join(lines)
    df = pd.read_csv(StringIO(csv_string))
    res = requests.post(endpoint,auth=auth,
                        data=df_to_json(df),
                        headers={'content-type':'application/json'})
    if res.status_code != 200:
        log_to_user("ERROR","Could not connect to model")
    result = res.json()
    if 'result' not in result:
        log_to_user("ERROR",result)
    df = pd.DataFrame(result['result'])
    s = StringIO()
    df.to_csv(s,index=False)
    s = s.getvalue().split('\n')
    if response_header is None:
        response_header = s[0]
        out_file.write(response_header + '\n')
    result_string = '\n'.join(s[1:])
    out_file.write(result_string) 
    return response_header


def score(in_filename, out_filename, username, apikey, endpoint):
    response_header = None
    auth=(username,apikey)
    try:
        num_lines = sum(1 for line in open(in_filename))

        in_file = open(in_filename)
        header = in_file.readline()
        
        out_file = open(out_filename,'w')
        log_to_user("UPDATE","0")       
 
        read_lines = []
        for i in xrange(num_lines - 2):
            read_lines.append(in_file.readline())
            if len(read_lines) >= 100:
                response_header = make_pred(read_lines,header,
                                            response_header,endpoint,
                                            auth,out_file)
                log_to_user("UPDATE","%.0f" % ((i / float(num_lines)) * 100))
                read_lines = []
        
        read_lines.extend(in_file.readlines())
        make_pred(read_lines,header,response_header,endpoint,auth,out_file)
        log_to_user("UPDATE","100")
        
    except Exception as e:
        log_to_user("ERROR",str(e))
    finally:
        in_file.close()
        out_file.close()
