'''
Use with crunch ;-)

crunch <min> <max> pattern -o password-file.txt
+-----VAD3R-----+

'''

import zipfile
import os
import time
from threading import Thread


def extract(zFile,passw):
    try:
        zFile.extractall(pwd=passw)
        return passw
    except:
        pass
        
    


def main():
    start_time = time.time()
    zFile = zipfile.ZipFile("crack.zip")
    with open("password-list.txt",'r')  as f:
        for line in f:
            passw = line.strip('\n')
            t = Thread(target=extract, args=(zFile,passw))
            t.start()
            #ans = extract(zFile,passw)                                #without threading {without lock it generates bizzare result}
        if passw:                                                      #ans 
            print("Password :"+passw+'\n')                             #+ans+ 
            print("--- %s seconds ---" % (time.time() - start_time))
            exit(0)

if __name__ == "__main__":
    main()
            
