# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 17:14:51 2017

@author: David Cartbo
"""
import urllib.request
import ssl
import time

def find_signature(name,grade):
    url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php?name=" + name + "&grade=" + str(grade) + "&signature="
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    signature = ''
    time_list = [0]*16
    for i in range(19):
        vote_list = [0]*16
        for x in range(5):
            for k in range(16):
                new_url = url + signature + (hex(k)[2])
                start_time = time.time()
                f = urllib.request.urlopen(new_url, context=ctx)
                time_list[k] = (time.time() - start_time)
            vote_list[time_list.index(max(time_list))] += 1
        print(i)
        signature += hex(vote_list.index(max(vote_list)))[2]
    for n in range(16):
        new_url = url + signature + (hex(n)[2])
        f = urllib.request.urlopen(new_url, context=ctx)
        if (int(f.read()) == 1):
            signature += hex(n)[2]
            return signature
    return -1

def signature(name,grade):
    while(True):
        sign = find_signature(name,grade)
        if(sign != -1):
            return sign

print(signature('Kalle',5))