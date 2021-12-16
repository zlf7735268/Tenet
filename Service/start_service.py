from Ipv4_stun.transfer import Transfer as ipv4_stun
from Ipv4_turn.transfer import Transfer as ipv4_turn
from Ipv6_stun.transfer import Transfer as ipv6_stun
from Ipv6_turn.transfer import Transfer as ipv6_turn


#m=Transfer(address=('172.16.0.156',9080))
m1 = ipv4_stun(address=('127.0.0.1', 82))
m1.run()

m2 = ipv4_turn(address=('127.0.0.1', 84))
m2.run()

m3 = ipv6_stun(address=('::', 86))
m3.run()

m4 = ipv6_turn(address=('::', 88))
m4.run()