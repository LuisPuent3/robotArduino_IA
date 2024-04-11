import csv
import time
import serial
from sklearn.tree import DecisionTreeRegressor
import numpy as np

# Configurar la conexión serial
ser = serial.Serial('COM3', 9600)  # Cambia 'COM3' al puerto serial correcto
time.sleep(2)  # Esperar a que la conexión se establezca

# Lista para almacenar datos del servo
datos_servo = []

# Variables para ángulo y distancia
angulo = 0
distancia = 0

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
                with open(csv_filename, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([angulo, distancia])

except KeyboardInterrupt:
    print("Recopilación de datos finalizada.")
    ser.close()  # Cerrar la conexión serial al terminar

# Separar datos en X (ángulo) y y (distancia)
X = np.array([dato[0] for dato in datos_servo]).reshape(-1, 1)
y = np.array([dato[1] for dato in datos_servo])

# Entrenar un modelo de regresión simple
model = DecisionTreeRegressor()
model.fit(X, y)

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
                
                # Tomar decisiones de movimiento basadas en la distancia
                if distancia_predicha < 20:
                    print("Distancia predicha:", distancia_predicha)
                    ser.write(b'forward\n')  # Mover hacia adelante
                elif distancia_predicha > 30:
                    print("Distancia predicha:", distancia_predicha)
                    ser.write(b'backward\n')  # Mover hacia atrás
                else:
                    print("Distancia predicha:", distancia_predicha)
                    if angulo < 90:
                        print("Girando a la izquierda")
                        ser.write(b'left\n')  # Mover hacia la izquierda
                    else:
                        print("Girando a la derecha")
                        ser.write(b'right\n')  # Mover hacia la derecha

                    if distancia_predicha < 25:
                        print("Ascendiendo")
                        ser.write(b'up\n')  # Ascender
                    elif distancia_predicha > 35:
                        print("Descendiendo")
                        ser.write(b'down\n')  # Descender

        time.sleep(1)  # Esperar un segundo antes de la siguiente lectura

except KeyboardInterrupt:
    print("Terminando programa.")
    ser.close()  # Cerrar la conexión serial al terminar
