using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Position : MonoBehaviour
{
    // Start is called before the first frame update
    public ReceiverTrackingData receiver;
    public Material material;

    Material materialAux;
    public bool pincou = false;
     
    void Start()
    {
        materialAux = material;

        transform.position = new Vector3(0f, 0f, 0f);
       
    }

    // Update is called once per frame
    void Update()
    {
        
        //Debug.Log(receiver.position[1]);

        float x = float.Parse(receiver.position[0]) / -50f;
        float y = float.Parse(receiver.position[1]) / -50f;
        float z = float.Parse(receiver.position[2]) / -30f;

        Vector3 pos = new Vector3(x, y, transform.position.z);
        //transform.position = Vector3.Lerp(transform.position, pos, 100f * Time.deltaTime);
        transform.position = pos;

        Pinca();
    }

    void Pinca() {

        float indicador_x = float.Parse(receiver.position[3]);
        float indicador_y = float.Parse(receiver.position[4]);
        float indicador_z = float.Parse(receiver.position[5]);

        float dedao_x = float.Parse(receiver.position[6]);
        float dedao_y = float.Parse(receiver.position[7]);
        float dedao_z = float.Parse(receiver.position[8]);

        float diferenca_x = Math.Abs(indicador_x - dedao_x);
        float diferenca_y = Math.Abs(indicador_y - dedao_y);

        if(diferenca_x < 10 && diferenca_y < 50) {
            pincou = true;
            Debug.Log("Pinçou");
            material.color = Color.Lerp(material.color, Color.green, 50);
        }
        else {
            pincou = false;
            material.color = Color.red;
        }


    }

    
}
