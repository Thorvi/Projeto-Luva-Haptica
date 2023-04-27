import cv2
import socket
import mediapipe as mp

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



cap = cv2.VideoCapture(0)

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

        
        ###   PUNHO  
        punho_x = format(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * largura, ".0f")
        punho_y = format(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * altura, ".0f")
        punho_z = format(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].z * largura * altura * 50, ".5f")
        '''
        ###   INDICADOR
        indicador_x = format(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * largura, ".0f")
        indicador_y = format(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * altura, ".0f")
        indicador_z = format(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].z * largura * altura * 100000, ".0f")

        ###   INDICADOR
        dedao_x = format(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * largura, ".0f")
        dedao_y = format(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * altura, ".0f")
        dedao_z = format(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].z * largura * altura * 100000, ".0f")
        '''
        data = []
        for landmark in hand_landmarks.landmark:
          data.extend([format(landmark.x * largura, ".0f"), format(landmark.y * altura, ".0f"), format(landmark.z, ".8f")])

        data[2] = data[5]
        #data[5] = data[29]

        print(data)

  
        if(conectar):
          data_str = ','.join(map(str,data)).encode()
          sock.sendto(data_str, client)
          

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()