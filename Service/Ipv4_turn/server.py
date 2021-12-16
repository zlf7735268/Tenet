import socket
from threading import Thread
import time
import json

class Node:
    def __init__(self, A_addr, B_addr):
        self.a_sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.b_sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.a_sock.bind(A_addr)
        self.b_sock.bind(B_addr)
        self.a_sock.setblocking(False)
        self.b_sock.setblocking(False)
        self.serve = True
        self.a_addr = None
        self.b_addr = None
        pass

    def A_service(self):
        while self.serve:
            time.sleep(0.01)
            try:
                data, addr = self.a_sock.recvfrom(1024)
            except Exception as e:
                continue
            ############
            if data == b'"heart"':
                self.a_addr=addr
                continue
            try:
                self.b_sock.sendto(data, self.b_addr)
            except Exception as e:
                continue
            pass

    def B_service(self):
        while self.serve:
            time.sleep(0.01)
            try:
                data, addr = self.b_sock.recvfrom(1024)
            except:
                continue

            if data == b'"heart"':
                self.b_addr = addr
                continue
            try:
                self.a_sock.sendto(data, self.a_addr)
            except Exception as e:
                continue

    def run(self):
        t1 = Thread(target=self.A_service)
        t2 = Thread(target=self.B_service)
        t1.start()
        t2.start()
        pass

    def __del__(self):
        self.serve = False
        self.a_sock.close()
        self.b_sock.close()
        exit()
        pass

class Service:
    def __init__(self, port, get_addr):
        self.A_addr = port['A-00']
        self.B_addr = port['B-00']
        self.serve = True
        self.start_time = time.time()
        self.nodes = {}
        self.A = ['A-00']
        self.B = ['B-00']
        self.A_return = {'A-00': self.A_addr}
        self.B_return = {'B-00': self.B_addr}
        self.get_addr = get_addr
        self.lock = False
        self.A_live = True
        self.B_live = True
        self.A_last_time = time.time()
        self.B_last_time = time.time()
        pass

    def keeper(self):
        ##########
        while self.serve:
            if time.time()-self.A_last_time >= 20:
                self.A_live = False
            if time.time()-self.B_last_time >= 20:
                self.B_live = False
            if self.B_live == False and self.A_live == False and self.lock == False:
                self.serve = False
                pass
            pass
            time.sleep(4)
        pass

    def A_master(self):
        ############
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(self.A_addr)
        last_time = time.time()
        self.A_last_time = time.time()
        while self.serve:
            data,address=sock.recvfrom(1024)
            data = json.loads(data.decode('utf-8'))
            self.A_last_time = time.time()
            ##############
            if data == 'lock':
                self.lock = True
            if data == 'unlock':
                self.lock = False

            if type(data) == list:
                self.A = data

            if time.time()-last_time > 3:
                #print('a_return'+str(self.A_return))
                send_data = json.dumps(self.A_return).encode('utf-8')
                sock.sendto(send_data, address)
                last_time = time.time()
            pass
        pass

    def B_master(self):
        ############
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(self.B_addr)
        last_time = time.time()
        self.B_last_time = time.time()
        while self.serve:
            data, address = sock.recvfrom(1024)
            data = json.loads(data.decode('utf-8'))
            self.B_last_time = time.time()
            #############
            if data == 'lock':
                self.lock=True
            if data == 'unlock':
                self.lock=False

            if type(data) == list:
                self.B = data
            if time.time() - last_time > 4:
                send_data = json.dumps(self.B_return).encode('utf-8')
                sock.sendto(send_data, address)
                last_time = time.time()
            pass
        pass

    def monotir(self):
        #######
        while self.serve:
            ##############
            for a in self.A:
                b = a.replace('A','B')
                node_name = str(a[1:])
                if a == 'A-00':
                    continue

                if b not in self.B:
                    try:
                        del self.nodes[node_name]
                        continue
                    except Exception as e:
                        continue
                ###############
                if node_name in self.nodes:
                    continue
                addr = self.get_addr.get_addr(2)
                self.A_return[a] = addr[0]
                self.B_return[b] = addr[1]
                self.nodes[node_name] = Node(addr[0], addr[1])
                self.nodes[node_name].run()
            pass
            time.sleep(0.01)
        pass

    def run(self):
        t1 = Thread(target=self.A_master)
        t2 = Thread(target=self.B_master)
        t3 = Thread(target=self.monotir)
        t4 = Thread(target=self.keeper)
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        pass

    def __del__(self):
        print('del service')
        self.serve = False
        for node in list(self.nodes.keys()):
            del self.nodes[node]
            pass
        del self.A
        del self.B
        del self.A_return
        del self.B_return