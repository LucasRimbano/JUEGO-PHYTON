import pygame
import random
import os
import time
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def medir_tiempo(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        resultado = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} se ejecutó en {end - start:.4f} segundos")
        return resultado
    return wrapper

@medir_tiempo
def disparar():
    # lógica de disparo simulada
    time.sleep(0.1)
    
def menu_controles():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    try:
        fondo_imagen = pygame.image.load('nuevo_juego/imagenes/fondo_princ.jpg')
        fondo_imagen = pygame.transform.scale(fondo_imagen, (screen.get_width(), screen.get_height()))
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {e}")
        fondo_imagen = None  # Asigna None o una imagen por defecto si falla
    if fondo_imagen:
        screen.blit(fondo_imagen, (0, 0))
    else:
        screen.fill((0, 0, 0))
    

    pygame.display.set_caption("Seleccioná los controles")
    font = pygame.font.SysFont('Arial', 30)
    font2 = pygame.font.SysFont('Arial', 70)
    seleccion = None

    while seleccion is None:
        if fondo_imagen:
            screen.blit(fondo_imagen, (0, 0))
        else:
            screen.fill((30, 30, 30))
      
        titulo1 = font2.render("¡Bienvenido al juego!", True, (255, 233, 255))
        titulo2= font.render("Selecciona tu modo de control", True, (255, 255, 255)) 
        titulo3 = font.render("¿Como queres moverte?", True, (255, 255, 255))
        opcion1 = font.render("Presiona [←][→] Flechitas", True, (200, 202, 200))
        opcion2 = font.render("Presiona [A][D] WASD", True, (200, 202, 200))
        opcion4 = font.render("Presiona [R] para reiniciar", True, (200, 202, 200))
        opcion6= font.render("CON [SPACE] disparas", True, (200, 202, 200))
        titulo4 = font.render("Presiona [ESC] para salir", True, (200, 202, 200))   
        titulo5 = font.render("¡Para entrar al juego apreta [←][→]  SI queres moverte con las flechas!", True, (255, 233, 255))   
        titulo6 = font.render("¡Para entrar al juego apreta [A][D]  SI queres moverte con AD!", True, (255, 233, 255))
        textos =[
             (titulo1, (700, 15)),
            (titulo2, (800, 108)),
            (titulo3, (800, 150)),
            (opcion1, (800, 200)),
            (opcion2, (800, 250)),
            (opcion4, (800, 320)),
            (opcion6, (800, 380)),
            (titulo4, (800, 440)),
            (titulo5, (590, 800)),
            (titulo6, (590, 860)),
            
        ]
       
        
        for texto, pos in textos:
            rect = texto.get_rect(topleft=pos)
            rect.inflate_ip(20, 10)  # Margen alrededor del texto
            pygame.draw.rect(screen, (0, 0, 0), rect, border_radius=12)
            screen.blit(texto, pos)

        
        pygame.display.flip()

        for evento in pygame.event.get():
        
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    print("esc valido")
                    pygame.quit()
                    exit()
                if evento.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    seleccion = "flechas"
                elif evento.key in [pygame.K_a, pygame.K_d]:
                    seleccion = "ad"
    return seleccion
def main():
    pygame.init()
    control = menu_controles()
    
    try:
        info = pygame.display.Info()
        screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
        fondo = pygame.image.load('nuevo_juego/imagenes/fondo_juego.png')
        fondo = pygame.transform.scale(fondo, (info.current_w, info.current_h))
    except pygame.error:
        info = pygame.display.Info()
        screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
        fondo = pygame.Surface((1000, 600))
        fondo.fill((0, 0, 0))
    if fondo.get_width() < 500 or fondo.get_height() < 500:
        fondo = pygame.transform.scale(fondo, (1000, 600))
    

    try:
        laser_sonido = pygame.mixer.Sound('nuevo_juego/sonidos/laser.wav')
        laser_sonido.set_volume(0.3) 
        explosion_sonido = pygame.mixer.Sound('nuevo_juego/sonidos/explosion.wav')
        explosion_sonido.set_volume(0.0000000000002)
        golpe_sonido = pygame.mixer.Sound('nuevo_juego/sonidos/choque.wav')
        golpe_sonido.set_volume(0.2)
    except pygame.error:
        print("Error al cargar sonidos")
        
    width = fondo.get_width()
    height = fondo.get_height()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mi Juego")
    blanco = (255,255,255)
    negro = (0,0,0)
    score = 0
    curacion_max = 1000

    def score_total(frame, text, size, x, y):
        font = pygame.font.SysFont('Small fonts', size, bold=True)
        text_frame = font.render(text, True, blanco, negro)
        text_rect = text_frame.get_rect()
        text_rect.midtop = (1840, y-25)
        frame.blit(text_frame, text_rect)

    def barra_vida(frame, x, y, nivel):
        longitud = 100
        alto = 20
        fill = int((nivel/100)*longitud)
        border = pygame.Rect(1770, 50, longitud, alto)
        fill_rect = pygame.Rect(1770, 50, fill, alto)
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
            self.velocidad = 20
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
            self.velocidad_y = -35
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
            self.velocidad_y = 15
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
            self.velocidad_x = 10
            self.puede_bajar = True
            self.last_bajada_time = 0 

        
        def update(self):
            self.rect.x += self.velocidad_x
            if self.rect.right >= width or self.rect.left <= 0:
                current_time = time.time()
                if self.puede_bajar and (current_time - self.last_bajada_time > 0.7):
                 self.velocidad_x *= -1
                 self.rect.y += 20  # Baja 20 píxeles cada vez que rebota
                 self.last_bajada_time = current_time


           
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

    for x in range(12):
        enemigo = Enemigos(10, 10)
        grupo_enemigos.add(enemigo)

    run = True
    fps = 60
    clock = pygame.time.Clock()
    enemigos_que_disparan = set()
    curacion_max = 1000  # Puntuación para curar al jugador
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_r:
                    return mostrar_game_over()
                if control == "flechas":
                    if event.key == pygame.K_LEFT:
                        jugador.velocidad_x = -jugador.velocidad
                    elif event.key == pygame.K_RIGHT:
                        jugador.velocidad_x = jugador.velocidad
                    elif event.key == pygame.K_SPACE:
                        jugador.disparar()
                elif control == "ad":
                    if event.key == pygame.K_a:
                        jugador.velocidad_x = -jugador.velocidad
                    elif event.key == pygame.K_d:
                        jugador.velocidad_x = jugador.velocidad
                    elif event.key == pygame.K_SPACE:
                        jugador.disparar()
            elif event.type == pygame.KEYUP:
                if control == "flechas":
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        jugador.velocidad_x = 0
                elif control == "ad":
                    if event.key == pygame.K_a or event.key == pygame.K_d:
                        jugador.velocidad_x = 0
                
        enemigos_que_disparan = set()  # Reinicia el conjunto de enemigos que disparan en cada frame
        for enemigo in grupo_enemigos:
            if random.randint(0, 25 ) < 1 and enemigo not in enemigos_que_disparan:
                enemigo.disparar_enemigos()
                enemigos_que_disparan.add(enemigo)

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
        enemigos_que_disparan.clear()
        
        colicion1 = pygame.sprite.groupcollide(grupo_enemigos, grupo_balas_jugador, True, True)
        for enemigo in colicion1:
            score += 10
            nuevo_enemigo = Enemigos(10, 10)
            grupo_enemigos.add(nuevo_enemigo)
            explo = Explosion((enemigo.rect.centerx, enemigo.rect.centery - 25))
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
        if score >= curacion_max:
            jugador.vida = 100 # Restablece la vida del jugador al máximo
            curacion_max += 1000 # Actualiza el próximo hito de puntuación 
            print(f"¡Vida restablecida! Próximo punto de vida extra: {curacion_max}") 


        pygame.display.update()

    return score

def mostrar_game_over(puntuacion):
    window = pygame.display.get_surface()
    width, height = window.get_size()
    window.fill((0, 0, 0))
    font = pygame.font.SysFont('Arial', 40, bold=True)
    texto1 = font.render("¡Perdiste! Bien jugado.", True, (255, 60, 60))
    texto2 = font.render(f"Puntuacion final: {puntuacion}", True, (255, 255, 255))
    texto3 = font.render("Presiona [R] para volver a jugar o [ESC] para salir", True, (200, 200, 200))
    texto4 = font.render("¡Gracias por jugar!", True, (255, 233, 255))
    window.blit(texto1, texto1.get_rect(center=(width // 2, height // 2 - 60)))
    window.blit(texto2, texto2.get_rect(center=(width // 2, height // 2)))
    window.blit(texto3, texto3.get_rect(center=(width // 2, height // 2 + 60)))
    window.blit(texto4, texto4.get_rect(center=(width // 2, height // 2 + 120)))
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