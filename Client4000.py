#client .py

import socket 
import time
#Wait for server started
time.sleep(1)
s = socket.socket()
host = '192.168.219.43'
port = 4000
s.connect((host, port))
print("Sucess connet to host {} on port {}".format(host, port)) 

# 1024 là số bytes mà client có thể nhận được trong 1 lần
while (1):
    # Read message
    print("Recieved: ", end = '')
    msg = s.recv(1024)
    # Processing message
    a = msg.decode()
    if (a[:4] == "rpm: "):
        wd = a[:4].split()
    # Phần tin nhắn tiếp theo 
    print(msg.decode())
    if msg  == "Bye".encode():
        s.close()
        break
    

