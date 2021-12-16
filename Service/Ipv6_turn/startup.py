from Ipv6_turn.transfer import Transfer

m=Transfer(address=('0:0:0:0:0:0:0:1',9082))
#m=Transfer(address=('127.0.0.1',9080))
m.run()