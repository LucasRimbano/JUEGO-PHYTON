import asyncio
import json
import os
import random

import pygame


WIDTH = 960
HEIGHT = 540
FPS = 60
MAX_HIGH_SCORES = 5
SCORES_STORAGE_KEY = "nave_espacial_scores"
ASSET_DIR = os.path.dirname(os.path.abspath(__file__))


def asset(*parts):
    return os.path.join(ASSET_DIR, *parts)


class SilentSound:
    def play(self):
        pass

    def set_volume(self, _volume):
        pass


def load_image(relative_parts, size=None, alpha=True, fallback=(255, 255, 255)):
    try:
        image = pygame.image.load(asset(*relative_parts))
        image = image.convert_alpha() if alpha else image.convert()
    except pygame.error:
        image = pygame.Surface(size or (64, 64), pygame.SRCALPHA)
        image.fill(fallback)

    if size:
        image = pygame.transform.smoothscale(image, size)
    return image


def load_sound(*parts, volume=0.3):
    try:
        sound = pygame.mixer.Sound(asset(*parts))
        sound.set_volume(volume)
        return sound
    except pygame.error:
        return SilentSound()


def get_local_storage():
    try:
        import platform

        return platform.window.localStorage
    except Exception:
        return None


def load_high_scores():
    storage = get_local_storage()
    if storage is None:
        return []

    try:
        raw_scores = storage.getItem(SCORES_STORAGE_KEY)
        if not raw_scores:
            return []
        scores = json.loads(str(raw_scores))
        normalized_scores = []
        for score in scores:
            if isinstance(score, dict):
                normalized_scores.append(
                    {
                        "name": sanitize_name(score.get("name", "")),
                        "score": int(score.get("score", 0)),
                    }
                )
            else:
                normalized_scores.append({"name": "Jugador", "score": int(score)})
        return sorted(normalized_scores, key=lambda item: item["score"], reverse=True)[:MAX_HIGH_SCORES]
    except Exception:
        return []


def save_high_scores(scores):
    storage = get_local_storage()
    if storage is None:
        return

    try:
        storage.setItem(SCORES_STORAGE_KEY, json.dumps(scores[:MAX_HIGH_SCORES]))
    except Exception:
        pass


def sanitize_name(name):
    clean_name = str(name).strip()
    if not clean_name:
        return "Jugador"
    return clean_name[:14]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image(("imagenes", "A1.png"), (64, 64), fallback=(255, 80, 80))
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 22))
        self.speed = 8
        self.health = 100

    def update(self, direction):
        self.rect.x += direction * self.speed
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image(("imagenes", "B1.png"), (14, 30), fallback=(255, 255, 0))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = -13

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image(("imagenes", "B2.png"), (14, 30), fallback=(0, 255, 255))
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect(midtop=(x, y))
        self.speed = 7

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image(("imagenes", "E1.png"), (58, 58), fallback=(0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(20, WIDTH - self.rect.width - 20)
        self.rect.y = random.randrange(26, 96)
        self.speed = random.choice((-3, 3))
        self.last_drop = 0

    def update(self):
        self.rect.x += self.speed
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            now = pygame.time.get_ticks()
            if now - self.last_drop > 350:
                self.speed *= -1
                self.rect.y += 18
                self.last_drop = now


class Explosion(pygame.sprite.Sprite):
    frames = None

    def __init__(self, center):
        super().__init__()
        if Explosion.frames is None:
            Explosion.frames = [
                load_image(("explosion_imagen", f"Ex{i}.png"), (70, 70), fallback=(255, 128, 0))
                for i in range(1, 12)
            ]
        self.frame = 0
        self.image = Explosion.frames[self.frame]
        self.rect = self.image.get_rect(center=center)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 55:
            self.frame += 1
            self.last_update = now
            if self.frame >= len(Explosion.frames):
                self.kill()
            else:
                self.image = Explosion.frames[self.frame]


class Game:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            pass

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Nave Espacial")
        self.clock = pygame.time.Clock()
        self.font_path = asset("fonts", "game.otf")
        self.font_big = pygame.font.Font(self.font_path, 42)
        self.font_medium = pygame.font.Font(self.font_path, 24)
        self.font_small = pygame.font.Font(self.font_path, 18)
        self.menu_background = load_image(("imagenes", "fondo_princ.jpg"), (WIDTH, HEIGHT), alpha=False)
        self.game_background = load_image(("imagenes", "fondo_juego.png"), (WIDTH, HEIGHT), alpha=False)
        self.laser_sound = load_sound("sonidos", "laser.wav", volume=0.25)
        self.explosion_sound = load_sound("sonidos", "explosion.wav", volume=0.08)
        self.hit_sound = load_sound("sonidos", "choque.wav", volume=0.2)
        self.state = "intro"
        self.control_mode = "arrows"
        self.start_button = pygame.Rect(WIDTH // 2 - 150, 372, 300, 62)
        self.touch_left = pygame.Rect(24, HEIGHT - 88, 68, 68)
        self.touch_right = pygame.Rect(108, HEIGHT - 88, 68, 68)
        self.touch_fire = pygame.Rect(WIDTH - 92, HEIGHT - 88, 68, 68)
        self.left_pressed = False
        self.right_pressed = False
        self.fire_pressed = False
        self.last_shot = 0
        self.final_score = 0
        self.player_name = "Jugador"
        self.name_input = ""
        self.high_scores = load_high_scores()
        self.score_saved = False
        self.reset_round()

    def reset_round(self):
        self.player = Player()
        self.players = pygame.sprite.Group(self.player)
        self.enemies = pygame.sprite.Group(Enemy() for _ in range(12))
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.score = 0
        self.next_heal = 1000

    def draw_text(self, text, font, color, center, shadow=True):
        if shadow:
            shadow_image = font.render(text, True, (0, 0, 0))
            self.screen.blit(shadow_image, shadow_image.get_rect(center=(center[0] + 3, center[1] + 3)))
        image = font.render(text, True, color)
        self.screen.blit(image, image.get_rect(center=center))

    def draw_button_text(self, rect, label, active=False):
        color = (255, 233, 120) if active else (235, 235, 235)
        pygame.draw.rect(self.screen, (8, 12, 26), rect, border_radius=8)
        pygame.draw.rect(self.screen, color, rect, width=2, border_radius=8)
        self.draw_text(label, self.font_small, color, rect.center, shadow=False)

    def draw_intro(self):
        self.screen.blit(self.menu_background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 115))
        self.screen.blit(overlay, (0, 0))
        self.draw_text("Nave Espacial", self.font_big, (255, 233, 255), (WIDTH // 2, 96))
        self.draw_text("Defende tu nave y destrui la mayor cantidad de enemigos.", self.font_small, (245, 245, 245), (WIDTH // 2, 178))
        self.draw_text("Cada enemigo suma puntos. Si aguantas, recuperas vida.", self.font_small, (245, 245, 245), (WIDTH // 2, 218))
        self.draw_text("Controles: flechas o A/D para moverte, espacio para disparar.", self.font_small, (245, 245, 245), (WIDTH // 2, 258))
        pygame.draw.rect(self.screen, (10, 14, 28), self.start_button, border_radius=8)
        pygame.draw.rect(self.screen, (255, 233, 120), self.start_button, width=3, border_radius=8)
        self.draw_text("JUGAR", self.font_medium, (255, 233, 120), self.start_button.center, shadow=False)

    def draw_menu(self):
        self.screen.blit(self.menu_background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 90))
        self.screen.blit(overlay, (0, 0))
        self.draw_text("Nave Espacial", self.font_big, (255, 233, 255), (WIDTH // 2, 104))
        self.draw_text("Elegi controles y empezamos", self.font_medium, (255, 255, 255), (WIDTH // 2, 166))

        arrows = pygame.Rect(WIDTH // 2 - 270, 230, 240, 58)
        ad = pygame.Rect(WIDTH // 2 + 30, 230, 240, 58)
        self.draw_button_text(arrows, "FLECHAS", self.control_mode == "arrows")
        self.draw_button_text(ad, "A / D", self.control_mode == "ad")

        self.draw_text("Espacio dispara - R reinicia", self.font_small, (230, 230, 230), (WIDTH // 2, 334))
        self.draw_text("Tambien podes jugar tocando los botones en pantalla", self.font_small, (230, 230, 230), (WIDTH // 2, 374))
        self.draw_text("Presiona ENTER para jugar", self.font_medium, (255, 233, 120), (WIDTH // 2, 440))

    def draw_hud(self):
        pygame.draw.rect(self.screen, (15, 16, 28), (24, 22, 170, 20), border_radius=4)
        pygame.draw.rect(self.screen, (255, 0, 55), (24, 22, int(170 * self.player.health / 100), 20), border_radius=4)
        pygame.draw.rect(self.screen, (0, 0, 0), (24, 22, 170, 20), width=3, border_radius=4)
        score = self.font_small.render(f"Puntuacion: {self.score}", True, (255, 255, 255))
        self.screen.blit(score, (24, 54))

    def draw_touch_controls(self):
        controls = [
            (self.touch_left, "<", self.left_pressed),
            (self.touch_right, ">", self.right_pressed),
            (self.touch_fire, "FIRE", self.fire_pressed),
        ]
        for rect, label, active in controls:
            surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            surface.fill((12, 16, 28, 170 if active else 115))
            self.screen.blit(surface, rect)
            pygame.draw.rect(self.screen, (255, 233, 120), rect, width=2, border_radius=8)
            self.draw_text(label, self.font_small, (255, 255, 255), rect.center, shadow=False)

    def draw_game(self):
        self.screen.blit(self.game_background, (0, 0))
        self.players.draw(self.screen)
        self.enemies.draw(self.screen)
        self.player_bullets.draw(self.screen)
        self.enemy_bullets.draw(self.screen)
        self.explosions.draw(self.screen)
        self.draw_hud()
        self.draw_touch_controls()

    def draw_game_over(self):
        self.screen.blit(self.menu_background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 130))
        self.screen.blit(overlay, (0, 0))
        self.draw_text("Perdiste, bien jugado", self.font_big, (255, 80, 80), (WIDTH // 2, 92))
        self.draw_text(f"Puntuacion final: {self.final_score}", self.font_medium, (255, 255, 255), (WIDTH // 2, 158))
        self.draw_text("Mejores puntajes", self.font_medium, (255, 233, 120), (WIDTH // 2, 222))

        if self.high_scores:
            for index, entry in enumerate(self.high_scores, start=1):
                y = 252 + index * 30
                self.draw_text(
                    f"{index}. {entry['name']} - {entry['score']} puntos",
                    self.font_small,
                    (245, 245, 245),
                    (WIDTH // 2, y),
                )
        else:
            self.draw_text("Todavia no hay puntajes guardados", self.font_small, (245, 245, 245), (WIDTH // 2, 290))

        self.draw_text("Presiona R o ENTER para volver a jugar", self.font_medium, (255, 233, 120), (WIDTH // 2, 438))
        self.draw_text("Gracias por jugar", self.font_small, (255, 233, 255), (WIDTH // 2, 486))

    def draw_name_entry(self):
        self.screen.blit(self.menu_background, (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 135))
        self.screen.blit(overlay, (0, 0))
        self.draw_text("Fin de la partida", self.font_big, (255, 233, 255), (WIDTH // 2, 100))
        self.draw_text(f"Puntuacion final: {self.final_score}", self.font_medium, (255, 255, 255), (WIDTH // 2, 176))
        self.draw_text("Escribi tu nombre para guardar el puntaje", self.font_small, (245, 245, 245), (WIDTH // 2, 246))

        input_rect = pygame.Rect(WIDTH // 2 - 210, 286, 420, 58)
        pygame.draw.rect(self.screen, (8, 12, 26), input_rect, border_radius=8)
        pygame.draw.rect(self.screen, (255, 233, 120), input_rect, width=2, border_radius=8)
        display_name = self.name_input if self.name_input else "Jugador"
        self.draw_text(display_name, self.font_medium, (255, 255, 255), input_rect.center, shadow=False)

        self.draw_text("ENTER guarda - BACKSPACE borra - ESC guarda como Jugador", self.font_small, (210, 215, 230), (WIDTH // 2, 390))

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot < 220:
            return
        self.player_bullets.add(PlayerBullet(self.player.rect.centerx, self.player.rect.top))
        self.laser_sound.play()
        self.last_shot = now

    def start_game(self):
        self.reset_round()
        self.score_saved = False
        self.state = "playing"

    def record_final_score(self):
        if self.score_saved:
            return
        self.player_name = sanitize_name(self.name_input)
        self.high_scores.append({"name": self.player_name, "score": self.final_score})
        self.high_scores = sorted(self.high_scores, key=lambda item: item["score"], reverse=True)[:MAX_HIGH_SCORES]
        save_high_scores(self.high_scores)
        self.score_saved = True

    def finish_game(self):
        self.final_score = self.score
        self.name_input = ""
        self.left_pressed = False
        self.right_pressed = False
        self.fire_pressed = False
        self.state = "name_entry"

    def handle_mouse_down(self, pos):
        if self.state == "intro":
            if self.start_button.collidepoint(pos):
                self.state = "menu"
            return

        if self.state == "menu":
            if pygame.Rect(WIDTH // 2 - 270, 230, 240, 58).collidepoint(pos):
                self.control_mode = "arrows"
                self.start_game()
            elif pygame.Rect(WIDTH // 2 + 30, 230, 240, 58).collidepoint(pos):
                self.control_mode = "ad"
                self.start_game()
            return

        if self.state == "game_over":
            self.start_game()
            return

        if self.touch_left.collidepoint(pos):
            self.left_pressed = True
        if self.touch_right.collidepoint(pos):
            self.right_pressed = True
        if self.touch_fire.collidepoint(pos):
            self.fire_pressed = True
            self.shoot()

    def handle_mouse_up(self):
        self.left_pressed = False
        self.right_pressed = False
        self.fire_pressed = False

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up()

        if event.type != pygame.KEYDOWN and event.type != pygame.KEYUP:
            return True

        is_down = event.type == pygame.KEYDOWN
        if self.state == "intro" and is_down:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.state = "menu"
            elif event.key == pygame.K_ESCAPE:
                return False
        elif self.state == "menu" and is_down:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.control_mode = "arrows"
                self.start_game()
            elif event.key in (pygame.K_a, pygame.K_d):
                self.control_mode = "ad"
                self.start_game()
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.start_game()
            elif event.key == pygame.K_ESCAPE:
                return False
        elif self.state == "name_entry" and is_down:
            if event.key == pygame.K_RETURN:
                self.record_final_score()
                self.state = "game_over"
            elif event.key == pygame.K_ESCAPE:
                self.name_input = "Jugador"
                self.record_final_score()
                self.state = "game_over"
            elif event.key == pygame.K_BACKSPACE:
                self.name_input = self.name_input[:-1]
            elif event.unicode and event.unicode.isprintable() and len(self.name_input) < 14:
                self.name_input += event.unicode
        elif self.state == "game_over" and is_down:
            if event.key in (pygame.K_r, pygame.K_RETURN, pygame.K_SPACE):
                self.start_game()
            elif event.key == pygame.K_ESCAPE:
                return False
        elif self.state == "playing":
            if event.key == pygame.K_r and is_down:
                self.start_game()
            elif event.key == pygame.K_ESCAPE and is_down:
                self.finish_game()
            elif event.key == pygame.K_SPACE and is_down:
                self.shoot()
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.left_pressed = is_down
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.right_pressed = is_down
        return True

    def update_game(self):
        keys = pygame.key.get_pressed()
        keyboard_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        keyboard_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        keyboard_fire = keys[pygame.K_SPACE]
        direction = int(self.right_pressed or keyboard_right) - int(self.left_pressed or keyboard_left)
        if self.fire_pressed or keyboard_fire:
            self.shoot()

        self.players.update(direction)
        self.player_bullets.update()
        self.enemy_bullets.update()
        self.enemies.update()
        self.explosions.update()

        for enemy in self.enemies:
            if random.randrange(60) == 0:
                self.enemy_bullets.add(EnemyBullet(enemy.rect.centerx, enemy.rect.bottom))

        hits = pygame.sprite.groupcollide(self.enemies, self.player_bullets, True, True)
        for enemy in hits:
            self.score += 10
            self.enemies.add(Enemy())
            self.explosions.add(Explosion(enemy.rect.center))
            self.explosion_sound.play()

        player_hits = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        for _bullet in player_hits:
            self.player.health -= 10
            self.explosions.add(Explosion(self.player.rect.center))
            self.hit_sound.play()

        enemy_crashes = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if enemy_crashes:
            self.player.health = 0
            self.explosions.add(Explosion(self.player.rect.center))
            self.hit_sound.play()

        if self.score >= self.next_heal:
            self.player.health = 100
            self.next_heal += 1000

        if self.player.health <= 0:
            self.finish_game()

    async def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                running = self.handle_event(event)
                if not running:
                    break

            if self.state == "playing":
                self.update_game()
                self.draw_game()
            elif self.state == "intro":
                self.draw_intro()
            elif self.state == "menu":
                self.draw_menu()
            elif self.state == "name_entry":
                self.draw_name_entry()
            else:
                self.draw_game_over()

            pygame.display.flip()
            await asyncio.sleep(0)

        pygame.quit()


async def main():
    await Game().run()


if __name__ == "__main__":
    asyncio.run(main())
