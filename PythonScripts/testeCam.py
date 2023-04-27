import socket
import json
import time

HOST = ''    # endereço IP do servidor
PORT = 5005  # porta de conexão

# cria o socket do servidor e faz a ligação com o endereço e porta
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Conexão estabelecida com', addr)

        while True:
            # obtém os dados do Mediapipe ou de qualquer outra fonte
            # e os armazena em uma variável
            tracking_data = 'x:1.23,y:4.56,z:7.89'

            # envia os dados para a Unity
            conn.sendall(tracking_data.encode())

            # aguarda um tempo antes de enviar novos dados
            time.sleep(0.1)
