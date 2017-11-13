# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 14:39:43 2017

@author: Daniel
"""



def DC(sa, sb, da, db, m, b):
    res = 0
    
    if b == 0:
        f = sa^sb
        s = f^da^db
        res = format(f,'04X')+format(s,'04X')
    if b == 1:
        res = format(sa^sb^m,'04X')
        
    print(res)





sa = int("0C73", 16)
sb = int("80C1", 16)
da = int("A2A9", 16)
db = int("92F5", 16)
m = int("9B57", 16)
b = 0


DC(sa, sb, da, db, m, b)



sa = int("27C2", 16)
sb = int("0879", 16)
da = int("35F6", 16)
db = int("1A4D", 16)
m = int("27BC", 16)
b = 1

DC(sa, sb, da, db, m, b)