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
        self.fila = fila #posicion del nodo en cuadricula
        self.col = col #posicion del nodo 
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.g = float("inf") #costo acumulado, en inf porque no conocemos su valor al inicio
        self.h = 0 #heuristica
        self.padre = None #nodo del que viene
    
    def __lt__(self, otro):
        return (self.g + self.h) < (otro.g + otro.h)
    
    
    def get_pos(self):
        return self.fila, self.col
    
    #verifica si es pared
    def es_pared(self):
        return self.color == NEGRO

    #verifica si es el inicio
    def es_inicio(self):
        return self.color == NARANJA

    #verifica si es el fin
    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO

    #se cambia el color del nodo para indicar que es el inicio
    def hacer_inicio(self):
        self.color = NARANJA

    #se cambia el color del nodo para indicar que es una pared
    def hacer_pared(self):
        self.color = NEGRO

    #se cambia el color del nodo para indicar que es el nodo final
    def hacer_fin(self):
        self.color = PURPURA

    #pintamos el camino de verde
    def hacer_camino(self):
        if not self.es_fin() and not self.es_inicio():
            self.color = VERDE

    #pintamos el nodo y si este ya se visito sus valores g,h,f
    def dibujar(self, ventana, fuente):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

        if self.g < float("inf"):  # Solo mostrar si el nodo ha sido visitado
            color_texto = NEGRO if self.color in [BLANCO, VERDE, AZUL] else BLANCO

            #impresion de g,h,f
            g_text = fuente.render(f"G:{int(self.g)}", True, color_texto)
            h_text = fuente.render(f"H:{int(self.h)}", True, color_texto)
            f_text = fuente.render(f"F:{int(self.g + self.h)}", True, color_texto)

            #nos permite ubicar el texto dentro del nodo
            ventana.blit(g_text, (self.x + 5, self.y + 5))
            ventana.blit(h_text, (self.x + 5, self.y + self.ancho // 2 - 5))
            ventana.blit(f_text, (self.x + 5, self.y + self.ancho - 15))


#Se crea la cuadricula calculando la posicion de cada cuadricula
def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

#se encarda de dibujar las lineas del grid
def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

#se encarga de dibujar la cuadricula
def dibujar(ventana, grid, filas, ancho, fuente):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana, fuente)
    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

#se encarga de obtener la posicion del click, dentro de la cuadricula
def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

#heuristica para calcular la distancia entre dos nodos, con la distancia de manhattan
def heuristica(nodo1, nodo2):
    x1, y1 = nodo1.get_pos() #fila y columna del nodo1
    x2, y2 = nodo2.get_pos() #fila y columna del nodo2
    return (abs(x1 - x2) + abs(y1 - y2)) * 10 #distancia de manhattan, valores positivos

#reconstruye el camino mas corto desde el fin hasta el inicio
def reconstruir_camino(nodo_final):
    actual = nodo_final.padre  
    camino = []
    while actual and actual.padre: #mientras todos los nodos tengan padre
        if not actual.es_fin():  
            actual.hacer_camino() #pintamos el camino de verde
        camino.append(actual.get_pos()) #agregamos la posicion del nodo al camino
        actual = actual.padre
    camino.reverse()
    print("Ruta más corta:", camino)


def a_estrella(grid, inicio, fin, ventana, filas, ancho, fuente, paso_a_paso=True):
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)] #posibles movimientos
    open_set = [] #lista abierta
    heapq.heappush(open_set, (0, inicio))
    inicio.g = 0 #inicializamos el punto de partida
    inicio.h = heuristica(inicio, fin) #calculamos la heuristica
    lista_cerrada = set()
    
    while open_set: #mientras la lista abierta no este vacia
        _, nodo_actual = heapq.heappop(open_set) #se jala el nodo con menor f 

        if nodo_actual in lista_cerrada: #valido que el nodo no este en la lista cerrada
            continue

        lista_cerrada.add(nodo_actual)

        #si ya llegamos al final que se reconstruya el camino
        if nodo_actual == fin:
            reconstruir_camino(fin)
            return True

        # Solo imprimimos las listas al presionar "Enter"
        if paso_a_paso:
            esperando = True
            while esperando:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        # Imprimir el estado actual de open_set y lista_cerrada con mejor formato
                        print("Lista abierta:", end=" ")
                        for nodo in open_set:
                            print(f"({nodo[1].fila}, {nodo[1].col})", end=" ")
                        print()  # Salto de línea

                        print("Lista cerrada:", end=" ")
                        for nodo in lista_cerrada:
                            print(f"({nodo.fila}, {nodo.col})", end=" ")
                        print()  # Salto de línea

                        esperando = False

        for dx, dy in direcciones: #visitamos los nodos vecinos
            fila, col = nodo_actual.fila + dx, nodo_actual.col + dy #Aqui unicamente calculo donde esta el vecino
            if 0 <= fila < filas and 0 <= col < filas:
                vecino = grid[fila][col] #jalamos el nodo vecino
                if vecino.es_pared() or vecino in lista_cerrada:
                    continue

                nuevo_g = nodo_actual.g + (14 if dx != 0 and dy != 0 else 10) #verificar si es movimiento diagonal
                
                #Verificar si el nuevo camino es mejor o peor y recalcular
                if nuevo_g < vecino.g:
                    vecino.g = nuevo_g
                    vecino.h = heuristica(vecino, fin)
                    vecino.padre = nodo_actual
                    heapq.heappush(open_set, (vecino.g + vecino.h, vecino))
                    # Solo actualizar el color si no es el nodo de inicio o fin
                    if vecino != inicio and vecino != fin:
                        vecino.color = AZUL

        dibujar(ventana, grid, filas, ancho, fuente)

        # Visualizar la lista cerrada (rojo) sin cambiar el color del nodo final
        for nodo in lista_cerrada:
            if nodo != inicio and nodo != fin:
                nodo.color = ROJO

    return False

def main(ventana, ancho):
    pygame.font.init()
    fuente = pygame.font.Font(None, 18)  
    FILAS = 10
    grid = crear_grid(FILAS, ancho)
    inicio = None
    fin = None
    corriendo = True
    
    while corriendo:
        dibujar(ventana, grid, FILAS, ancho, fuente)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False
            #clicks del mouse para inicio, fin y paredes
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
            #borrar nodos
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None
            #poner a chambear el algoritmo
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and inicio and fin:
                    a_estrella(grid, inicio, fin, ventana, FILAS, ancho, fuente, paso_a_paso=True)
                if event.key == pygame.K_c and inicio and fin:
                    a_estrella(grid, inicio, fin, ventana, FILAS, ancho, fuente, paso_a_paso=False)
    
    pygame.quit()

main(VENTANA, ANCHO_VENTANA)
