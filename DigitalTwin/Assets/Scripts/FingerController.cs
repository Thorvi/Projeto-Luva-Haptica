using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Animations.Rigging;

public class FingerController : MonoBehaviour
{
    [SerializeField] ReceiverTrackingData receiver;
    [SerializeField] ChainIKConstraint dedao;
    [SerializeField] ChainIKConstraint indicador;
    [SerializeField] ChainIKConstraint meio;
    [SerializeField] ChainIKConstraint anelar;
    [SerializeField] ChainIKConstraint mindinho;

    [SerializeField] int iterations = 50;

    float[] dedaoValues = { 0, 0 };
    float[] indicadorValues = { 0, 0 };
    float[] meioValues = { 0, 0 };
    float[] anelarValues = { 0, 0 };
    float[] mindinhoValues = { 0, 0 };

    


    void Start()
    {
        StartCoroutine(Calibrar());
    }
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.C))
        {
            Debug.Log("C Apertado.");
            StartCoroutine(Calibrar());
        }
        else
            Fingers();
    }
    void Fingers()
    {
        //receiver.position = 0   1   2   3   4   5   6   7
        //                    x   y   z   d1  d2  d3  d4  d5
        if (receiver.position.Length > 0)
        {
            dedao.weight = 1 - Remap((float.Parse(receiver.position[3]) / 100f), dedaoValues[0], dedaoValues[1]);
            indicador.weight = 1 - Remap((float.Parse(receiver.position[4]) / 100f), indicadorValues[0], indicadorValues[1]);
            meio.weight = 1 - Remap((float.Parse(receiver.position[5]) / 100f), meioValues[0], meioValues[1]);
            anelar.weight = 1 - Remap((float.Parse(receiver.position[6]) / 100f), anelarValues[0], anelarValues[1]);
            mindinho.weight = 1 - Remap((float.Parse(receiver.position[7]) / 100f), mindinhoValues[0], mindinhoValues[1]);
        }

    }

    float Remap(float value, float minIn, float maxIn)
    { //Y = (X-A)/(B-A) * (D-C) + C -> c = 0, d = 1
        return ((value - minIn) / (maxIn - minIn)) * 2;
    }

    IEnumerator Calibrar()
    {
        

        float[] dedaoCalib = new float[iterations]; // min: 0 - 24; max: 25 - 49
        float[] indicadorCalib = new float[iterations];
        float[] meioCalib = new float[iterations];
        float[] anelarCalib = new float[iterations];
        float[] mindinhoCalib = new float[iterations];

        

        //TODO: Mensagens de log no Canvas do jogo
        Debug.Log("****Calibracao Iniciada");
        Debug.Log("Feche sua mão e aperte ESPAÇO em seu teclado");

        yield return new WaitUntil(() => Input.GetKeyDown(KeyCode.Space));

        for (int i = 0; i < (iterations / 2); i++)
        {
            dedaoCalib[i] = float.Parse(receiver.position[3]) / 100f;
            indicadorCalib[i] = float.Parse(receiver.position[4]) / 100f;
            meioCalib[i] = float.Parse(receiver.position[5]) / 100f;
            anelarCalib[i] = float.Parse(receiver.position[6]) / 100f;
            mindinhoCalib[i] = float.Parse(receiver.position[7]) / 100f;
        }

        //TODO: Mensagens de log no Canvas do jogo
        Debug.Log("Abra sua mão e aperte ESPAÇO novamente");
        yield return new WaitUntil(() => Input.GetKeyUp(KeyCode.Space));
        yield return new WaitUntil(() => Input.GetKeyDown(KeyCode.Space));

        for (int i = (iterations / 2); i < iterations; i++)
        {
            dedaoCalib[i] = float.Parse(receiver.position[3]) / 100f;
            indicadorCalib[i] = float.Parse(receiver.position[4]) / 100f;
            meioCalib[i] = float.Parse(receiver.position[5]) / 100f;
            anelarCalib[i] = float.Parse(receiver.position[6]) / 100f;
            mindinhoCalib[i] = float.Parse(receiver.position[7]) / 100f;
        }

        for (int i = 0; i < (iterations / 2); i++)
        {
            //Min values
            dedaoValues[0] += dedaoCalib[i];
            indicadorValues[0] += indicadorCalib[i];
            meioValues[0] += meioCalib[i];
            anelarValues[0] += anelarCalib[i];
            mindinhoValues[0] += mindinhoCalib[i];

            //Max values
            dedaoValues[1] += dedaoCalib[i + (iterations / 2)];
            indicadorValues[1] += indicadorCalib[i + (iterations / 2)];
            meioValues[1] += meioCalib[i + (iterations / 2)];
            anelarValues[1] += anelarCalib[i + (iterations / 2)];
            mindinhoValues[1] += mindinhoCalib[i + (iterations / 2)];
        }

        //Media dos Min Values
        dedaoValues[0] = dedaoValues[0] / (iterations / 2);
        indicadorValues[0] = indicadorValues[0] / (iterations / 2);
        meioValues[0] = meioValues[0] / (iterations / 2);
        anelarValues[0] = anelarValues[0] / (iterations / 2);
        mindinhoValues[0] = mindinhoValues[0] / (iterations / 2);

        //Media dos Max Values
        dedaoValues[1] = dedaoValues[1] / (iterations / 2);
        indicadorValues[1] = indicadorValues[1] / (iterations / 2);
        meioValues[1] = meioValues[1] / (iterations / 2);
        anelarValues[1] = anelarValues[1] / (iterations / 2);
        mindinhoValues[1] = mindinhoValues[1] / (iterations / 2);

        //TODO: Mensagens de log no Canvas do jogo
        Debug.Log("Calibracao Encerrada");

    }




}
