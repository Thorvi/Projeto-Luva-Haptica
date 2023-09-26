import cv2
import socket
import numpy as np
from utils import DLT, get_projection_matrix

def ServidorSend(data):
    Host = 'localhost'
    Port = 5005
    client = (Host, Port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data_str = ','.join(map(str,data)).encode()
    sock.sendto(data_str, client)

def Contornos(tracking, cam1, cam2):
    centroTracker1 = (0,0)
    centroTracker2 = (0,0)

    cap1 = cv2.VideoCapture(cam1)
    cap2 = cv2.VideoCapture(cam2)

    lower_range = tracking[0]
    upper_range = tracking[1]
    kernel = np.ones((5,5), np.uint8)

 
    if not (cap1.isOpened() and cap2.isOpened()):
        print("Erro ao abrir uma das Cameras")
        return
        
    while (cap1.isOpened() and cap1.isOpened()):
        success1, frame1 = cap1.read()
        success2, frame2 = cap2.read()

        if not (success1 and success2):
            print("Erro ao capturar quadro de uma das Cameras")
            return

        image1 = cv2.flip(frame1, 1)
        image2 = cv2.flip(frame2, 1)

        hsv1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(hsv1, lower_range, upper_range)
        mask1 = cv2.erode(mask1, kernel, iterations = 1)
        mask1 = cv2.dilate(mask1, kernel, iterations = 2)

        hsv2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)

        mask2 = cv2.inRange(hsv2, lower_range, upper_range)
        mask2 = cv2.erode(mask2, kernel, iterations = 1)
        mask2 = cv2.dilate(mask2, kernel, iterations = 2)

        contours1, hierarchy1 = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours1 and cv2.contourArea(max(contours1, key = cv2.contourArea)) > 1:
            contour = max(contours1, key = cv2.contourArea)
            x, y, w, h = cv2.boundingRect(contour)

            centroTracker1 = ((2*x + w) // 2, (2*y + h)//2)

            cv2.rectangle(image1, (x, y), (x+w, y+h), (0, 25, 255), 2)
            cv2.circle(image1, centroTracker1, 2, (255, 0, 0), 2)

        contours2, hierarchy2 = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours2 and cv2.contourArea(max(contours2, key = cv2.contourArea)) > 1:
            contour = max(contours2, key = cv2.contourArea)
            x, y, w, h = cv2.boundingRect(contour)

            centroTracker2 = ((2*x + w) // 2, (2*y + h)//2)

            cv2.rectangle(image2, (x, y), (x+w, y+h), (0, 25, 255), 2)
            cv2.circle(image2, centroTracker2, 2, (255, 0, 0), 2)
        
        pos = DLT(P1, P2, centroTracker1, centroTracker2)
    
        #pos = np.vectorize(pos)
        
        

        imagens = cv2.vconcat([image1, image2])
        cv2.imshow("Imagens", imagens)
        
        ServidorSend(data = pos)

        if cv2.waitKey(5) & 0xFF == 27:
            break

if __name__ == '__main__':
    P1 = get_projection_matrix(0)
    P2 = get_projection_matrix(1)

    tracking = np.load('cor.npy')

    
    Contornos(tracking, 0, 1)

    
    



