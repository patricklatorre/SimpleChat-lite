import socket
import time


#host = '127.0.0.1'
#port = 5000

#Initialize Address and Port Number
host= input("Enter Server Address:")
port=  int(input("Enter Port Number:"))
clients = []


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
        for client in clients:
            s.sendto(data, client)



        if "/whisper" in str(data):
            pmdata,pmaddr=s.recvfrom(1024)
            print(pmaddr)
            for client in clients:
                s.sendto(pmdata,pmaddr)
        else:       
            print (time.ctime(time.time()) + str(addr) + ": :" + str(data))

        if "/members" in str(data):
            for i in range(len(clients)):
                print("User {}: Address:{}".format(i+1, clients[i]))
          
      
    except:
        pass
s.close()