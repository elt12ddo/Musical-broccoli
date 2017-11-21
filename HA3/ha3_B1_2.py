# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 18:43:12 2017

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
    


def find_v(commit,X):
    assertion = commit+1
    V_0 = False
    V_1 = False
    for k in range(65535+1):
        assertion = hash(0,k,X)
        if commit == assertion:
            V_0 = True
            if V_1:
                return True
        assertion = hash(1,k,X)
        if commit == assertion:
            V_1 = True
            if V_0:
                return True
    return False



start_time = time.time()
print(time.ctime(time.time()))
t=40
h=150
X = []
v = 1
other_v = 0
y = []
for i in range(1,t+1):
    X.append(i)
    prob = 0
    
    for j in range(h):
        k = random.randint(0,65535)#65535 = 2**16 -1
        commit = hash(v, k, i)
        temp = find_v(commit,i)
        if not temp:
            prob += 1
    y.append(prob/h)
    
plt.figure(1)
plt.plot(X,y,'ro')
plt.plot(X,y)
plt.xlabel('X values')
plt.ylabel('Probability')
plt.title('Probability of breaking the consealing property')
plt.show()
print("----- %s seconds -----" % (time.time() - start_time))
