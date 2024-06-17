# Asignaciones

## Asignacion de fechas grupos y evaluadores

Para la asignacion de fechas entre grupos y evaluadores, se tomaron dos algoritmos. El primer algoritmo utiliza programacion lineal y el segundo utiliza dos redes de flujos compuestas para buscar las asignaciones deseadas

Se tomaron en cuenta diferentes restricciones que influyeron en la construccion y resolucion de algoritmos.

- Un evaluador puede ir como maximo `5` slots por semana
- Se busca minimizar la cantidad de veces que el evaluador va a la facultad
- Un evaluador no puede evaluar a un grupo cuyo tutor es el evaluador
- Se buscan al menos 1 suplente que este disponible en ese dia si el evaluador no logra estar presente por x motivo particular


### Flujo

Para resolver la asignacion a partir de redes de flujos se divide el problema en dos grafos donde el primer grafo es utilizado para la construccion del segundo.

El primer grafo es un grafo ponderado donde conecta *evaluadores a semanas* mediante una arista y luego conecta esa semana a los diferentes grupos que poseen al menos un dia en comun con ese evaluador en esa semana.

De esa manera, se puede interpretar como *"el evaluador x evualua al grupo i en la semana j"*.

Una vez con los resultados, se conectan los grupos con todas las fechas que corresponden en esa semana y se calcula asi que grupo expone en que fecha.

Luego con ambos resultados sabremos:
* Que evaluador evalua a que grupo y en que semana
* Que grupo expone en x fecha.

Por ultimo, se hace una iteracion extra en busqueda de posibles tutores para cada exposicion aunque esto ya no forma parte de la resolucion del grafo.