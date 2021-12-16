from threading import Thread
from time import sleep, time
from Tenet.sock_stun import udpSocket
'''
####
Tenet库，网络传输库，实现连入互联网的客户端点对点传输。
// 使用时可能需要关闭电脑的防火墙 //
####
'''
###### Tenet #####
class Tenet_stun:
    def __init__(self, server_addr=('127.0.0.1', 9084), group='A'):
        self.group = group
        self.server_addr = server_addr
        self.serve = True
        self.address = None
        self.nodes = []
        self.lock = False
        pass

    ### 注册函数，向服务器发送信息并返回心跳地址  ###
    def sign(self, info={'id':None, 'passward':None}, timeout=60):
        ###########
        info['group'] = self.group
        sign_sock = udpSocket(data_addr=self.server_addr)
        ### 计时，每5秒打印一次连接状况 ###
        last_time = time()
        start_time = time()
        while self.serve:
            sign_sock.send(info)
            data = sign_sock.recv()

            if type(data) == str:
                print(data)
                continue

            if type(data) == list:
                data[0] = self.server_addr[0]
                self.heart_addr = tuple(data)
                print('< mode: stun> connect to '+str(self.server_addr)+' success...')
                print('< mode: stun> heart_addr: '+str(self.heart_addr))
                return True

            if time() - last_time >= 4:
                print('< mode: stun> trying to connect to '+str(self.server_addr))
                last_time=time()

            if time() - start_time > timeout:
                print('< mode: stun> connect to '+str(self.server_addr)+' failed...')
                sign_sock.sock.close()
                self.serve = False
                return False
            sleep(0.2)
            pass
        pass


    def create_node(self, name):   # create a new data transfer node
        node = udpSocket(heart_addr=self.heart_addr)
        node.name = name
        self.nodes.append(node)
        return node

    def delete_node(self, node):
        self.nodes.remove(node)
        del node
        pass

    def update(self):
        last_time = time()
        name = self.group + '-00'
        update_sock = udpSocket(heart_addr=self.heart_addr)
        update_sock.data_addr = self.heart_addr
        update_sock.name = name
        #####################
        while self.serve:
            update_sock.heartbit()
            data = update_sock.recv()
            sleep(0.2)
            if data != None:
                print('get address seccuss: '+str(data))
                self.address = data
                break
            pass
        ####################### 初次分配节点
        flag = 'A'
        if self.group == 'A':
            flag = 'B'
        if self.group == 'B':
            flag = 'A'

        for node in self.nodes:
            name = node.name
            name = name.replace(name[0], flag)
            try:
                node.data_addr = self.address[name]
                node.serve = True
                # print('node_name：' + node.name + ' data_addr: ' + str(node.data_addr))
            except Exception as e:
                node.serve = False
                #print('address update error')
                pass
        ######################初次分配节点
        while self.serve:
            if time() - last_time >= 4:
                update_sock.heartbit()
                last_time = time()
                ########
                if self.lock == True:
                    update_sock.send('lock')
                    pass
                if self.lock == False:
                    update_sock.send('unlock')
                    pass
                pass

            data = update_sock.recv()
            if data == None:
                continue
            self.address = data
        pass

    def maintain(self):  # 维护器,更新发送的地址信息给各个节点
        flag = 'A'
        if self.group == 'A':
            flag = 'B'
        if self.group == 'B':
            flag = 'A'
        for node in self.nodes:
            node.heartbit()
            pass
        ############
        while self.serve:
            sleep(32)
            for node in self.nodes:
                name = node.name
                name = name.replace(name[0], flag)
                try:
                    node.data_addr = self.address[name]
                    node.serve = True
                    #print('node_name：' + node.name + ' data_addr: ' + str(node.data_addr))
                except Exception as e:
                    node.serve = False
                    #print('address update error')
                    pass
                node.heartbit()
                pass
            pass
        pass

    def run(self):
        if self.serve == False:
            return
        t1 = Thread(target=self.update)
        print('update node start success .....')
        sleep(0.2)
        t2 = Thread(target=self.maintain)
        print('maintain node start success .....')
        t1.start()
        t2.start()
        pass

    def __del__(self):
        self.serve = False
        try:
            for node in self.nodes:
                node.sock.close()
                pass
        except:
            pass
        pass
