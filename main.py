import time
import numpy as np
from configSerial import configurar_serial
from manejoDatosServo import guardar_datos_csv
from entrenamientoModelo import entrenar_modelo
from controlRobot import controlar_robot

# Configurar la conexión serial
ser = configurar_serial()

# Lista para almacenar datos del servo
datos_servo = []

# Nombre del archivo CSV para guardar los datos
csv_filename = 'datos_servo.csv'

# Ejemplo de uso para recopilar datos del servo
try:
    while True:
        # Leer datos del puerto serial
        if ser.in_waiting > 0:
            data = ser.readline().decode().rstrip()
            if data.startswith('A:'):
                angulo = int(data[2:])
                print("Angulo:", angulo)

            if data.startswith('D:'):
                distancia = int(data[2:])
                print("Distancia:", distancia)
                
                # Agregar datos a la lista
                datos_servo.append([angulo, distancia])

                # Escribir datos en el archivo CSV
                guardar_datos_csv([[angulo, distancia]], csv_filename)

except KeyboardInterrupt:
    print("Recopilación de datos finalizada.")

# Separar datos en X (ángulo) y y (distancia)
X = np.array([dato[0] for dato in datos_servo]).reshape(-1, 1)
y = np.array([dato[1] for dato in datos_servo])

# Entrenar un modelo de regresión simple
model = entrenar_modelo(X, y)

# Ejemplo de uso para controlar el robot con Machine Learning
try:
    while True:
        # Leer datos del puerto serial
        if ser.in_waiting > 0:
            data = ser.readline().decode().rstrip()
            if data.startswith('A:'):
                angulo = int(data[2:])
                print("Angulo:", angulo)
                
                # Predecir la distancia con el modelo
                distancia_predicha = model.predict([[angulo]])[0]
                
                # Controlar el robot basado en las predicciones del modelo
                controlar_robot(angulo, distancia_predicha, ser)
        time.sleep(1)  # Esperar un segundo antes de la siguiente lectura

except KeyboardInterrupt:
    print("Terminando programa.")
    ser.close()  # Cerrar la conexión serial al terminar
