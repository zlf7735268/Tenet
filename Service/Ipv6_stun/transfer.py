from Ipv6_stun.server import Service
import socket
from threading import Thread
import json
import time
from datetime import datetime

class Transfer:
    def __init__(self,address=('127.0.0.1',9080)):
        self.user_info ={}
        #self.user_info={'000000':{'passward':'sdlab123','service':None,'heart_addr':None}}
        self.serve=True
        self.address=address
        self.sock_addr=(address[0],9090)
        pass
    ### 开启心跳端口 ###
    def start_heart(self,id):
        sock=socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        data = json.dumps(id).encode('utf-8')
        while self.serve:
            sock.sendto(data,self.sock_addr)
            if 'heart_addr' in self.user_info[id]:
                sock.close()
                break
            pass
        self.user_info[id]['service']=Service(self.user_info[id]['heart_addr'])
        self.user_info[id]['service'].run()
        print('id:' + str(id) + ' service start success .....')
        pass

    ### 注册sock，用来确定分配给心跳端口的地址  ###
    def addr_sock(self):
        addr_sock=socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        addr_sock.bind(self.sock_addr)
        while self.serve:
            data, address = addr_sock.recvfrom(1024)
            id=json.loads(data.decode('utf-8'))
            if id in self.user_info:
                self.user_info[id]['heart_addr']=address
                pass
            pass
        pass

    ###  维护用户登录信息，将离线的用户id删除  ###
    def maintain(self):
        while self.serve:
            A = 1
            B = 1
            for id in list(self.user_info.keys()):
                try:
                    A = len(self.user_info[id]['service'].A)
                    B = len(self.user_info[id]['service'].B)
                except:
                    pass
                if A == 0 and B == 0:
                    t1=self.user_info[id]['service'].start_time
                    if time.time()-t1 >18:
                        try:
                            del self.user_info[id]
                            print('id:' + str(id) + ' service close success .....')
                        except:
                            pass
                    pass
                pass
            ############
            time.sleep(2)
            pass
        pass

    def print_info(self):
        while self.serve:
            now_time = datetime.now()
            str_time = now_time.strftime("%Y-%m-%d %X")
            print('time: '+str_time)
            print('user info: ' + str(self.user_info))
            time.sleep(20)
            pass
        pass

    def sign_service(self):
        sign_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        sign_sock.bind(self.address)
        while self.serve:
            try:
                data,address=sign_sock.recvfrom(1024)
            except:
                continue
            info=json.loads(data.decode('utf-8'))
            id=info['id']
            passward=info['passward']
            group=info['group']
            if id not in self.user_info:
                self.user_info[id]={}
                self.user_info[id]['passward']=passward
                self.start_heart(id)
                continue
            ### 如果密码对不上 ###
            if passward != self.user_info[id]['passward']:
                data = 'passward error,change id or input the correct passward....'
                data = json.dumps(data).encode('utf-8')
                sign_sock.sendto(data, address)
                continue
            heart_addr = self.user_info[id]['heart_addr']
            heart_addr = json.dumps(heart_addr).encode('utf-8')
            sign_sock.sendto(heart_addr, address)
        pass

    def run(self):
        t1 = Thread(target=self.addr_sock)
        print('addr_sock start success .....')
        time.sleep(0.2)
        t2 = Thread(target=self.sign_service)
        t3 = Thread(target=self.maintain)
        print('sign_service start success .....')
        t4 = Thread(target=self.print_info)
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        pass

    def __del__(self):
        pass
    pass