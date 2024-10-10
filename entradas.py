import json

# Datos originales
nodos = [0, 1, 2, 3, 4, 5]
distancias = {
    0: {0: 0, 1: 2, 2: 9, 3: 10, 4: 7, 5: 3},
    # ... resto de las distancias
}
demanda = {
    0: 0,
    # ... resto de la demanda
}

# Crear un diccionario que contenga toda la información
data = {
    "nodos": nodos,
    "distancias": distancias,
    "demanda": demanda
}

# Convertir el diccionario a formato JSON
json_data = json.dumps(data)

# Imprimir el resultado (o guardarlo en un archivo)
print(json_data)