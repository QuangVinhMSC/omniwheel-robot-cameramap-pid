import numpy as np
from numpy import sin,cos,sqrt

def Controller_Velocity(X_d,Y_d,Phi_d,X,Y,Phi):
    kpx=0.1 #constanst
    kpy=0.1 #constanst
    kphi=0.1#constanst
    velocity = np.empty(2)
    velocity[0]=(X_d-X)*kpx
    velocity[1]=(Y_d-Y)*kpy
    omega = (Phi_d-Phi)*kphi
    return velocity,omega
def block1(Vx,Vy,phi,ome):
    MatrixV = np.array([Vx, Vy, 0]).reshape(3, 1)
    a = np.dot(np.array([[cos(-phi),-sin(-phi),0],[sin(-phi),cos(-phi),0],[0,0,1]]),MatrixV)
    V_x = a[0,0]+ome*a[1,0]
    V_y = a[1,0]-ome*a[0,0]
    return Vx,Vy
def block2(vx,vy,w,R,L):
    invMatrix = np.array([[0,0,1/L],[-sqrt(3)/2,-1/2,1/L],[sqrt(3)/2,-1/2,1/L]])
    a = np.array([[vx],[vy],[w]])
    b= np.dot(invMatrix,a)
    W1=b[0,0]/R
    W2=b[1,0]/R
    W3=b[2,0]/R
    return W1,W2,W3
def Converter2(v,R,L,phi,omega,omega_now):
    V_x,V_y = block1(v[0],v[1],phi,omega_now*0.18)#0.18 need to adjust
    omega = omega if omega <1 else 1#need to adjust
    omega = omega if omega >-1 else -1#need to adjust
    w1,w2,w3 = block2(V_x,V_y,omega,R,L)
    wd = np.array([[w1],[w2],[w3]])
    return wd
def main(X_d,Y_d,Phi_d,X,Y,Phi,R,L,omega_now):
    velocity,omega = Controller_Velocity(X_d,Y_d,Phi_d,X,Y,Phi)
    wd = Converter2(velocity,R,L,Phi,omega,omega_now)
    return wd