const int dedao;
const int indicador;
const int dedoMeio;
const int anelar;
const int mindinho; 

const int tamanhoDoVetor = 5;
int dedos[tamanhoDoVetor];



void setup() {
  pinMode(dedao, OUTPUT);
  pinMode(indicador, OUTPUT);
  pinMode(dedoMeio, OUTPUT);
  pinMode(anelar, OUTPUT);
  pinMode(mindinho, OUTPUT);

  Serial.begin(9600);
}

void loop() {
   if (Serial.available()) {
    // Recebe os bytes enviados via porta serial
    byte bytesDoVetor[tamanhoDoVetor * sizeof(int)];
    Serial.readBytes(bytesDoVetor, sizeof(bytesDoVetor));

    // Reconstrói o vetor a partir dos bytes recebidos
    for (int i = 0; i < tamanhoDoVetor; i++) {
      dedos[i] = *((int*)&bytesDoVetor[i * sizeof(int)]);
    }   
  }

  delay(20);
}
