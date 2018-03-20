import socket
import time
from tkinter import *
import tkinter.messagebox
import tkinter.simpledialog
from models import *


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

    tkinter.messagebox.showinfo("SimpleChat 0.1 (Server)", "Server is now online\n" + serverip + " - " + serverport)
    '''
    loginLbl.config(text="Online\n(" +serverip+ " - " +serverport +")", bg="#1B5E20")
    frame.config(bg="#1B5E20")
    loginLbl.update()
    frame.update()
    '''
    loginScreen.quit()
    loginScreen.destroy()
    return serverip, serverport


# Parse create group config string
def parse_creategroup(details):
    split_details = details.split(" ")
    src = split_details[0].split(":")[0]
    members = split_details[3:]
    name = split_details[2]
    print("<ParseGroupConfig src=" + str(src) + " gname=" + str(name) + " members=" + str(members) + ">")
    return str(src), str(name), members

# Parse message group
def parse_groupmessage(details):
    split_details = details.split(" ")
    src = split_details[0]
    message = " ".join(split_details[2:])
    name = split_details[1][1:]
    rawsrc = src.split(":")[0]
    src = "<"+str(name)+"> " + str(src)
    print("<ParseGroupMsg src=" + str(src) + " gname=" + str(name) + " msg=" + str(message) + ">")
    return rawsrc, str(src), str(name), message

# Parse message whisper
def parse_whisper(details):
    split_details = details.split(" ")
    src = split_details[0]
    rawsrc = src.split(":")[0]
    message = " ".join(split_details[2:])
    name = split_details[1][1:]
    src = "<whisper> " + str(src)
    print("<ParseWhisper src=" + str(src) + " gname=" + str(name) + " msg=" + str(message) + ">")
    return str(rawsrc), str(src), str(name), message

def parse_createroom(details):
    split_details = details.split(" ")
    src = split_details[0].split(":")[0]
    password = split_details[3]
    name = split_details[2]
    print("<ParseRoomConfig src=" + str(src) + " gname=" + str(name) + " password=" + str(password) + ">")
    return str(src), str(name), str(password)

def parse_joinroom(details):
    split_details = details.split(" ")
    src = split_details[0].split(":")[0]
    password = split_details[3]
    name = split_details[2]
    print("<ParseJoin src=" + str(src) + " gname=" + str(name) + " password=" + str(password) + ">")
    return str(src), str(name), str(password)


# Initialize Address and Port Number
in_host, in_port = getStarted()
host = in_host
port = int(in_port)

userbase = UserManager()
groupbase = GroupManager()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

close = False

print("Server " + host + " Started.")



while not close:
    try:
        data, addr = s.recvfrom(1024)
        clients = userbase.clients

        # Registration services
        if "Close Server" in str(data):
            close = True

        if not userbase.is_member(address=addr):
            userbase.clients.append(User(username=data.decode('utf-8'), address=addr))


        # Custom services
            # removed /whisper on server-side
        elif "/members" in str(data):
            s.sendto(userbase.to_string().encode('utf-8'), addr)

        elif "/creategroup" in str(data):
            details = str(data.decode('utf-8'))
            srcname, groupname, members = parse_creategroup(details)
            groupbase.add_groupchat(group_id=groupname, first_client=srcname)
            for mem in members:
                groupbase.join_groupchat(str(groupname), str(mem))

        elif "!" in str(data).split(" ")[1][0]:
            details = str(data.decode('utf-8'))
            rawsrc, srcname, groupname, message = parse_groupmessage(details)
            broadcast_message = " ".join([str(srcname), str(message)])

            if groupbase.find_group(str(groupname)).is_in_group(str(rawsrc)):
                for i in range(len(userbase.clients)):
                    if groupbase.find_group(str(groupname)).is_in_group(str(userbase.clients[i].username)):
                        s.sendto(broadcast_message.encode('utf-8'), userbase.clients[i].address)
            else:
                print("<GroupMessage src does not have access>")

        elif "@" in str(data).split(" ")[1][0]:
            details = str(data.decode('utf-8'))
            rawsrc, srcname, destname, message = parse_whisper(details)
            message = " ".join([str(srcname), str(message)])

            for i in range(len(userbase.clients)):
                if str(destname) == str(userbase.clients[i].username) or \
                        str(rawsrc) == str(userbase.clients[i].username):
                    s.sendto(message.encode('utf-8'), userbase.clients[i].address)


        elif "/createroom" in str(data):
            details = str(data.decode('utf-8'))
            srcname, groupname, password = parse_createroom(details)
            groupbase.add_chatroom(group_id=str(groupname), first_client=str(srcname), password=str(password))

        elif "/join" in str(data):
            details = str(data.decode('utf-8'))
            srcname, groupname, password = parse_joinroom(details)
            groupbase.join_chatroom(group_id=str(groupname), client=str(srcname), password=str(password))

        elif "#" in str(data).split(" ")[1][0]:
            details = str(data.decode('utf-8'))
            rawsrc, srcname, groupname, message = parse_groupmessage(details)
            broadcast_message = " ".join([str(srcname), str(message)])

            if groupbase.find_group(str(groupname)).is_in_group(str(rawsrc)):
                for i in range(len(userbase.clients)):
                    if groupbase.find_group(str(groupname)).is_in_group(str(userbase.clients[i].username)):
                        s.sendto(broadcast_message.encode('utf-8'), userbase.clients[i].address)
            else:
                print("<RoomMessage src does not have access>")






        # Default service
        else:
            print(time.ctime(time.time()) + str(addr) + ": :" + str(data))
            if ":" in str(data):
                for client in clients:
                    s.sendto(data, client.address)

        ''' not yet functional
        elif "/leave" in str(data):
            for i in range(len(clients)):
                if addr == clients[i]:
                    clients.pop(i)
                    clientsNames.pop(i)
        '''
    except:
        pass

s.close()
