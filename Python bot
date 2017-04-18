import sys
import socket
import time
import math

#simple PING-PONG function

def ppong():
    while 1:
        text=b""
        text=irc.recv(8000)
        print(text)
        if text.find(b"PING") !=-1:
            irc.send(b"PONG "+text.split()[1]+b"\r\n")

        break

def reply():
    irc.send(b"PRIVMSG "+target+ b":!Your Mssg\r\n") #send private message to your target
    while 1:
        text=b""
        text=irc.recv(8000)
        print(text)
        if text.find(b"/")>-1:                     
            try:
               text=text[(text[1:].find(b":"))+2:]  # to slice string message from (:){excluding} to next 2 numbers/text...
                text=text[:text.find(b".")]         # to slice from start to end exluding everything
                print(text)                              
                break
            except:
                print(b"Waiting for quextion....")

# Filling form ,hence define global var

host     =" " #for host (optional)
server   =" " #for server/host to connect
botnick  =" " #bot identification name
channel  =" " #channel to join
ident    =" " #(optional)
realname =" " #(optional)
target   =" " #(optional)for user/bot
port     = #6667

#Establisihng connection...
#filling form...

try:
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((server,port))
except:
    print("! Can`t connect!")
else:
    irc.send("USER "+botnick+" "+botnick+" "+botnick+" :My Bot!\r\n")
    irc.send("NICK "+botnick+"\n")
    irc.send("JOIN "+channel+"\n")
    time.sleep(1)
    print("ping:pong")
    ppong()
    print("reply")                    #define functions to increase bot interaction
    reply()

print("good day:")
irc.close()                                          #close command


# more robust approach but nonetheless gets thing done for our challenge
#taken from 0day blog -try/except for error handling at connextion time



