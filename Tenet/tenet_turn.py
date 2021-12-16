from threading import Thread
from time import sleep, time
from Tenet.sock_turn import udpSocket
'''
####
Tenet_turn库，网络传输库，实现连入互联网的客户端经过服务器中转传输。
// 使用时可能需要关闭电脑的防火墙 //
####
'''
###### Tenet #####
class Tenet_turn:
    def __init__(self, server_addr=('127.0.0.1', 9084), group='A'):
        self.group = group
        self.server_addr=server_addr
        self.serve = True
        self.address = {}
        self.nodes = []
        self.lock = False
        pass

    ### 注册函数，向服务器发送信息并返回心跳地址  ###
    def sign(self, info={'id':None,'passward':None}, timeout=60):
        ###########
        info['group'] = self.group
        sign_sock = udpSocket(data_addr=self.server_addr)
        ### 计时，每5秒打印一次连接状况 ###
        last_time = time()
        start_time = time()
        name = str(self.group + '-00')
        while self.serve:
            sign_sock.send(info)
            data = sign_sock.recv()

            if type(data) == str:
                print(data)
                self.serve = False
                return False

            if type(data) == dict:
                data = data[name]
                data[0] = self.server_addr[0]
                self.address[name]=tuple(data)
                print('< mode: turn> connect to '+str(self.server_addr)+' success...')
                print('< mode: turn> node %c-00 addr: ' % self.group+str(self.address[name]))
                sign_sock.sock.close()
                return True
            ######### args: 打印当前连接状态
            if time() - last_time >= 4:
                print('< mode: turn> trying to connect to '+str(self.server_addr))
                last_time = time()

            if time() - start_time > timeout:
                print('< mode: turn> connect to '+str(self.server_addr)+' failed...')
                sign_sock.sock.close()
                self.serve = False
                return False
            sleep(0.2)
            pass
        pass

    def create_node(self, name):   # create a new data transfer node
        node = udpSocket(data_addr=(self.server_addr[0], 60080))
        node.name = name
        self.nodes.append(node)
        return node

    def delete_node(self,node):
        self.nodes.remove(node)
        del node
        pass

    def update(self):
        last_time = time()
        last_time_2 = time()
        update_sock = udpSocket(data_addr=self.address['%c-00' % self.group])
        send_data = ['%c-00' % self.group]
        for node in self.nodes:
            send_data.append(node.name)
            pass

        while self.serve:
            update_sock.send(send_data)
            sleep(0.08)
            data = update_sock.recv()
            if data != None:
                self.address = data
                print('get heart-address seccuss: ' + str(data))
                break
            pass

        send_data = ['%c-00' % self.group]
        while self.serve:
            if time()-last_time > 4:
                ##############
                if self.lock == True:
                    update_sock.send('lock')
                    pass
                if self.lock == False:
                    update_sock.send('unlock')
                    pass
                ##############
                for node in self.nodes:
                    send_data.append(node.name)
                    pass
                update_sock.send(send_data)
                send_data = ['%c-00' % self.group]
                last_time = time()
                pass
            data = update_sock.recv()
            if data == None:
                ############ 判断客户端同服务器是否掉线......
                if time() - last_time_2 >= 32:
                    self.serve = False
                    print('Lost connection with the server......')
                    break
                continue
            last_time_2 = time()
            self.address = data
        pass

    def maintain(self):  # 维护器，更新发送的地址信息给各个节点
        ############
        while self.serve:
            for node in self.nodes:
                try:
                    node.data_addr = (self.server_addr[0], self.address[node.name][1])
                    node.serve = True
                except Exception as e:
                    node.serve = False
                    pass
                node.heartbit()
                pass
            sleep(8)
            pass
        pass

    def run(self):
        if self.serve == False:
            return
        t1 = Thread(target=self.update)
        sleep(0.2)
        t2 = Thread(target=self.maintain)
        t1.start()
        t2.start()
        print('update node start success .....')
        print('maintain node start success .....')
        pass

    def __del__(self):
        self.serve = False
        try:
            for node in self.nodes:
                node.sock.close()
                pass
        except:
            pass
        del self.nodes