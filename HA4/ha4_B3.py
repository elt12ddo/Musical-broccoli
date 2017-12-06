# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 14:43:29 2017

@author: David Cartbo
"""

import hashlib
import math

def MGF1(mgfSeed, maskLen):
    hLen = 20
    if(maskLen > (2**32) * hLen):
        raise ValueError("mask too long")
    T = b''
    count_length = math.ceil(maskLen / hLen)
    for counter in range (0,count_length):
        C = I2OSP(counter, 4)
        temp =  bytes.fromhex(mgfSeed + C)
        T += hashlib.sha1(temp).digest()
    T = T.hex()
    return T[:(maskLen*2)] #maskLen 2 


def I2OSP(x, xLen):
    if(x >= 256**xLen):
        raise ValueError("integer too large")
    x = x.to_bytes(xLen, 'big')#This is basically
    return x.hex()

