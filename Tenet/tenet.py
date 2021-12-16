#-*-coding:utf-8-*-
from Tenet.tenet_stun import Tenet_stun
from Tenet.tenet_turn import Tenet_turn
from Tenet import config

class Tenet:
    def __init__(self, turn_addr=None, stun_addr=None, group='A', mode='ipv4'):
        self.turn_addr = turn_addr
        self.turn_addr = stun_addr

        if turn_addr == None and mode == 'ipv4':
            self.turn_addr=config.turn_ipv4
            pass
        if stun_addr == None and mode == 'ipv4':
            self.stun_addr=config.stun_ipv4
            pass
        if turn_addr == None and mode == 'ipv6':
            self.turn_addr=config.turn_ipv6
            pass
        if stun_addr == None and mode == 'ipv6':
            self.stun_addr=config.stun_ipv6
            pass

        self.turn = Tenet_turn(server_addr=self.turn_addr,group=group)
        self.stun = Tenet_stun(server_addr=self.stun_addr,group=group)
        self.tenet = None
        self.lock = False
        self.serve = True
        self.group = group
        pass

    def set_lock(self, value=False):
        try:
            self.tenet.lock = value
        except:
            return
        pass

    def address(self):
        addr = None
        try:
            addr = self.tenet.address
        except Exception as e:
            pass
        return addr

    def sign(self, info={'id':None,'passward':None}, timeout=12):
        info['group']=self.group
        flag = self.stun.sign(info=info,timeout=timeout)
        ##########
        if flag == True:
            self.tenet=self.stun
            return True
        ##########
        flag = self.turn.sign(info=info,timeout=timeout)
        self.tenet=self.turn
        if flag == False:
            self.serve = False
        return flag

    def create_node(self,name):
        node = self.tenet.create_node(name=name)
        return node

    def delete_node(self,node):
        self.tenet.delete_node(node=node)
        pass

    def run(self):
        if self.serve == True:
            self.tenet.run()
            pass
        pass

    def __del__(self):
        pass