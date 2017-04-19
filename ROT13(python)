def rot13(s):
    def lookup(v):
        o, c = ord(v), v.lower()
        if 'a' <= c <= 'm':
            return chr(o + 13)
        if 'n' <= c <= 'z':
            return chr(o - 13)
        return v
    return ''.join(map(lookup, s)) # map lookup with our text = s and join without spaces
text='VAD3R'
u=rot13(text)
print u 

#taken from eddmann.com/posts/implementing-rot13-and-rot-n-caesar-ciphers-in-python/
