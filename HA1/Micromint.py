# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 15:22:42 2017

@author: David Cartbo
"""

import array
import random
import numpy
import time

def MicroMint(u, k, c):
    u = (2**u)
    a = array.array('i',(0 for i in range(0,u)))
    t = 0
    while(c > 0):
        n = random.randrange(u)
        a[n] += 1
        if(a[n] == k):
            c -= 1
        t += 1
    return t

def MicroMint2(c, u, k, width):
    start_time = time.time()
    results = []
    for y in range(0,10): # Make sure we have a decent amount of data to be confident that std is not 0 (and it saves a few cycles in most cases too as there is no evalution here)
        results.append(MicroMint(u, k, c))
    while((7.32 * numpy.std(results) / (len(results)**0.5)) > width): # As we only need the width of the intervall we do not use the average which is in the formula. As the start/end point of the intervall is equal distance from the average value it, one simply needs to multiply with 2 (3.66*2=7.32) to get the width. 
        results.append(MicroMint(u, k, c))
    print("----- width: %s -----" % (7.32 * numpy.std(results) / (len(results)**0.5)))
    print("----- %s seconds -----" % (time.time() - start_time))
    return numpy.mean(results)