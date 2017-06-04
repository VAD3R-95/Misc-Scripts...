# rail - fence cipher decode
# ---VAD3R--- 

def fence(width, numrails):
    fence = [[None] * len(width) for n in range(numrails)]
    rails = range(numrails - 1) + range(numrails - 1, 0, -1)
    for n, x in enumerate(width):
        fence[rails[n % len(rails)]][n] = x

    if 0:                                            # debug         rails > 3
        for rail in fence:                           # StackOverflow/George
            print (''.join('.' if c is None else str(c) for c in rail))

    return [c for rail in fence for c in rail if c is not None]

def encode(text, n):
    return ''.join(fence(text, n))
    
def decode(text, n):
    rng = range(len(text))
    pos = fence(rng, n)
    return ''.join(text[pos.index(n)] for n in rng)

z = encode('ATTACK.AT.DAWN', 3)    
print (z) # ACTWTAKA.ANT.D

y = decode(z, 3)
print (y) # ATTACK.AT.DAWN


'''
# n - rails
for i in range(3,15):
    y = decode(z, i)
    print y # ATTACK.AT.DAWN
'''
