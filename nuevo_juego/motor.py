import pygame

pygame.init()

# Imagen de fondo
try:
    fondo = pygame.image.load('imagenes/fondo_juego.png')
except pygame.error:
    print("Error al cargar la imagen. Verifica la ruta.")
    fondo = pygame.Surface((500, 500)) 

# Configuracion de pantalla
width = fondo.get_width()
height = fondo.get_height()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mi Juego")



run = True
fps = 60
clock = pygame.time.Clock()


while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    
    window.blit(fondo, (0, 0))
    pygame.display.update()

pygame.quit()


        










