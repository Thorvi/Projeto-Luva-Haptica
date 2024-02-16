using UnityEngine;

public class RotationTarget : MonoBehaviour
{
    public Transform center;  // O ponto central ou foco da órbita
    public float rotationSpeed = 1.0f;
    public float semiMajorAxis = 5.0f;  // Metade do comprimento maior da elipse
    public float semiMinorAxis = 3.0f;  // Metade do comprimento menor da elipse

    private float angle = 0.0f;

    void Update()
    {
        // Calcula a posição na órbita elíptica
        float y = center.position.y + semiMajorAxis * Mathf.Cos(angle);
        float z = center.position.z + semiMinorAxis * Mathf.Sin(angle);
        float x = center.position.x;

        // Atualiza a posição do objeto
        transform.position = new Vector3(x, y, z);

        // Incrementa o ângulo para movimento contínuo
        angle += rotationSpeed * Time.deltaTime;
    }
}
