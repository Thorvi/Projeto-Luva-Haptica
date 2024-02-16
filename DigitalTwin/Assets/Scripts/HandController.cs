using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HandController : MonoBehaviour
{
    public ReceiverTrackingData receiver;
    public GameObject hand;


    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (receiver.position.Length > 0)
        {
            float x = (float.Parse(receiver.position[0]) / 10.3f);
            float y = (float.Parse(receiver.position[1]) / -10.3f);
            float z = (float.Parse(receiver.position[2]) / 500f);


            Vector3 position = new Vector3(x, y, z);

            hand.transform.position = Vector3.Lerp(hand.transform.position, position, 5f * Time.deltaTime);
        }
    }

    void remap(float valor, float intervaloInf, float intervaloSup) {

    }
}
