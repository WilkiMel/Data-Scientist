mi_numero = int(input("ingresa tu numero: "))

if mi_numero < 10:
    print("Tu número es menor que 10")
elif mi_numero > 60:

    if mi_numero % 2 == 0:
        print("Tu número es mayor que 60 y es par")
    else:
        print("Tu número es mayor que 60 y es impar")

elif mi_numero > 40:
    print("Tu número es mayor que 40")
elif mi_numero > 20:
    print("Tu número es mayor que 20")
else:
    print("Tu número está entre 10 y 20")

contador = 0
while contador <= 100:
    print(f"El valor del contador es: {contador}")
    contador += 1
