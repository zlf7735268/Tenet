import socket
from threading import Thread
import time
import json

class Service:
    def __init__(self,heart_addr):
        self.recv_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.send_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.recv_sock.bind(heart_addr)
        #self.A = {'A-00':None}
        #self.B = {'B-00':None}
        self.A = {}
        self.B = {}
        self.serve=True
        self.heart_A = {}
        self.heart_B = {}
        self.start_time=time.time()
        pass

    '''
    #########
    维护器，用来删除掉线的节点
    可以更改检测心跳时间来判断是否掉线
    #########
    '''
    def monitor(self):
        #################
        while self.serve:
            time.sleep(0.01)
            for node in list(self.heart_A.keys()):
                if time.time()-self.heart_A[node] >14:
                    del self.heart_A[node]
                    del self.A[node]

            for node in list(self.heart_B.keys()):
                if time.time()-self.heart_B[node] >14:
                    del self.heart_B[node]
                    del self.B[node]
            pass
        pass

    def run(self):
        t1 = Thread(target=self.service_recv)
        t2 = Thread(target=self.service_send)
        time.sleep(2)
        t3 = Thread(target=self.monitor)
        t1.start()
        t2.start()
        t3.start()
        pass

    def service_recv(self):
        ############
        while self.serve:
            data,address=self.recv_sock.recvfrom(2048)
            data=json.loads(data.decode('utf-8'))

            if data[0] == 'A':
                self.A[data]=address
                self.heart_A[data] = time.time()

            if data[0] == 'B':
                self.B[data]=address
                self.heart_B[data] = time.time()
            pass
        pass

    def service_send(self):
        last_time=time.time()
        while self.serve:
            if time.time() - last_time < 5:
                continue
            last_time = time.time()
            try:
                data=json.dumps(self.B).encode('utf-8')
                self.send_sock.sendto(data,self.A['A-00'])
            except Exception as e:
                #print("error:", e)
                pass
            try:
                data = json.dumps(self.A).encode('utf-8')
                self.send_sock.sendto(data, self.B['B-00'])
            except Exception as e:
                #print("error:", e)
                pass
            pass
        pass

    def __del__(self):
        self.recv_sock.close()
        self.send_sock.close()
        del self.recv_sock
        del self.send_sock
        exit()