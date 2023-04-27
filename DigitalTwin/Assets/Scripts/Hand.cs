using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Hand : MonoBehaviour
{
    public ReceiverTrackingData receiver;

    public  GameObject[] points;
    public  LineRenderer[] linhas;
    

    public float offsetCamX;
    public float offsetCamY;
    public float offsetCamZ;

    void Start()
    {
        offsetCamX = -30f;
        offsetCamY = -30f;
        offsetCamZ = -40f;
    }

    // Update is called once per frame
    void Update()
    {
        Points();
        //Linhas();

        
    }

    void Points() {
        for(int i = 0; i < 21; i++) {

            float x = (float.Parse(receiver.position[i * 3]) / 10f) + offsetCamX;
            float y = (float.Parse(receiver.position[i * 3 + 1]) / -10f) - offsetCamY;
            float z = (float.Parse(receiver.position[i * 3 + 2]) / 700000f) - offsetCamZ;

            

            //points[i].transform.localPosition = new Vector3(x, y, z);

            Vector3 pos = new Vector3(x, y, z);
            

            points[i].transform.position = Vector3.Lerp(points[i].transform.position, pos, 17f * Time.deltaTime);
 
            Linhas();
        }

        
    }

    void Linhas() {
        for(int i = 0; i < 21; i++) {
            linhas[i].startWidth = 1f;
            linhas[i].endWidth = 1f;
            
            //  linhas 0, 4, 8, 12, 16, 20
            if(i == 0) {
                linhas[0].SetPosition(0, points[0].transform.position);
                linhas[0].SetPosition(1, points[1].transform.position);
            }

            else if(i % 4 != 0) {
                linhas[i].SetPosition(0, points[i].transform.position);
                linhas[i].SetPosition(1, points[i + 1].transform.position);
            }
            else if(i != 20) {
                linhas[i].SetPosition(0, points[i + 1].transform.position);
                linhas[i].SetPosition(1, points[i + 2].transform.position);
            }

            if(i == 5 || i == 17) {
                linhas[i].SetPosition(0, points[0].transform.localPosition);
                linhas[i].SetPosition(1, points[i].transform.localPosition);
            }

            else {
                linhas[9].SetPosition(0, points[5].transform.localPosition);
                linhas[9].SetPosition(1, points[9].transform.localPosition);

                linhas[13].SetPosition(0, points[9].transform.localPosition);
                linhas[13].SetPosition(1, points[13].transform.localPosition);

                linhas[20].SetPosition(0, points[9].transform.localPosition);
                linhas[20].SetPosition(1, points[13].transform.localPosition);
            }

        }

        
    }
}

