import numpy as np
import pygame
import time

# Datos
ANCHO, ALTO = 800, 600
# TAM_CELDA_BASE para el zoom
TAM_CELDA_BASE = 10 
NX, NY = 160, 120 # Tamaño del mundo
DENSIDAD_INICIAL = 0.2

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

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Game of Life | Rueda: Zoom | Clic central: Mover | Espacio: Pausa")

    estado_juego = (np.random.rand(NY, NX) < DENSIDAD_INICIAL).astype(int)
    pausa = True

    zoom = 1.0
    offsetX, offsetY = 0, 0
    arrastrando = False
    pos_arrastre_inicio = (0, 0)

    while True:
        estado_a_dibujar = np.copy(estado_juego)
        pantalla.fill(COLOR_FONDO)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pausa = not pausa
            
            if event.type == pygame.MOUSEWHEEL:
                # 1. Obtenemos la posición del ratón y el zoom antiguo
                mx, my = pygame.mouse.get_pos()
                zoom_viejo = zoom

                # 2. Calculamos la posición en el mundo que está bajo el ratón ANTES del zoom
                mundo_x_antes = offsetX + mx
                mundo_y_antes = offsetY + my

                # 3. Aplicamos el nuevo zoom
                zoom += event.y * 0.1
                zoom = max(0.2, min(5.0, zoom))

                # 4. Calculamos dónde estaría ese mismo punto del mundo DESPUÉS del zoom
                mundo_x_despues = mundo_x_antes * (zoom / zoom_viejo)
                mundo_y_despues = mundo_y_antes * (zoom / zoom_viejo)

                # 5. Ajustamos el offset para que el punto vuelva a estar bajo el ratón
                offsetX = mundo_x_despues - mx
                offsetY = mundo_y_despues - my
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and pausa:
                    mouseX, mouseY = event.pos
                    celdaX = int((mouseX + offsetX) / (TAM_CELDA_BASE * zoom))
                    celdaY = int((mouseY + offsetY) / (TAM_CELDA_BASE * zoom))
                    if 0 <= celdaX < NX and 0 <= celdaY < NY:
                         estado_juego[celdaY, celdaX] = not estado_juego[celdaY, celdaX]
                elif event.button == 2:
                    arrastrando = True
                    pos_arrastre_inicio = event.pos
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    arrastrando = False

            if event.type == pygame.MOUSEMOTION:
                if arrastrando:
                    # El movimiento del offset debe tener en cuenta el zoom actual para que la velocidad de paneo sea consistente
                    dx = event.rel[0] / zoom
                    dy = event.rel[1] / zoom
                    offsetX -= dx
                    offsetY -= dy
        
        # Logica de dibujo
        tam_celda_actual = TAM_CELDA_BASE * zoom
        
        x_start = max(0, int(offsetX / tam_celda_actual))
        y_start = max(0, int(offsetY / tam_celda_actual))
        x_end = min(NX, int((offsetX + ANCHO) / tam_celda_actual) + 1)
        y_end = min(NY, int((offsetY + ALTO) / tam_celda_actual) + 1)

        for y in range(y_start, y_end):
            for x in range(x_start, x_end):
                screen_x = x * tam_celda_actual - offsetX
                screen_y = y * tam_celda_actual - offsetY
                
                poly = [(screen_x, screen_y),
                        (screen_x + tam_celda_actual, screen_y),
                        (screen_x + tam_celda_actual, screen_y + tam_celda_actual),
                        (screen_x, screen_y + tam_celda_actual)]
                
                if estado_a_dibujar[y, x] == 1:
                    pygame.draw.polygon(pantalla, COLOR_CELDA_VIVA, poly, 0)
                if zoom > 0.5:
                    pygame.draw.polygon(pantalla, COLOR_REJILLA, poly, 1)

        if not pausa:
            estado_juego = siguiente_generacion(estado_juego)
            time.sleep(0.05)

        pygame.display.flip()

if __name__ == '__main__':
    main()