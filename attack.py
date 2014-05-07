from subprocess import Popen, PIPE

# proc = Popen(["./badencrypt.py", "hellooooworlddd"],stdout=PIPE)
# hexCiphertext = proc.communicate()[0].strip()

hexCiphertext = "1610aa2d1ec8acf4a0d746141d5d558fc0f6d5b4bd7465ed9e9f4dd69870f4f753a30c1537acf9c577439fcf64e156419389df0d374cb8d81b36e3a2ef14fcee6de760208ecb316dd82ae44f84566476"

print hexCiphertext
print str(len(hexCiphertext)/16)+" blocks"

xor = 0
versionCiphertext = ""
for b in range(4):
	hexGuess = b*2
	for i in range(256):
		ciphertextGuess = int(hexCiphertext[32+hexGuess:34+hexGuess], 16) ^ i
		# import pdb
		# pdb.set_trace()
		if ciphertextGuess < 16:
			ciphertextGuess = "0%x" % ciphertextGuess
		else:		
			ciphertextGuess = "%x" % ciphertextGuess
		# print ("%x" % ciphertextGuess)+hexCiphertext[34:96]
		proc = Popen(["./baddecrypt.py", versionCiphertext+ciphertextGuess+hexCiphertext[34+hexGuess:96]],stdout=PIPE)
		output = proc.communicate()[0].strip()

		if b == 0 and "Wrong version!" != output:
			mask = i << 24
			xor |= mask 
			versionCiphertext += ciphertextGuess
			break
		elif b == 1 and "Wrong subversion!" != output:
			mask = i << 16
			xor |= mask 
			versionCiphertext += ciphertextGuess
			break
		elif b == 2 and "First reserved byte error!" != output:
			mask = i << 8
			xor |= mask 
			versionCiphertext += ciphertextGuess
			break
		elif b == 3 and "Second reserved byte error!" != output:
			xor |= i
			versionCiphertext += ciphertextGuess
			break

print hex(16842752) #0x01010000
plaintext = xor ^ 16842752
for i in range(4):
    # if i == 3:
    #     msglen -= 104
    print str(unichr(plaintext % 256))
    plaintext = plaintext >> 8
		
# print str(unichr(xor ^ 1))

print len(hexCiphertext[40:96])
proc = Popen(["./baddecrypt.py", versionCiphertext+hexCiphertext[40:96]],stdout=PIPE)
output = proc.communicate()[0]

print output