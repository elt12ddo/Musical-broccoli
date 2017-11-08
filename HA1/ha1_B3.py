# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 13:06:39 2017

@author: Daniel
"""
import hashlib

def p1():
    file = open("B3_1.txt","r")
    a = file.read().splitlines()
    file.close()
    
    current = bytearray.fromhex(a[0])
    for i in range(1,len(a)):
        temp = a[i]
        array = bytearray.fromhex(temp[1:])
        if temp[0] == "R":
            current.extend(array)
            current = bytearray(hashlib.sha1(current).digest())
        else:
            array.extend(current)
            current = bytearray(hashlib.sha1(array).digest())
    
    print("Result:")
    print(current.hex())



def p2():
    file = open("B3_2.txt","r")
    i = int(file.readline()[:-1])
    j = int(file.readline()[:-1])
    a = file.read().splitlines()
    file.close()
    print(i)
    print(j)
    print(a)














p1()
print("*****P2*****")
p2()