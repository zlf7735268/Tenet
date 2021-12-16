from Tenet.tenet import Tenet
import threading
import time

m=Tenet(turn_addr=None,stun_addr=None,group='A',mode='ipv4')
# 实例化对象，turn_addr为中转服务器注册地址
# stun_addr 为stun服务器注册地址
# Tenet库会优先使用stun模式连接,如果失败则切换为turn中转模式
# group 可以为 'A' 或 'B' ,对应着A或者B端
# 理论上A端节点与对应得B端节点进行数据传输

m.set_lock(False)
# 当set_lock为True时，服务器会一直保留此登录的接口和信息之类的
# 当set_lock为False时，服务器会定时检查A,B端在线情况，如果双方掉线超过一定时间，服务器将会删除相关信息

result=m.sign(info={'id':'123456','passward':'sclab123'},timeout=22)
# 登录函数，info为登录的信息，id为账号，最好为6位数字组成
# 拥有相同账号和密码的A,B端会被互相连接起来
# passward为密码，最好长度8位
# timeout 为超时时间，登录超过这个时间如果没有登录上将会自动返回False
# sign() 函数为阻塞模式，登录过程将会一直停留在此处

send1=m.create_node('A-009')
send1.encode='utf-8'
recv1=m.create_node('A-02')
# 创建节点，相同名称的 A,B端节点会互相连接起来
# A端节点名称 A-01 ~ A-99
# B端节点名称 B-01 ~ B-99
# node.recv() 接收函数为非阻塞模式，无数据返回 None
# node.send(data)
# 数据将会自动采用json打包成 'utf-8' 格式

m.run()
# 开始运行

def recv():
    while True:
        data = recv1.recv()
        if data != None:
            print('recv: '+str(data))
    pass

def send():
    while True:
        data = input('send: ')
        #data='whta is your wrong and my data is noat uasddddddddd'
        print(m.address())
        send1.send(data)
        # print(data)
        pass
    pass

if m.serve == True:
    t1=threading.Thread(target=recv)
    t2=threading.Thread(target=send)
    t1.start()
    t2.start()
    pass