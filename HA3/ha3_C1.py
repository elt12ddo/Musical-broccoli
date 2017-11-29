# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 15:45:45 2017

@author: Daniel
"""

import math



def L(x,n):
    return (x-1)/n
def lcm(a,b):
    return abs(a*b)//math.gcd(a,b)


#As described on Wikipedia
def invmod(a,n):
    t, t1 = 1, 0 
    r, r1 = a, n 
    while r1: 
        q = r // r1 
        t, t1 = t1, t - q * t1 
        r, r1 = r1, r - q * r1 
    return t 


p = 1117
q = 1471
n = p*q
n2 = n**2
g = 652534095028
file = open("C1.txt","r")
a = file.read().splitlines()
file.close()
prod = 1
for i in range(len(a)):
    prod *= int(a[i])
    prod %= n2
print(prod)

lam = lcm(p-1,q-1)
mu = invmod(L(pow(g,lam,n2),n),n)

plain = int(L(pow(prod,lam,n2),n) * mu % n)
if plain > len(a):
    plain = plain - n
print(plain)