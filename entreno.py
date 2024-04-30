import tkinter as tk
from tkinter import ttk
import serial
import time
from sklearn.tree import DecisionTreeRegressor
import numpy as np
import csv

# Variables globales
angulo = 0

# Funciones para el movimiento del robot
def move_forward():
    ser.write(b'forward\n')

def move_backward():
    ser.write(b'backward\n')

def turn_left():
    ser.write(b'left\n')

def turn_right():
    ser.write(b'right\n')

# Función para guardar los datos en el archivo CSV
def save_data(angulo, distancia):
    with open('datos_servo.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([angulo, distancia])

# Configurar la conexión serial
ser = serial.Serial('COM7', 9600)  # Cambiar 'COM7' al puerto serial correcto
time.sleep(2)  # Esperar a que la conexión se establezca

# Crear la ventana principal
root = tk.Tk()
root.title("Control de Robot con IA")
root.geometry("400x300")
root.configure(bg="#263238")  # Color de fondo

# Estilos para los botones
style = ttk.Style()
style.configure('Custom.TButton', font=('Arial', 12), background='#FF5722', foreground='white', width=10)  # Estilo personalizado para los botones

# Función para actualizar la información de la interfaz
def update_info():
    global angulo  # Declaración global de la variable angulo
    if ser.in_waiting > 0:
        data = ser.readline().decode().rstrip()
        if data.startswith('D:'):
            label_distance.config(text="Distancia: " + data[2:])
            save_data(angulo, int(data[2:]))  # Guardar datos en el archivo CSV
        elif data.startswith('A:'):
            label_angle.config(text="Ángulo: " + data[2:])
            angulo = int(data[2:])
    root.after(100, update_info)

# Etiquetas para mostrar la información de distancia y ángulo
label_distance = ttk.Label(root, text="Distancia: ", font=('Arial', 14), background='#263238', foreground='#ffffff')  # Color de fondo y texto
label_distance.pack(pady=(20, 5))

label_angle = ttk.Label(root, text="Ángulo: ", font=('Arial', 14), background='#263238', foreground='#ffffff')  # Color de fondo y texto
label_angle.pack(pady=5)

# Botones para controlar el movimiento del robot
button_forward = ttk.Button(root, text="Adelante", style='Custom.TButton', command=move_forward)
button_forward.pack(pady=5)

button_backward = ttk.Button(root, text="Atrás", style='Custom.TButton', command=move_backward)
button_backward.pack(pady=5)

button_left = ttk.Button(root, text="Izquierda", style='Custom.TButton', command=turn_left)
button_left.pack(side="left", padx=20, pady=5)

button_right = ttk.Button(root, text="Derecha", style='Custom.TButton', command=turn_right)
button_right.pack(side="right", padx=20, pady=5)

# Entrenar un modelo de regresión simple
X_train = np.array([[0], [45], [90], [135], [180]])
y_train = np.array([30, 25, 20, 25, 30])
model = DecisionTreeRegressor()
model.fit(X_train, y_train)

# Función para tomar decisiones de movimiento basadas en la distancia predicha
def control_robot(angle):
    distancia_predicha = model.predict([[angle]])[0]
    if distancia_predicha < 20:
        move_forward()
        print("Decision: forward")
    elif distancia_predicha > 30:
        move_backward()
        print("Decision: backward")
    else:
        print("Decision: turn")
        if angle < 90:
            turn_left()
        else:
            turn_right()

# Actualizar la información de la interfaz
update_info()

# Función principal para ejecutar la interfaz
root.mainloop()

# Cerrar la conexión serial al salir
ser.close()
