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

HOST = "localhost"  # endereço IP do servidor
PORT = 5005  # porta de conexão
client = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

###################################

################################### KALMAN FILTER
kalman = cv2.KalmanFilter(4, 2)  # Modelo com 4 estados e 2 observações

# Definindo a matriz de transição de estado
kalman.transitionMatrix = np.array(
    [[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.float32
)

# Definindo a matriz de observação
kalman.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], dtype=np.float32)

# Definindo a matriz de covariância do processo
kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 2

# Definindo a matriz de covariância da observação
kalman.measurementNoiseCov = np.eye(2, dtype=np.float32) * 0.05

###################################


def distancia(xa, ya, xb, yb):
    return ((xb - xa) ** 2 + (yb - ya) ** 2) ** 0.5


with mp_hands.Hands(
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
) as hands:
    while cap.isOpened():
        success, image = cap.read()
        altura, largura, _ = image.shape

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
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )

                data = []

                for landmark in hand_landmarks.landmark:
                    measurement = np.array(
                        [[landmark.x], [landmark.y]],
                        dtype=np.float32,
                    )
                    prediction = kalman.predict()
                    kalman.correct(measurement)
                    state = kalman.statePost

                    data.extend(
                        [
                            format(state[0, 0] * largura, ".0f"),
                            format(state[1, 0] * altura, ".0f"),
                        ]
                    )

                distanciaFixa = distancia(
                    float(data[0]), float(data[1]), float(data[34]), float(data[35])
                )

                cv2.circle(
                    image,
                    (int(data[18]), int(data[19])),
                    int(distanciaFixa * 0.1),
                    (255, 255, 0),
                    2,
                )

                pontos = []

                distanciaCorrigida = []
                pontos.extend([data[18], data[19]])
                pontos.extend([format(distanciaFixa * 0.2, ".3f")])

                for i in range(5):
                    pontoAtual = 8 * (i + 1)  # 4, 8, 12, 16, 20

                    if pontoAtual == 8: #A distancia do dedao deve ser calculada usando outro referencial
                        xa = int(data[34])
                        ya = int(data[35])
                        print("Dedao")
                    else:
                        xa = int(data[0])
                        ya = int(data[1])

                    xb = int(data[pontoAtual])
                    yb = int(data[pontoAtual + 1])

                    distanciaAux = distancia(xa, ya, xb, yb)

                    distanciaCorrigida.extend(
                        [format(distanciaAux / distanciaFixa, ".2f")]
                    )

                    cv2.line(image, (xa, ya), (xb, yb), (255, 0, 0), thickness=2)

                pontos.extend(distanciaCorrigida)
                #print("\n", pontos)

                if conectar:
                    data_str = ",".join(map(str, pontos)).encode()
                    sock.sendto(data_str, client)

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow("MediaPipe Hands", cv2.flip(image, 1))

        if cv2.waitKey(5) & 0xFF == 27:
            cap.release()
            cv2.destroyAllWindows()
            break
