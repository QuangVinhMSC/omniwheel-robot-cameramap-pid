#server.py 

import socket 
import time
import serial
import threading
import re
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
omega_now = [] 

"""               Setup TCP/IP               """
"""   server    """

j_cleint = socket.socket()
c_host = '192.168.219.43'
c_port = 4000
j_cleint.connect((c_host, c_port))
print("Sucess connet to host {} on port {}".format(c_host, c_port))

# Định nghĩa host và port mà server sẽ chạy và lắng nghe
#Wait for server started
time.sleep(1)
s_host = '192.168.219.65'
s_port = 2000

j_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
j_server.bind((s_host, s_port))

j_server.listen(1) # 1 ở đây có nghĩa chỉ chấp nhận 1 kết nối
print("Server listening on port", s_port)

s_cleint, addr = j_server.accept()
print("Connect from ", str(addr))

def Server():
    #server sử dụng kết nối gửi dữ liệu tới client dưới dạng binary
    while(1):
        #Update velocity of wheel
        #wd =  CrtSys.main(X_d,Y_d,Phi_d,X,Y,Phi,R,L,omega_now)
        #but = bytes("{},{},{},{},{},{}".format(wd[0],wd[1],wd[2],int(wd[0]>=0),int(wd[1]>=0),int(wd[2]>=0)).encode())
        but = bytes(input("Send:").encode())
        s_cleint.send(but)
        print("OK")
        time.sleep(0.05)
        if but  == "Bye".encode():
            time.sleep(1)
            s_cleint.close()
            break

def Cleint():
    while(1):
        # Read message
        #print("Recieved: ", end = '')
        msg = j_cleint.recv(1024)
        # Processing message
        a = msg.decode()
        l = a.split('\n')[0]
        if (l[:5] == "rpm: ")and(len(l) == 31):
            print(l)
            print("end")
            omega_now = list(map(float, l[5:].split()))
        # Encode the string to bytes
        if msg  == "Bye".encode():
            j_cleint.close()
            break

if __name__ =="__main__":
    t1 = threading.Thread(target=Server)
    t2 = threading.Thread(target=Cleint)
 
    t1.start()
    t2.start()
 
    t1.join()
    t2.join()
 
    print("Done!")