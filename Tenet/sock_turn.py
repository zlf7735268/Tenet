import socket
import json
'''
####
udp socket
####
'''
class udpSocket:
    def __init__(self, data_addr=None, buffsize=1024):
        #####################
        if data_addr != None:
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            if '.' in data_addr[0]:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            pass
        ####################
        self.heart_data = 'heart'
        self.data_addr = data_addr
        self.heart_addr = None
        self.buffsize = buffsize
        self.name = None
        self.sock.setblocking(False)
        self.serve = True
        self.encode = 'utf-8'
        pass

    def send(self, data):
        try:
            data = json.dumps(data).encode(self.encode)
            self.sock.sendto(data, self.data_addr)
        except Exception as e:
            #print(e)
            return

    def recv(self):
        try:
            data, _ = self.sock.recvfrom(self.buffsize)
            data=json.loads(data.decode(self.encode))
        except Exception as e:
            #print(e)
            return None
        return data

    def r_send(self, data):
        try:
            self.sock.sendto(data, self.data_addr)
        except Exception as e:
            #print(e)
            return

    def r_recv(self):
        try:
            data, _ = self.sock.recvfrom(self.buffsize)
        except Exception as e:
            #print(e)
            return None
        return data

    def heartbit(self):
        data = json.dumps(self.heart_data).encode(self.encode)
        self.sock.sendto(data, self.data_addr)
        pass

    def __del__(self):
        self.sock.close()
        self.serve = False