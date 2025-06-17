import pygame

class Jugador(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        try:
            self.image = pygame.image.load('nuevo_juego/imagenes/A1.png')
        except pygame.error:
            print("Error al cargar la imagen del jugador. Verifica la ruta.")
            self.image = pygame.Surface((50, 50))  
            self.image.fill((255, 0, 0))  # Cuadrado rojo si la imagen falla
        
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.centery = height - 50
        self.velocidad_x = 0
        self.vida = 100





