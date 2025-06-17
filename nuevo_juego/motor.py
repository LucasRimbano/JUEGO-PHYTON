import pygame

pygame.init()

# Imagen de fondo
try:
    fondo = pygame.image.load('nuevo_juego//imagenes//fondo_juego.png')
except pygame.error:
    print("Error al cargar la imagen. Verifica la ruta.")
    fondo = pygame.Surface((500, 500)) 
#quiero que me pantalla seamas grande que la imagen de fondo
    fondo.fill((0, 0, 0))

# Si la imagen de fondo es más pequeña que la pantalla, la escalamos
if fondo.get_width() < 500 or fondo.get_height() < 500:
    fondo = pygame.transform.scale(fondo, (1000, 600))       
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


        










