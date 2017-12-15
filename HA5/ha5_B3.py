# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 16:30:30 2017

@author: David Cartbo
"""
import sys
import math

def DER_encode(a):
    data = hex(a)[2:]
    
    #begin magic
    temp = bin(a)[2:]
    if temp[0] == '1':
        data = '00'+data
    #end magic

    if(len(data) % 2 == 1):
        data = '0' + data
    print("IT WILL NOT WORK FOR EVERYTHING")
    return '02' + getLengthString(len(data)//2) + data
    
def getLengthString(a):
    string = hex(a)[2:]
    if(len(string) % 2 == 1):
        string = '0' + string
    if(a <= 127): # Short form it is
        return string
    
    string = hex(a)[2:]
    if(len(string) % 2 == 1):
        string = '0' + string
    length = 128+(len(string)//2)
    return hex(length)[2:] + string

#The 2-complement is a bit off
#https://lapo.it/asn1js/#028180E6802D70D04DEA6724D9398116CBDAD4A7D824A6846432D8CAE83EA9BE7027F7BF80082FD9B6ED5A36656DC92E1141290C9437FEC219F981C255599849E1B65C64D4184A96F4C0AF287577997BE19CF500A7997F2E362A2EF263E75AF3BE6611DED3D18E5E9C02AAEE4484593017806531D9A9507C2241806E7CFA7298C9DBCD
#print(DER_encode(161863091426469985001358176493540241719547661391527305133576978132107887717901972545655469921112454527920502763568908799229786534949082469136818503316047702610019730504769581772016806386178260077157969035841180863069299401978140025225333279044855057641079117234814239380100022886557142183337228046784055073741))
print(DER_encode(13))