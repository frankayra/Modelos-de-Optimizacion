**Proyecto**: Optimización de Rutas de Entrega para una Empresa de Logística
**Objetivo**: Optimizar las rutas de entrega para minimizar los costos operativos, considerando restricciones como la capacidad de los vehículos y el tiempo máximo de entrega.

#### Descripción:
Una pequeña empresa de logística quiere optimizar sus rutas de entrega para reducir costos y mejorar la eficiencia. La empresa cuenta con varios vehículos y una lista de clientes que deben ser atendidos diariamente. Cada cliente tiene una demanda específica de productos, y los vehículos tienen una capacidad máxima. Además, existe una ventana de tiempo durante la cual las entregas deben ser realizadas.

## Pasos del Proyecto:

#### Formulación del Problema:
- Definir las variables de decisión (por ejemplo, $x_{ij}$ que indica si el vehículo viaja del punto $i$ al punto j.

- Establecer la función objetivo que se va a minimizar, que puede ser el costo total de las rutas (suma de las distancias recorridas).
Plantear las restricciones del problema, como la capacidad de los vehículos y las ventanas de tiempo para las entregas.

#### Aplicación del Método Simplex:
- Formular el problema en su forma estándar para aplicar el método simplex.
- Resolver el problema usando el método simplex para obtener la ruta óptima.

#### Método de las Dos Fases:
- Utilizar el método de las dos fases si el problema no está inicialmente en forma estándar (por ejemplo, si hay restricciones de igualdad que no pueden ser directamente manejadas por el simplex).
**Primera fase**: Encontrar una solución factible inicial.
**Segunda fase**: Optimizar la solución encontrada en la primera fase.

#### Análisis del Espacio Dual:
- Formular el problema dual del problema de optimización de rutas.
- Resolver el problema dual para obtener información adicional, como el precio sombra de las restricciones.
- Interpretar los resultados del problema dual en el contexto del problema original.

#### Implementación Computacional:
=> Implementar el modelo matemático utilizando un software de optimización como Python 

=> Validar los resultados obtenidos y realizar análisis de sensibilidad para ver cómo cambian las soluciones óptimas con diferentes parámetros.