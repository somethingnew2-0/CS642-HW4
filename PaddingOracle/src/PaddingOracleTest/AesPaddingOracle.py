'''
Created on Jul 4, 2010

@author: Eloi Sanfelix < eloi AT limited-entropy.com >
'''

from Crypto.Cipher import AES
from PaddingOracle.DecryptionOracle import DecryptionOracle
import random
import struct

def hex_string(data):
    x = struct.unpack("B"*len(data),data)
    return "".join([ hex(i)+" " for i in x])
#Random key globally initialized 
key = "".join([struct.pack("B",random.getrandbits(8)) for i in range(16) ])

def oracle(ctext):
    oracleCipher = AES.new(key,AES.MODE_CBC,"\x00"*16)
    ptext = oracleCipher.decrypt(ctext)
    
    paddingLen = struct.unpack("B",ptext[-1])[0]
    goodPadding = (ptext[-paddingLen:] == struct.pack("B",paddingLen)*paddingLen)

    return goodPadding

if __name__ == '__main__':
    
    #Random 4 block plaintext
    data = "".join([struct.pack("B",random.getrandbits(8)) for i in range(64) ])
    print "Plaintext: "+hex_string(data)
        
    cipher = AES.new(key,AES.MODE_CBC,"\x00"*16)
    ctext = cipher.encrypt(data)
    
    print "Ciphertext: "+hex_string(ctext)
    
    decryptOracle = DecryptionOracle(oracle,16)
    
    result = decryptOracle.decrypt_message(ctext)

    if(data == result ):
        print "CORRECT ptext recovered: "+hex_string(result)
    else:
        print "INCORRECT ptext recovered: "+hex_string(result)
    
