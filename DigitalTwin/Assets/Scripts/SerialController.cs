using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO.Ports;

public class SerialController : MonoBehaviour
{
    public GameObject[] dedos;

    public string porta = "COM5";
    public int taxaDeTransmissao = 9600;

    private SerialPort portaSerial;

    private bool[] dedosTouch;

    void Start()
    {
        portaSerial = new SerialPort(porta, taxaDeTransmissao);
        portaSerial.Open();

        dedosTouch = new bool[dedos.Length];
    }

    // Update is called once per frame
    void Update() {

        int i = 0;

        foreach (GameObject obj in dedos) {
            
            Colisor Colisor = obj.GetComponent<Colisor>();

            dedosTouch[i] = Colisor.touch;
            i++;
        }

        EnviarDados(dedosTouch);
    }

    void EnviarDados(bool[] dado) {

        byte[] bytesDoVetor = new byte[dado.Length];

        for (int i = 0; i < dado.Length; i++)
        {
            bytesDoVetor[i] = dado[i] ? (byte)1 : (byte)0;
        }

        // Envia a sequência de bytes pela porta serial
        portaSerial.Write(bytesDoVetor, 0, bytesDoVetor.Length);
    }
}
