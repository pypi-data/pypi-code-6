#!/usr/bin/env python

import threading
import dTests.utils.my_socket
import socket
import node_communicator
import json
import random

class Server:


    def __init__(self, nodes_port, jobs_port):
        self.nodes_port = nodes_port
        self.jobs_port = jobs_port
        self.nodes = []
        self.job_count = 0
        self.nodes_id = 0

    def listen_node(self):
        self.node_socket = dTests.utils.my_socket.MySocket()
        host = socket.gethostname()
        port = self.nodes_port
        self.node_socket.bind(host, port)
        self.node_socket.listen(5)
        print "Node listener started and listening on port %s" % port
        while True:
            client, address = self.node_socket.accept()
            print 'Node ', address , ' connected to the server'
            new_node = node_communicator.NodeCommunicator(self, self.nodes_id, address, client)
            self.nodes_id += 1
            self.nodes.append(new_node)
    
    def listen_job(self):
        self.job_socket = dTests.utils.my_socket.MySocket()
        host = socket.gethostname()
        port = self.jobs_port
        self.job_socket.bind(host,port)
        self.job_socket.listen(5)
        print "Job listener started and listening on port %s" % port
        while True:
            client, address = self.job_socket.accept()
            print 'New job is being initiated'
            if not len(self.nodes):
                print 'Job aborted, Not enough nodes'
                client.send("There must be at least one running node.")
                continue
            print 'The new job will run on %s nodes' % len(self.nodes)
            job_description = json.loads(client.recv())
            job_id = random.randrange(1000000000000,10000000000000000)
            print 'Job %s recieved : %s' % (job_id, json.dumps(job_description))
            self.job_count += 1
            node_job_description = {}
            node_job_description["job_id"] = job_id
            node_job_description["lang"] = job_description["lang"]
            node_job_description["source_file_name"] = job_description["source_file"]
            node_job_description["source_file"] = Server.read_code(job_description["source_file"])
            testcases_per_node = (len(job_description["testcases"]) + len(self.nodes) - 1 )/len(self.nodes)
            index = 0
            self.partial_outputs = []
            self.running_nodes = 0
            for node in self.nodes:
                tests = []
                for i in range(0,testcases_per_node):
                    if index < len(job_description["testcases"]):
                        tests.append(job_description["testcases"][index])
                        index += 1
                node_job_description["testcases"] = tests
                if tests:
                    node.run_job(json.dumps(node_job_description))
                    self.running_nodes += 1

            self.semaphore = threading.Semaphore(0)
            self.semaphore.acquire()
            self.finalize_output()
            client.send(self.output)
            client.close()
            print "Job %s is executed successfully with output %s" % (job_id, json.dumps(self.output))

    def start(self):
        node_listener = threading.Thread(target=self.listen_node)
        node_listener.daemon = True
        node_listener.start()
        self.listen_job()

    def register_done(self, node, output):
        self.partial_outputs += output
        print "Node %s finished its work and responded with %s" % (str(node.get_address()), str(output))
        self.running_nodes -= 1
        if not self.running_nodes:
            self.semaphore.release()
            
    def finalize_output(self):
        self.partial_outputs.sort()
        self.output = [ x[1] for x in self.partial_outputs ]
        self.output = "".join(self.output)
    
    def unregister_node(self, node):
        self.nodes = [ i for i in self.nodes if i.node_id != node.node_id ]
        print "Node %s disconnected" % str(node.get_address())

    @staticmethod
    def read_code(path):
        content = ''
        with open(path, 'r') as content_file:
            content = content_file.read()
        return content

    def close_sockets(self):
        self.node_socket.close()
        self.job_socket.close()

