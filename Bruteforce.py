'''
Simple Python Bruteforce scripts for n digits/alphabets
to crack file(zip) encryption or passwords.
---------------VAD3R
{Use responsibly}
'''
import zipfile
import os
import itertools
import time


start_time = time.time()
passw =''                                                     # for cracking zipped files
zfile = zipfile.ZipFile('secret.zip')


for combination in itertools.product(range(10), repeat=2):   # repeat=3,4,5,6 (Pin)
     passw = ''.join(map(str, combination))
     try:
         zfile.extractall(pwd=passw)
         print ('password = ' + passw + '\n')
         print("--- %s seconds ---" % (time.time() - start_time))
         exit(0)
     except Exception as e:
         pass

'''
passw =''
start_time = time.time()
s = 'ABCDEFGHIJKLMNOPQRSTUVWXZY'
for combination in itertools.product(s, repeat=5):            # repeat=3,4,5,6 (UPPERCASE alphabets)
     passw = ''.join(map(str, combination))
     try:
         if passw == 'VADER':
             print ('passwword found :' + passw + '\n')
             print("--- %s seconds ---" % (time.time() - start_time))
             exit(0)
     except Exception as e:
         pass
'''        
