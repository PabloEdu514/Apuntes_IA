Actividad red neuronal 1
Nombre: Pablo Eduardo Reyes Aguirre                                                            Calificación:____________

Red neuronal para jugar al 5 en línea sin gravedad en un tablero de 25*25
1.	Definir el Tipo de red neuronal y describir cada una de sus partes 
R= Para el diseño de la red neuronal considero que la major opcion es utilizar busqueda a lo profundo y realizar algo similar al algoritmo A-asterisco para identificar que esta pasando al rededor del nodo en el que nos encontramos en este caso donde se acaba de colocar la ficha 

•	Para las entradas se me ocurre que podemos dividir el tablero como si cada casilla fuera una entrada y esta tuviera dos valores ocupada o no y a que participante corresponde (podria ser un numero por ejemplo si es 1 es el participante 1 y si es 2 el participante 2).
•	Para las capas ocultas podria ser algun dato que nos permita identificar que esta pasando al rededor de la casilla actual es decir buscar a sus lados si las casillas estan ocupadas por la misma ficha del participante al que le toca para poder saltar a esta y reevaluar si siguen existiendo Casillas ocupadas en linea recta, otra capa occulta se puede encargar de evaluar los movimientos del oponente para tenerlo en cuenta, y una mas para conocer que esta pasando en todo el tablero es decir que zonas ya se encuentran muy cargadas con fichas.
•	Para las salidas lo que esperaria seria una coordenada que me indique a que parte del tablero deberia moverme es decir mueve a tal posicion (x,y)


2.	Definir los patrones a utilizar
Podriamos utilizar como patrones evaluar el tablero para ver en que parte de este hay mas espacio libre para arrancar colocando la primer ficha antes de cualquier cosa evaluamos de nuevo donde colocamos la ficha para conocer el estado de sus Casillas aledañas si estas se encuentran libres y ademas tienen mas Casillas libres en la misma linea recta nos permitiria mediante coordenadas enviar una ficha ahi en el siguiente turno en caso de encontrarnos acorralados Podemos evaluar todo e tablero y dirigirnos a otra zona

Otro patron que debemos tener en cuenta es que no solo debemos buscar ubicar bien nuestras fichas si no Tambien afectar al oponente entonces se me ocurre que Podemos evaluar a la vez los movimientos del oponente para ir tapando sus caminos.

3.	Definir función de activación es necesaria para este problema
No se cual funcion de activacion sea la mas optima para el problema 

4.	Definir el número máximo de entradas
R= 800 entradas esto porque tendremos 400 casillas con dos valores
5.	¿Qué valores a la salida de la red se podrían esperar?
R= En la salida podria esperar una coordenada que me permita enviar la ficha a la casilla cercana mas viable que me permita ganar
6.	¿Cuáles son los valores máximos que puede tener el bias?
R= El valor maximo podria ser 1, con un nivel de precision de 98% 
