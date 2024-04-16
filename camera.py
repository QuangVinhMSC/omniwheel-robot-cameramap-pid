import cv2
import numpy as np
import time
import sys
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_100)
parameters =  cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dictionary, parameters)
try:
    video = cv2.VideoCapture(1)

except:
    print("[Lỗi] Chưa cung cấp vị trí tập tin video")
    sys.exit(1)

center = np.zeros([4, 2])#------------------------
center_angular = np.zeros([4, 2])
def distance():
    a1 = (center[0][1]-center[1][1])/(center[0][0]-center[1][0])
    a2 = (center[0][1]-center[2][1])/(center[0][0]-center[2][0])
    pos_x = np.abs(a1*center[3][0]-center[0][0]*a1 + center[0][1] -center[3][1])/np.sqrt(a1**2+1)
    pos_y = np.abs(a2*center[3][0]-center[0][0]*a2 + center[0][1] -center[3][1])/np.sqrt(a2**2+1)
    resize_pos_x = round(pos_x/length_x*100)
    resize_pos_y = round(pos_y/length_y*100)
    return resize_pos_x,resize_pos_y,get_angular_robot()
def get_map(frame):
    corners, ids,_ = detector.detectMarkers(frame)
    count = 0
    try:
        for corner, id in zip(corners, ids):
            count +=1
            id = int(np.mean(id))
            if id < 4:
                center[id - 1][0] = np.mean(corner[0, :, 0])
                center[id - 1][1] = np.mean(corner[0, :, 1])
                if id < 3:
                    center_angular[id - 1] = center[id - 1][:]
        if count == 3:
            return True
        else:
            return False
    except:
        print("cc")

def pos_robot(frame):
    corners, ids,_ = detector.detectMarkers(frame)
    count = False
    for corner, id in zip(corners, ids):
        id = int(np.mean(id))
        if id == 4:
            center[id - 1][0] = np.mean(corner[0, :, 0])
            center[id - 1][1] = np.mean(corner[0, :, 1])
            center_angular[id - 2] = center[id - 1][:]
        if id == 5:
            center_angular[id - 2][0] = np.mean(corner[0, :, 0])
            center_angular[id - 2][1] = np.mean(corner[0, :, 1])
            # print(center_angular)
            count = True
            break
        else:
            count = False
    if count:
        return distance()
    else:
        return False
def get_angular_robot():
    del_x12 = center_angular[0][0]-center_angular[1][0]
    del_y12 = center_angular[0][1]-center_angular[1][1]
    del_xrb = center_angular[2][0]-center_angular[3][0]
    del_yrb = center_angular[2][1]-center_angular[3][1]
    phi = np.abs(np.arctan2(del_y12,del_x12)-np.arctan2(del_yrb,del_xrb))/np.pi*180
    return phi


while True:#maping
    ret, frame = video.read()
    print(get_map(frame))
    if not ret:
        continue
    if get_map(frame):
        length_x = np.sqrt((center[0][0]-center[1][0])**2+(center[0][1]-center[1][1])**2)
        length_y = np.sqrt((center[0][0]-center[2][0])**2+(center[0][1]-center[2][1])**2)
        break

while True:
    ret, frame = video.read()
    print(pos_robot(frame))
video.release()
cv2.destroyAllWindows()