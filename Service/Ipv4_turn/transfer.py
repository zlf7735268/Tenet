from Ipv4_turn.server import Service
import socket
from threading import Thread
import json
import time
from datetime import datetime
from Ipv4_turn.addr import Address

class Transfer:
    def __init__(self, address=('127.0.0.1', 9080)):
        self.user_info = {}
        #self.user_info={'000000':{'passward':'sdlab123','service':None,'heart_addr':None}}
        self.serve = True
        self.address = address
        self.sock_addr = (address[0], 102)
        pass

    ###  维护用户登录信息，将离线的用户id删除  ###
    def maintain(self):
        while self.serve:
            time.sleep(5)
            for id in list(self.user_info.keys()):
                try:
                    if self.user_info[id]['service'].serve == False:
                        del self.user_info[id]
                        print('id: '+str(id)+' close success...')
                        pass
                except Exception as e:
                    #print(t)
                    pass
                pass
        pass

    def print_info(self):
        while self.serve:
            now_time = datetime.now()
            str_time = now_time.strftime("%Y-%m-%d %X")
            print(' ')
            print('time: '+str_time)
            print('user info: ' + str(self.user_info))
            time.sleep(20)
            pass
        pass

    def sign_service(self):
        get_addr = Address((self.address[0], 104))
        sign_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sign_sock.bind(self.address)
        while self.serve:
            try:
                data, address = sign_sock.recvfrom(1024)
            except Exception as e:
                continue
            info = json.loads(data.decode('utf-8'))
            ###################
            if type(info) != dict:
                continue

            id = info['id']
            passward = info['passward']
            if id not in self.user_info:
                self.user_info[id] = {}
                self.user_info[id]['passward'] = passward
                addr = get_addr.get_addr(2)
                self.user_info[id]['port'] = {'A-00': addr[0], 'B-00': addr[1]}
                self.user_info[id]['service'] = Service(self.user_info[id]['port'],get_addr=get_addr)
                print('id: '+str(id)+' service start success...')
                self.user_info[id]['service'].run()
                continue

            ### 如果密码对不上 ###
            if passward != self.user_info[id]['passward']:
                data = 'passward error,change id or input the correct passward....'
                data = json.dumps(data).encode('utf-8')
                sign_sock.sendto(data, address)
                continue

            result = self.user_info[id]['port']
            result = json.dumps(result).encode('utf-8')
            sign_sock.sendto(result, address)
        pass

    def run(self):
        time.sleep(0.2)
        t1 = Thread(target=self.sign_service)
        t2 = Thread(target=self.maintain)
        print('sign_service start success .....')
        print('maintain node start success .....')
        t3 = Thread(target=self.print_info)
        t1.start()
        t2.start()
        t3.start()
        pass

    def __del__(self):
        pass
    pass