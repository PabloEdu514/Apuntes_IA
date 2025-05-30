# Juego de IA para Esquivar Balas con Entrenamiento en Tiempo Real

Este proyecto es un juego desarrollado en Python utilizando Pygame, donde un personaje debe esquivar balas disparadas desde diferentes posiciones. Lo interesante de este juego es que incorpora modelos de Machine Learning para aprender y mejorar la habilidad de esquivar balas mientras se juega en modo manual.

---

## Descripción del proyecto

El juego permite dos modos:

- **Modo manual:** El jugador controla al personaje con el teclado, moviéndose y saltando para esquivar balas. Mientras se juega, se recolectan datos que se usan para entrenar los modelos de IA.

- **Modo automático:** El juego utiliza modelos de Machine Learning para decidir cuándo saltar y cómo moverse lateralmente para esquivar las balas, aplicando el conocimiento aprendido.

Se entrenan tres tipos de modelos para cada acción (salto y movimiento):

- Árboles de decisión (`DecisionTreeClassifier`)
- Redes neuronales (`MLPClassifier`)
- K-vecinos más cercanos (`KNeighborsClassifier`)

Estos modelos se actualizan en tiempo real con los datos generados durante el modo manual, mejorando su rendimiento conforme se juega.

---

## Tecnologías utilizadas

- Python 3.x
- Pygame para gráficos y control del juego
- Scikit-learn para los modelos de Machine Learning

---

## Cómo funciona el juego

- El jugador debe esquivar dos tipos de balas: una que se mueve horizontalmente y otra que cae verticalmente.
- En modo manual, el jugador se mueve con las flechas y salta con espacio.
- En modo automático, la IA predice las acciones basándose en modelos entrenados con datos anteriores.
- Cuando el jugador colisiona con una bala, el juego se reinicia y vuelve a mostrar el menú para seleccionar modo y modelo.
- El juego guarda datos de comportamiento que sirven para entrenar los modelos.

---

## Revisión del desarrollo y commits

Si desea revisar el proceso completo de desarrollo, los ajustes realizados y el historial detallado de commits, por favor consulta la rama **master** del repositorio. Ahí podrás ver paso a paso cómo se construyó y evolucionó este proyecto.

Enlace a la rama master:

[https://github.com/PabloEdu514/Apuntes_IA.git](https://github.com/PabloEdu514/Apuntes_IA.git)

---

## Instrucciones para ejecutar

1. Asegúrate de tener Python 3 y las librerías necesarias instaladas: `pygame` y `scikit-learn`.
2. Descarga o clona el repositorio.
3. Ejecuta el script principal con:

   ```bash
   python juego_ia.py
