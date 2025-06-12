import pygame
pygame.init()
# Definir la clase Personaje
class Personaje():
    def __init__(self, x, y,image):
        self.flip = False

        if image:
            self.image = image.convert_alpha()  

        else:
            print("Advertencia: Imagen no válida, se usará un rectángulo blanco por defecto.")
            self.image = pygame.Surface((25, 25))
            self.image.fill((255, 0, 0))

        self.forma = pygame.Rect(x, y, 25, 25)

   
         
    
    def dibujar(self, pantalla):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False) #cambia la imagen del personaje
        if self.flip:  # Si el personaje está volteado
            pantalla.blit(imagen_flip, (self.forma.x, self.forma.y))
        else:  # Si el personaje no está volteado
           pantalla.blit(self.image, (self.forma.x, self.forma.y))  # Dibujar la imagen del personaje
        
        pygame.draw.rect(pantalla, (255, 255, 0), self.forma)  # Usar la forma directamente
        # Dibujar el personaje en la pantalla
    def mover(self, dx, dy):
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False
                
        # Mover el personaje
        self.forma.x += dx
        self.forma.y += dy
    

                
  
                