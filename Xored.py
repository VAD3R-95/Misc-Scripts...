# Simple python script to xor_encrypt message with key
# key = rand() for more secure cipher_text
# original_function to show decryption
# ----VAD3R------

def crypt_message(message,key):
    count = 0
    cryptmessage = ""
    for i in range(0,len(message)):
        cryptmessage += chr(ord(message[count]) ^ ord(key[count % len(key)]))
        count += 1
    return cryptmessage
msg = crypt_message("VADER","CLONE")
print("Text: "+msg)
original = crypt_message(msg,"CLONE")
print("Original: "+original)
