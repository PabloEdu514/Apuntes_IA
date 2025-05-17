import pygame
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier

pygame.init()

# Pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego ML - Esquivar y Retornar")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Estados
salto = False
salto_altura = 15
gravedad = 1
en_suelo = True
menu_activo = True
modo_auto = False
modo_modelo = None  # 'arbol', 'nn', 'knn'

# Datos y modelos
datos_salto = []
datos_movimiento = []

modelo_salto_arbol = None
modelo_movimiento_arbol = None

modelo_salto_nn = None
modelo_movimiento_nn = None

modelo_salto_knn = None
modelo_movimiento_knn = None

# Cooldown movimiento
accion_actual = 0
tiempo_accion = 0
UMBRAL_TIEMPO = 10
UMBRAL_PELIGRO = 50

# Posiciones
POSICION_ORIGEN = 50
jugador = pygame.Rect(POSICION_ORIGEN, h - 100, 32, 48)
bala_horizontal = pygame.Rect(w - 50, h - 90, 16, 16)
bala_vertical = pygame.Rect(30 + 24, 60, 16, 16)
nave_superior = pygame.Rect(30, 20, 64, 64)
nave = pygame.Rect(w - 100, h - 100, 64, 64)

# Velocidades
velocidad_bala = -6
velocidad_bala_vertical = 6
bala_disparada = False

# Animación
current_frame = 0
frame_speed = 10
frame_count = 0

# Fondo
fondo_x1 = 0
fondo_x2 = w

# Fuente
fuente = pygame.font.SysFont('Arial', 24)

# Recursos visuales
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

def disparar_bala_horizontal():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-8, -4)
        bala_disparada = True

def reset_bala_horizontal():
    global bala_disparada
    bala_horizontal.x = w - 50
    bala_disparada = False

def reset_bala_vertical():
    bala_vertical.x = 30 + 24
    bala_vertical.y = nave_superior.bottom

def manejar_salto():
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
    global modelo_salto_arbol, modelo_movimiento_arbol
    global modelo_salto_nn, modelo_movimiento_nn
    global modelo_salto_knn, modelo_movimiento_knn

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
    dx = abs(jugador.x - bala_horizontal.x)
    salto_hecho = 1 if salto else 0
    datos_salto.append((velocidad_bala, dx, salto_hecho))

def guardar_datos_movimiento(accion):
    dx = abs(jugador.x - bala_vertical.x)
    datos_movimiento.append(((dx, jugador.x, bala_vertical.x), accion))

def mostrar_menu():
    global menu_activo, modo_auto, modo_modelo
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona M: Manual | D: Árbol | N: Red Neuronal | K: KNN | Q: Salir", True, BLANCO)
    pantalla.blit(texto, (w // 8, h // 2))
    pygame.display.flip()
    while menu_activo:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_m:
                    modo_auto = False
                    modo_modelo = None
                    menu_activo = False
                    print("Modo manual activado.")
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
    global current_frame, frame_count, fondo_x1, fondo_x2

    fondo_x1 -= 1
    fondo_x2 -= 1
    if fondo_x1 <= -w: fondo_x1 = w
    if fondo_x2 <= -w: fondo_x2 = w
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    global current_frame, frame_count
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))
    pantalla.blit(nave_img, (nave.x, nave.y))
    pantalla.blit(nave_img, (nave_superior.x, nave_superior.y))

    if bala_disparada:
        bala_horizontal.x += velocidad_bala
        if bala_horizontal.x < 0:
            reset_bala_horizontal()

    bala_vertical.y += velocidad_bala_vertical
    if bala_vertical.y > h:
        reset_bala_vertical()

    pantalla.blit(bala_img, (bala_horizontal.x, bala_horizontal.y))
    pantalla.blit(bala_img, (bala_vertical.x, bala_vertical.y))

    if jugador.colliderect(bala_horizontal) or jugador.colliderect(bala_vertical):
        print("\u00a1Colisi\u00f3n!")
        reiniciar_juego()

def main():
    global salto, en_suelo, accion_actual, tiempo_accion
    reloj = pygame.time.Clock()
    mostrar_menu()
    correr = True
    reset_bala_horizontal()
    reset_bala_vertical()

    while correr:
        movimiento = 0
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

        if salto:
            manejar_salto()

        # Evaluar si debe regresar caminando
        destino = bala_vertical.x - jugador.width // 2
        regresar_caminando = (
            bala_vertical.y > jugador.y + jugador.height and
            abs(jugador.x - destino) > 3
        )

        if modo_auto:
            if en_suelo and prediccion_salto():
                salto = True
                en_suelo = False

            if regresar_caminando:
                if jugador.x < destino:
                    jugador.x += 6
                elif jugador.x > destino:
                    jugador.x -= 6
            else:
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
                if accion_actual == 1 and jugador.x > 0 and abs(dx) < UMBRAL_PELIGRO:
                    jugador.x -= 5
                elif accion_actual == 2 and jugador.x < w - jugador.width and abs(dx) < UMBRAL_PELIGRO:
                    jugador.x += 5
        else:
            if regresar_caminando:
                if jugador.x < destino:
                    jugador.x += 6
                elif jugador.x > destino:
                    jugador.x -= 6
            else:
                guardar_datos_salto()
                if movimiento != 0:
                    guardar_datos_movimiento(movimiento)

        if not bala_disparada:
            disparar_bala_horizontal()

        update()
        pygame.display.flip()
        reloj.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
