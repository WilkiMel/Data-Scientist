Nombre = "Carne"
Precio = 33500.53
Cantidad_bodega = 5
Disponible = Cantidad_bodega > 0
impuesto = 0.19
precio_con_impuesto = (Precio * impuesto) + Precio
Precio_total = precio_con_impuesto * Cantidad_bodega
print(f"Precio con impuesto: {precio_con_impuesto}")
print(f"El precio total de los productos es: {Precio_total}")
print(f"¿Hay stock disponible?, {Disponible}")
print(type(Precio_total))
print(type(Disponible))
