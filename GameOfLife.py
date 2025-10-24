import numpy as np
import pygame
import time

# Datos
ANCHO, ALTO = 800, 600
TAM_CELDA = 10
NX, NY = ANCHO // TAM_CELDA, ALTO // TAM_CELDA

# Colores
COLOR_FONDO = (25, 25, 25)
COLOR_CELDA_VIVA = (255, 255, 255)
COLOR_REJILLA = (40, 40, 40)

# Logica

def siguiente_generacion(estado_actual):
    # Copia para el nuevo estado
    nuevo_estado = np.copy(estado_actual)

    for y in range(NY):
        for x in range(NX):
            # Contar vecinos vivos
            # Módulo (%) para que el tablero sea infinito
            num_vecinos = estado_actual[(y-1) % NY, (x-1) % NX] + \
                          estado_actual[(y-1) % NY, (x)   % NX] + \
                          estado_actual[(y-1) % NY, (x+1) % NX] + \
                          estado_actual[(y)   % NY, (x-1) % NX] + \
                          estado_actual[(y)   % NY, (x+1) % NX] + \
                          estado_actual[(y+1) % NY, (x-1) % NX] + \
                          estado_actual[(y+1) % NY, (x)   % NX] + \
                          estado_actual[(y+1) % NY, (x+1) % NX]

            # Reglas de Conway simplificadas
            # Regla 1: Una célula muerta con exactamente 3 vecinas vivas, "nace".
            if estado_actual[y, x] == 0 and num_vecinos == 3:
                nuevo_estado[y, x] = 1
            # Regla 2: Una célula viva con menos de 2 o más de 3 vecinas vivas, "muere".
            elif estado_actual[y, x] == 1 and (num_vecinos < 2 or num_vecinos > 3):
                nuevo_estado[y, x] = 0

    return nuevo_estado

# Visualizacion

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Conway's Game of Life")

    # Estado inicial del tablero aleatorio
    estado_juego = np.random.randint(2, size=(NY, NX))

    pausa = False

    while True:
        # Copiamos el estado actual para que no cambie mientras dibujamos
        estado_a_dibujar = np.copy(estado_juego)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            # Espacio para pausar/reanudar la simulación
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pausa = not pausa

        pantalla.fill(COLOR_FONDO)

        # Dibujar Tablero
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

        # Update Step
        if not pausa:
            estado_juego = siguiente_generacion(estado_juego)
            # Velocidad
            time.sleep(0.1)

        pygame.display.flip()

if __name__ == '__main__':
    main()