using System.Collections;
using System.Collections.Generic;
using System.IO.Ports;
using UnityEngine;

public class SerialController : MonoBehaviour
{
    // Start is called before the first frame update
    [Header("Serial Port")]
    [SerializeField] private string port;
    private SerialPort ESPSerialPort;
    private string[] data;
    void Start()
    {
        int baudRate = 115200;
        ESPSerialPort = new SerialPort(port, baudRate);
        ESPSerialPort.Open();
    }

    void Update()
    {
        ReadCOMPort();
    }

    void ReadCOMPort()
    {
        string rawData;

        if (!ESPSerialPort.IsOpen)
        {
            Debug.Log("Serial port unavailable");
            return;
        }
        
        rawData = ESPSerialPort.ReadLine();
        data = rawData.Split(", ");
        // Debug.Log(rawData);
    }
    
    void WriteCOMPort(string command)
    {

    }

    void OnDestroy()
    {
        if (ESPSerialPort.IsOpen)
        {
            ESPSerialPort.Close();  // Fecha a porta serial
        }
    }

    public string[] GetData()
    {
        //if(data.Length > 0)
        return data;
    }
}
