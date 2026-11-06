# mi_nombre = "Camilo"
# Edad = 26
# print("hola", mi_nombre)

mi_nombre = input("Ingresa tu nombre: ")
input("hola", mi_nombre)

# edad = 26
# temperatura = 29.3
# calificacion = 3.4

# funcion = "Camila?"
# cargo = "Analista de datos!!!!"

# es_intructor = True
# tiene_perro = False

# variable1 = "Camila"
# variable2 = "2"
# variable3 = variable1 + variable2

asignacion = 10
print(f"inicia: {asignacion}")
asignacion += 5
print(f"suma y asignacion: {asignacion}")
asignacion -= 5
print(f"resta y asignacion: {asignacion}")
asignacion *= 5
print(f"multiplicacion y asignacion {asignacion}")
asignacion /= 5
print(f"division y asignacion {asignacion}")


comparacion_1 = 10 > 5  # True
comparacion_2 = 10 > 11  # false

print(comparacion_1 or comparacion_2)
print(comparacion_1 and comparacion_2)

lista = [1, 2, 3, 4, 5]

print("Esta 3 en la lista?", 3 in lista)
print("No esta 12 en la lista?", 12 not in lista)
