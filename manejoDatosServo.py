import csv

def guardar_datos_csv(datos_servo, csv_filename):
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        for dato in datos_servo:
            writer.writerow(dato)
