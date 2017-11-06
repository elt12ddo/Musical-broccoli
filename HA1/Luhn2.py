#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 15:45:58 2017

@author: david
"""

def find_x(s):
    k = len(s)-1
    total = 0
    even = False
    even_for_x = False
    while(k >= 0):#Or =<?
        character = s[k]
        if(character == 'X'):
            even_for_x = even
        else:
            digit = int(character)
            #print(digit)
            if(even):
                digit *= 2
                if(digit > 9):
                    digit -= 9
            total += digit
        even = not even
        k -= 1
    x = 0
    if((total % 10) != 0): #Otherwise x = 0
        if(even_for_x):
            if((total % 2) == 0): #Check if even
                x = (10 - (total % 10)) / 2
            else:
                x = ((10 - (total % 10)) + 9) / 2
        else:
            x = 10 - (total % 10)
    return int(x)

#find_x('12774212857X4109')
find_x('123456789X')
#We want 5 or just test with Luhn.py instead (checking is implemented)

file = open('numbers.txt')
out = 0
while(True):
    s = file.readline().rstrip('\n')
    if(s == ''):
        break
    out *= 10
    out += find_x(s)
print(out)
    