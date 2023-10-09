import cv2
import socket
import numpy as np
import mediapipe as mp
import math

cap = cv2.VideoCapture(0)

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

def distancia(xa, ya, xb, yb):
  return ((xb-xa)**2 + (yb-ya)**2)**0.5

with mp_hands.Hands(
    max_num_hands = 1,
    model_complexity=1,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9) as hands:
  
  while cap.isOpened():
    success, image = cap.read()
    altura, largura, _ = image.shape

    #print(altura, largura)

    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks: 
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        data = []
        
        for landmark in hand_landmarks.landmark:
          
          data.extend([format(landmark.x * largura, ".0f"), format(landmark.y * altura, ".0f")])

        distanciaFixa = distancia(float(data[0]),float(data[1]), float(data[34]), float(data[35]))
        

        cv2.circle(image, (int(data[18]), int(data[19])), int(distanciaFixa * 0.1), (255, 255, 0), 2)

        pontos = []
        
        distanciaCorrigida = []
        pontos.extend([data[18], data[19]])
        pontos.extend([format(distanciaFixa * 0.2, ".3f")])

        for i in range(5):
          pontoAtual = 8 * (i + 1) # 4, 8, 12, 16, 20
          

          xa = int(data[0])
          ya = int(data[1])

          xb = int(data[pontoAtual])
          yb = int(data[pontoAtual + 1])

          distanciaAux = distancia(xa, ya, xb, yb)

          distanciaCorrigida.extend([format(distanciaAux / distanciaFixa, ".3f")])
          

          cv2.line(image, (xa, ya), (xb, yb), (255, 0, 0), thickness = 2)
          
        
        pontos.extend(distanciaCorrigida)
        print("\n", pontos)
          
       
  
        if(conectar):
          data_str = ','.join(map(str, pontos)).encode()
          sock.sendto(data_str, client)
          

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    
    if cv2.waitKey(5) & 0xFF == 27:
        cap.release()
        cv2.destroyAllWindows()
        break
        