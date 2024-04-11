import serial
import time

def configurar_serial(puerto='COM3', velocidad=9600):
    ser = serial.Serial(puerto, velocidad)
    time.sleep(2)  # Esperar a que la conexión se establezca
    return ser
