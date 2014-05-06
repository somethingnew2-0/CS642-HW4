from subprocess import Popen, PIPE

proc = Popen(["./badencrypt.py", "hellooooworlddd"],stdout=PIPE)
hexCiphertext = proc.communicate()[0].strip()

import pdb
pdb.set_trace()
print hexCiphertext
print str(len(hexCiphertext)/16)+" blocks"

proc = Popen(["./baddecrypt.py", hexCiphertext],stdout=PIPE)
output = proc.communicate()[0]

print output

