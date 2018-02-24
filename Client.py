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
# Placeholder function
def foo():
    tkinter.messagebox.showinfo(title="SimpleChat 0.1", message="This function is for future use")

# Closes window
def shutdown():
    __lock.acquire()
    global shutdown
    shutdown = True
    __lock.release()

# Gets NAME and IP of user
def getNameIP():
    name = ""
    clientip = ""
    serverip = ""
    while name == "":
        name = tkinter.simpledialog.askstring(title="SimpleChat 0.1", prompt="Username:")
    while clientip == "":
        clientip = tkinter.simpledialog.askstring(title="SimpleChat 0.1", prompt="Client IP Address:")
    while serverip == "":
        serverip = tkinter.simpledialog.askstring(title="SimpleChat 0.1", prompt="Server IP Address:")
    submitAnswer = tkinter.messagebox.showinfo(title="SimpleChat 0.1", message="Welcome " + name + "!")

    return name, clientip, serverip


# Mainloop for login. Ends after submitting credentials.
def getStarted():
    loginScreen = Tk()
    loginScreen.focus_force()
    loginScreen.wm_title("SimpleChat 0.1")
    frame = Frame(loginScreen, width=200, height=64, bg="white")
    frame.pack()
    loginLbl = Label(frame, text="waiting for credentials..", bg="white")
    loginLbl.place(x=100, y=32, anchor=CENTER)

    username, userIP, serverIP = getNameIP()
    loginScreen.destroy()

    return username, userIP, serverIP


# Receiving function
def receving(name, sock):
    while not shutdown:
        try:
            __lock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                line = data.decode('utf-8')
                addToFeed(line)
        except:
            pass
        finally:
            __lock.release()


# Print whatever's in input
def printInput(messageField):
    print(messageField.get())
    messageField.destroy()


# SEND function
def send(messageField):
    __lock.acquire()

    message = messageField.get()
    messageField.delete(0, 'end')

    if "/whisper" in message:
        privateIP = ""
        privatePort = ""
        while privateIP == "":
            privateIP = tkinter.simpledialog.askstring(title="SimpleChat 0.1", prompt="Send to (IP):")
        while privatePort == "":
            privatePort = tkinter.simpledialog.askstring(title="SimpleChat 0.1", prompt="Destination Port:")
        privateSocket = (privateIP, int(privatePort))
        m = alias + ": " + message[9:]
        m = m.encode('utf-8')
        s.sendto(m, privateSocket)

    elif message == '/members':
        m = alias + ": " + message
        m = m.encode('utf-8')
        s.sendto(m, server)

    elif message != '':
        m = alias + ": " + message
        m = m.encode('utf-8')
        s.sendto(m, server)

    __lock.release()
    time.sleep(0.2)


# Add to feed
def addToFeed(message):
    feed.config(state=NORMAL)
    feed.insert(INSERT, '%s\n' % message)
    feed.see("end")
    feed.config(state=DISABLED)


# Kill switch
def killProgram():
    raise SystemExit




''' 
================================
GUI
================================
'''

''' Login '''
# moved to func getStarted()

''' Main Screen '''
def gui():
    mainScreen = Tk()
    mainScreen.wm_title("SimpleChat 0.1")
    mainScreen.resizable(width=False, height=False)

    menu = Menu(mainScreen)
    mainScreen.config(menu=menu)

    fileMenu = Menu(menu)
    fileMenu.add_separator()
    menu.add_cascade(label="Menu", menu=fileMenu)
    fileMenu.add_command(label="Global Chat", command=foo)
    fileMenu.add_command(label="Personal Message", command=foo)
    fileMenu.add_separator()
    fileMenu.add_command(label="Settings", command=foo)
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=killProgram)

    # FRAME - Message Feed
    feedFrame = Frame(mainScreen, width=512, height=400, bg="white")
    feedFrame.pack(side=TOP, fill=BOTH)

    # Globalized Text Feed
    global feed
    feed = Text(feedFrame, font=('Calibri', 11))

    # Scrollbar for Text Feed
    scroll = Scrollbar(feedFrame, orient=VERTICAL, command=feed.yview)

    # Text Feed config
    feed.config(yscrollcommand=scroll.set, state=DISABLED)
    feed.pack()


    # FRAME - Interaction Bar
    panelFrame = Frame(mainScreen, width=512, height=20, bg="#263238")
    panelFrame.pack(side=BOTTOM, fill=X)

    # Message Field
    messageField = Entry(panelFrame)
    messageField.bind("<Return>", lambda event: send(messageField))
    messageField.pack(fill=X)

    # Send button
    sendBtn = Button(panelFrame, text="Send", width=10, height=2, bg="#009688", fg="white", relief=FLAT)
    sendBtn.bind("<Button-1>", lambda event: send(messageField))
    sendBtn.pack(fill=X)

    mainScreen.mainloop()






''' 
================================
Shared vars
================================
'''
# shutdown boolean
shutdown = False

# Init backend with credentials
myName, myIP, serverIP = getStarted()
alias = myName
host = myIP
port = 0
server = (serverIP, 5000)





''' 
================================
Connection
================================
'''
# Init socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

# Send Alias
init_alias = alias.encode('utf-8')
s.sendto(init_alias, server)





''' 
================================
Threading
================================
'''
# thread lock
__lock = threading.Lock()

# receive thread
__receive = threading.Thread(target=receving, args=("RecvThread", s))
__receive.setName("Receiver Thread") #for debugging purposes

# gui thread
__gui = threading.Thread(target=gui)
__gui.setName("GUI Thread") #for debugging purposes

# START threads
__receive.start()
__gui.start()





''' 
================================
MainThread Start/Maintain/End
================================
'''

# Chat Proper
while True:
    if shutdown:
        break

leave = alias + "left"
leave = leave.encode('utf-8')
s.sendto(leave, server)
leave = "/leave"
leave = leave.encode('utf-8')
s.sendto(leave, server)
shutdown = True
__receive.join()
__gui.join()
s.close()
