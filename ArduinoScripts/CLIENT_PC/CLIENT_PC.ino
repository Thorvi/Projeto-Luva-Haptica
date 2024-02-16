#include <BluetoothSerial.h>

#define bluetoothName "SERVER-PC"
#define bluetoothHands "CLIENT-HANDS"
#define bluetoothPin "1234"
#define sizeReceivedData 3

BluetoothSerial SerialBT;



void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  BluetoothConnect();
  Serial.begin(115200);
  //Serial.setRxBufferSize(1024);
}

void loop() { 
  // if(Serial.available()) {
  //   SerialBT.print(Serial.read());
  // }
  float data[sizeReceivedData];


  if (SerialBT.available() > 0) {

    for (int i = 0; i < sizeReceivedData * sizeof(float); i += sizeof(float)) {
      SerialBT.readBytes((char*)&data[i / sizeof(float)], sizeof(float));
    }

    for (int j = 0; j < sizeReceivedData; j++) {
      Serial.print(data[j]);

      if (j != sizeReceivedData - 1) {
        Serial.print(", ");
      } 
      else {
        Serial.println("");
      }
    }

    delay(1);
  }
}

void BluetoothConnect() {
  SerialBT.begin(bluetoothName, true);
  SerialBT.setPin(bluetoothPin);

  do {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
  } while (!SerialBT.connect(bluetoothHands));

  digitalWrite(LED_BUILTIN, LOW);
}
