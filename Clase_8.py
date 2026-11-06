import numpy as np

ventas = np.array([120, 150, 90, 200, 180])

print("Ventas:", ventas)
print("Tipo de objeto:", type(ventas))
print("Forma (shape):", ventas.shape)
print("Número de dimensiones (ndim):", ventas.ndim)
print("Tipo de dato (dtype):", ventas.dtype)
print("Cantidad de elementos (size):", ventas.size)

ventas_ajustadas = ventas * 1.10

print("Ventas originales:", ventas)
print("Ventas ajustadas:", ventas_ajustadas)

ventas_sucursales = np.array([
    [120, 150, 180],  # Sucursal A
    [90,  200, 170],  # Sucursal B
    [160, 140, 210]   # Sucursal C
])

print(ventas_sucursales)
print("Forma:", ventas_sucursales.shape)
print("Primera sucursal:", ventas_sucursales[0])
print("Segundo día de todas las sucursales:", ventas_sucursales[:, 1])

ventas = np.array([120, 150, 90, 200, 180, 160, 140, 250, 80, 190])

# 1. Ventas inferiores a 100
ventas_menores_100 = ventas[ventas < 100]
print("1.", ventas_menores_100)

# 2. Ventas iguales o superiores a 180
ventas_mayores_igual_180 = ventas[ventas >= 180]
print("2.", ventas_mayores_igual_180)

# 3. Porcentaje de días con ventas inferiores a 100
porcentaje_menores_100 = (ventas < 100).mean() * 100
print("3.", porcentaje_menores_100, "%")