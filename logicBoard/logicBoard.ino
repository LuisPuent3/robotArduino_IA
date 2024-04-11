#include <Servo.h>

const int PinIN1 = 8;
const int PinIN2 = 9;
const int trigPin = 3;  // Pin del sensor ultrasónico Trig
const int echoPin = 4;  // Pin del sensor ultrasónico Echo
long duration;
int distance;
Servo servoMotor;

void setup() {
  Serial.begin(9600);
  pinMode(PinIN1, OUTPUT);
  pinMode(PinIN2, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  servoMotor.attach(2);
}

void moveServoAndMeasure(int startAngle, int endAngle, int step) {
  for (int angle = startAngle; angle != endAngle; angle += step) {
    servoMotor.write(angle);
    Serial.print("A:");
    Serial.println(angle);
    
    // Medir distancia con el sensor ultrasónico
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    distance = duration * 0.034 / 2;

    // Enviar distancia a Python a través de Serial
    Serial.print("D:");  // Identificador de distancia
    Serial.println(distance);

    delay(40);  // Espera antes de la siguiente medición
  }
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    
    if (command == "forward") {
      // Lógica para avanzar
      digitalWrite(PinIN1, HIGH);
      digitalWrite(PinIN2, LOW);
    } else if (command == "backward") {
      // Lógica para retroceder
      digitalWrite(PinIN1, LOW);
      digitalWrite(PinIN2, HIGH);
    } else if (command == "left") {
      // Lógica para girar a la izquierda
      servoMotor.write(90); // Ajusta el ángulo del servo según sea necesario
    } else if (command == "right") {
      // Lógica para girar a la derecha
      servoMotor.write(90); // Ajusta el ángulo del servo según sea necesario
    } else if (command == "up") {
      // Lógica para ascender
      servoMotor.write(90); // Ajusta el ángulo del servo según sea necesario
    } else if (command == "down") {
      // Lógica para descender
      servoMotor.write(90); // Ajusta el ángulo del servo según sea necesario
    }
  }

  // Mover servo y medir distancia
  moveServoAndMeasure(0, 180, 10);  // Mover servo de 0 a 180 grados
  moveServoAndMeasure(180, 0, -10); // Mover servo de 180 a 0 grados
}
