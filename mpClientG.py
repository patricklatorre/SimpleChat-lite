import socket
import threading
import time
from tkinter import *
import tkinter.messagebox
import tkinter.simpledialog

''' 
================================
Classes
================================
'''
class Client:
    name = ""
    ip = ""
    port = 0

    def getName(self):
        return self.name
''' 
================================
Functions
================================
'''
def foo():
    tkinter.messagebox.showinfo(title="works", message="Placeholder.")


def getNameIP():
    name = ""
    ip = ""
    while name == "":
        name = tkinter.simpledialog.askstring(title="PyChat 0.1", prompt="Username:")
    while ip == "":
        ip = tkinter.simpledialog.askstring(title="PyChat 0.1", prompt="Client IP Address:")
    submitAnswer = tkinter.messagebox.showinfo(title="PyChat 0.1", message="Welcome " + name + "!")

    return name, ip


def getStarted():
    loginScreen = Tk()
    frame = Frame(loginScreen, width=200, height=64)
    frame.pack()
    loginLbl = Label(loginScreen, text="waiting for credentials..")
    loginLbl.place(x=100, y=32, anchor=CENTER)
    continueBtn = Button(loginScreen, text="continue", command=foo)

    username = ""
    userIP = ""
    username, userIP = getNameIP()

    loginScreen.destroy()

    return username, userIP



''' 
================================
GUI
================================
'''

''' Login '''
myName, myIP = getStarted()




''' Main Screen '''
mainScreen = Tk()

menu = Menu(mainScreen)
mainScreen.config(menu=menu)

fileMenu = Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="New Project", command=foo)
fileMenu.add_command(label="New", command=foo)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=foo)

frame = Frame(mainScreen, width=1280, height=720, bg="white")
frame.pack()

mainScreen.mainloop()




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

# Join a Server or Create
chatDestination = input(" [1]Join Global Chat ")
if chatDestination == '1':
    server = ('192.168.1.5', 5000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

# Threading
rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

# Chat Proper
alias = input("Name: ")
message = input(alias + "-> ")
while message != '/leave':
    # You have to put /whiser next to your message to PM, ex. /whisper hello!
    if "/whisper" in message:
        pmhostnum = (input("Enter Host Name:"))
        pmportnum = int(input("Enter Port Number:"))
        privateserver = (pmhostnum, pmportnum)
        pm = alias + ": " + message
        pm = pm.encode('utf-8')
        s.sendto(pm, privateserver)

    elif message == '/members':
        m = alias + ": " + message
        m = m.encode('utf-8')
        s.sendto(m, server)

    elif message != '':
        b = alias + ": " + message
        b = b.encode('utf-8')
        s.sendto(b, server)

    tlock.acquire()
    message = input(alias + "-> ")
    tlock.release()
    time.sleep(0.2)

leave = alias + "left"
leave = leave.encode('utf-8')
s.sendto(leave, server)
print(alias + " left ")
shutdown = True
rT.join()
s.close()
