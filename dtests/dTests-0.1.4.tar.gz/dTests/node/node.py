import dTests.utils.my_socket
import dTests.utils.utils
from dTests.utils.utils import compile_file, exec_file
import socket
import os
import json
import random

class Node:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        s = dTests.utils.my_socket.MySocket()
        s.connect(self.host, self.port)
        print "Connected to server %s:%s" % (self.host,self.port)
        while True:
            job = s.recv()
            if not job:
                print "Server Disconnected"
                break
            print "New job recieved : %s " % job
            job = json.loads(job)
            self.execute_job(job)
            output = self.finalize_output()
            s.send(output)
            print "Job executed successfully with output %s" % output

    def execute_job(self, job):
        working_directory = "/tmp/dTests/" + str(job["job_id"]) + "_" + str(random.randrange(0,1000))
        if not os.path.isdir("/tmp/dTests"):
            os.mkdir("/tmp/dTests")
        os.mkdir(working_directory)
        os.chdir(working_directory)
        
        code = job["source_file"]
        file_name = job["source_file_name"].split("/")[-1]
        f = open(file_name,'w')
        f.write(code)
        f.close()
        
        file_name = os.path.abspath(file_name)
        compile_file(file_name, job["lang"])

        self.outputs = []
        for testcase in job["testcases"]:
            testcase_output = exec_file(file_name, job["lang"], testcase[1])            
            self.outputs.append( [testcase[0], testcase_output] )
   
    def finalize_output(self):
        return json.dumps(self.outputs)

