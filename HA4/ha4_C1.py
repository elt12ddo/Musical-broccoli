#!/usr/bin/python3

import socket
import secrets
import hashlib


#As described on Wikipedia
def invmod(a,n):
    t, t1 = 1, 0 
    r, r1 = a, n 
    while r1: 
        q = r // r1 
        t, t1 = t1, t - q * t1 
        r, r1 = r1, r - q * r1 
    return t 

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
soc.connect(("eitn41.eit.lth.se", 1337))

# the p shall be the one given in the manual
p1 = 'FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF'
p = int(p1, 16)
g = 2

##########################
#### D-H Key Exchange ####
##########################

## receive g**x1
# receive the hex-string, decode, and remove trailing '\n'
g_x1 = soc.recv(4096).decode('utf8').strip()
#print ('g**x1:', g_x1)
# interpret as a number
g_x1 = int(g_x1, 16)

# generate g**x2, x2 shall be a random number
x2 = secrets.randbelow(p*2)
# calculate g**x2 mod p
g_x2 = pow(g, x2, p)
# convert to hex-string
g_x2_str = format(g_x2, 'x')
# send it
soc.send(g_x2_str.encode('utf8'))
# read the ack/nak. This should yield a nak due to x2 being 0
response = soc.recv(4096).decode('utf8').strip()
if response != "ack":
    raise ValueError("Error in communication")
print ('\nsent g_x2:', response)
# calculate the secret
secret = pow(g_x1,x2,p)

##########################
########## SMP ###########
##########################

# receive g**a2
g_a2 = soc.recv(4096).decode('utf8').strip()
#print ('g**a2:', g_a2)
# interpret as a number
g_a2 = int(g_a2, 16)

b2 = secrets.randbelow(p*2)

g_b2 = pow(g, b2, p)

g_b2_str = format(g_b2, 'x')

soc.send(g_b2_str.encode('utf8'))

response = soc.recv(4096).decode('utf8').strip()
if response != "ack":
    raise ValueError("Error in communication")
print ('\nsent g_b2:', response)

# receive g**a3
g_a3 = soc.recv(4096).decode('utf8').strip()
#print ('g**a3:', g_a3)
# interpret as a number
g_a3 = int(g_a3, 16)

b3 = secrets.randbelow(p*2)

g_b3 = pow(g, b3, p)

g_b3_str = format(g_b3, 'x')

soc.send(g_b3_str.encode('utf8'))

response = soc.recv(4096).decode('utf8').strip()
if response != "ack":
    raise ValueError("Error in communication")
print ('\nsent g_b3:', response)

# calculate g_2 and g_3
g_2 = pow(g_a2, b2, p)
g_3 = pow(g_a3, b3, p)

# generate b
b = secrets.randbelow(p*2)
# calculate P_b and Q_b
P_b = pow(g_3, b, p)

# calculate shared secret y
secret2 = secret.to_bytes((secret.bit_length() + 7) // 8, 'big')
passphrase = 'eitn41 <3'
passphrase2 = bytes(passphrase,'utf8')
y = hashlib.sha1(secret2+passphrase2).hexdigest()
y = int(y, 16)

Q_b = pow(g, b, p) * pow(g_2, y, p) % p

# receive P_a
P_a = soc.recv(4096).decode('utf8').strip()
#print ('P_a:', P_a)
# interpret as a number
P_a = int(P_a, 16)


# send P_b
P_b_str = format(P_b, 'x')

soc.send(P_b_str.encode('utf8'))

response = soc.recv(4096).decode('utf8').strip()
if response != "ack":
    raise ValueError("Error in communication")
print ('\nsent P_b:', response)

# receive Q_a
Q_a = soc.recv(4096).decode('utf8').strip()
#print ('Q_a:', Q_a)
# interpret as a number
Q_a = int(Q_a, 16)


# send Q_b
Q_b_str = format(Q_b, 'x')

soc.send(Q_b_str.encode('utf8'))

response = soc.recv(4096).decode('utf8').strip()
if response != "ack":
    raise ValueError("Error in communication")
print ('\nsent Q_b:', response)

# receive R_a
R_a = soc.recv(4096).decode('utf8').strip()
#print ('R_a:', R_a)
# interpret as a number
R_a = int(R_a, 16)

Q_b_inv = invmod(Q_b,p)
Q_prod = Q_a * Q_b_inv
R_b = pow(Q_prod, b3, p)


# send R_b
R_b_str = format(R_b, 'x')

soc.send(R_b_str.encode('utf8'))

response = soc.recv(4096).decode('utf8').strip()
if response != "ack":
    raise ValueError("Error in communication")
print ('\nsent R_b:', response)

response = soc.recv(4096).decode('utf8').strip()
if response != "ack":
    raise ValueError("Error in communication")
print ('\nAuthentication:', response)

msg = '1337'
enc_msg = int(msg, 16) ^ secret

# send enc_msg
enc_msg_str = format(enc_msg, 'x')

soc.send(enc_msg_str.encode('utf8'))

print ('\nResponse:', soc.recv(4096).decode('utf8').strip())
