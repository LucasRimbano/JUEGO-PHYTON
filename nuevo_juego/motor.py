import pygame

# Inicializar pygame
pygame.init()

# Configuración de pantalla
try:
    fondo = pygame.image.load('nuevo_juego/imagenes/fondo_juego.png')
except pygame.error:
    print("Error al cargar la imagen de fondo. Verifica la ruta.")
    fondo = pygame.Surface((1000, 600))  
    fondo.fill((0, 0, 0))  # Fondo negro en caso de error

if fondo.get_width() < 500 or fondo.get_height() < 500:
    fondo = pygame.transform.scale(fondo, (1000, 600))

width = fondo.get_width()
height = fondo.get_height()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mi Juego")


# Clase del jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        try:
            self.image = pygame.image.load('nuevo_juego/imagenes/A1.png')
        except pygame.error:
            print("Error al cargar la imagen del jugador. Verifica la ruta.")
            self.image = pygame.Surface((50, 50))  
            self.image.fill((255, 0, 0))  # Cuadrado rojo en caso de error
        
        pygame.display.set_icon(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.centery = height - 50
        self.velocidad_x = 0
        self.vida = 100


# Instancia del jugador
jugador = Jugador(width, height)
jugadores = pygame.sprite.Group()
jugadores.add(jugador)

# Bucle principal del juego
run = True
fps = 60
clock = pygame.time.Clock()

while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.blit(fondo, (0, 0))
    jugadores.draw(window)  # Dibujar el jugador
    pygame.display.update()

pygame.quit()

        










