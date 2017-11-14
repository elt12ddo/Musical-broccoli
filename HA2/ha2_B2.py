# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 14:52:56 2017

@author: David Cartbo
"""
from pcapfile import savefile

def find_terrorists(filename, terip, mixip, m):
    testcap = open(filename, 'rb')
    capfile = savefile.load_savefile(testcap, layers=2, verbose=True)
    
    ter_sent = False
    mix_sent = False
    set_list = []
    current_set = set()
    for pkt in capfile.packets:
        #timestamp = pkt.timestamp
        # all data is ASCII encoded (byte arrays). If we want to compare with strings
        # we need to decode the byte arrays into UTF8 coded strings
        #eth_src = pkt.packet.src.decode('UTF8')
        #eth_dst = pkt.packet.dst.decode('UTF8')
        ip_src = pkt.packet.payload.src.decode('UTF8')
        ip_dst = pkt.packet.payload.dst.decode('UTF8')
        if(ip_src == terip):
            ter_sent = True
            mix_sent = False # So we avoid the problem of setting t_sent to False in the scenario of Nazir sending the first package after the mixer is done sending packages
        else:
            if(ter_sent and (ip_src == mixip)): # We assume that no packages will come between the packages sent in one batch from the mixer (or we would have to use an more complicated time based evaluation)
                current_set.add(ip_dst)
                mix_sent = True
            else:
                if(mix_sent):
                    if(len(set_list) < m):
                        if(disjoint(set_list,current_set)):
                            set_list.append(current_set)
                        else:
                            remove_elements(set_list,current_set)
                    else:
                        remove_elements(set_list,current_set)
                    current_set = set()
                    ter_sent = False
                    mix_sent = False
    print(set_list)
    total = 0
    for k in set_list:
        x = k.pop().split('.',4)
        y = int(x[0])
        y = y << 8
        y += int(x[1])
        y = y << 8
        y += int(x[2])
        y = y << 8
        y += int(x[3])
        total += y
    print(total)

def disjoint(l, s):
    for k in l:
        if(not k.isdisjoint(s)):
            return False
    return True

def remove_elements(l, s):
    i = -1
    for k in range(len(l)):
        if(not l[k].isdisjoint(s)):
            if(i == -1):
                i = k
            else:
                return
    if(i == -1): # It is disjoint from all the sets we have, but as we only want m sets there is nothing for us to do with it
        return
    #Do the thing
    l[i] = l[i].intersection(s)

find_terrorists('cia.log.1337.pcap','159.237.13.37','94.147.150.188',2)
find_terrorists('cia.log.1339.pcap','161.53.13.37','11.192.206.171',12)
