import pygame
from personaje import Personaje  

pygame.init()
# Definir la pantalla       

screen = pygame.display.set_mode([1500, 900]) #quiero que sea blanco cual es? 

pygame.display.set_caption("Mi primer juego")
try:
    player_image = pygame.image.load("asetts//imagenes//personaje1.png")
    player_image = pygame.transform.scale(player_image,(player_image.get_width()*0.09,player_image.get_height()*0.09))  # Redimensionar
except pygame.error:
    print("Error: No se pudo cargar la imagen. Verifica la ruta.")
    player_image = None  # Evita que el juego falle si la imagen no se encuentra
# Definir la clase Personaje
jugador = Personaje(20, 20,image=player_image)  # Crear una instancia del personaje con la imagen cargada

# Variables de movimiento
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

clock = pygame.time.Clock()  # Control del tiempo

running = True
while running:
    screen.fill((255, 255, 255))

    # Calcular movimiento del jugador
    delta_x = 0
    delta_y = 0

    if mover_arriba:
        delta_y = -2
    if mover_abajo:
        delta_y = 2
    if mover_izquierda:
        delta_x = -2
    if mover_derecha:
        delta_x = 2

    # Procesar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True
        elif event.type == pygame.KEYUP:  # Detectar cuando sueltas la tecla
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False

    # Aplicar movimiento al jugador
    jugador.mover(delta_x, delta_y)

    # Dibujar el personaje
    jugador.dibujar(screen)

    pygame.display.flip()
    clock.tick(60)  # Limitar la velocidad del bucle a 60 FPS

pygame.quit()