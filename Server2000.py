#server.py 

import socket 
import time
import controll_system as CrtSys

#Pos Target
X_d = 0
Y_d = 0
Phi_d = 0
#Pos feedback
X = 0
Y = 0
Phi = 0

R = 0.04 #radius of wheel (m)
L = 0.05 #width of wheel
#angular velocity
omega_now = 0 

# Định nghĩa host và port mà server sẽ chạy và lắng nghe
host = '192.168.219.65'
port = 2000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1) # 1 ở đây có nghĩa chỉ chấp nhận 1 kết nối
print("Server listening on port", port)

c, addr = s.accept()
print("Connect from ", str(addr))

while(1):
    #Update velocity of wheel
    #wd =  CrtSys.main(X_d,Y_d,Phi_d,X,Y,Phi,R,L,omega_now)
    #but = bytes("{},{},{},{},{},{}".format(wd[0],wd[1],wd[2],int(wd[0]>=0),int(wd[1]>=0),int(wd[2]>=0)).encode())
    but = bytes(input("Send:").encode())

    c.send(but)
    print("OK")
    time.sleep(0.05)
    if but  == "Bye".encode():
        time.sleep(1)
        c.close()
        break



