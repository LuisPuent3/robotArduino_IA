#include <Servo.h>

const int PinIN1 = 8;
const int PinIN2 = 9;
const int trigPin = 3;  // Pin del sensor ultrasónico Trig
const int echoPin = 4;  // Pin del sensor ultrasónico Echo
long duration;
int distance;
Servo servoMotor;

// Configuración del módulo Bluetooth HC-06
#define bluetoothSerial Serial // Renombrar Serial a bluetoothSerial
#define bluetoothTx 1         // Conectar el pin TX del módulo Bluetooth al pin digital 1 del Arduino
#define bluetoothRx 0         // Conectar el pin RX del módulo Bluetooth al pin digital 0 del Arduino

void setup() {
  Serial.begin(9600);  // Inicializar comunicación serial para depuración
  bluetoothSerial.begin(9600); // Inicializar comunicación serial para Bluetooth
  pinMode(PinIN1, OUTPUT);
  pinMode(PinIN2, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  servoMotor.attach(2);

  // Configurar los pines del motor para que siempre estén funcionando
  digitalWrite(PinIN1, HIGH);
  digitalWrite(PinIN2, LOW);
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

    // Enviar distancia a través de Bluetooth
    bluetoothSerial.print("D:");  // Identificador de distancia
    bluetoothSerial.println(distance);

    delay(80);  // Espera antes de la siguiente medición
  }
}

void loop() {
  if (bluetoothSerial.available() > 0) {
    String command = bluetoothSerial.readStringUntil('\n');
    
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
    } else if (command.startsWith("P:")) {
      // Obtener la distancia predicha de los datos recibidos
      int distancia_predicha = command.substring(2).toInt();
      
      // Lógica para controlar el carrito basado en la distancia predicha
      if (distancia_predicha < 20) {
          // Lógica para mover hacia adelante
          digitalWrite(PinIN1, HIGH);
          digitalWrite(PinIN2, LOW);
      } else if (distancia_predicha > 30) {
          // Lógica para mover hacia atrás
          digitalWrite(PinIN1, LOW);
          digitalWrite(PinIN2, HIGH);
      } else {
          // Lógica para detener el movimiento
          digitalWrite(PinIN1, HIGH); // Cambia a LOW si quieres detener completamente
          digitalWrite(PinIN2, LOW);  // Cambia a HIGH si quieres detener completamente
      }
    }
  }

  // Mover servo y medir distancia
  moveServoAndMeasure(0, 180, 10);  // Mover servo de 0 a 180 grados
  moveServoAndMeasure(180, 0, -10); // Mover servo de 180 a 0 grados
}

