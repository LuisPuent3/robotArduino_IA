def controlar_robot(angulo, distancia_predicha, ser):
    if distancia_predicha < 20:
        ser.write(b'forward\n')  # Mover hacia adelante
    elif distancia_predicha > 30:
        ser.write(b'backward\n')  # Mover hacia atrás
    else:
        if angulo < 90:
            ser.write(b'left\n')  # Mover hacia la izquierda
        else:
            ser.write(b'right\n')  # Mover hacia la derecha

        if distancia_predicha < 25:
            ser.write(b'up\n')  # Ascender
        elif distancia_predicha > 35:
            ser.write(b'down\n')  # Descender
