using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Linhas : MonoBehaviour
{
    LineRenderer linha;

    public Transform inicio;
    public Transform fim;
    

    void Start()
    {
        linha = GetComponent<LineRenderer>();
        linha.startWidth = 0.5f;
        linha.endWidth = 0.5f;
    }

    // Update is called once per frame
    void Update()
    {
        linha.SetPosition(0, inicio.position);
        linha.SetPosition(1, fim.position);
    }
}
