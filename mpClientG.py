import socket
import threading
import time
from tkinter import *
import tkinter.messagebox

''' 
================================
GUI Object
================================
'''
class client:
	def __init__(self, master):
		frame = Frame(master)
		frame.pack()


''' 
================================
Logic Handling
================================
'''
tlock = threading.Lock()
shutdown = False

# Receiving func
def receving(name, sock):
    while not shutdown:
        try:
            tlock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print(str(data))
        except:
            pass
        finally:
            tlock.release()

host = '192.168.1.5'
port = 0

#Join a Server or Create
chatDestination= input(" [1]Join Global Chat ")
if chatDestination == '1':
    #server = ('127.0.0.1', 5000)
    server = ('192.168.1.5', 5000)
    


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

#Threading
rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

#Chat Proper
alias = input("Name: ")
message = input(alias + "-> ")
while message != '/leave':
    #You have to put /whiser next to your message to PM, ex. /whisper hello!
    if "/whisper" in message:
        pmhostnum=(input("Enter Host Name:"))
        pmportnum=int(input("Enter Port Number:"))
        privateserver=(pmhostnum,pmportnum)
        pm = alias + ": " + message
        pm= pm.encode('utf-8') 
        s.sendto(pm, privateserver)
    
    elif message == '/members':
        m = alias + ": " + message
        m= m.encode('utf-8')
        s.sendto(m, server)
        
    elif message != '':
        b = alias + ": " + message
        b= b.encode('utf-8')
        s.sendto(b, server)
    
    
    
    
    tlock.acquire()
    message = input(alias + "-> ")
    tlock.release()
    time.sleep(0.2)
    
leave=alias+ "left" 
leave= leave.encode('utf-8')   
s.sendto(leave, server)
print(alias +" left ")    
shutdown = True
rT.join()
s.close()



