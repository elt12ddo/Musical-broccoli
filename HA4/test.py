# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 17:14:51 2017

@author: David Cartbo
"""
import urllib.request
import ssl
import time


url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php?name=Kalle&grade=5&signature="
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
signature = '6823ea50b133c58c'
time_list = [0]*16
vote_list = [0]*16
for x in range(5):
    for k in range(16):
        new_url = url + signature + (hex(k)[2])
        start_time = time.time()
        f = urllib.request.urlopen(new_url, context=ctx)
        time_list[k] = (time.time() - start_time)
    vote_list[time_list.index(max(time_list))] += 1
print(vote_list)
print(hex(vote_list.index(max(vote_list)))[2])