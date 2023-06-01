import cv2
import numpy as np

# Parâmetros intrínsecos da câmera (obtidos por calibração)
fx = 500  # Valor de escala focal em pixels
fy = 500
cx = 320  # Coordenada do ponto principal (centro óptico) em pixels
cy = 240

# Distância fixa entre a câmera e a mão (em centímetros)
constant_distance = 50.0

def estimate_depth(x, y):
    # Normaliza as coordenadas de pixel
    u_normalized = (x - cx) / fx
    v_normalized = (y - cy) / fy

    # Estimativa da coordenada Z
    z = constant_distance / np.sqrt(u_normalized**2 + v_normalized**2 + 1)

    return z

def main():
    # Inicializa a câmera
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # Detecta as mãos no quadro usando o MediaPipe ou outros métodos

        # Exemplo de coordenadas de landmark da mão (X e Y)
        x = 300
        y = 200

        # Estima a coordenada Z
        z = estimate_depth(x, y)

        # Exibe as coordenadas (X, Y, Z) na imagem
        cv2.putText(frame, f"X: {x}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Y: {y}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Z: {z:.2f} cm", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Exibe o quadro
        cv2.imshow('Hand Depth Estimation', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
