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

def OAEP_ENCODE(M, seed, L=''):
    hLen = 20
    k = 128
    L = bytes.fromhex(L)
    mLen = len(M)//2
    lLen =len(L)
    
    
    if(lLen >= 2**61): # If L is in bytes format and I replaced -1 with >= 
        raise ValueError("label too long")
    if(mLen >  k - (2*hLen) - 2):
        raise ValueError("message too long")
    lHash = hashlib.sha1(L).hexdigest()
    
    PS = '00' * (k - mLen - 2 * hLen - 2)
    
    DB = lHash + PS + '01' + M
    
    dbMask = MGF1(seed, k - hLen - 1)
    
    maskedDB = XOR(DB,dbMask)
    
    seedMask = MGF1(maskedDB, hLen)
    
    maskedSeed = XOR(seed, seedMask)
    
    EM = '00' + maskedSeed + maskedDB
    return EM

def OAEP_DECODE(EM, L=''):
    hLen = 20
    k = 128
    Y = EM[:2]
    if(Y != '00'):
        raise ValueError("decryption error")
    L = bytes.fromhex(L)
    lHash = hashlib.sha1(L).hexdigest()
    maskedSeed = EM[2:(hLen*2)+2]
    maskedDB = EM[(hLen*2)+2:]
    
    seedMask = MGF1(maskedDB, hLen)
    seed = XOR2(maskedSeed, seedMask)
    
    dbMask = MGF1(seed, k - hLen - 1)
    DB = XOR(maskedDB, dbMask)
    lHash2 = DB[:hLen*2] # *2 as hLen is for bytes not hex digits
    
    if(lHash != lHash2):
        raise ValueError("decryption error")
    temp = DB[hLen*2:]
    #kolla hexsiffor par tills vi får 01
    byte = temp[:2]
    t = 0
    while(byte == '00' and t < len(temp)):
        t += 2
        byte = temp[t:t+2]
    if(temp[t:t+2] != '01'):
        print
        raise ValueError("decryption error")
    M = temp[t+2:]
    return M

def XOR(a,b): # a.k.a. the nightmare code remover
    return hex(int(a,16)^int(b,16))[2:].zfill(max(len(a),len(b)))

def XOR2(a,b): # Now without zfill, because MGF1 in decode do NOT like leading zeroes apparantly
    return hex(int(a,16)^int(b,16))[2:]

M = 'fd5507e917ecbe833878'
seed = '1e652ec152d0bfcd65190ffc604c0933d0423381'

M2 = 'c107782954829b34dc531c14b40e9ea482578f988b719497aa0687'
seed2 = '1e652ec152d0bfcd65190ffc604c0933d0423381'
EM2 = '0063b462be5e84d382c86eb6725f70e59cd12c0060f9d3778a18b7aa067f90b2178406fa1e1bf77f03f86629dd5607d11b9961707736c2d16e7c668b367890bc6ef1745396404ba7832b1cdfb0388ef601947fc0aff1fd2dcd279dabde9b10bfc51efc06d40d25f96bd0f4c5d88f32c7d33dbc20f8a528b77f0c16a7b4dcdd8f'

print(OAEP_DECODE(OAEP_ENCODE(M,seed)))
print(OAEP_DECODE(OAEP_ENCODE('aa','aa')))

print(OAEP_DECODE(OAEP_ENCODE(M2,seed2)))

print(OAEP_ENCODE(M2,seed2))
print(OAEP_DECODE(EM2))