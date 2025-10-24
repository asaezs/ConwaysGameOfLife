import numpy as np
import pygame
import time

# Datos
ANCHO, ALTO = 800, 600
TAM_CELDA = 10
NX, NY = ANCHO // TAM_CELDA, ALTO // TAM_CELDA
DENSIDAD_INICIAL = 0.1

# Colores
COLOR_FONDO = (25, 25, 25)
COLOR_CELDA_VIVA = (255, 255, 255)
COLOR_REJILLA = (40, 40, 40)

# Logica

def siguiente_generacion(estado_actual):
    nuevo_estado = np.copy(estado_actual)

    for y in range(NY):
        for x in range(NX):
            num_vecinos = estado_actual[(y-1) % NY, (x-1) % NX] + \
                          estado_actual[(y-1) % NY, (x)   % NX] + \
                          estado_actual[(y-1) % NY, (x+1) % NX] + \
                          estado_actual[(y)   % NY, (x-1) % NX] + \
                          estado_actual[(y)   % NY, (x+1) % NX] + \
                          estado_actual[(y+1) % NY, (x-1) % NX] + \
                          estado_actual[(y+1) % NY, (x)   % NX] + \
                          estado_actual[(y+1) % NY, (x+1) % NX]

            if estado_actual[y, x] == 0 and num_vecinos == 3:
                nuevo_estado[y, x] = 1
            elif estado_actual[y, x] == 1 and (num_vecinos < 2 or num_vecinos > 3):
                nuevo_estado[y, x] = 0

    return nuevo_estado

# Visualizacion

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Conway's Game of Life - Barra espaciadora para pausar")

    # Estado inicial usando la variable de densidad
    estado_juego = (np.random.rand(NY, NX) < DENSIDAD_INICIAL).astype(int)

    pausa = False

    while True:
        # Copiamos el estado para evitar problemas si se modifica mientras se dibuja
        estado_a_dibujar = np.copy(estado_juego)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pausa = not pausa
            
            # Manejo de clics del ratón para cambiar células
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pausa:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    celdaX, celdaY = mouseX // TAM_CELDA, mouseY // TAM_CELDA
                    estado_juego[celdaY, celdaX] = not estado_juego[celdaY, celdaX]

        pantalla.fill(COLOR_FONDO)

        for y in range(NY):
            for x in range(NX):
                poly = [((x)   * TAM_CELDA, y * TAM_CELDA),
                        ((x+1) * TAM_CELDA, y * TAM_CELDA),
                        ((x+1) * TAM_CELDA, (y+1) * TAM_CELDA),
                        ((x)   * TAM_CELDA, (y+1) * TAM_CELDA)]
                
                if estado_a_dibujar[y, x] == 1:
                    pygame.draw.polygon(pantalla, COLOR_CELDA_VIVA, poly, 0)
                else:
                    pygame.draw.polygon(pantalla, COLOR_REJILLA, poly, 1)

        if not pausa:
            estado_juego = siguiente_generacion(estado_juego)
            time.sleep(0.1)

        pygame.display.flip()

if __name__ == '__main__':
    main()