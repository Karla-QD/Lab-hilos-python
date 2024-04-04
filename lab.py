import threading
import random
import time
from tabulate import tabulate


def ordenar_subvector(subvector, hilo):
    timepo_inicio = time.time()
    subvector.sort()
    print(subvector)
    tiempo_fin = time.time()
    tiempo_ejecucion = tiempo_fin - timepo_inicio
    print(f"Hilo {hilo}: Subvector ordenado (Tiempo: {tiempo_ejecucion} segundos)")

def dividir_vector(vector, num_hilos):
    longitud_subvector = len(vector) // num_hilos
    subvectores = [vector[i:i+longitud_subvector]for i in range(0, len(vector),longitud_subvector)]
    return subvectores

def unir_vectores(subvectores):
    vector_ordenado = [num for subvector in subvectores for num in subvector]

    return vector_ordenado

def ordenar_vector(vector, num_hilos):
    subvectores = dividir_vector(vector, num_hilos)
    threads = []
    for i, subvector in enumerate(subvectores):
        thread = threading.Thread(target=ordenar_subvector, args=(subvector, i))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    vector_ordenado = unir_vectores(subvectores)
    # vector_ordenado.sort()
    print(f"Vector ordenado final: {vector_ordenado}")
    return vector_ordenado  # Agregar esta línea para devolver el vector ordenado


def probar_tiempo_ejecucion(vector_grande, num_hilos):
    tiempo_inicio_total = time.time()
    vector_ordenado = ordenar_vector(vector_grande, num_hilos)
    tiempo_fin_total = time.time()
    tiempo_ejecucion_total = tiempo_fin_total - tiempo_inicio_total
    return vector_ordenado, tiempo_ejecucion_total  # Cambiar el orden de los valores devueltos



vector_grande = [random.randint(1, 1000) for _ in range(1000)]
vector_ordenado = []
resultados = []
for num_hilos in range (2, 100, 20):
    
    vector_ordenado, tiempo_total = probar_tiempo_ejecucion(vector_grande, num_hilos)
   
    resultados.append([num_hilos, tiempo_total])


# Generar la tabla comparativa de tiempos
print(tabulate(resultados, headers=["Hilos", "Tiempo total (segundos)"], tablefmt="grid"))

# Probar que no se pierdan datos
min_tiempo_total = min(resultados, key=lambda x: x[1])[1]
num_hilos_menor_tiempo = [r[0] for r in resultados if r[1] == min_tiempo_total]

vector_ordenado, tiempo_total = probar_tiempo_ejecucion(vector_grande, num_hilos_menor_tiempo[0])
son_iguales = len(vector_grande) == len(vector_ordenado)
print("Se mantienen los datos") if son_iguales else print("No se mantienen")

"""

¿Cómo solucionar el tema del ordenamiento?

Se visualizó que los subvectores ya se encontrababn ordenados, por lo que basto con colocarle un sort al vector grande que contiene cada subvector.


Se probo con 1, 21,41,61 y 81 hilos en un vector de 1000 elementos, en los cuales note un comportamiento donde obtuve
+---------+---------------------------+
|   Hilos |   Tiempo total (segundos) |
+=========+===========================+
|       1 |                 0.0184453 |
+---------+---------------------------+
|      21 |                 0.0274293 |
+---------+---------------------------+
|      41 |                 0.0923455 |
+---------+---------------------------+
|      61 |                 0.0857716 |
+---------+---------------------------+
|      81 |                 0.09903   |
+---------+---------------------------+
En lo que resulta que 21 Hilos parece ser el número óptimo de hilos, para lo que se compara si la cantidad de elementos del vector ordenado es la misma que el original
y así verificar que no hayan pérdida de datos y afirmar que este comportamiento es el que se esperaba.

"""

# cuando agrega muchos datos y pocos hilos, se encuentra mas sentido en los tiempos de ejecución
# Entre más hilos se tiene 
"""
NOTA:
Probar si el vector grande y vector ordenado tienen la misma cantidad de elementos no se perdieron datos.
"""
