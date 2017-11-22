# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 14:28:43 2017

@author: David Cartbo
"""

def extra(f_list,j_list):
    total = 0
    for i in range(len(f_list)):
        total += f_list[i] * mult(j_list,j_list[i])
    print(total)

def mult(j_list,i):
    temp = 1
    for j in range(len(j_list)):
        if j_list[j] != i:
            temp *= j_list[j] / (j_list[j] - i)
    return temp

class poly():
    def __init__(self,k,x1,x2,x3,x4):
        self.k = k
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3
        self.x4 = x4
    def f(self,x):
        return self.k + self.x1*x + self.x2*(x**2) + self.x3*(x**3) + self.x4*(x**4)

def sums(polynomial,f1):
    a = sum(f1)
    a += polynomial.f(1)
    return a



p = poly(9,19,5,0,0)
k = 4
n = 6

f1 = [37,18,40,44,28]

j_list = [1,4,5]

f_list = [sums(p,f1),1385,2028]

extra(f_list,j_list)
