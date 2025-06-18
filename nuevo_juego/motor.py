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
vida=100
score=0
blanco=(255,255,255)
negro=(0,0,0)

def score_total (frame, text , size, x, y):
    font=pygame.font.SysFont('Small fonts',size, bold=True)
    text_frame= font.render(text, True, blanco,negro)
    text_rect = text_frame.get_rect()
    text_rect.midtop=(900,y-25)
    frame.blit (text_frame, text_rect)
    
def barra_vida(frame,x,y, nivel):
    longitud=100
    alto=20
    fill=int((nivel/100)*longitud)
    border=pygame.Rect (855,50, longitud, alto )
    fill= pygame.Rect(855,50,fill , alto)
    pygame.draw.rect(frame, (255,0,55),fill)
    pygame.draw.rect(frame,negro,border,4)
        
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
        
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.centery = height - 50
        self.velocidad_x = 0
        self.velocidad = 5
        self.vida=100

    def update(self):
        self.rect.x += self.velocidad_x

        # Limitar el movimiento dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

# Crear el jugador
jugador = Jugador(width, height)
jugadores = pygame.sprite.Group()
jugadores.add(jugador)

# Bucle principal
run = True
fps = 60
clock = pygame.time.Clock()

while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jugador.velocidad_x = -jugador.velocidad
            elif event.key == pygame.K_RIGHT:
                jugador.velocidad_x = jugador.velocidad

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                jugador.velocidad_x = 0

    # Actualizar y dibujar
    jugadores.update()
    window.blit(fondo, (0, 0))
    jugadores.draw(window)
    
     # Llamar a la función para dibujar la barra de vida
    barra_vida(window, 50, 50, jugador.vida)  # Cambia las coordenadas según sea necesario

    # Llamar a la función para dibujar la puntuación
    score_total(window, f"Puntuación: {score}", 30, 400, 50)
    
    pygame.display.update()



pygame.quit()