using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HandRotate : MonoBehaviour
{
    [SerializeField] SerialController serialController;
    [SerializeField] GameObject hand;
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        string[] serialData = serialController.GetData();
        float[] data = new float[serialData.Length];

        for (int i = 0; i < serialData.Length; i++) {
            data[i] = float.Parse(serialData[i]) / 100;
        }

        Quaternion rotation = Quaternion.Euler(data[1], data[0], -data[2]);

        hand.transform.rotation = Quaternion.Lerp(hand.transform.rotation, rotation, 5f * Time.deltaTime);
    }
}
