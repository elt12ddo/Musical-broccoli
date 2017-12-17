# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 16:30:30 2017

@author: David Cartbo
"""
import math
import base64

#As described on Wikipedia
def invmod(a,n):
    t, t1 = 1, 0
    r, r1 = a, n
    while r1:
        q = r // r1
        t, t1 = t1, t - q * t1
        r, r1 = r1, r - q * r1
    if(r > 1):
        raise Exception('modular inverse does not exist')
    if(t < 0):
        t += n
    return t

def lcm(a,b):
    return abs(a*b)//math.gcd(a,b)

def DER_encode_INT(a):
    data = hex(a)[2:]
    
    #begin magic
    temp = bin(int(data[0],16))[2:].zfill(4)
    if temp[0] == '1':
        data = '00'+data
    #end magic

    if(len(data) % 2 == 1):
        data = '0' + data
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

def DER_encode_SEQ(p, q, e):
    n = p*q
    #lambda_n = lcm(p-1,q-1) # Apparantly the given values was longer than necessary
    lambda_n = (p-1)*(q-1)
    d = invmod(e,lambda_n)
    exponent1 = d % (p-1)
    exponent2 = d % (q-1)
    coefficient = invmod(q,p)
    
    string = DER_encode_INT(0) + DER_encode_INT(n) + DER_encode_INT(e) + DER_encode_INT(d) + DER_encode_INT(p) + DER_encode_INT(q) + DER_encode_INT(exponent1) + DER_encode_INT(exponent2) + DER_encode_INT(coefficient)
    string = '30' + getLengthString(len(string)//2) + string

    return base64.b64encode(bytearray.fromhex(string))

#print(DER_encode_SEQ(2530368937,2612592767,65537))
    
print(DER_encode_SEQ(139721121696950524826588106850589277149201407609721772094240512732263435522747938311240453050931930261483801083660740974606647762343797901776568952627044034430252415109426271529273025919247232149498325412099418785867055970264559033471714066901728022294156913563009971882292507967574638004022912842160046962763,141482624370070397331659016840167171669762175617573550670131965177212458081250216130985545188965601581445995499595853199665045326236858265192627970970480636850683227427420000655754305398076045013588894161738893242561531526805416653594689480170103763171879023351810966896841177322118521251310975456956247827719,65537))