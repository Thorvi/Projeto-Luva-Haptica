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

    void Start()
    {
        udpClient = new UdpClient(port);

        udpClient.BeginReceive(ReceiveCallback, null);
    }

    public void ReceiveCallback(IAsyncResult ar)
    {
        // Obtém o endereço IP do remetente e a porta do pacote recebido
        IPEndPoint ip = new IPEndPoint(IPAddress.Any, port);
        byte[] data = udpClient.EndReceive(ar, ref ip);

        // Converte os dados recebidos em uma string
        string message = Encoding.UTF8.GetString(data);

        position = message.Split(',');

        udpClient.BeginReceive(ReceiveCallback, null);
    }


    private void OnApplicationQuit()
    {
        udpClient.Close();
    }
}