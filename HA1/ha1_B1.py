# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 10:57:29 2017

@author: Daniel
"""

def findDigit(str):
    sum = 0
    mult = 1
    factor = 0
    for i in reversed(range(len(str))):
        if str[i] == "X":
            factor=mult
        if str[i] != "X":
            temp = int(str[i])*mult
            if temp > 9:
                temp = temp - 9
            sum = sum + temp
        mult = mult%2 + 1
    temp = sum
    for j in range(0,10):
        term = j*factor
        if term > 9:
            term= term - 9
        temp = temp + term
        if temp%10 == 0:
           return j
        temp = sum
            
        

file = open("B1.txt","r")
a = file.read().splitlines()
file.close()
print("Numbers:")
for i in range(len(a)):
    print(a[i])
print("****************")
print("Missing digits:")
for i in range(len(a)):
    print(findDigit(a[i]), end="")
