# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 14:45:43 2017

@author: Daniel
"""

import hashlib

# As given
def jacobi (a, m):
    j = 1
    a %= m
    while a:
        t = 0
        while not a & 1:
            a = a >> 1
            t += 1
        if t&1 and m%8 in (3, 5):
            j = -j
        if (a % 4 == m % 4 == 3):
            j = -j
        a, m = m % a, a
    return j if m == 1 else 0



p = '9240633d434a8b71a013b5b00513323f'
q = 'f870cfcd47e6d5a0598fc1eb7e999d1b'


M = int(p,16)*int(q,16)

identity = 'walterwhite@crypto.sec'

enc = ['2f2aa07cfb07c64be95586cfc394ebf26c2f383f90ce1d494dde9b2a3728ae9b',
'63ed324439c0f6b823d4828982a1bbe5c34e66d985f55792028acd2e207daa4f',
'85bb7964196bf6cce070a5e8f30bc822018a7ad70690b97814374c54fddf8e4b',
'30fbcc37643cc433d42581f784e3a0648c91c9f46b5671b71f8cc65d2737da5c',
'5a732f73fb288d2c90f537a831c18250af720071b6a7fac88a5de32b0df67c53',
'504d6be8542e546dfbd78a7ac470fab7f35ea98f2aff42c890f6146ae4fe11d6',
'10956aff2a90c54001e85be12cb2fa07c0029c608a51c4c804300b70a47c33bf',
'461aa66ef153649d69b9e2c699418a7f8f75af3f3172dbc175311d57aeb0fd12']

a_0 = bytes(identity,'utf8')
a = hashlib.sha1(a_0).digest()
a = int.from_bytes(a,byteorder='big')
while jacobi(a,M) != 1:
    a = a.to_bytes((a.bit_length()+7)//8,'big')
    a = hashlib.sha1(a).digest()
    a = int.from_bytes(a,byteorder='big')


exp = (M+5-(int(p,16)+int(q,16)))//8
r = pow(a,exp,M)
print(hex(r))

x = ['']*len(enc)
for i in range(len(enc)):
    x[i] = jacobi(int(enc[i],16)+2*r,M)


bits = '0b'
for i in range(len(x)):
    if x[i] == 1:
        bits += '1'
    else:
        bits += '0'
print(int(bits,2))



