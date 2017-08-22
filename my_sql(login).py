# https://github.com/dbcli/mycli/issues/17#issuecomment-104175743

import struct
from Crypto.Cipher import AES

LOGIN_KEY_LEN = 20
MY_LOGIN_HEADER_LEN = 24
MAX_CIPHER_STORE_LEN = 4

f = open(".mylogin.cnf")
f.seek(4)                                                 # set current position of file at offset
b = f.read(LOGIN_KEY_LEN)          
key = [0] * 16
for i in xrange(LOGIN_KEY_LEN):
    key[i % 16] ^= ord(b[i])
key = struct.pack('16B', *key)                               # 16 byte key in AES-ECB 
encryptor = AES.new(key, AES.MODE_ECB)    # no IV ;-)

f.seek(MY_LOGIN_HEADER_LEN)
while True:
    b = f.read(MAX_CIPHER_STORE_LEN)
    if len(b) < MAX_CIPHER_STORE_LEN:
        break
    cipher_len, = struct.unpack("<i", b)          # simply reading file as txt file ;-)
    b = f.read(cipher_len)
    plain = encryptor.decrypt(b)
    print plain[:-ord(plain[-1])]
f.close()
