import cv2
import socket
import numpy as np
import mediapipe as mp
from scipy import linalg
from utils import DLT, get_projection_matrix

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

conectar = True

################################### SERVIDOR

HOST = 'localhost'    # endereço IP do servidor
PORT = 5005  # porta de conexão
client = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

###################################



###########################################

def mp(P1, P2):
    #with mp_hands.Hands(max_num_hands = 1, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.7) as hands:
    hand1 = mp_hands.Hands(max_num_hands = 1, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.7)
    hand2 = mp_hands.Hands(max_num_hands = 1, model_complexity=1, min_detection_confidence=0.5, min_tracking_confidence=0.7)
    
    if True:
        
        while cap1.isOpened() & cap2.isOpened():
            success1, image1 = cap1.read()
            success2, image2 = cap2.read()
            
            altura, largura, _ = image1.shape #As duas cameras devem ter as mesmas proporcoes

            if not success1 and not success2:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image1.flags.writeable = False
            image2.flags.writeable = False
            
            image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
            results1 = hand1.process(image1)
            
            image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
            results2 = hand2.process(image2)

            # Draw the hand annotations on the image.
  

            if results1.multi_hand_landmarks and results2.multi_hand_landmarks:
                
                for hand_landmarks1 in results1.multi_hand_landmarks: 
                    mp_drawing.draw_landmarks(image1, hand_landmarks1, mp_hands.HAND_CONNECTIONS)

                    data1 = []
                    
                    for landmark in hand_landmarks1.landmark:
                        data1.extend([format(landmark.x * largura, ".0f"), format(landmark.y * altura, ".0f")])


                    data1[2] = data1[5] #Fator de Correcao
                    
                for hand_landmarks2 in results2.multi_hand_landmarks: 
                    mp_drawing.draw_landmarks(image2, hand_landmarks2, mp_hands.HAND_CONNECTIONS)

                    data2 = []
                    
                    for landmark in hand_landmarks2.landmark:
                        data2.extend([format(landmark.x * largura, ".0f"), format(landmark.y * altura, ".0f")])


                    data2[2] = data2[5] #Fator de Correcao

                for i in range(40):
                    
                    dataZ = []
                    tupla1 = []
                    tupla2 = []
                    
                    tupla1 = np.float64((data1[i], data1[i + 1]))
                    tupla2 = np.float64((data2[i], data2[i + 1]))
                    
                    dataZ.extend(DLT(P1, P2, tupla1, tupla2))
                    
                    print(dataZ[0])
                    
                k = 0
                
                for hand_landmarks2 in results2.multi_hand_landmarks: 
                   

                    dataFull = []
                    
                    for landmark in hand_landmarks2.landmark:
                        dataFull.extend([format(landmark.x * largura, ".0f"), format(landmark.y * altura, ".0f"), format(dataZ[k], ".0f")])  

                        if k < hand_landmarks2.length: 
                            k = k + 1
                    
                    if(conectar):
                        data_str = ','.join(map(str,dataFull)).encode()
                        sock.sendto(data_str, client)
                        
                    
                

            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', cv2.flip(image1, 1))
            
            if cv2.waitKey(5) & 0xFF == 27:
                cap1.release()
                cap2.release()
                cv2.destroyAllWindows()
                break

if __name__ == '__main__':
    
    P1 = get_projection_matrix(0)
    P2 = get_projection_matrix(1)
    
