# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 13:31:40 2017

@author: Daniel
"""

'''
Throw balls in bins, if we have k balls in bin make coin and do not make more
coins from that bin how many itr to get c coins?
'''

import random
import numpy
import time


start_time = time.time()
c = 10000
u = 20
k = 7
b = 2**u
n = 80
lam = 3.66

x_vals = [0]*n

for i in range(n):
    if i%10 ==0:
        print(i)
    bins = [0]*b
    gen_c = 0
    count = 0
    
    while True:
        count += 1
        assertion = random.randint(0,b-1)
        bins[assertion] += 1
        if bins[assertion] == k:
            gen_c +=1
        if gen_c == c:
            break

    x_vals[i] = count

x_mean = numpy.mean(x_vals)
s = numpy.std(x_vals)
high_val = x_mean + (lam*(s/n**(1/2)))
low_val = x_mean - (lam*(s/n**(1/2)))
diff = high_val - low_val

print("n: " + repr(n))
print("s: " + repr(s))
print ("mean: " + repr(x_mean))
print("**********Confidence interval**********")
print("Upper bound: " + repr(high_val))
print("Lower bound: " + repr(low_val))
print("diff: " + repr(diff))
print("----- %s seconds -----" % (time.time() - start_time))