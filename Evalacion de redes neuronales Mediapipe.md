**Pablo Eduardo Reyes Aguirre 21120251** 
# Evaluación de Redes Neuronales con MediaPipe  

## 1. Definir el tipo de red neuronal y describir cada una de sus partes  

Para este caso, considero que la mejor opción es utilizar una **Red Neuronal Convolucional**. Ya que nos puede ayudar a identificar que esta pasando cuando una persona realiza un gesto porque podemos usarla para identificar patrones repetitivos.  

Usar una red convolucional nos puede ayudar a identificar gestos de la cara esto porque por ejemplo si nos enfocamos en una sonrisa para determinar que el sugetoo esta sonriendo lo que necesitamos es ver mas de un punto de la boca, ya que en mediapipe se uiliza mas de un punto para identificar que se trata de la boca entonces en vez de utilizar una red que evalue punto por punto podemos usar una convolucional que puede detectar como estan relacionados todos los puntos entre si es decir todo el patron de la boca.
  

## 2. Definir los patrones a utilizar  

Los patrones que vamos a utilizar es enfocarnos en que la red aprenda a reconocer las emociones completas ya que estas no solo utilizan una parte del rostro sino que muchas acciones en el rostro forman una emocion para esto podemos comenzar clasificando que pasa en cada emocion.

Por ejemplo:  
- Si la boca está muy abierta y las cejas están levantadas, probablemente la persona este sorprendida.  
- Si una sola ceja se encuentra levantada problablemente signifique se esta confundida.
- Si las orillas de los labios se encuentran mas elevadas de lo normal y los ojos medio cerrados probablemente se este riendo.

Y asi podemos continuar identificando que pasa en cada emocion, para entrenar el modelo podemos pasar un monton de imagenes clasificadas acorde a cada emocion para que el modelo comience a identificar los patrones de cada accion.

## 3. Definir funcion de activacion es necesaria para este problema  

Podemos utilizar la funcion de activacion  
- **Softmax** ya que esta nos arroja un porcentaje de probabilidad para cada emoción, por lo tanto si nosotros colocamos una validacion que diga sabes que a partir de 95% ya dime si se trata de alegria o enojo, antes de esto como no estamos seguros mejor lanzar algun mensaje diciendo es probable que se trate de tal emocion.    

## 4. definir el numero maximo de entradas  


En mediapipe cada punto esta en 3 dimensiones por lo tanto por cada punto de la cara vamos a tener 3 entradas es decir lo que corresponde a la coordenada (x,y,z), por lo tanto mediapipe usa 468 puntos para todo el rostro entronces 468*3=1404 y este sera nuestro numero maximo de entradas

## 5. ¿Que valores a la salida de la red se podrian esperar?  

Considero que dependiendo la cantidad de emociones que queraos detectar sera el numero de salidas que tenga el modelo porque por ejemplo no sera lo mismo si solo le pedimos que nos diga si esta enojado o triste, a decirle oye puede estar feliz, enojado, triste, asombrado o confundido, en este caso la salida va a cambiar y sera el valor de la probabilidad de cada emocion, para poder comparar cual es la probabilidad mas alta y irnos por ese lado.


## 5. ¿cuales son los valores maximos que puede tener el bias?
 No lo podemos determinar porque este va ajustandose durante el entrenamiento pero deberia ser un valor bajo.