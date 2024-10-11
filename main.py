##################### Definicion de los datos para luego modelar el problema #####################

import pandas as pd
import numpy as np
import json

data = None
with open('data.json', 'r') as f:
    data = json.load(f)
    print(data)

### Datos del problema
# Nodos (incluyendo el deposito)
nodos = data['nodos']

# Distancias entre nodos (matriz simetrica)
distancias = data['distancias']

# Demanda de cada cliente
demanda = data['demanda']

# Ventanas de tiempo (simplificadas)
# Para este ejemplo, omitiremos las ventanas de tiempo o las incorporaremos en los costos
# Se puede extender el modelo para incluirlas si se desea

# Capacidad de los vehiculos
Q = 5

# Numero de vehiculos
K = 2




##################### Creacion del modelo en PulP #####################
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, LpInteger, LpStatus, value

# Crear el modelo
modelo = LpProblem("Optimizacion_de_Rutas_de_Entrega", LpMinimize)

# Variables de decision
# x[i][j][k] = 1 si el vehiculo k viaja de i a j, 0 en otro caso
x = {}
for k in range(K):
    for i in nodos:
        for j in nodos:
            if i != j:
                x[i, j, k] = LpVariable(cat=LpBinary, name=f"x_{i}_{j}_{k}")

# Variables de posicion para eliminar subciclos
u = {}
for k in range(K):
    for i in nodos:
        if i != 0:
            u[i, k] = LpVariable(cat=LpInteger, lowBound=1, upBound=len(nodos)-1, name=f"u_{i}_{k}")

# Funcion objetivo: minimizar la distancia total recorrida
modelo += lpSum(distancias[str(i)][str(j)] * x[i, j, k] for k in range(K) for i in nodos for j in nodos if i != j)

# Restricciones

# 1. Cada cliente es visitado exactamente una vez
for j in nodos:
    if j != 0:
        modelo += lpSum(x[i, j, k] for k in range(K) for i in nodos if i != j) == 1, f"Visita_unica_{j}"

# 2. Cada vehiculo sale del deposito una vez
for k in range(K):
    modelo += lpSum(x[0, j, k] for j in nodos if j != 0) == 1, f"Salida_deposito_{k}"

# 3. Cada vehiculo regresa al deposito una vez
for k in range(K):
    modelo += lpSum(x[i, 0, k] for i in nodos if i != 0) == 1, f"Regreso_deposito_{k}"

# 4. Flujos de vehiculos
for k in range(K):
    for h in nodos:
        if h != 0:
            modelo += lpSum(x[i, h, k] for i in nodos if i != h) == lpSum(x[h, j, k] for j in nodos if j != h), f"Flujo_{h}_vehiculo_{k}"

# 5. Capacidad de los vehiculos
for k in range(K):
    modelo += lpSum(demanda[str(i)] * lpSum(x[i, j, k] for j in nodos if j != i) for i in nodos if i != 0) <= Q, f"Capacidad_vehiculo_{k}"

# 6. Eliminar subciclos (MTZ Constraints)
for k in range(K):
    for i in nodos:
        if i != 0:
            for j in nodos:
                if j != 0 and j != i:
                    modelo += u[i, k] - u[j, k] + Q * x[i, j, k] <= Q - demanda[str(j)], f"Eliminacion_subciclo_{i}_{j}_vehiculo_{k}"





##################### Resolucion del modelo en PulP #####################
modelo.solve()
# Mostrar el estado de la solucion
print("Estado de la solucion:", LpStatus[modelo.status])
# Mostrar el valor de la funcion objetivo
print("Valor de la funcion objetivo(Costo total de las rutas):", value(modelo.objective))

##################### Interpretacion de los resultados #####################
# Funcion para extraer las rutas
def extraer_rutas(x, K, nodos):
    rutas = {k: [] for k in range(K)}
    for k in range(K):
        ruta = []
        current_node = 0  # Deposito
        while True:
            for j in nodos:
                if j != current_node:
                    var = x.get((current_node, j, k))
                    if var and var.varValue > 0.5:
                        ruta.append((current_node, j))
                        current_node = j
                        break
            if current_node == 0:
                break
        rutas[k] = ruta
    return rutas

# Extraer y mostrar las rutas
rutas = extraer_rutas(x, K, nodos)
for k in rutas:
    print(f"Ruta para el vehiculo {k+1}: {rutas[k]}")




##################### Aplicacacion del metodo Simulated Annealing #####################
# def simulated_annealing(x, K, nodos, distancias, demanda, Q, T_inicial=100, alpha=0.99, iteraciones=1000):
#     # Inicializar la temperatura
#     T = T_inicial
#     # Inicializar la solucion actual
#     mejor_solucion = x.copy()
#     mejor_costo = value(modelo.objective)
#     # Iterar
#     for _ in range(iteraciones):
#         # Seleccionar un vecino aleatorio
#         k_vecino = np.random.randint(K)
#         i_vecino, j
#         vecino = x.copy()
#         for i in nodos:
#             for j in nodos:
#                 if i != j:
#                     vecino[i, j, k_vecino] = 1 - vecino[i, j, k_vecino]
#                     # Verificar si el vecino es factible
#                     if verificar_factibilidad(vecino, K, nodos, distancias, demanda, Q):
#                         # Calcular el costo del vecino
#                         costo_vecino = value(modelo.objective)
#                         # Aceptar el vecino si es mejor o con una probabilidad dada
#                         if costo_vecino < mejor_costo or np.random.rand() < np.exp((mejor_costo - costo_vecino) / T):
#                             x = vecino.copy()
#                             mejor_
#                             mejor_costo = costo_vecino
#                             tura
#                             n x, mejor_costo
#                             # Reducir la temperatura
#                             T *= alpha
#                             break
#                         else:
#                             vecino = x.copy()
#                             break
#                         # Reducir la temperatura
#                         T *= alpha
#                         break
#                     return x, mejor_costo
#                 # Verificar si el vecino es factible
#                 if verificar_factibilidad(vecino, K, nodos, distancias, demanda, Q):
#                         # Calcular el costo del vecino
#                         costo_vecino = value(modelo.objective)
#                         # Aceptar el vecino si es mejor o con una probabilidad dada
#                         if costo_vecino < mejor_costo or np.random.rand() < np.exp((mejor_costo - costo_vecino) / T):
#                             x = vecino.copy()
#                             mejor_costo = costo_vecino
#                             break
#                         else:
#                             vecino = x.copy()
#                             break
#                         # Reducir la temperatura
#                         T *= alpha
#                         break
#                     return x, mejor_costo
#                 # Reducir la temperatura
#                 T *= alpha
#                 break
#             return x, mejor_costo
#             # Reducir la temperatura
#             T *= alpha
#             break
#         return x, mejor_costo
#         # Reducir la temperatura
#         T *= alpha
#         break

##################### Aplicacacion del metodo Simplex #####################
### Relajacion del problema

# Crear una copia del modelo para la relajacion
modelo_relajado = modelo.copy()

# Relajar las variables binaria a continuas
for var in modelo_relajado.variables():
    if var.name.startswith("x_"):
        var.cat = "Continuous"
        var.lowBound = 0
        var.upBound = 1

# Resolver el modelo relajado
modelo_relajado.solve()

# Mostrar el estado de la solucion relajada
print("Estado de la solucion relajada:", LpStatus[modelo_relajado.status])

# Mostrar el valor de la funcion objetivo relajada
print("Costo total de las rutas (relajado):", value(modelo_relajado.objective))


##################### Metodo de las dos fases #####################
### Fase 1: Encontrar una solucion basica factible
# Crear un nuevo modelo para la Fase I
fase1 = LpProblem("Fase_I", LpMinimize)

# Variables de decision para fase 1 (mismas que x)
x_fase1 = {}
for k in range(K):
    for i in nodos:
        for j in nodos:
            if i != j:
                x_fase1[i, j, k] = LpVariable(cat=LpBinary, name=f"x_{i}_{j}_{k}_f1")

# Variables artificiales
a = {}
for k in range(K):
    for i in nodos:
        for j in nodos:
            if i != j:
                a[i, j, k] = LpVariable(cat=LpBinary, name=f"a_{i}_{j}_{k}")

# Funcion objetivo: minimizar la suma de variables artificiales
fase1 += lpSum(a[i, j, k] for k in range(K) for i in nodos for j in nodos if i != j)

# Añadir restricciones similares al modelo original y agregar restricciones de artificiales
# Aqui simplificamos y asumimos que el modelo original ya tiene una solucion factible

# Resolver fase 1
fase1.solve()

# Verificar si la solucion es factible
if value(fase1.objective) > 0:
    print("No existe una solucion factible.")
else:
    print("Solucion factible encontrada en la Fase I.")

### Fase 2: Optimizacion con la solucion factible de la Fase I
# Crear un nuevo modelo para la Fase II
fase2 = LpProblem("Fase_II", LpMinimize)

# Variables de decision para fase 2 (mismas que x)
x_fase2 = {}
for k in range(K):
    for i in nodos:
        for j in nodos:
            if i != j:
                x_fase2[i, j, k] = LpVariable(cat=LpBinary, name=f"x_{i}_{j}_{k}_f2")

# Funcion objetivo: minimizar el costo total
fase2 += lpSum(distancias[str(i)][str(j)] * x_fase2[i, j, k] for k in range(K) for i in nodos for j in nodos if i != j)

# Añadir restricciones similares al modelo original
# ... (igual que en la definicion del modelo original)

# Resolver fase 2
fase2.solve()

# Mostrar resultados
print("Estado de la solucion Fase II:", LpStatus[fase2.status])
print("Costo total de las rutas (Fase II):", value(fase2.objective))





############################### Analisis del espacio dual ###############################
# Asegurarse de que el modelo relajado esta resuelto
if modelo_relajado.status != 1:
    print("El modelo relajado no se resolvio correctamente.")
else:
    # Acceder a las restricciones y sus precios sombra
    for name, constraint in modelo_relajado.constraints.items():
        print(f"{name}: Precio sombra = {constraint.pi}")
        
        
        

############################### Validacion y analisis de sensibilidad ###############################
# Ejemplo: Incrementar la demanda del cliente 1 en 1 unidad
modelo.constraints["Visita_unica_1"].constant += 1

# Re-solver el modelo
modelo.solve()

# Mostrar el nuevo costo total
print("Nuevo costo total despues de incrementar la demanda del cliente 1:", value(modelo.objective))





############################### Visualizacion de las rutas optimas ###############################
import matplotlib.pyplot as plt

# Coordenadas de los nodos (ejemplo)
coordenadas = {
    0: (0, 0),
    1: (2, 3),
    2: (5, 2),
    3: (6, 6),
    4: (8, 3),
    5: (1, 7)
}

# Dibujar los nodos
plt.figure(figsize=(8,6))
for nodo in nodos:
    plt.scatter(coordenadas[nodo][0], coordenadas[nodo][1], marker='o', color='blue')
    plt.text(coordenadas[nodo][0]+0.1, coordenadas[nodo][1]+0.1, str(nodo), fontsize=12)

# Dibujar las rutas
for k in rutas:
    ruta = rutas[k]
    if ruta:
        x_coords = [coordenadas[0][0]]
        y_coords = [coordenadas[0][1]]
        for (i, j) in ruta:
            x_coords.append(coordenadas[j][0])
            y_coords.append(coordenadas[j][1])
        x_coords.append(coordenadas[0][0])
        y_coords.append(coordenadas[0][1])
        plt.plot(x_coords, y_coords, label=f"Vehiculo {k+1}")

plt.title("Rutas optimas de Entrega")
plt.xlabel("Coordenada X")
plt.ylabel("Coordenada Y")
plt.legend()
plt.grid(True)
plt.show()
