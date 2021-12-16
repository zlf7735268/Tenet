import socket
from threading import Thread
import json
from time import sleep

class mAddress:
    def __init__(self,ip='127.0.0.1',port=[3020,8060]):
        self.ip=ip
        self.address=list(range(port[0],port[1]))
        pass

    def get_addr(self,num):
        addr=[]
        for i in range(num):
            port=self.address[0]
            self.address.remove(port)
            addr.append((self.ip,port))
        return addr

    def add_addr(self,addr):
        port=addr[1]
        self.address.append(port)
        pass

class Address:
    def __init__(self,address):
        self.sock_addr=address
        self.serve=True
        t1=Thread(target=self.addr_sock)
        t1.start()
        self.addr=[]
        pass

    def addr_sock(self):
        addr_sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr_sock.bind(self.sock_addr)
        data = json.dumps('hello').encode('utf-8')
        while self.serve:
            _,address = addr_sock.recvfrom(64)
            addr_sock.sendto(data,address)
            sleep(0.01)
            if tuple(address) not in self.addr:
                self.addr.append(tuple(address))
                pass
            pass
        pass

    def get_addr(self,num):
        data = json.dumps('hello').encode('utf-8')
        for i in range(num):
            sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setblocking(0)
            while self.serve:
                sock.sendto(data,self.sock_addr)
                sleep(0.1)
                try:
                    data = sock.recv(1024)
                    if data != None:
                        sock.close()
                        break
                except:
                    pass
            pass
        addr=self.addr
        self.addr=[]
        return addr