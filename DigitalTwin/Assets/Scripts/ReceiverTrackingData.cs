using UnityEngine;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

public class ReceiverTrackingData : MonoBehaviour
{
    public string[] position;
    
    public int port = 5005;

    private UdpClient udpClient;
    public string message;

    private void Start()
    {
        // Cria o objeto UdpClient e associa-o à porta especificada
        udpClient = new UdpClient(port);

        // Inicia a recepção assíncrona de dados
        udpClient.BeginReceive(ReceiveCallback, null);
    }

    public void ReceiveCallback(IAsyncResult ar)
    {
        // Obtém o endereço IP do remetente e a porta do pacote recebido
        IPEndPoint ip = new IPEndPoint(IPAddress.Any, port);
        byte[] data = udpClient.EndReceive(ar, ref ip);

        // Converte os dados recebidos em uma string
        string message = Encoding.UTF8.GetString(data);

        // Faz algo com a mensagem recebida
        position = message.Split(',');

        //Debug.Log("Vetor Position " + position.Length);

        //Debug.Log("Mensagem recebida: " + message);

        // Inicia a recepção assíncrona de dados novamente
        udpClient.BeginReceive(ReceiveCallback, null);
    }


    private void OnApplicationQuit()
    {
        // Fecha o objeto UdpClient quando a aplicação for encerrada
        udpClient.Close();
    }
}