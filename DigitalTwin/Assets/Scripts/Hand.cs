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


    private bool boolCalibrar = false;
    private Material material;
    private float[] distance1;

    void Start()
    {
        offsetCamX = -30f;
        offsetCamY = -30f;
        offsetCamZ = -50f;


    }

    // Update is called once per frame
    void Update()
    {
        MovePoints();
        Linhas(); //Construção das falanges

    
        if(Input.GetKeyDown(KeyCode.C)) {
            boolCalibrar = !boolCalibrar;
            distance1 = Distancia(points);
            Calibrar();      
        }

        
        
        
        if(boolCalibrar) 
            for(int i = 0; i < points.Length; i++)
                points[i].GetComponent<Renderer>().material.SetColor("_Color", Color.green);
        
        else
            for(int i = 0; i < points.Length; i++)
                points[i].GetComponent<Renderer>().material.SetColor("_Color", Color.red);

        
    }

    void Calibrar() {
        distance1 = Distancia(points);
    }


    float[] Distancia(GameObject[] elements) {  

        float[] distanceBetweenPoints = new float[elements.Length];

        for(int i = 0; i < elements.Length; i++) {

            if(i == 0) {
                distanceBetweenPoints[i] = Vector3.Distance(elements[0].transform.position, elements[1].transform.position);
                i++;
                distanceBetweenPoints[i] = Vector3.Distance(elements[0].transform.position, elements[5].transform.position);
                i++;
                distanceBetweenPoints[i] = Vector3.Distance(elements[0].transform.position, elements[17].transform.position);
            }

            else if(i % 4 != 0 && i < 20) {
                distanceBetweenPoints[i] = Vector3.Distance(elements[i].transform.position, elements[i + 1].transform.position);
            } 

            else 
                distanceBetweenPoints[i] = Vector3.Distance(elements[5].transform.position, elements[9].transform.position);
                i++;
                distanceBetweenPoints[i] = Vector3.Distance(elements[9].transform.position, elements[13].transform.position);
                i++;
                distanceBetweenPoints[i] = Vector3.Distance(elements[13].transform.position, elements[17].transform.position);            
        } 

        return distanceBetweenPoints;

    }

    void MovePoints() {
  

        for(int i = 0; i < points.Length; i++) {

            float x = (float.Parse(receiver.position[i * 3]) / 10f) + offsetCamX;
            float y = (float.Parse(receiver.position[i * 3 + 1]) / -10f) - offsetCamY;
            float z = (float.Parse(receiver.position[i * 3 + 2]) / 3f) - offsetCamZ;


            Vector3 pos = new Vector3(x, y, z);  
                
            points[i].transform.position = Vector3.Lerp(points[i].transform.position, pos, 100f * Time.deltaTime);

            //if(distance1[i] < Distancia(points)[i])
           
        }
    }

    void Linhas() {
        for(int i = 0; i < linhas.Length; i++) {

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

            else if(i + 5 < linhas.Length) {
                linhas[i].SetPosition(0, points[i + 1].transform.localPosition);
                linhas[i].SetPosition(1, points[i + 5].transform.localPosition);

            }

            else {
                linhas[16].SetPosition(0, points[0].transform.localPosition);
                linhas[16].SetPosition(1, points[5].transform.localPosition);

                linhas[20].SetPosition(0, points[0].transform.localPosition);
                linhas[20].SetPosition(1, points[17].transform.localPosition);
            }
        }        
    }
}

