import socket,struct,sys,time

class MySocket:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket()
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        else:
            self.sock = sock

    def bind(self,host, port):
        config = (host, port)
        self.sock.bind(config)

    def send(self, data):
        self.sock.sendall(struct.pack('>Q', len(data))+data)
    
    # From : http://code.activestate.com/recipes/408859-socketrecv-three-ways-to-turn-it-into-recvall/
    def recv(self):
        #data length is packed into 8 bytes
        total_len=0
        total_data=[]
        size=sys.maxint
        body_started = False
        size_data = sock_data = '';
        recv_size=8192
        while total_len<size:
            sock_data = self.sock.recv(recv_size)
            if not sock_data:
                return ''
            if not body_started:
                if len(sock_data)>8:
                    size_data+=sock_data
                    size=struct.unpack('>Q', size_data[:8])[0]
                    recv_size=size
                    if recv_size>524288:recv_size=524288
                    total_data.append(size_data[8:])
                    body_started = True
                else:
                    size_data+=sock_data
            else:
                total_data.append(sock_data)
            total_len=sum([len(i) for i in total_data ])
        return ''.join(total_data)
    
    def accept(self):
        client, address = self.sock.accept()
        return (MySocket(client), address)

    def connect(self, host, port):
        config = (host, port)
        self.sock.connect(config)
    
    def listen(self, num):
        self.sock.listen(num)
    def close(self):
        self.sock.close()

