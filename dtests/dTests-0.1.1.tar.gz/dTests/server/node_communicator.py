import threading
import json

class NodeCommunicator:
    
    def __init__(self, server, node_id, address, socket):
        self.server = server
        self.address = address
        self.socket = socket
        self.node_id = node_id
        threading.Thread(target=self.run).start()

    def run(self):
        while True:
            output = self.socket.recv()
            if not output:
                self.server.unregister_node(self)
                break
            else: 
                output = json.loads(output)
                self.server.register_done(self, output)

    def run_job(self, job):
        self.socket.send(job)


    def get_address(self):
        return self.address
