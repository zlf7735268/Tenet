
class Address:
    def __init__(self,ip,port=[3020,8060]):
        self.address=list(range(port[0],port[1]))
        pass

    def get_addr(self):
        addr=self.address[0]
        self.address.remove(addr)
        return (ip,addr)

    def add_addr(self,addr):
        addr=addr[0]
        self.address.append(addr)
        pass