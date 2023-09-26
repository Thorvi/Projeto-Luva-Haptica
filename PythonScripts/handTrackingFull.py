import cv2
import socket
import numpy as np
import mediapipe as mp

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

fx = 200  # Valor de escala focal em pixels
fy = 200


constant_distance = 1

def estimate_depth(x, y, cx, cy):
    # Normaliza as coordenadas de pixel
    u_normalized = (x - cx) / fx
    v_normalized = (y - cy) / fy

    # Estimativa da coordenada Z
    z = constant_distance / np.sqrt(u_normalized**2 + v_normalized**2 + 1)

    return z

###########################################

with mp_hands.Hands(
    max_num_hands = 1,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7) as hands:
  
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
          #data.extend([format(landmark.x * largura, ".0f"), format(landmark.y * altura, ".0f"), format(estimate_depth(landmark.x * altura, landmark.y * largura, largura, altura), ".3f")])
          data.extend([format(landmark.x * largura, ".0f"), format(landmark.y * altura, ".0f"), 0])

        data[2] = data[5] #Fator de Correcao
        #data[5] = data[29]

        print(data[26])

  
        if(conectar):
          data_str = ','.join(map(str,data)).encode()
          sock.sendto(data_str, client)
          

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    
    if cv2.waitKey(5) & 0xFF == 27:
        cap.release()
        cv2.destroyAllWindows()
        break
        