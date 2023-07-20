using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Ossos : MonoBehaviour
{
    public GameObject[] Linhas;
    public GameObject[] Osso;
    void Start()
    {
        
    }

    
    void Update()
    {
        for(int i = 0; i < Linhas.Length; i++) {
            
            Renderer r = Linhas[i].GetComponent<Renderer>();

           // Osso[i].transform.position = r.bounds.center;
            //Osso[i].transform.position = r.transform.position;
            Osso[i].transform.position = Linhas[i].transform.position;
           // Osso[i].transform.rotation = Linhas[i].transform.rotation;
        }
    }
}
