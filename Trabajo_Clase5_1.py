nombres = ["Juan", "Pedro", "Jorge", "María", "Ana"]
i = 0
while i < len(nombres):
    nombre = nombres[i]
    
    if nombre == "Ana":
        print("¡Ana está en la lista!")
        break
        
    if nombre.startswith("J"):
        i += 1
        continue
        
    print(nombre)
    
    i += 1