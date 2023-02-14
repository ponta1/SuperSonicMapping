// 超音波距離センサーでマッピング
//
//   超音波距離センサーモジュール : HC-SR04
//
//       Pin4 GP2        -> サーボ
//       Pin6 GP4        -> Echo
//       Pin7 GP5        -> Trig

#include <Servo.h>		// サーボライブラリ

#define SRV_PIN 2
#define SS_ECHO_PIN 4
#define SS_TRIG_PIN 5
#define SRV_CENTER 90

Servo servo;
int sign = 2;
int dir = 0;

double sound_speed;

void setup() {
  pinMode(SS_ECHO_PIN, INPUT );
  pinMode(SS_TRIG_PIN, OUTPUT );
  digitalWrite(SS_TRIG_PIN, LOW); 
  
  servo.attach(SRV_PIN, 544, 2400);
  servo.write(SRV_CENTER);

  Serial.begin(115200);

  double temperature = analogReadTemp() + 6;
  sound_speed = 331.5 + 0.6 * temperature;

  delay(1000);  // 1秒待つ
}

// 距離(m)を計測
// 計測できなかった時は-1
double measure_distance() {
  digitalWrite(SS_TRIG_PIN, HIGH);
  delayMicroseconds(10); 
  digitalWrite(SS_TRIG_PIN, LOW);
  double duration = pulseIn(SS_ECHO_PIN, HIGH); // 往復にかかった時間(マイクロ秒)

	double distance = -1;
  if (duration > 0) {
    distance = (duration / 2) * sound_speed / 1000000;
  }
  
  return distance;
}

void loop() {
  dir += sign;
  if (dir >  90) { dir =  90; sign = -sign; }
  if (dir < -90) { dir = -90; sign = -sign; }
  
  servo.write(SRV_CENTER + dir);
  delay(20);
  
  double distance = measure_distance();
  if (distance == -1) return;
  distance *= 100;
  
  Serial.print(dir);
  Serial.print(",");
  Serial.println((int)distance);
}
