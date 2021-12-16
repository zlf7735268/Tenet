from Tenet.tenet import Tenet
import threading
import time

m=Tenet(turn_addr=None,stun_addr=None,group='B',mode='ipv4')
# 实例化对象，server为服务器地址
# group 可以为 'A' 或 'B' ,对应着A或者B端
m.set_lock(False)
# 当set_lock为True时，服务器会一直保留此登录得接口和信息之类的
# 当set_lock为False时，服务器会定时检查A,B端在线情况，如果双方掉线超过一定时间，服务器将会删除相关信息

#m=Tenet(server=('0:0:0:0:0:0:0:1',9082),group='A')
#m=Tenet(server=('127.0.0.1',9080),group='A')
result=m.sign(info={'id':'123456','passward':'sclab123'},timeout=12)
# 登录函数，info为登录的信息，id为账号，最好为6位数字组成
# passward为密码，最好长度与上面长度相同
# timeout 为超时时间，登录超过这个时间如果没有登录上将会自动返回False

recv1=m.create_node('B-009')
send1=m.create_node('B-02')
# 创建节点，每个节点A端和B端相互对应
# send1.recv()
# send1.send(data)
# recv1.send(data)
# recv1.recv()

m.run()

def recv():
    while True:
        data = recv1.recv()
        if data != None:
            print('recv: '+str(data))
    pass

def send():
    while True:
        data = input('send: ')
        print(m.address())
        send1.send(data)
    pass

if m.serve == True:
    t1=threading.Thread(target=recv)
    t2=threading.Thread(target=send)
    t1.start()
    t2.start()
    pass