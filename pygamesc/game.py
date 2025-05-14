import pygame
import random
from sklearn.tree import DecisionTreeClassifier

pygame.init()

# Pantalla
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego ML - Separado y Mejorado")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Estados
salto = False
salto_altura = 15
gravedad = 1
en_suelo = True
pausa = False
menu_activo = True
modo_auto = False

# Datos y modelos
datos_salto = []
datos_movimiento = []
modelo_salto = None
modelo_movimiento = None

# Variables para cooldown movimiento
accion_actual = 0
tiempo_accion = 0
UMBRAL_TIEMPO = 10  # frames mínimos para mantener acción

# Umbral de peligro para movimiento lateral
UMBRAL_PELIGRO = 50

# Posiciones y objetos
jugador = pygame.Rect(200, h - 100, 32, 48)
bala_horizontal = pygame.Rect(w - 50, h - 90, 16, 16)
bala_vertical = pygame.Rect(jugador.x + 8, 60, 16, 16)
nave_superior = pygame.Rect(jugador.x - 16, 20, 64, 64)
nave = pygame.Rect(w - 100, h - 100, 64, 64)

# Velocidades
velocidad_bala = -6
velocidad_bala_vertical = 6
bala_disparada = False

# Animación
current_frame = 0
frame_speed = 10
frame_count = 0

# Fondo en movimiento
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
    bala_vertical.x = jugador.x + 8
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
    global modelo_salto, modelo_movimiento
    if datos_salto:
        X_salto = [(v, d) for v, d, s in datos_salto]
        y_salto = [s for v, d, s in datos_salto]
        modelo_salto = DecisionTreeClassifier()
        modelo_salto.fit(X_salto, y_salto)
        print(f"Modelo salto entrenado con {len(X_salto)} muestras.")
    else:
        modelo_salto = None

    if datos_movimiento:
        X_mov = [[dx, jug_x, bala_x] for (dx, jug_x, bala_x), accion in datos_movimiento]
        y_mov = [accion for (_, _, _), accion in datos_movimiento]
        modelo_movimiento = DecisionTreeClassifier()
        modelo_movimiento.fit(X_mov, y_mov)
        print(f"Modelo movimiento entrenado con {len(X_mov)} muestras.")
    else:
        modelo_movimiento = None

def prediccion_salto():
    if not modelo_salto:
        return False
    dx = abs(jugador.x - bala_horizontal.x)
    entrada = [(velocidad_bala, dx)]
    return modelo_salto.predict(entrada)[0] == 1

def prediccion_movimiento():
    if not modelo_movimiento:
        return 0
    dx = abs(jugador.x - bala_vertical.x)
    entrada = [[dx, jugador.x, bala_vertical.x]]
    return modelo_movimiento.predict(entrada)[0]

def guardar_datos_salto():
    dx = abs(jugador.x - bala_horizontal.x)
    salto_hecho = 1 if salto else 0
    datos_salto.append((velocidad_bala, dx, salto_hecho))

def guardar_datos_movimiento(accion):
    dx = abs(jugador.x - bala_vertical.x)
    datos_movimiento.append(((dx, jugador.x, bala_vertical.x), accion))

def mostrar_menu():
    global menu_activo, modo_auto
    pantalla.fill(NEGRO)
    texto = fuente.render("Presiona M: Manual | D: Árbol | Q: Salir", True, BLANCO)
    pantalla.blit(texto, (w // 8, h // 2))
    pygame.display.flip()
    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_m:
                    modo_auto = False
                    menu_activo = False
                    print("Modo manual activado.")
                elif evento.key == pygame.K_d:
                    modo_auto = True
                    entrenar_modelos()
                    menu_activo = False
                elif evento.key == pygame.K_q:
                    pygame.quit()
                    exit()

def reiniciar_juego():
    global salto, en_suelo, bala_disparada, menu_activo, fondo_x1, fondo_x2, accion_actual, tiempo_accion
    jugador.x, jugador.y = 200, h - 100
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

    # Mover fondo para dar sensación de desplazamiento
    fondo_x1 -= 1
    fondo_x2 -= 1
    if fondo_x1 <= -w: fondo_x1 = w
    if fondo_x2 <= -w: fondo_x2 = w
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación jugador
    global current_frame, frame_count
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Nave superior sigue al jugador
    nave_superior.x = jugador.x - 16
    pantalla.blit(nave_img, (nave_superior.x, nave_superior.y))

    # Mover balas
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
        print("¡Colisión!")
        reiniciar_juego()

def main():
    global salto, en_suelo, accion_actual, tiempo_accion
    reloj = pygame.time.Clock()
    mostrar_menu()
    correr = True
    reset_bala_horizontal()
    reset_bala_vertical()

    # Inicializar cooldown
    accion_actual = 0
    tiempo_accion = 0

    while correr:
        movimiento = 0

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo:
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

        if modo_auto:
            if en_suelo and prediccion_salto():
                salto = True
                en_suelo = False

            mov_pred = prediccion_movimiento()

            # Control cooldown para estabilizar la acción
            if mov_pred != accion_actual:
                if tiempo_accion >= UMBRAL_TIEMPO:
                    accion_actual = mov_pred
                    tiempo_accion = 0
                else:
                    tiempo_accion += 1
            else:
                tiempo_accion = 0

            # Ejecutar acción actual con lógica para salir del área de riesgo
            dx = bala_vertical.x - jugador.x
            if accion_actual == 1 and jugador.x > 0:
                if dx > 0 or abs(dx) < UMBRAL_PELIGRO:
                    jugador.x -= 5
            elif accion_actual == 2 and jugador.x < w - jugador.width:
                if dx < 0 or abs(dx) < UMBRAL_PELIGRO:
                    jugador.x += 5
            # Si accion_actual == 0 no mueve

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
