import pygame
import random
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def main():
    pygame.init()
    try:
        fondo = pygame.image.load('nuevo_juego/imagenes/fondo_juego.png')
    except pygame.error:
        fondo = pygame.Surface((1000, 600))
        fondo.fill((0, 0, 0))
    if fondo.get_width() < 500 or fondo.get_height() < 500:
        fondo = pygame.transform.scale(fondo, (1000, 600))
    try:
        laser_sonido = pygame.mixer.Sound('nuevo_juego/sonidos/laser.wav')
        laser_sonido.set_volume(0.3) 
        explosion_sonido = pygame.mixer.Sound('nuevo_juego/sonidos/explosion.wav')
        explosion_sonido.set_volume(0.1)
        golpe_sonido = pygame.mixer.Sound('nuevo_juego/sonidos/choque.wav')
        golpe_sonido.set_volume(0.1)
    except pygame.error:
        print("Error al cargar sonidos")
    width = fondo.get_width()
    height = fondo.get_height()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mi Juego")
    blanco = (255,255,255)
    negro = (0,0,0)
    score = 0

    def score_total(frame, text, size, x, y):
        font = pygame.font.SysFont('Small fonts', size, bold=True)
        text_frame = font.render(text, True, blanco, negro)
        text_rect = text_frame.get_rect()
        text_rect.midtop = (900, y-25)
        frame.blit(text_frame, text_rect)

    def barra_vida(frame, x, y, nivel):
        longitud = 100
        alto = 20
        fill = int((nivel/100)*longitud)
        border = pygame.Rect(855, 50, longitud, alto)
        fill_rect = pygame.Rect(855, 50, fill, alto)
        pygame.draw.rect(frame, (255,0,55), fill_rect)
        pygame.draw.rect(frame, negro, border, 4)

    class Jugador(pygame.sprite.Sprite):
        def __init__(self, width, height):
            super().__init__()
            try:
                self.image = pygame.image.load('nuevo_juego/imagenes/A1.png')
            except pygame.error:
                self.image = pygame.Surface((50, 50))
                self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.centerx = width // 2
            self.rect.centery = height - 50
            self.velocidad_x = 0
            self.velocidad = 5
            self.vida = 100
        def update(self):
            self.rect.x += self.velocidad_x
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > width:
                self.rect.right = width
        def disparar(self):
            bala = Balas(self.rect.centerx, self.rect.top)
            grupo_balas_jugador.add(bala)
            laser_sonido.play()

    class Balas(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            try:
                self.image = pygame.image.load('nuevo_juego/imagenes/B1.png').convert_alpha()
            except pygame.error:
                self.image = pygame.Surface((10, 20))
                self.image.fill((255, 255, 0))
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.bottom = y
            self.velocidad_y = -20
        def update(self):
            self.rect.y += self.velocidad_y
            if self.rect.bottom < 0:
                self.kill()

    class Balas_enemigos(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            try:
                self.image = pygame.image.load('nuevo_juego/imagenes/B2.png').convert_alpha()
                self.image = pygame.transform.rotate(self.image, 180)
            except pygame.error:
                self.image = pygame.Surface((10, 20))
                self.image.fill((0, 255, 255))
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.y = y
            self.velocidad_y = 4
        def update(self):
            self.rect.y += self.velocidad_y
            if self.rect.top > height:
                self.kill()

    class Enemigos(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            try:
                self.image = pygame.image.load('nuevo_juego/imagenes/E1.png').convert_alpha()
            except pygame.error:
                self.image = pygame.Surface((40, 40))
                self.image.fill((0, 255, 0))
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(1, width-50)
            self.rect.y = 10
            self.velocidad_x = 2
        def update(self):
            self.rect.x += self.velocidad_x
            if self.rect.right >= width or self.rect.left <= 0:
                self.velocidad_x *= -1
                self.rect.y += 20  # Baja 20 píxeles cada vez que rebota

           
        def disparar_enemigos(self):
            bala = Balas_enemigos(self.rect.centerx, self.rect.bottom)
            grupo_balas_enemigos.add(bala)
            laser_sonido.play()

    class Explosion(pygame.sprite.Sprite):
        def __init__(self, center):
            super().__init__()
            self.frames = []
            for i in range(1, 12):
                try:
                    img = pygame.image.load(f'nuevo_juego/explosion_imagen/Ex{i}.png').convert_alpha()
                except pygame.error:
                    img = pygame.Surface((50, 50))
                    img.fill((255, 128, 0))
                self.frames.append(img)
            self.frame = 0
            self.image = self.frames[self.frame]
            self.rect = self.image.get_rect(center=center)
            self.last_update = pygame.time.get_ticks()
            self.animation_duration = 100
        def update(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.animation_duration:
                self.frame += 1
                self.last_update = now
                if self.frame < len(self.frames):
                    self.image = self.frames[self.frame]
                else:
                    self.kill()

    grupo_enemigos = pygame.sprite.Group()
    grupo_balas_jugador = pygame.sprite.Group()
    grupo_balas_enemigos = pygame.sprite.Group()
    grupo_explosiones = pygame.sprite.Group()
    jugador = Jugador(width, height)
    jugadores = pygame.sprite.Group()
    jugadores.add(jugador)

    for x in range(10):
        enemigo = Enemigos(10, 10)
        grupo_enemigos.add(enemigo)

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
                elif event.key == pygame.K_SPACE:
                    jugador.disparar()
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    jugador.velocidad_x = 0

        for enemigo in grupo_enemigos:
            if random.randint(0, 125) < 1: #probabilidad de disparo 1 entre 100
                enemigo.disparar_enemigos()

        jugadores.update()
        grupo_balas_jugador.update()
        grupo_enemigos.update()
        grupo_balas_enemigos.update()
        grupo_explosiones.update()

        window.blit(fondo, (0, 0))
        jugadores.draw(window)
        grupo_enemigos.draw(window)
        grupo_balas_jugador.draw(window)
        grupo_balas_enemigos.draw(window)
        grupo_explosiones.draw(window)

        colicion1 = pygame.sprite.groupcollide(grupo_enemigos, grupo_balas_jugador, True, True)
        for enemigo in colicion1:
            score += 10
            nuevo_enemigo = Enemigos(10, 10)
            grupo_enemigos.add(nuevo_enemigo)
            explo = Explosion(enemigo.rect.center)
            grupo_explosiones.add(explo)
            explosion_sonido.set_volume(0.3)
            explosion_sonido.play()

        colicion2 = pygame.sprite.spritecollide(jugador, grupo_balas_enemigos, True)
        for bala in colicion2:
            jugador.vida -= 10
            explo1 = Explosion(jugador.rect.center)
            grupo_explosiones.add(explo1)
            golpe_sonido.play()
            if jugador.vida <= 0:
                run = False

        hits = pygame.sprite.spritecollide(jugador, grupo_enemigos, False)
        for hit in hits:
            jugador.vida -= 100
            explo2 = Explosion(jugador.rect.center)
            grupo_explosiones.add(explo2)
            golpe_sonido.play()
            if jugador.vida <= 0:
                run = False

        barra_vida(window, 50, 50, jugador.vida)
        score_total(window, f"Puntuación: {score}", 30, 400, 50)
        pygame.display.update()

    return score

def mostrar_game_over(puntuacion):
    window = pygame.display.get_surface()
    width, height = window.get_size()
    window.fill((0, 0, 0))
    font = pygame.font.SysFont('Arial', 40, bold=True)
    texto1 = font.render("¡Perdiste! Bien jugado.", True, (255, 60, 60))
    texto2 = font.render(f"Puntuación final: {puntuacion}", True, (255, 255, 255))
    texto3 = font.render("Presioná [R] para volver a jugar o [ESC] para salir", True, (200, 200, 200))
    window.blit(texto1, texto1.get_rect(center=(width // 2, height // 2 - 60)))
    window.blit(texto2, texto2.get_rect(center=(width // 2, height // 2)))
    window.blit(texto3, texto3.get_rect(center=(width // 2, height // 2 + 60)))
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando = False
                return False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True
                elif evento.key == pygame.K_ESCAPE:
                    return False

if __name__ == "__main__":
    seguir = True
    while seguir:
        score = main()
        seguir = mostrar_game_over(score)
    pygame.quit()