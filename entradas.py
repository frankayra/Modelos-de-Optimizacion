import json

# Datos originales
nodos = [0, 1, 2, 3, 4, 5]

# Distancias entre nodos (matriz simetrica)
distancias = [
    [0, 2, 9, 10, 7, 3],
    [2, 0, 6, 4, 3, 5],
    [9, 6, 0, 8, 5, 7],
    [10, 4, 8, 0, 2, 6],
    [7, 3, 5, 2, 0, 4],
    [3, 5, 7, 6, 4, 0]
]

# Demanda de cada cliente
demanda = {
    0: 0,  # Deposito no tiene demanda
    1: 1,
    2: 1,
    3: 2,
    4: 4,
    5: 2
}
# Capacidad de los vehiculos
Q = 5

# Numero de vehiculos
K = 2




distancias_dict = {}
for i, d in enumerate(distancias):
    distancias_dict[nodos[i]] = {nodos[j]: distancias[i][j] for j in range(len(d))}
    
distancias = distancias_dict   
    
# distancias = {
#     0: {0: 0, 1: 2, 2: 9, 3: 10, 4: 7, 5: 3},
#     1: {0: 2, 1: 0, 2: 6, 3: 4, 4: 3, 5: 5},
#     2: {0: 9, 1: 6, 2: 0, 3: 8, 4: 5, 5: 7},  
#     3: {0: 10, 1: 4, 2: 8, 3: 0, 4: 2, 5: 6}, 
#     4: {0: 7, 1: 3, 2: 5, 3: 2, 4: 0, 5: 4},  
#     5: {0: 3, 1: 5, 2: 7, 3: 6, 4: 4, 5: 0}
# }





# Crear un diccionario que contenga toda la informacion
data = {
    "nodos": nodos,
    "distancias": distancias,
    "demanda": demanda,
    "Q": Q,
    "K": K
}

# Convertir el diccionario a formato JSON
json_data = json.dumps(data)

# Imprimir el resultado (o guardarlo en un archivo)
print(json_data)
with open('data.json', 'w') as file:
    json.dump(data, file)