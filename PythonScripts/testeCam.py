import cv2
import pseyepy

# Inicializa o pseyepy
pseyepy.init()

# Obtém a lista de dispositivos
devices = pseyepy.get_devices()

# Verifica se há dispositivos conectados
if len(devices) == 0:
    print("Nenhum dispositivo PlayStation Eye encontrado.")
    exit()

# Abre o primeiro dispositivo encontrado
device = pseyepy.PSEye(devices[0])

# Inicializa a captura de vídeo
device.start()

while True:
    # Obtém o quadro de vídeo
    frame = device.get_frame()

    # Exibe o quadro de vídeo
    cv2.imshow('Câmera', frame)

    # Verifica se a tecla 'q' foi pressionada para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Para a captura de vídeo e fecha a janela
device.stop()
cv2.destroyAllWindows()
