import serial
import time

# Configurar la conexión serial
ser = serial.Serial('COM3', 9600)  # Cambia 'COM3' al puerto serial correcto

time.sleep(2)  # Esperar a que la conexión se establezca

def move_forward():
    print("Moviendo hacia adelante")

def move_backward():
    print("Moviendo hacia atrás")

def stop():
    print("Deteniéndose")

try:
    while True:
        # Leer datos del puerto serial
        if ser.in_waiting > 0:
            data = ser.readline().decode().rstrip()
            if data.startswith('D:'):
                distance = int(data[2:])
                print("Distancia:", distance)
                
                # Ejemplo de decisión basada en distancia
                if distance < 20:
                    move_backward()
                else:
                    move_forward()

        time.sleep(1)  # Esperar un segundo antes de la siguiente lectura

except KeyboardInterrupt:
    ser.close()  # Cerrar la conexión serial al terminar
    print("Conexión cerrada.")
