# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 23:20:44 2017

@author: Daniel
"""

import struct
import hashlib

'''
.encode() used when dealing with strings
def sha1(str):  
    return hashlib.sha1(str.encode()).hexdigest()
'''

'''
param is a byte array
returns the sha1 hash as a hex string
'''
def sha1_H(array):  
    return hashlib.sha1(array).hexdigest()

'''
param is a byte array
returns the sha1 hash as a byte array
'''
def sha1_B(array):  
    return hashlib.sha1(array).digest()

'''
param is a integer
returns a byte array
'''
def bigEndian(nbr):
    return struct.pack('>I',nbr)

'''
param is a byte array
returns a hex string of the array
'''
def byteArrayToHexString(array):
    return array.hex()
#old    return "".join("%02x" % b for b in array)
    
'''
param is a hex string
returns a byte array
'''
def hexStringToByteArray(hexString):
    return bytearray.fromhex(hexString)

'''
param is a byte array
returns the integer interpretation
'''
def byteArrayToInteger(array):
    return int.from_bytes(array, byteorder='big', signed=False)




a = 2897
big = bigEndian(a)
hex_string = byteArrayToHexString(big)
sha = sha1_H(big)

hex_stuff = "0123456789abcdef"
hex_out = hexStringToByteArray(hex_stuff)
number = byteArrayToInteger(hex_out)
shaOf_hex_out = sha1_B(hex_out)
number2 = byteArrayToInteger(shaOf_hex_out)

print(big)
print(hex_string)
print(sha)
print(hex_out)#Unsure about this, seems to work but print is weird.
print(number)
print(number2)