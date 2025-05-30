import pygame
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier

pygame.init()

# --- CONFIGURACIÓN DE PANTALLA ---
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego ML - Esquivar y Retornar")

# --- COLORES ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# --- ESTADOS DEL JUEGO ---
salto = False               # Indica si el jugador está saltando
salto_altura = 15           # Velocidad inicial del salto vertical
gravedad = 1                # Valor de la gravedad para el salto
en_suelo = True             # Si el jugador está tocando el suelo (puede saltar)
menu_activo = True          # Controla si el menú está activo
modo_auto = False           # Indica si el juego está en modo automático
modo_modelo = None          # Almacena el modelo ML activo: 'arbol', 'nn', 'knn'

# --- DATOS Y MODELOS PARA ML ---
datos_salto = []            # Lista con datos para entrenar el salto
datos_movimiento = []       # Lista con datos para entrenar movimiento lateral

# Modelos para cada tipo de algoritmo y tarea
modelo_salto_arbol = None
modelo_movimiento_arbol = None
modelo_salto_nn = None
modelo_movimiento_nn = None
modelo_salto_knn = None
modelo_movimiento_knn = None

# --- VARIABLES PARA CONTROLAR MOVIMIENTO ---
accion_actual = 0           # Acción actual del jugador (0: nada, 1: izquierda, 2: derecha)
tiempo_accion = 0           # Contador para mantener acción establecida (cooldown)
UMBRAL_TIEMPO = 10          # Frames mínimos para cambiar acción
UMBRAL_PELIGRO = 50         # Distancia mínima para considerar zona peligrosa lateral

# --- POSICIONES Y OBJETOS DEL JUEGO ---
POSICION_ORIGEN = 50                                   # Posición fija donde el jugador debe volver
jugador = pygame.Rect(POSICION_ORIGEN, h - 100, 32, 48)  # Rectángulo que representa al jugador
bala_horizontal = pygame.Rect(w - 50, h - 90, 16, 16)    # Bala que viene horizontalmente
bala_vertical = pygame.Rect(30 + 24, 60, 16, 16)         # Bala que cae verticalmente desde la nave
nave_superior = pygame.Rect(30, 20, 64, 64)               # Nave fija arriba a la izquierda
nave = pygame.Rect(w - 100, h - 100, 64, 64)              # Nave enemiga (no usada para lógica)

# --- VELOCIDADES DE OBJETOS ---
velocidad_bala = -6           # Velocidad horizontal de la bala (variable al disparar)
velocidad_bala_vertical = 6   # Velocidad constante de la bala vertical
bala_disparada = False        # Estado si la bala horizontal está disparada

# --- ANIMACIÓN ---
current_frame = 0
frame_speed = 10
frame_count = 0

# --- FONDO ---
fondo_x1 = 0
fondo_x2 = w

# --- FUENTE PARA TEXTO ---
fuente = pygame.font.SysFont('Arial', 24)

# --- RECURSOS VISUALES (IMÁGENES) ---
jugador_frames = [
    pygame.image.load('C:\\Users\\pablo\\OneDrive\\Documentos\\Phaser\\pygamesc\\assets\\sprites\\mono_frame_1.png'),
    pygame.image.load('C:\\Users\\pablo\\OneDrive\\Documentos\\Phaser\\pygamesc\\assets\\sprites\\mono_frame_2.png'),
    pygame.image.load('C:\\Users\\pablo\\OneDrive\\Documentos\\Phaser\\pygamesc\\assets\\sprites\\mono_frame_3.png'),
    pygame.image.load('C:\\Users\\pablo\\OneDrive\\Documentos\\Phaser\\pygamesc\\assets\\sprites\\mono_frame_4.png')
]
bala_img = pygame.image.load('C:\\Users\\pablo\\OneDrive\\Documentos\\Phaser\\pygamesc\\assets\\sprites\\purple_ball.png')
fondo_img = pygame.image.load('C:\\Users\\pablo\\OneDrive\\Documentos\\Phaser\\pygamesc\\assets\\game\\fondo2.png')
nave_img = pygame.image.load('C:\\Users\\pablo\\OneDrive\\Documentos\\Phaser\\pygamesc\\assets\\game\\ufo.png')
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# --- FUNCIONES DE JUEGO ---

def disparar_bala_horizontal():
    """Dispara la bala horizontal con velocidad aleatoria si no está disparada."""
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -4)
        bala_disparada = True

def reset_bala_horizontal():
    """Reubica la bala horizontal a la posición inicial y marca que no está disparada."""
    global bala_disparada
    bala_horizontal.x = w - 50
    bala_disparada = False

def reset_bala_vertical():
    """Reubica la bala vertical justo debajo de la nave superior."""
    bala_vertical.x = 30 + 24
    bala_vertical.y = nave_superior.bottom

def manejar_salto():
    """Controla el salto del jugador con gravedad y vuelve al suelo."""
    global salto, salto_altura, en_suelo
    if salto:
        jugador.y -= salto_altura
        salto_altura -= gravedad
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15
            en_suelo = True

def entrenar_modelos():
    """Entrena todos los modelos disponibles con los datos actuales de salto y movimiento."""
    global modelo_salto_arbol, modelo_movimiento_arbol
    global modelo_salto_nn, modelo_movimiento_nn
    global modelo_salto_knn, modelo_movimiento_knn

    # Entrenar modelos para salto si hay datos
    if datos_salto:
        X = [(v, d) for v, d, s in datos_salto]
        y = [s for v, d, s in datos_salto]
        modelo_salto_arbol = DecisionTreeClassifier().fit(X, y)
        modelo_salto_nn = MLPClassifier(max_iter=500).fit(X, y)
        modelo_salto_knn = KNeighborsClassifier(n_neighbors=3).fit(X, y)
        print(f"Modelos salto entrenados con {len(X)} muestras.")
    else:
        modelo_salto_arbol = None
        modelo_salto_nn = None
        modelo_salto_knn = None

    # Entrenar modelos para movimiento si hay datos
    if datos_movimiento:
        X_mov = [[dx, jug_x, bala_x] for (dx, jug_x, bala_x), accion in datos_movimiento]
        y_mov = [accion for (_, _, _), accion in datos_movimiento]
        modelo_movimiento_arbol = DecisionTreeClassifier().fit(X_mov, y_mov)
        modelo_movimiento_nn = MLPClassifier(max_iter=500).fit(X_mov, y_mov)
        modelo_movimiento_knn = KNeighborsClassifier(n_neighbors=3).fit(X_mov, y_mov)
        print(f"Modelos movimiento entrenados con {len(X_mov)} muestras.")
    else:
        modelo_movimiento_arbol = None
        modelo_movimiento_nn = None
        modelo_movimiento_knn = None

def prediccion_salto():
    """Devuelve True o False si el modelo predice que debe saltar."""
    if modo_modelo == 'arbol' and modelo_salto_arbol:
        dx = abs(jugador.x - bala_horizontal.x)
        return modelo_salto_arbol.predict([(velocidad_bala, dx)])[0] == 1
    elif modo_modelo == 'nn' and modelo_salto_nn:
        dx = abs(jugador.x - bala_horizontal.x)
        return modelo_salto_nn.predict([(velocidad_bala, dx)])[0] == 1
    elif modo_modelo == 'knn' and modelo_salto_knn:
        dx = abs(jugador.x - bala_horizontal.x)
        return modelo_salto_knn.predict([(velocidad_bala, dx)])[0] == 1
    return False

def prediccion_movimiento():
    """Devuelve la acción de movimiento predicha por el modelo (0,1,2)."""
    if modo_modelo == 'arbol' and modelo_movimiento_arbol:
        dx = abs(jugador.x - bala_vertical.x)
        return modelo_movimiento_arbol.predict([[dx, jugador.x, bala_vertical.x]])[0]
    elif modo_modelo == 'nn' and modelo_movimiento_nn:
        dx = abs(jugador.x - bala_vertical.x)
        return modelo_movimiento_nn.predict([[dx, jugador.x, bala_vertical.x]])[0]
    elif modo_modelo == 'knn' and modelo_movimiento_knn:
        dx = abs(jugador.x - bala_vertical.x)
        return modelo_movimiento_knn.predict([[dx, jugador.x, bala_vertical.x]])[0]
    return 0

def guardar_datos_salto():
    """Guarda el dato actual de salto para entrenamiento futuro."""
    dx = abs(jugador.x - bala_horizontal.x)
    salto_hecho = 1 if salto else 0
    datos_salto.append((velocidad_bala, dx, salto_hecho))

def guardar_datos_movimiento(accion):
    """Guarda el dato actual de movimiento para entrenamiento futuro."""
    dx = abs(jugador.x - bala_vertical.x)
    datos_movimiento.append(((dx, jugador.x, bala_vertical.x), accion))

def mostrar_menu():
    """Muestra el menú y espera a que el jugador elija modo y modelo."""
    global menu_activo, modo_auto, modo_modelo
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona M: Manual | D: Árbol | N: Red Neuronal | K: KNN | Q: Salir", True, BLANCO)
    pantalla.blit(texto, (w // 8, h // 2))
    pygame.display.flip()
    while menu_activo:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_m:
                    modo_auto = False
                    modo_modelo = None
                    # Reiniciar datos para nuevo entrenamiento
                    datos_salto.clear()
                    datos_movimiento.clear()
                    menu_activo = False
                    print("Modo manual activado y datos de entrenamiento reiniciados.")
                elif e.key == pygame.K_d:
                    modo_auto = True
                    modo_modelo = 'arbol'
                    entrenar_modelos()
                    menu_activo = False
                elif e.key == pygame.K_n:
                    modo_auto = True
                    modo_modelo = 'nn'
                    entrenar_modelos()
                    menu_activo = False
                elif e.key == pygame.K_k:
                    modo_auto = True
                    modo_modelo = 'knn'
                    entrenar_modelos()
                    menu_activo = False
                elif e.key == pygame.K_q:
                    pygame.quit()
                    exit()

def reiniciar_juego():
    """Reinicia el estado del juego y muestra el menú."""
    global salto, en_suelo, bala_disparada, menu_activo, fondo_x1, fondo_x2, accion_actual, tiempo_accion
    jugador.x, jugador.y = POSICION_ORIGEN, h - 100
    reset_bala_horizontal()
    reset_bala_vertical()
    salto = False
    en_suelo = True
    bala_disparada = False
    fondo_x1 = 0
    fondo_x2 = w
    accion_actual = 0
    tiempo_accion = 0
    menu_activo = True
    mostrar_menu()

def update():
    """Actualiza todo lo visual y el estado de las balas y jugador en cada frame."""
    global current_frame, frame_count, fondo_x1, fondo_x2

    # Mover fondo para dar sensación de desplazamiento
    fondo_x1 -= 1
    fondo_x2 -= 1
    if fondo_x1 <= -w:
        fondo_x1 = w
    if fondo_x2 <= -w:
        fondo_x2 = w
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Control animación jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar jugador y naves
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))
    pantalla.blit(nave_img, (nave.x, nave.y))
    pantalla.blit(nave_img, (nave_superior.x, nave_superior.y))

    # Mover bala horizontal y resetear si sale de pantalla
    if bala_disparada:
        bala_horizontal.x += velocidad_bala
        if bala_horizontal.x < 0:
            reset_bala_horizontal()

    # Mover bala vertical y resetear si sale de pantalla
    bala_vertical.y += velocidad_bala_vertical
    if bala_vertical.y > h:
        reset_bala_vertical()

    # Dibujar balas
    pantalla.blit(bala_img, (bala_horizontal.x, bala_horizontal.y))
    pantalla.blit(bala_img, (bala_vertical.x, bala_vertical.y))

    # Verificar colisiones y reiniciar juego si colisiona el jugador con alguna bala
    if jugador.colliderect(bala_horizontal) or jugador.colliderect(bala_vertical):
        print("¡Colisión!")
        reiniciar_juego()

def main():
    """Bucle principal del juego, maneja eventos y lógica."""
    global salto, en_suelo, accion_actual, tiempo_accion
    reloj = pygame.time.Clock()
    mostrar_menu()
    correr = True
    reset_bala_horizontal()
    reset_bala_vertical()

    while correr:
        movimiento = 0

        # Manejar eventos de teclado y ventana
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE and en_suelo:
                salto = True
                en_suelo = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            jugador.x = max(0, jugador.x - 5)
            movimiento = 1
        elif keys[pygame.K_RIGHT]:
            jugador.x = min(w - jugador.width, jugador.x + 5)
            movimiento = 2
        else:
            movimiento = 0

        # Control del salto del jugador
        if salto:
            manejar_salto()

        # Definir posición a la que debe regresar el jugador luego de esquivar
        destino = bala_vertical.x - jugador.width // 2
        regresar_caminando = (
            bala_vertical.y > jugador.y + jugador.height and
            abs(jugador.x - destino) > 3
        )

        if modo_auto:
            # Si debe saltar, predecir con modelo elegido
            if en_suelo and prediccion_salto():
                salto = True
                en_suelo = False

            # Lógica para regresar caminando a la posición origen luego de esquivar
            if regresar_caminando:
                if jugador.x < destino:
                    jugador.x += 6
                elif jugador.x > destino:
                    jugador.x -= 6
            else:
                # Control de cooldown para acciones laterales
                mov_pred = prediccion_movimiento()
                if mov_pred != accion_actual:
                    if tiempo_accion >= UMBRAL_TIEMPO:
                        accion_actual = mov_pred
                        tiempo_accion = 0
                    else:
                        tiempo_accion += 1
                else:
                    tiempo_accion = 0

                dx = bala_vertical.x - jugador.x
                # Mover según acción predicha solo si está en zona de peligro
                if accion_actual == 1 and jugador.x > 0 and abs(dx) < UMBRAL_PELIGRO:
                    jugador.x -= 5
                elif accion_actual == 2 and jugador.x < w - jugador.width and abs(dx) < UMBRAL_PELIGRO:
                    jugador.x += 5
        else:
            # En modo manual también hacer que regrese caminando si debe
            if regresar_caminando:
                if jugador.x < destino:
                    jugador.x += 6
                elif jugador.x > destino:
                    jugador.x -= 6
            else:
                # Guardar datos para entrenamiento futuro
                guardar_datos_salto()
                if movimiento != 0:
                    guardar_datos_movimiento(movimiento)

        # Disparar bala horizontal si no está disparada
        if not bala_disparada:
            disparar_bala_horizontal()

        # Actualizar pantalla y limitar FPS
        update()
        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()

# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    main()
