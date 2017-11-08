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



class Node:
    def __init__(self, left, right, h):
        self.left = left
        self.right = right
        self.h = h


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
            temp = left.h
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
    for i in range(len(a)):
        nodes.append(Node(None, None, bytearray.fromhex(a[i])))
    
    root = build(nodes)
    print(root[0].h.hex())
    




p1()
print("*****P2*****")
p2()