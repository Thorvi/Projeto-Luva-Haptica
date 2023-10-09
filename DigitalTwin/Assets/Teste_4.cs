using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Teste_4 : MonoBehaviour
{
    // Start is called before the first frame update
    public ReceiverTrackingData receiver;

    public  GameObject Objeto;
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        float x = float.Parse(receiver.position[0]) / -2.5f;
        float y = float.Parse(receiver.position[1]) / -2.5f;
        float z = float.Parse(receiver.position[2]) / 25f;


            Vector3 pos = new Vector3(x, y, z);  
                
            Objeto.transform.position = Vector3.Lerp(Objeto.transform.position, pos, 10f * Time.deltaTime);
        
    }   
}