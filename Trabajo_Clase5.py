edades = [12, 17, 8, 15, 22, 9, 30, 25]

for edad in edades:
    if edad == 25:
        print("¡Encontramos al estudiante de 25 años! Deteniendo el análisis.")
        break
    elif edad < 10:
        continue
    elif edad >= 18:
        print(f"Adulto: {edad} años")
    else:
        print(f"Menor: {edad} años")
