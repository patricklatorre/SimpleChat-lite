import socket
import time
from tkinter import *
import tkinter.messagebox
import tkinter.simpledialog

# Gets NAME and IP of user
def initServer():
    input_serverip = ""
    input_port = ""

    while input_serverip == "":
        input_serverip = tkinter.simpledialog.askstring(title="SimpleChat 0.1 (Server)", prompt="Server IP:")
    while input_port == "":
        input_port = tkinter.simpledialog.askstring(title="SimpleChat 0.1 (Server)", prompt="Port:")

    return input_serverip, input_port


# Mainloop for login. Ends after submitting credentials.
def getStarted():
    global loginScreen
    loginScreen = Tk()
    loginScreen.wm_title("SimpleChat 0.1 (Server)")
    loginScreen.focus_force()
    frame = Frame(loginScreen, width=200, height=64, bg="#B71C1C")
    frame.pack()
    loginLbl = Label(frame, text="Offline", bg="#B71C1C", fg="white")
    loginLbl.place(x=100, y=32, anchor=CENTER)


    serverip, serverport = initServer()

    tkinter.messagebox.showinfo("SimpleChat 0.1 (Server)", "Server is now online\n" +serverip+ " - " +serverport)
    '''
    loginLbl.config(text="Online\n(" +serverip+ " - " +serverport +")", bg="#1B5E20")
    frame.config(bg="#1B5E20")
    loginLbl.update()
    frame.update()
    '''
    loginScreen.quit()
    loginScreen.destroy()
    return serverip, serverport


#Initialize Address and Port Number
in_host, in_port = getStarted()
host = in_host
port = int(in_port)
clients = []
clientsNames = []


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)

close = False


print ("Server "+ host + " Started.")

while not close:
    try:
        data, addr = s.recvfrom(1024)
        if "Close Server" in str(data):
            close = True
        if addr not in clients:
            clients.append(addr)
            clientsNames.append(data)

        if "/whisper" in str(data):
            pmdata,pmaddr = s.recvfrom(1024)
            for client in clients:
                s.sendto(pmdata,pmaddr)

        elif "/members" in str(data):
            for i in range(len(clients)):
                memdata = ("\t\t{} : {}".format(clientsNames[i].decode('utf-8'), clients[i])).encode('utf-8')
                s.sendto(memdata, addr)

        elif "/leave" in str(data):
            for i in range(len(clients)):
                if addr == clients[i]:
                    clients.pop(i)
                    clientsNames.pop(i)

        else:
            print (time.ctime(time.time()) + str(addr) + ": :" + str(data))
            if ":" in str(data):
                for client in clients:
                    s.sendto(data, client)

      
    except:
        pass

s.close()