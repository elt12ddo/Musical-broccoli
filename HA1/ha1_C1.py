# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:04:25 2017

@author: David Cartbo
"""
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import secrets
import hashlib
import random


def test():
    b = Bank()
    id = 123456
    alice = User(b,id)
    k = 100
    S = alice.generate_coins(k)
    vector = []
    for i in range(k):
        vector.append(random.randint(0,1))
    list = alice.verify(vector)
    f = 1
    for j in range(k):
        if vector[j] == 1:
            temp = hash_two_inputs(list[j][1],list[j][2])
            f *= hash_two_inputs(temp, list[j][0])
            f %= b.get_n()
        else:
            temp = hash_two_inputs(list[j][1],list[j][2])
            f *= hash_two_inputs(list[j][0],temp)
            f %= b.get_n()
    sign_pow_e = pow(S, b.get_e(), b.get_n())
    print("Bobs calculated signature:")
    print(f)
    print("The sign provided by Alice to the power of the banks public exponent:")
    print(sign_pow_e)
    if f == sign_pow_e:
        print("Success")
    else:
        print("Error")
    
    #Now check double spending
    print("**********")
    print("Check double spending")
    vector2 = vector
    if vector2[0] == 1:
        vector2[0] = 0
    else:
        vector2[0] = 1
    list2 = alice.verify(vector2)
    alice_id = list2[0][1]^list[0][1]
    print("Alice id:")
    print(id)
    print("Calculated id:")
    print(alice_id)
    if id == alice_id:
        print("Success")
    else:
        print("Error")
    
    
    
#As described on Wikipedia
def invmod(a,n):
    t, t1 = 1, 0 
    r, r1 = a, n 
    while r1: 
        q = r // r1 
        t, t1 = t1, t - q * t1 
        r, r1 = r1, r - q * r1 
    return t 


'''
Class representing the bank with methods for doing a coin generation
'''
class Bank:
    def __init__(self):
        self.generate_keys()
        
    def generate_keys(self):
        self.key = rsa.generate_private_key(public_exponent=65537,key_size=2048,backend=default_backend())
        
    def fetch_indices(self,b):
        self.b = b
        self.indices = []
        while(len(self.indices) < len(b)/2):
            k = secrets.randbelow(len(b))
            if(k not in self.indices):
                self.indices.append(k)
                
        return self.indices
    
    def check(self,quads,identity):
        sign = 1
        for i in range(len(quads)):
            if(self.B(quads[i],identity) != self.b[self.indices[i]]):
                return None
            
        for k in range(len(self.b)):
            if(k not in self.indices):
                sign *= pow(self.b[k],self.key.private_numbers().d,self.get_n()) 
        return sign
            
    def B(self,quad,identity):
        p = pow(quad.r,self.get_e(),self.get_n())
        return (p*hash_two_inputs(quad.x(),quad.y(identity))) % self.get_n()
    
    def get_e(self):
        return self.key.private_numbers().public_numbers.e
    
    def get_n(self):
        return self.key.private_numbers().public_numbers.n

'''
Class simulating a user, includes methods for generating coins and verify them.
'''
class User:
    def __init__(self, bank, identity):
        self.bank = bank
        self.identity = identity
        self.n = bank.get_n()
        self.e = bank.get_e()
        
    def generate_coins(self,k):
        quads = self.generate_quads(k)
        b_list = []
        
        for i in range(len(quads)):
            b_list.append(self.B(quads[i]))
            
        #Time to get indices from the bank
        indices = self.bank.fetch_indices(b_list)
        bank_quads = []
        
        for k in range(len(indices)):
            l = indices[k]
            bank_quads.append(quads[l])
        
        #send requested quads to bank
        sign = self.bank.check(bank_quads,self.identity)
        prod_ri = 1
        self.sign_quads = []
        for i in range(len(quads)):
            if i not in indices:
                prod_ri *= quads[i].r
                self.sign_quads.append(quads[i])
        self.S = sign * invmod(prod_ri,self.n) % self.n
        
        print("This is the signature S:")
        print(self.S)
        return self.S
        
    def generate_quads(self,k):
        n = self.n
        quads = []
        for i in range(2*k):
            a = secrets.randbelow(n) # No modulo needed as it will be below n as it will be in range [0,n)
            c = secrets.randbelow(n)
            d = secrets.randbelow(n)
            r = secrets.randbelow(n)
            quads.append(Quadruple(a,c,d,r))
        return quads
    
    def B(self,quad):
        f = pow(quad.r,self.e,self.n)
        x = quad.x()
        y = quad.y(self.identity)
        g = hash_two_inputs(x,y)
        return (f*g) % self.n
    
    def verify(self,vector):
        l = []
        for i in range(len(vector)):
            if vector[i] == 1:
                temp = []
                temp_quad = self.sign_quads[i]
                temp.append(temp_quad.y(self.identity))
                temp.append(temp_quad.a)
                temp.append(temp_quad.c)
                l.append(temp)
            else:
                temp = []
                temp_quad = self.sign_quads[i]
                temp.append(temp_quad.x())
                temp.append((temp_quad.a)^(self.identity))
                temp.append(temp_quad.d)
                l.append(temp)
        return l

'''
Small class for holding quadruple data and calculating x and y.
'''
class Quadruple:
    def __init__(self,a,c,d,r):
        self.a = a
        self.c = c
        self.d = d
        self.r = r
        
    def x(self):
        return hash_two_inputs(self.a,self.c)
    
    def y(self,identity):
        return hash_two_inputs((self.a)^identity,self.d)

'''
Implementation of a two input hash function based on sha512. used as both h and f in this implementation
'''
def hash_two_inputs(a,b):
    a_bytes = a.to_bytes((a.bit_length()+7)//8, 'big')
    b_bytes = b.to_bytes((b.bit_length()+7)//8, 'big')
    a_hash = bytearray(hashlib.sha512(a_bytes).digest())
    b_hash = hashlib.sha512(b_bytes).digest()
    a_hash.extend(b_hash)
    return int.from_bytes(hashlib.sha512(a_hash).digest(),'big')

test()