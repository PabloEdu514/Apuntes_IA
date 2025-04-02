Detección de Vida Mediante Deteccion Facial

Para detectar con visión artificial que una persona está viva y no únicamente esta intentando acceder al sistema con alguna trampa como utilizar una imagen de la cara, necesitamos implementar un modelo que nos permita detectar si una persona se encuentra viva o no, para esto se me ocurre que podemos utilizar los distintos puntos que mediapipe nos proporciona de la cara para identificar patrones por ejemplo la boca no tiene la misma posición por un largo periodo de tiempo este tipo de cosas es lo que vamos a buscar por ejemplo centrarnos en un punto en específico que corresponda a los labios en este caso y compararlo con otro para medir la distancia entre ellos si esta cambia tener un conjunto de valores que nos permitan saber si se trata de un gesto de enojo, si se está riendo o si se encuentra asombrado, además si esto lo complemento con más puntos de la cara como los ojos podemos determinar que se trata de una persona viva, otro punto que se me ocurre es enfocarnos en el parpadeo de los ojos, ya que en caso de necesitar acceder con una imagen esta por obvias razones no va a parpadear a menos que sea un video pero podemos agregar otra característica que nos permita validar que no se trata de un video, para esto podemos medir profundidades en la cara.

2. Puntos Clave para la Detección
El modelo de MEDIAPIPE ya nos proporciona puntos de referencia en la cara, de los cuales hay algunos que son mas que necesarios para saber que se trata de una persona real y viva:

 
2.1 Movimiento de los Párpados
Según información de fuentes confiables estos son los puntos característicos que corresponden a los parpados 33, 133, 159, 145, 362, 263, 386, 374. Con estos puntos podemos medir la apertura y cierre de los ojos. Si la persona no parpadea en cierto periodo de tiempo podemos decir que están intentando hackear el sistema.

2.2 Movimiento de los Labios
Los puntos relevantes para el movimiento de los labios son 13, 14, 78, 308, 191. Con esto podemos checar la apertura de la boca. Podríamos hacer algo como lo que realiza mercado libre cuando te pide autenticar tu identidad que te da un texto y lo tienes que leer así podemos ver si se trata de una persona viva.

2.3 Expresiones Faciales
Los puntos relevantes que nos pueden ayudar a identificar gestos son 70, 107, 336, 285 (cejas); 13, 14, 78, 308 (labios); 6, 195 (mentón). 
Con estos pequeños movimientos musculares en cejas, mejillas y labios nos dan una pista de que se trata de una persona viva. La ausencia de estos podría indicar una imagen estática o una máscara.

2.4 Movimientos de Cabeza
Los puntos relevantes son 1 (frente), 4 (mentón), 6 (nariz), 195 (mejilla inferior). Pedirle a la persona que incline o gire la cabeza ayuda a comprobar que es un objeto tridimensional y no una imagen plana.

3. Detección de Emociones
Además de verificar si es una persona real, podemos analizar sus emociones con los puntos faciales clave.
•	Alegría: Cachetes más elevados, labios estirados y un poco hacia arriba, ojos un poco cerrados.
•	Tristeza: Cejas inclinadas hacia arriba y hacia el centro, comisuras de los labios hacia abajo.
•	Enojo: Cejas juntas y hacia abajo, tensión en la boca y los labios.
•	Sorpresa: Ojos muy abiertos, boca abierta, cejas elevadas.
