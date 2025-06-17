import pygame
import random

pygame.init()
pygame.mixer.init()

#imagen de fondo

try:
    fondo = pygame.image.load('imagenes/fondo_juego.png')
except pygame.error:
    print("Error al cargar la imagen. Verifica la ruta.")


laser_sonido=pygame.mixer.Sound('sonidos/laser.wav')


explosion_sonido=pygame.mixer.Sound('sonidos/explosion.wav')

golpe_sonido=pygame.mixer.Sound('sonidos/choque.wav')

explosion_lis=[]
for i in range (1,13):
    explosion=pygame.image.load(f'explosion_imagen{i}.png')
    explosion_lis.append(explosion)

width=fondo.get_width()
height=fondo.get_height()
window=pygame.display.set_mode((width,height))

pygame.display.set_caption("mi juego")
run=True
fps=60
clock=pygame.time.Clock()
score=0
vida=100
blanco=(255,255,255)
negro=(0,0,0)

def texto_puntacion(forme,text,size,x,y):
    font=pygame.font.SysFont('small fonts',size,bold=True)
    text_frame=font.render(text,True,blanco,negro)
    text_rect=text_frame.get_rect()
    text_rect.midtop=(x,y)
    frame.blit(text_frame,text_rect)

def barra_vida(frame,x,y,nivel):
    longitud=100
    alto=20
    fill=int((nivel/100)*longitud)
    border=pygame.rect(x,y,longitud,alto)
    pygame.draw.rect(x,y,fill,alto)
    pygame.draw.rect(frame,negro,border,4)


class jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('explocion_imagen/A1.png')
        pygame.display.set_icon(self.image)
        self.rect=self.image.get_rect()
        self.rect.centerx=width//2
        self.rect.centery=height-50
        self.velocidad_x=0
        self.vida=100


    def update(self, *args, **kwargs):
        self.velocidad_x=0
        keyscate=pygame.key.get_pressed()

pygame.quit

        










