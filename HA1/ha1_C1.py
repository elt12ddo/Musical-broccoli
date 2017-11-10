# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:04:25 2017

@author: David Cartbo
"""
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import secrets

class Bank:
    def __init__(self):
        self.generate_keys()
    def generate_keys(self):
        self.key = rsa.generate_private_key(public_exponent=65537,key_size=2048,backend=default_backend())

class User:
    def __init__(self, bank, identity):
        self.bank = bank
        self.identitiy = identity
    def showmethemoney(self,k):
        quads = self.generate_quads(k)
        
    def generate_quads(self,k):
        n = self.bank.key.private_numbers().public_numbers.n
        quads = []
        for i in range(2*k):
            a = secrets.randbelow(n) # No modulo needed as it will be below n as it will be in range [0,n)
            c = secrets.randbelow(n)
            d = secrets.randbelow(n)
            r = secrets.randbelow(n)
            quads.append(Quadruple(a,c,d,r))
        return quads

class Quadruple:
    def __init__(self,a,c,d,r):
        self.a = a
        self.c = c
        self.d = d
        self.r = r







bank = Bank()
user = User(bank,1)
user.showmethemoney(10)