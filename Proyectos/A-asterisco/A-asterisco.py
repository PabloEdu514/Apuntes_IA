import pygame
import heapq

# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de A*")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
AZUL = (0, 0, 255)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.g = float("inf")
        self.h = 0
        self.padre = None
    
    def __lt__(self, otro):
        return (self.g + self.h) < (otro.g + otro.h)

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_camino(self):
        if not self.es_fin() and not self.es_inicio():
            self.color = VERDE

    def dibujar(self, ventana, fuente):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

        if self.g < float("inf"):  # Solo mostrar si el nodo ha sido visitado
            color_texto = NEGRO if self.color in [BLANCO, VERDE, AZUL] else BLANCO

            g_text = fuente.render(f"G:{int(self.g)}", True, color_texto)
            h_text = fuente.render(f"H:{int(self.h)}", True, color_texto)
            f_text = fuente.render(f"F:{int(self.g + self.h)}", True, color_texto)

            ventana.blit(g_text, (self.x + 5, self.y + 5))
            ventana.blit(h_text, (self.x + 5, self.y + self.ancho // 2 - 5))
            ventana.blit(f_text, (self.x + 5, self.y + self.ancho - 15))

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho, fuente):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana, fuente)
    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

def heuristica(nodo1, nodo2):
    x1, y1 = nodo1.get_pos()
    x2, y2 = nodo2.get_pos()
    return (abs(x1 - x2) + abs(y1 - y2))*10

def reconstruir_camino(nodo_final):
    actual = nodo_final.padre  
    camino = []
    while actual and actual.padre:
        if not actual.es_fin():  
            actual.hacer_camino()
        camino.append(actual.get_pos())
        actual = actual.padre
    camino.reverse()
    print("Ruta más corta:", camino)

def a_estrella(grid, inicio, fin, ventana, filas, ancho, fuente, paso_a_paso=True):
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    open_set = []
    heapq.heappush(open_set, (0, inicio))
    inicio.g = 0
    inicio.h = heuristica(inicio, fin)
    lista_cerrada = set()
    
    while open_set:
        _, nodo_actual = heapq.heappop(open_set)

        if nodo_actual in lista_cerrada:
            continue

        lista_cerrada.add(nodo_actual)
        
        if nodo_actual == fin:
            reconstruir_camino(fin)
            return True

        for dx, dy in direcciones:
            fila, col = nodo_actual.fila + dx, nodo_actual.col + dy
            if 0 <= fila < filas and 0 <= col < filas:
                vecino = grid[fila][col]
                if vecino.es_pared() or vecino in lista_cerrada:
                    continue

                nuevo_g = nodo_actual.g + (14 if dx != 0 and dy != 0 else 10)

                if nuevo_g < vecino.g:
                    vecino.g = nuevo_g
                    vecino.h = heuristica(vecino, fin)
                    vecino.padre = nodo_actual
                    heapq.heappush(open_set, (vecino.g + vecino.h, vecino))
                    if not vecino.es_fin():
                        vecino.color = AZUL
        
        dibujar(ventana, grid, filas, ancho, fuente)
        
        if paso_a_paso:
            esperando = True
            while esperando:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        esperando = False
    
    return False

def main(ventana, ancho):
    pygame.font.init()
    fuente = pygame.font.Font(None, 18)  
    FILAS = 15
    grid = crear_grid(FILAS, ancho)
    inicio = None
    fin = None
    corriendo = True
    
    while corriendo:
        dibujar(ventana, grid, FILAS, ancho, fuente)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio:
                    inicio = nodo
                    inicio.hacer_inicio()
                elif not fin:
                    fin = nodo
                    fin.hacer_fin()
                else:
                    nodo.hacer_pared()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and inicio and fin:
                    a_estrella(grid, inicio, fin, ventana, FILAS, ancho, fuente, paso_a_paso=True)
                if event.key == pygame.K_c and inicio and fin:
                    a_estrella(grid, inicio, fin, ventana, FILAS, ancho, fuente, paso_a_paso=False)
    
    pygame.quit()

main(VENTANA, ANCHO_VENTANA)
