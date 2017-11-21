# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:23:32 2017

@author: Daniel
"""

import hashlib
import random
import matplotlib.pyplot as plt
import time




def hash(v, k, X):
    k_bytes = k.to_bytes(2, 'big')
    v_bytes = v.to_bytes(1, 'big')
    temp = bytearray(v_bytes)
    temp.extend(bytearray(k_bytes))
    h = hashlib.sha1(temp).digest()
    h_int = int.from_bytes(h, 'big')
    #print(h_int)
    new_h = h_int & (2**X -1)
    #print(new_h)
    return new_h
    


def find_other_commit_prob(commit,v,X):
    i = 0
    assertion = commit+1
    while commit != assertion:
        k = random.randint(0,65535)
        assertion = hash(v, k, X)
        i += 1
    return 1/i



start_time = time.time()
t=20
h=150
X = []
v = 1
other_v = 0
y = []
for i in range(t):
    X.append(i)
    
    k = random.randint(0,65535)#65535 = 2**16 -1
    commit = hash(v, k, i)
    prob = 0
    for j in range(h):
        prob += find_other_commit_prob(commit,other_v,i)
    y.append(prob/h)
    

plt.plot(X,y)
print("----- %s seconds -----" % (time.time() - start_time))
    