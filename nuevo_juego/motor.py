import pygame
import random

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


try:
    laser_sonido = pygame.mixer.Sound('nuevo_juego/sonidos/laser.wav')
    explosion_sonido = pygame.mixer.Sound('nuevo_juego/sonidos/explosion.wav')
    golpe_sonido =pygame.mixer.Sound('nuevo_juego/sonidos/choque.wav')
except pygame.error:
    print("Error al cargar uno de los sonidos .wav")

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
    
    def disparar(self):
        bala = Balas(self.rect.centerx, self.rect.top)
        grupo_jugador.add(bala)
        grupo_balas_jugador.add(bala)
        laser_sonido.play()
# Clase de las balas
class Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load('nuevo_juego/imagenes/B1.png').convert_alpha()
        except pygame.error:
            print("Error al cargar la imagen de la bala. Verifica la ruta.")
            self.image = pygame.Surface((10, 20))
            self.image.fill((255, 255, 0))  # Cuadrado amarillo en caso de error
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidad_y = -20

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom < 0:
            self.kill()

class Balas_enemigos(pygame.sprite.Sprite):
    #balas enemigas neceitan un alto cambio
    # porque aparecen en tu cabeza y no salen de los enemigos 
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('nuevo_juego/imagenes/B2.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image,180)
        self.rect = self.image.get_rect()
        self.rect.centerx=x
        self.rect.y=random.randrange(3,width)
        self.velocidad_y=4
    
    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom>height:
            self.kill()

class Enemigos(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('nuevo_juego/imagenes/E1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1,width-50)
        self.rect.y = 10
        self.velocidad_y = random.randrange(-5,20)
    
    def update(self):
        self.time = random.randrange(-1,pygame.time.get_ticks()//5000)
        self.rect.x += self.time 
        if self.rect.x >= width:
            self.rect.x = 0
            self.rect.y += 37
    def disparar_enemigos(self):
        bala=Balas_enemigos(self.rect.centerx,self.rect.bottom)
        grupo_jugador.add(bala)
        grupo_balas_enemigos.add(bala)
        laser_sonido.play()

# Clase de explosión
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.frames = []
        for i in range(1, 12):  # Cargar imágenes de A1.png a A11.png
            try:
                img = pygame.image.load(f'nuevo_juego/explosion_imagen/Ex{i}.png').convert_alpha()
                
                self.frames.append(img)
            except pygame.error:
                print(f"Error al cargar la imagen de explosión Ex{i}.png. Verifica la ruta.")
        
        self.frame = 0
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect(center=center)
        self.last_update = pygame.time.get_ticks()
        self.animation_duration = 100  # Duración de cada frame en milisegundos

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_duration:
            self.frame += 1
            self.last_update = now
            if self.frame < len(self.frames):
                self.image = self.frames[self.frame]  # Cambiar a la siguiente imagen
            else:
                self.kill()  # Eliminar la explosión después de que termine
grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_jugador = pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()
grupo_explosiones = pygame.sprite.Group()

# Crear el jugador
jugador = Jugador(width, height)
jugadores = pygame.sprite.Group()
jugadores.add(jugador)
grupo_balas_jugador.add(jugador)


# Bucle principal
run = True
fps = 60
clock = pygame.time.Clock()

for x in range(10):
    enemigo = Enemigos(10,10)
    grupo_enemigos.add(enemigo)
    grupo_jugador.add(enemigo)

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
            elif event.key == pygame.K_SPACE:
                jugador.disparar()

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                jugador.velocidad_x = 0
        
        for enemigo in grupo_enemigos:
            if random.randint(0,100)<2:
                enemigo.disparar_enemigos()


    # Actualizar y dibujar
    jugadores.update()
    grupo_balas_jugador.update()
    grupo_enemigos.update()
    grupo_balas_enemigos.update()
    window.blit(fondo, (0, 0))
    jugadores.draw(window)
    grupo_enemigos.draw(window)
    grupo_balas_jugador.draw(window)
    grupo_balas_enemigos.draw(window)
    grupo_explosiones.update()
    grupo_explosiones.draw(window)

    colicion1 = pygame.sprite.groupcollide(grupo_enemigos, grupo_balas_jugador,True,True)
    for i in colicion1:
        score+=10
        enemigo.disparar_enemigos()
        enemigo = Enemigos(300,10)
        grupo_enemigos.add(enemigo)
        grupo_jugador.add(enemigo)

        explo = Explosion((i.rect.centerx, i.rect.centery - 30))
        grupo_explosiones.add(explo)
        explosion_sonido.set_volume(0.3)
        explosion_sonido.play()
    
    colicion2 = pygame.sprite.spritecollide(jugador,grupo_balas_enemigos,True)
    for j in colicion2:
        jugador.vida -= 10
        if jugador.vida <=0:
            run = False
        explo1 = Explosion((i.rect.centerx, i.rect.centery - 30))
        grupo_jugador.add(explo1)
        golpe_sonido.play()

    hits = pygame.sprite.spritecollide(jugador,grupo_enemigos,False)
    for hit in hits:
        jugador.vida -=100
        enemigos = Enemigos (10,10)
        grupo_explosiones.add(enemigos)
        grupo_enemigos.add(enemigos)
        if jugador.vida<=0:
            run = False

   
     # Llamar a la función para dibujar la barra de vida
    barra_vida(window, 50, 50, jugador.vida)  # Cambia las coordenadas según sea necesario

    # Llamar a la función para dibujar la puntuación
    score_total(window, f"Puntuación: {score}", 30, 400, 50)
    
    pygame.display.update()



pygame.quit()