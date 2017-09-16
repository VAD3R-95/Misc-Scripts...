from Crypto.Cipher import AES
import base64

cpass = ""

passw = base64.b64decode(cpass)

#https://msdn.microsoft.com/en-us/library/cc422924.aspx - key

key = b"\x4e\x99\x06\xe8\xfc\xb6\x6c\xc9\xfa\xf4\x93\x10\x62\x0f\xfe\xe8\xf4\x96\xe8\x06\xcc\x05\x79\x90\x20\x9b\x09\xa4\x33\xb6\x6c\x1b"


size = AES.block_size  # 16 bytes
mode = AES.MODE_CBC
IV = '\x00' * size
encryptor = AES.new(key, mode, IV=IV)
d = encryptor.decrypt(passw)
password = (d.decode().split('\x00')) # removing null bytes
passw = ''.join(str(i) for i in password) # list to string

print(passw)
