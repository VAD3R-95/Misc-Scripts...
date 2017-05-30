# Hash cracking python script
#---VAD3R----
import itertools
import hashlib
import crypt

hash_to_crack=''

file = 'dict.txt'                                                  # use crunch ;-) to create dictionary or go with online
with open(file,'rb') as f:
    for line in f:
        line = line.strip()
        try:
            if hashlib.sha1(line).hexdigest() == hash_to_crack:    # hash cracking (4 digtis sha1)
                print ("Success for crack: "+hash_to_crack)
                break
        except:
            pass

cracked_mssg = line.decode("utf-8")  # binary from file to string
print('Cracked hash: '+cracked_mssg)

# Salted Hash cracking
# with bruteforcing ;-)

hash=''
salt_message=''
salt_to_add = salt_message.encode('utf-8')
print("HASH:"+hash)
print("SALT:"+str(salt_to_add))

for combination in itertools.product(range(10), repeat=4):          # repeat=3,4,5,6 (Pin)
     sequence = ''.join(map(str, combination))
     try:
         if hashlib.sha1(str(sequence).encode('utf-8')+salt_to_add).hexdigest() == hash:    # hash cracking (4 digtis sha1)
             print ("Success for crack: "+hash)
             break
     except:
         pass

cracked_mssg = sequence                                             # to get cracked plain text hash
print('Cracked hash: '+cracked_mssg)


# Hashing messages
#---VAD3R----

byte_message = ''
byte_message = bytes(text,'utf-8')
hash_message = hashlib.sha512(byte_message).hexdigest()            # to hash the message
print(hash_message)                                                # with salt: append salt to end and start of hash

