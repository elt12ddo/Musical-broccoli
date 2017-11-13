# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:04:25 2017

@author: David Cartbo
"""
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import secrets
import hashlib

class Bank:
    def __init__(self):
        self.generate_keys()
        
    def generate_keys(self):
        self.key = rsa.generate_private_key(public_exponent=65537,key_size=1024,backend=default_backend())
        
    def fetch_indices(self,b):
        self.b = b
        self.indices = []
        print("fetch_indeces")
        while(len(self.indices) < len(b)/2):
            k = secrets.randbelow(len(b))
            if(k not in self.indices):
                self.indices.append(k)
                
        return self.indices
    
    def check(self,quads,identity):
        signs = []
        for i in range(len(quads)):
            if(self.B(quads[i],identity) != self.b[self.indices[i]]):
                return None
            
        for k in range(len(self.b)):
            if(k not in self.indices):
                #sign = 
                #signs.append(sign)
                a = 1 #CONTINUE HERE
                print(len(self.b)-k,"Bottles of beer")
            
    def B(self,quad,identity):
        p = pow(quad.r,self.get_e(),self.get_n())
        return (p*hash_two_inputs(quad.x(),quad.y(identity))) % self.get_n()
    
    def get_e(self):
        return self.key.private_numbers().public_numbers.e
    
    def get_n(self):
        return self.key.private_numbers().public_numbers.n

class User:
    def __init__(self, bank, identity):
        self.bank = bank
        self.identity = identity
        self.n = bank.get_n()
        self.e = bank.get_e()
        
    def generate_coins(self,k):
        print("THIS")
        quads = self.generate_quads(k)
        b_list = []
        print("HELLO")
        
        for i in range(len(quads)):
            print(i)
            b_list.append(self.B(quads[i]))
            
        print("hello")
        #Time to disturb the sleeping monster (i.e. the BANK!)
        indices = self.bank.fetch_indices(b_list)
        bank_quads = []
        
        for k in range(len(indices)):
            l = indices[k]
            print(l, len(quads))
            bank_quads.append(quads[l])
            
        signs = self.bank.check(bank_quads,self.identity)
        
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

def hash_two_inputs(a,b):
    a_bytes = a.to_bytes((a.bit_length()+7)//8, 'big')
    b_bytes = b.to_bytes((b.bit_length()+7)//8, 'big')
    a_hash = bytearray(hashlib.sha512(a_bytes).digest())
    b_hash = hashlib.sha512(b_bytes).digest()
    a_hash.extend(b_hash)
    return int.from_bytes(hashlib.sha512(a_hash).digest(),'big')



print("first")
bank = Bank()
print("I haz bank")
user = User(bank,1)
print("I haz the user")
user.generate_coins(10)
