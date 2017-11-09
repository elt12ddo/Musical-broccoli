# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 13:06:39 2017

@author: Daniel
"""
import hashlib
from math import log2, ceil

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



class Node:
    def __init__(self, left, right, h):
        self.left = left
        self.right = right
        self.h = h
    def p(self):
        if(self.left != None):
            self.left.p()
            self.right.p()
        print(self.h.hex())


def build(nodes):
    if len(nodes) == 1:
        #we are done
        return nodes
    else: 
        parents = []
        for i in range(0,len(nodes),2):
            left = nodes[i]
            if i == len(nodes)-1:
                nodes.append(nodes[-1])
            right = nodes[i+1]
            temp = bytearray(left.h) # Needed to get a copy so we do not extend left.h
            temp2 = right.h
            temp.extend(temp2)
            h = bytearray(hashlib.sha1(temp).digest())
            parents.append(Node(left, right, h))
        return build(parents)



def p2():
    file = open("B3_2.txt","r")
    i = int(file.readline()[:-1])
    j = int(file.readline()[:-1])
    a = file.read().splitlines()
    file.close()
    nodes = []
    leaf_at_i = a[i]
    for l in range(len(a)):
        nodes.append(Node(None, None, bytearray.fromhex(a[l])))
       # nodes[-1].p()
    
    
    root = build(nodes)
    
  #  print('***********************')
  #  print(root[0].p())
    
    depth = ceil(log2(len(a)))
    #middle = 2**(depth - 1)
    temp = root[0]
    print(i)
    low = 0
    high = 2**depth
    path = []
    for k in range(0, depth):
        #print((high+low)/2)
        if(i >= ((high+low)/2)):
            low = (high+low)/2
            #print(temp.left.h.hex())
            p = 'L' + temp.left.h.hex()
            temp = temp.right
            #go right
        else:
            high = (high+low)/2
            p = 'R' + temp.right.h.hex()
            temp = temp.left
            #go left
        path.insert(0, p)
    if(temp.h.hex() == leaf_at_i):
        print('We found the correct node')
    
    print("***********************************")
    print(root[0].h.hex())
    print("***********")
    print(path)
    print("***********")
    print(path[j][1:])
    print("***********")
    var = path[-j] + root[0].h.hex()
    print(var)



p1()
print("*****P2*****")
p2()