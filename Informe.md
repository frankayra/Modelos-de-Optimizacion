Informe Detallado para Proyecto de Curso Final: Optimización de Rutas de Entrega
## Introducción
El problema abordado en este proyecto es un caso típico de optimización conocido como Vehicle Routing Problem (VRP) con capacidad limitada y ventanas de tiempo, una variante del clásico problema de optimización de rutas. Este modelo busca minimizar el costo total de distribución, considerando restricciones como la capacidad de los vehículos, la demanda de los clientes, y el cumplimiento de ventanas de tiempo. La importancia de este modelo radica en su aplicabilidad a escenarios de logística y distribución, donde es necesario determinar rutas óptimas para minimizar costos y tiempos de entrega.

## Definición del Problema
Objetivo: Minimizar el costo total de las rutas para todos los vehículos utilizados, lo cual se traduce en minimizar la suma de las distancias recorridas por los vehículos en su recorrido entre el depósito y los clientes.

**Variables de Decisión:**

- $x_{ij}^k$ : Variable binaria que indica si el vehículo $k$ viaja del punto $i$ al punto $j$. Toma el valor 1 si el viaje se realiza, y 0 en caso contrario.
- $u_i^k$ : Variable continua que representa la posición del cliente $i$ en la ruta del vehículo $k$. Se utiliza para evitar la formación de subciclos.

**Datos del Problema:**
Los datos del problema incluyen:

- **Nodos**: Representados por el depósito ($0$) y los clientes ($1,2,…,n$).
- **Distancias** $d_{ij}$: Matriz de distancias entre cada par de nodos, donde $i$ y $j$ pueden ser el depósito o cualquiera de los clientes.
- **Demanda** $q_i$: Demanda de cada cliente $i$.
- **Capacidad** $Q$: Capacidad máxima de carga que puede transportar cada vehículo.
- **Ventanas de tiempo** [$e_i, l_i$]: Intervalo de tiempo en el cual el cliente $i$ debe ser atendido.

- **Número de Vehículos** $K$: Número de vehículos disponibles.

## Formulación Matemática del Modelo
#### Función Objetivo:

$$Minimizar \sum_{k\in K}\sum_{i\in N}\sum_{j\in N}d_{ij}\cdot x_{ij}^k$$
 
> La función objetivo busca minimizar la distancia total recorrida por todos los vehículos, lo que se traduce en la suma de las distancias recorridas por cada vehículo entre los diferentes puntos del problema.

#### Restricciones:
1) **Visita Única**: Cada cliente debe ser visitado exactamente una vez por algún vehículo.
$$\sum_{k\in K}\sum_{j\in N}x_{ij}^k=1 \quad \forall i\in Clientes$$
2) **Salida del Depósito**: Cada vehículo debe salir del depósito exactamente una vez.
$$\sum_{j\in Clientes}x_{0j}^k=1 \quad \forall k\in K$$
3) **Retorno al Depósito**: Cada vehículo debe regresar al depósito después de completar su ruta.
$$\sum_{i\in Clientes}x_{i0}^k=1 \quad \forall k\in K$$

4) **Flujo de Vehículos**: Asegura que cada vez que un vehículo llega a un cliente, sale de él.
$$\sum_{j\in N}x_{ij}^k=\sum_{j\in N}x_{ji}^k \quad \forall i\in Clientes, \forall k\in K$$
5) **Capacidad de los Vehículos**: La carga transportada por un vehículo en cada ruta no puede superar su capacidad.
$$\sum_{i\in Clientes}q_i\cdot x_{ij}^k\leq Q \quad \forall k\in K$$
6) **Eliminación de Subciclos**: Se utiliza la variable $u$ para evitar la formación de subciclos.
$$u_i^k-u_j^k+Q\cdot x_{ij}^k\leq Q-q_j \quad \forall i,j\in Clientes, \forall k\in K$$
7) **Ventanas de Tiempo**: Las visitas a los clientes deben respetar sus ventanas de tiempo. Esto se puede simplificar integrando las ventanas en el cálculo de las distancias o los costos.

#### Detalles de Implementación
La implementación de este modelo se realizó utilizando Python, usando la biblioteca `PuLP`. Los detalles de los datos se manejan en un archivo `JSON` que contiene las distancias entre nodos, la demanda de cada cliente, la capacidad de los vehículos y otros parámetros relevantes​(data).

**Lectura de Datos**: Los datos del problema, como las distancias y la demanda, se almacenan en un archivo JSON (`data.json`) que se lee al iniciar el programa. Esto facilita la modificación de los datos y hace el modelo más flexible. Este archivo debe estar en la carpeta del proyecto.

**Modelado del Problema**: Se define el problema de optimización con `LpProblem` y las variables $x_{ij}^k$ y $u_i^k$ se definen como variables de decisión binarias y continua, respectivamente. Esto asegura la formulación precisa de las restricciones.

**Restricciones**: Las restricciones se codifican directamente en el modelo usando las funciones proporcionadas por `PuLP` para asegurarse de que cada cliente es atendido, que se respetan las capacidades de los vehículos y que se evitan subciclos.

**Optimización**: Una vez definido el modelo con todas sus restricciones y la función objetivo, se ejecuta el solver para encontrar la solución óptima, minimizando el costo total de las rutas.

#### Detalles importantes
**Uso de Variables Binarias**: Las variables $x_{ij}^k$ se definen como binarias para garantizar que un vehículo viaje o no entre dos puntos, lo cual facilita la formulación del problema y la interpretación de los resultados.

**Uso de Variables Continuas**: Las variables $u_i^k$ se definen como variables continuas para representar la posición de los clientes en las rutas de los vehículos. Esto permite la formulación de restricciones que evitan la formación de subciclos. Esta técnica es usada para evitar la formación de subciclos en problemas de ruteo, lo que garantiza que las rutas de los vehículos no sean fragmentadas y todos los nodos sean visitados de manera continua.

**Integración de Ventanas de Tiempo en las Distancias**: Esto simplifica la implementación al evitar la necesidad de introducir variables adicionales para el tiempo de inicio de servicio, haciendo que el problema sea más manejable sin perder precisión en la representación de las restricciones temporales.

## Resultados Esperados y Conclusión
Con la implementación adecuada de este modelo, se espera obtener rutas óptimas para la distribución de bienes, respetando las capacidades de los vehículos y minimizando la distancia total recorrida. El modelo es flexible y puede ajustarse a diferentes tamaños de problemas modificando los datos de entrada. Esto lo convierte en una herramienta poderosa para problemas de logística y transporte.

El enfoque propuesto busca equilibrar la complejidad teórica del problema con una implementación práctica, utilizando herramientas de optimización lineal que facilitan la resolución de problemas complejos y brindan soluciones eficientes.


## Como ejecutar el programa
1. Asegúrese de tener Python 3 o superior (Ejemplo: Python 3.9.2) instalado en su sistema.
2. Instale las dependencias necesarias ejecutando el siguiente comando: pip install -r requirements.txt
3. Ejecute el programa con el siguiente comando: python main.py
4. El programa leerá los datos del archivo data.json y generará una solución óptima para el problema de ruteo de vehículos.
5. Los resultados se graficaran con el modulo matplotlib, graficando las rutas de los vehículos intuitivamente.

Nota 1: Es importante que el archivo data.json se encuentre en la misma carpeta que el archivo main.py para que el programa pueda leer los datos correctamente.
Nota 2: También es importante que el archivo data.json tenga la estructura correcta, de lo contrario el programa no podrá leer los datos correctamente.
Nota 3: Se desconectó la aplicación de Ramificación y acotación ya que la ejecución de dicho enfoque es demasiado lenta, pero se encuentra implementado en el código.
Nota 4: Para cambiar los datos del problema, se debe modificar el archivo data.json.
Nota 5: Los datos en el archivo data.json deben estar consistentes. Por ejemplo, la matriz de distancias debe ser simétrica, también la cantidad de clientes debe ser igual a la cantidad de demandas e igual a cada dimensión de la matrz distancias, la capacidad de los vehículos debe ser mayor a la demanda máxima, los vehículos deben ser capaces de suministrar la demanda, lo cual significa que $Q \cdot K \ge \sum_{i \in Clientes} demanda_i$. La cantidad de vehículos debe ser menor que la cantidad de clientes.


