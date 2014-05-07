from subprocess import Popen, PIPE

# proc = Popen(["./badencrypt.py", "poop"],stdout=PIPE)
# hexCiphertext = proc.communicate()[0].strip()

hexCiphertext = "1caaeb57ac2d4af7f0b7fce4e7238427d80721572ab7756552cecce8b3b35f30b098ba91594575af78cfaa06e282f53e286ce54345ea5dc244d20c2c370d4a332fcc462d463aa505ec31ec2c79d784bf"

xor = 0x0
versionCiphertext = ""
for b in range(4):
	hexGuess = b*2
	for i in range(256):
		ciphertextGuess = int(hexCiphertext[32+hexGuess:34+hexGuess], 16) ^ i
		
		# Add a leading 0 if hex is less than 16
		if ciphertextGuess < 16:
			ciphertextGuess = "0%x" % ciphertextGuess
		else:		
			ciphertextGuess = "%x" % ciphertextGuess

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

cracked = xor ^ 0x01010000
plaintext = ""
for i in range(4):
    plaintext = chr(cracked % 256) + plaintext
    cracked = cracked >> 8

print "The message is " + plaintext
		
# Forget about guessing the last three bytes, only first four are important
# proc = Popen(["./baddecrypt.py", versionCiphertext+hexCiphertext[40:96]],stdout=PIPE)
# output = proc.communicate()[0].strip()

# import re
# pattern = re.compile(r'(\d+)')
# # Capture msglen from "Length of ", msglen, "is too large!"
# msglen = pattern.search(output).group()

# # Check message length wasn't actually valid
# if msglen:
# 	msg = int(msglen)
# 	# Can't figure out the fourth to last char
# 	for i in range(3):
# 	    print chr(msg % 256)
#     	msg = msg >> 8