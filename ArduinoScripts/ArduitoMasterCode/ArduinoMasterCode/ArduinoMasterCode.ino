// The function GetQuaternion is Mahony_Update in https://github.com/jremington/MPU-6050-Fusion

#include <Wire.h>
#include <BluetoothSerial.h>

#define bluetoothCommunication true
#define bluetoothName "CLIENT-HANDS"
#define bluetoothPin "1234"
#define sizeData 3

#define MPU_addr 0x68
#define gscale ((250./32768.0)*(PI/180.0))

#define CALIB_ITERATIONS 600

float A_off[6] = {0.0, 0.0, 0.0, 1.000, 1.000, 1.000};
float G_off[3] = {0.0, 0.0, 0.0};


float quaternion[4] = {1.0, 0.0, 0.0, 0.0};
float Ki = 0.005;
float Kp = 60;
float gzAux = 0;

BluetoothSerial SerialBT;

void BluetoothConnect();
void CalibSensor();
void ToQuaternion(float aX, float aY, float aZ, float gX, float gY, float gZ);
void InitSensor();
void ReadSensorMeasurements();
void CalculateYPR(float ypr[]);
void SendData(float data[]);


void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  BluetoothConnect();
  InitSensor();
  
  // CalibSensor();
}

void loop() {
  float measurements[6];
  float ypr[3];
  
  static float deltaT = 0;
  static unsigned long now, last;

  ReadSensorMeasurements(measurements);
  
  now = micros();
  deltaT = (now - last) * 1.0e-6;
  delay(50);
  last = now;
  
  ToQuaternion(measurements, deltaT);
  CalculateYPR(ypr);
  SendData(ypr);
}

void InitSensor() {
  Wire.begin();
  Wire.beginTransmission(MPU_addr); 
  Wire.write(0x6B);
  Wire.write(0);  
  Wire.endTransmission(true);
}

void CalibSensor() {
  Serial.println("###################   CALIBRATION   ###################");

  float Axyz[3] = {0.0, 0.0, 0.0};
  float Gxyz[3] = {0.0, 0.0, 0.0};
  float AGxyz[6] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};

  for(int i = 0; i < CALIB_ITERATIONS; i++) {
    ReadSensorMeasurements(AGxyz);

    if(i < (CALIB_ITERATIONS / 3)) {          // X index
      Axyz[0] += AGxyz[0];
      Gxyz[0] += AGxyz[3];
    }

    else if(i < 2 * (CALIB_ITERATIONS / 3)) { // Y index
      Axyz[1] += AGxyz[1];
      Gxyz[1] += AGxyz[4];
    }

    else if(i < 3 * (CALIB_ITERATIONS / 3)) { // Z index
      Axyz[2] += AGxyz[2];
      Gxyz[2] += AGxyz[5];
    }
  }

  A_off[0] = Axyz[0] / (CALIB_ITERATIONS / 3);
  A_off[1] = Axyz[1] / (CALIB_ITERATIONS / 3);
  A_off[2] = Axyz[2] / (CALIB_ITERATIONS / 3);

  G_off[0] = Gxyz[0] / (CALIB_ITERATIONS / 3);
  G_off[1] = Gxyz[1] / (CALIB_ITERATIONS / 3);
  G_off[2] = Gxyz[2] / (CALIB_ITERATIONS / 3);

  Serial.print("Acc calib: ");
  for(int i = 0; i < 3; i++) {

    Serial.print(A_off[i]);
    Serial.print(" ");
  }
  Serial.println();

  Serial.print("Gyro calib: ");
  for(int i = 0; i < 3; i++) {
    
    Serial.print(G_off[i]);
    Serial.print(" ");
  }
  Serial.println();
}

void ReadSensorMeasurements(float AGxyz[]) {

  // float AGxyz[6]; //0..2 Axyz, 3..5 Gxyz
  int16_t ax, ay, az, gx, gy, gz, tmp;

  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr, 14); // request a total of 14 registers

  int t = Wire.read() << 8;

  ax = t | Wire.read(); // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  t = Wire.read() << 8;
  ay = t | Wire.read(); // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  t = Wire.read() << 8;
  az = t | Wire.read(); // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  t = Wire.read() << 8;
  tmp = t | Wire.read(); // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  t = Wire.read() << 8;
  gx = t | Wire.read(); // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  t = Wire.read() << 8;
  gy = t | Wire.read(); // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  t = Wire.read() << 8;
  gz = t | Wire.read(); // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)

  AGxyz[0] = (float) ax;
  AGxyz[1] = (float) ay;
  AGxyz[2] = (float) az;

  for (int i = 0; i < 3; i++) {
    AGxyz[i] = (AGxyz[i] - A_off[i]) * A_off[i + 3];
  }

  AGxyz[3] = ((float) gx - G_off[0]) * gscale;
  AGxyz[4] = ((float) gy - G_off[1]) * gscale;
  AGxyz[5] = ((float) gz - G_off[2]) * gscale;
}

void CalculateYPR(float ypr[]) {
  float yaw, pitch, roll;
  
  yaw   = -atan2((quaternion[1] * quaternion[2] + quaternion[0] * quaternion[3]), 0.5 - (quaternion[2] * quaternion[2] + quaternion[3] * quaternion[3]));
  pitch = asin(2.0 * (quaternion[0] * quaternion[2] - quaternion[1] * quaternion[3]));
  roll  = atan2((quaternion[0] * quaternion[1] + quaternion[2] * quaternion[3]), 0.5 - (quaternion[1] * quaternion[1] + quaternion[2] * quaternion[2]));
 
  yaw *= 180.0 / PI;
  pitch *= 180.0 / PI;
  roll *= 180.0 / PI;

  ypr[0] = yaw;
  ypr[1] = pitch;
  ypr[2] = roll;
}

void SendData(float data[]) {

  if(bluetoothCommunication)
      SerialBT.write((uint8_t*)data, sizeData * sizeof(float));

  for (int i = 0; i < sizeData; i++) {

    Serial.print(data[i]);

    if (i != sizeData - 1) {
      Serial.print(", ");
    } 
    else {
      Serial.println("");
    }
  }
}

void BluetoothConnect() {
  if(bluetoothCommunication) {
    SerialBT.begin(bluetoothName);
    SerialBT.setPin(bluetoothPin);

    do {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(500);
      digitalWrite(LED_BUILTIN, LOW);
      delay(500);
    } 
    while (!SerialBT.connected());

    digitalWrite(LED_BUILTIN, LOW);
  }
}

void ToQuaternion(float AGxyz[], float deltaT) {
  float recipNorm;
  float ax = AGxyz[0], 
        ay = AGxyz[1], 
        az = AGxyz[2];
  float gx = AGxyz[3], 
        gy = AGxyz[4], 
        gz = AGxyz[5];
  float vx, vy, vz;
  float ex, ey, ez;  //error terms
  float qa, qb, qc;
  static float ix = 0.0, iy = 0.0, iz = 0.0;  //integral feedback terms
  float tmp;

  // Compute feedback only if accelerometer measurement valid (avoids NaN in accelerometer normalisation)
  tmp = ax * ax + ay * ay + az * az;
  if (tmp > 0.0)
  {

    // Normalise accelerometer (assumed to measure the direction of gravity in body frame)
    recipNorm = 1.0 / sqrt(tmp);
    ax *= recipNorm;
    ay *= recipNorm;
    az *= recipNorm;

    // Estimated direction of gravity in the body frame (factor of two divided out)
    vx = quaternion[1] * quaternion[3] - quaternion[0] * quaternion[2];  //to normalize these terms, multiply each by 2.0
    vy = quaternion[0] * quaternion[1] + quaternion[2] * quaternion[3];
    vz = quaternion[0] * quaternion[0] - 0.5f + quaternion[3] * quaternion[3];

    // Error is cross product between estimated and measured direction of gravity in body frame
    // (half the actual magnitude)
    ex = (ay * vz - az * vy);
    ey = (az * vx - ax * vz);
    ez = (ax * vy - ay * vx);

    // Compute and apply to gyro term the integral feedback, if enabled
    if (Ki > 0.0f) {
      ix += Ki * ex * deltaT;  // integral error scaled by Ki
      iy += Ki * ey * deltaT;
      iz += Ki * ez * deltaT;
      gx += ix;  // apply integral feedback
      gy += iy;
      gz += iz;
    }

    // Apply proportional feedback to gyro term
    gx += Kp * ex;
    gy += Kp * ey;
    gz += Kp * ez;
  }

  // gzAux = gz;

  // if(abs(gz - gzAux) < 0.01)
  //   Serial.print(gz);
    

  // Integrate rate of change of quaternion, q cross gyro term
  deltaT = 0.5 * deltaT;
  gx *= deltaT;   // pre-multiply common factors
  gy *= deltaT;
  gz *= deltaT;
  qa = quaternion[0];
  qb = quaternion[1];
  qc = quaternion[2];
  quaternion[0] += (-qb * gx - qc * gy - quaternion[3] * gz);
  quaternion[1] += (qa * gx + qc * gz - quaternion[3] * gy);
  quaternion[2] += (qa * gy - qb * gz + quaternion[3] * gx);
  quaternion[3] += (qa * gz + qb * gy - qc * gx);

  // renormalise quaternion
  recipNorm = 1.0 / sqrt(quaternion[0] * quaternion[0] + quaternion[1] * quaternion[1] + quaternion[2] * quaternion[2] + quaternion[3] * quaternion[3]);
  quaternion[0] = quaternion[0] * recipNorm;
  quaternion[1] = quaternion[1] * recipNorm;
  quaternion[2] = quaternion[2] * recipNorm;
  quaternion[3] = quaternion[3] * recipNorm;
}