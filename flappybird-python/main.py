"""
Fixed Flappy Bird - single file runnable version
- Optional MySQL leaderboard (falls back to local JSON file if not available)
- Start, Game, End screens
- Simple procedural assets
Run:
    python main2.py
Requires:
    pip install pygame
"""

import pygame
import sys
import random
import math
import json
import os
from typing import List, Tuple

# optional mysql connector
try:
    import mysql.connector as mysql
except Exception:
    mysql = None

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
BIRD_START_X = 100
FPS = 60
# Physics in pixels / second units
GRAVITY = 1200.0        # px / s^2
JUMP_STRENGTH = -320.0  # initial upward velocity px / s
MAX_VELOCITY = 900.0    # terminal velocity px / s
PIPE_GAP = 150
PIPE_INTERVAL = 1400  # ms
PIPE_SPEED = 200.0    # px / s (pipe moves left)
BIRD_START_X = 100
BIRD_START_X = 100
GROUND_HEIGHT = 100
FONT_NAME = 'freesansbold.ttf'

ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
LEADERBOARD_FILE = os.path.join(ASSETS_DIR, 'leaderboard.json')
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR, exist_ok=True)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 250)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (144, 238, 144)
GRAY = (200, 200, 200)

# Screen and clock
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy - Fixed')
CLOCK = pygame.time.Clock()

# Simple procedural assets
bird_frames = [pygame.Surface((34, 24), pygame.SRCALPHA) for _ in range(3)]
for i, surf in enumerate(bird_frames):
    color = (255, max(0, 200 - i * 40), 0)
    pygame.draw.ellipse(surf, color, surf.get_rect())

pipe_img = pygame.Surface((80, 500), pygame.SRCALPHA)
pygame.draw.rect(pipe_img, (0, 180, 0), (0, 0, 80, 500), border_radius=20)

background_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
background_img.fill(SKY_BLUE)
cloud = pygame.Surface((100, 60), pygame.SRCALPHA)
pygame.draw.ellipse(cloud, WHITE, cloud.get_rect())
background_img.blit(cloud, (50, 100))
background_img.blit(cloud, (200, 150))
background_img.blit(cloud, (300, 80))

# Utility
def draw_text(surface, text, size, x, y, color=BLACK, center=True):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

# Leaderboard with optional MySQL, otherwise local JSON
class Leaderboard:
    def __init__(self):
        self.mysql_conn = None
        self.mysql_cursor = None
        if mysql is not None:
            try:
                # Attempt to connect (user should edit credentials if they want this)
                self.mysql_conn = mysql.connect(
                    host='localhost', user='your_mysql_username', password='your_mysql_password', database='flappy_game'
                )
                self.mysql_cursor = self.mysql_conn.cursor()
            except Exception:
                self.mysql_conn = None
                self.mysql_cursor = None
        # ensure json file exists
        if not os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def save_score(self, name: str, score: int):
        if self.mysql_conn and self.mysql_cursor:
            try:
                q = "INSERT INTO leaderboard (player_name, score) VALUES (%s, %s)"
                self.mysql_cursor.execute(q, (name, int(score)))
                self.mysql_conn.commit()
                return
            except Exception:
                pass
        # fallback to local file
        try:
            data = []
            with open(LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data.append({'name': name, 'score': int(score)})
            data = sorted(data, key=lambda x: x['score'], reverse=True)[:50]
            with open(LEADERBOARD_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def get_top_scores(self, limit=5) -> List[Tuple[str, int]]:
        if self.mysql_conn and self.mysql_cursor:
            try:
                q = "SELECT player_name, score FROM leaderboard ORDER BY score DESC LIMIT %s"
                self.mysql_cursor.execute(q, (limit,))
                return self.mysql_cursor.fetchall()
            except Exception:
                pass
        # fallback to file
        try:
            with open(LEADERBOARD_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [(item.get('name', 'Player'), int(item.get('score', 0))) for item in data[:limit]]
        except Exception:
            return []

# UI Elements
class Button:
    def __init__(self, rect, text, callback):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.hovered = False

    def draw(self, surface):
        color = LIGHT_GREEN if self.hovered else DARK_GREEN
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        draw_text(surface, self.text, 24, self.rect.centerx, self.rect.centery, WHITE)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                try:
                    self.callback()
                except Exception:
                    pass

class TextBox:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.text = ''
        self.active = False
        self.cursor = 0
        self.cursor_timer = 0

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)
        display = self.text if self.text else 'Enter Name'
        draw_text(surface, display, 20, self.rect.centerx, self.rect.centery, BLACK)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 20 and event.unicode.isprintable():
                    self.text += event.unicode

# Game Entities
class Bird:
    def __init__(self):
        self.x = BIRD_START_X
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0.0
        self.frame = 0
        self.frame_timer = 0.0
        self.image = bird_frames[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # rotation physics for more realistic feel
        self.rotation = 0.0
        self.angular_velocity = 0.0
        # brief timer after a flap for stronger wing animation / hold-sustain
        self.flap_timer = 0.0
        self.hold = False

    def update(self, dt):
        # dt in milliseconds -> convert to seconds
        dt_s = max(0.001, dt / 1000.0)
        # integrate gravity and clamp velocity
        self.velocity += GRAVITY * dt_s
        if self.velocity > MAX_VELOCITY:
            self.velocity = MAX_VELOCITY
        # allow a short sustain lift when player holds input right after flap
        if self.hold and self.flap_timer > 0:
            # small upward acceleration while holding (diminishing quickly)
            self.velocity += -800.0 * dt_s
            if self.velocity < -MAX_VELOCITY:
                self.velocity = -MAX_VELOCITY
        self.y += self.velocity * dt_s

        # wing animation: speed up when recently flapped or moving fast
        self.frame_timer += dt_s
        flap_speed = 12.0 if self.flap_timer > 0 else (6.0 if self.velocity < 0 else 4.0)
        frame_period = 1.0 / flap_speed
        if self.frame_timer >= frame_period:
            self.frame_timer -= frame_period
            self.frame = (self.frame + 1) % len(bird_frames)

        # rotation smoothing using a simple spring towards target angle
        target_rot = max(-30, min(-self.velocity * 0.06, 80))
        # spring-damper integration on rotation
        rot_acc = (target_rot - self.rotation) * 18.0
        self.angular_velocity += rot_acc * dt_s
        # damping
        self.angular_velocity *= (0.9 ** dt_s)
        self.rotation += self.angular_velocity * dt_s
        # produce the rotated image
        self.image = pygame.transform.rotozoom(bird_frames[self.frame], self.rotation, 1.0)
        self.rect = self.image.get_rect(center=(self.x, int(self.y)))
        # decay flap timer
        if self.flap_timer > 0:
            self.flap_timer = max(0.0, self.flap_timer - dt_s)

    def jump(self):
        # strong instant upward velocity and angular impulse
        self.velocity = JUMP_STRENGTH
        self.flap_timer = 0.18
        # give a quick negative angular velocity so bird tilts up
        self.angular_velocity = -6.0

    def draw(self, surface):
        # dynamic shadow beneath bird (bigger/darker when near ground)
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        # distance from bird bottom to ground
        dist = max(0.0, ground_y - (self.y + self.rect.height * 0.5))
        t = max(0.0, min(dist / 400.0, 1.0))
        shadow_scale = 0.6 + (1.0 - t) * 0.6
        sw = int(self.rect.width * shadow_scale)
        sh = max(6, int(self.rect.height * 0.18 * shadow_scale))
        shadow = pygame.Surface((sw, sh), pygame.SRCALPHA)
        alpha = int(120 * (1.0 - t))
        pygame.draw.ellipse(shadow, (0, 0, 0, alpha), (0, 0, sw, sh))
        # position shadow a bit below the bird
        sx = int(self.x - sw / 2)
        sy = int(min(self.y + self.rect.height * 0.5, ground_y - sh // 2))
        surface.blit(shadow, (sx, sy))

        surface.blit(self.image, self.rect)

class PipePair:
    def __init__(self, x):
        self.x = float(x)
        self.width = pipe_img.get_width()
        margin = 80
        max_top = SCREEN_HEIGHT - PIPE_GAP - GROUND_HEIGHT - margin
        self.top_h = random.randint(margin, max(margin, max_top))
        self.scored = False
        self.top_rect = pipe_img.get_rect(midbottom=(int(self.x), self.top_h))
        self.bottom_rect = pipe_img.get_rect(midtop=(int(self.x), self.top_h + PIPE_GAP))

    def update(self, dt):
        # move left at PIPE_SPEED px/sec
        dt_s = max(0.001, dt / 1000.0)
        self.x -= PIPE_SPEED * dt_s
        self.top_rect.midbottom = (int(self.x), self.top_h)
        self.bottom_rect.midtop = (int(self.x), self.top_h + PIPE_GAP)

    def get_top_mask(self):
        # mask for the pipe image; rect positioned same as draw
        rect = pipe_img.get_rect(midbottom=(int(self.x), self.top_h))
        mask = pygame.mask.from_surface(pipe_img)
        return mask, rect

    def get_bottom_mask(self):
        rect = pipe_img.get_rect(midtop=(int(self.x), self.top_h + PIPE_GAP))
        mask = pygame.mask.from_surface(pipe_img)
        return mask, rect

    def draw(self, surface):
        surface.blit(pipe_img, self.top_rect)
        surface.blit(pipe_img, self.bottom_rect)

    def off_screen(self):
        return self.x < -self.width

    def collides_with(self, bird_rect):
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)

# Screens
class StartScreen:
    def __init__(self, app):
        self.app = app
        self.textbox = TextBox((SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 20, 240, 44))
        self.start_button = Button((SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT//2 + 40, 120, 44), 'Start', self.start_game)

    def start_game(self):
        self.app.player_name = self.textbox.text.strip() or 'Player'
        self.app.change_screen('game')

    def draw(self, surface):
        surface.blit(background_img, (0, 0))
        draw_text(surface, 'Flappy', 56, SCREEN_WIDTH//2, 120)
        self.textbox.draw(surface)
        self.start_button.draw(surface)
        draw_text(surface, 'Click Start or press Enter', 18, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100)

    def handle_event(self, event):
        self.textbox.handle_event(event)
        self.start_button.handle_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.start_game()

    def update(self, dt):
        pass

class GameScreen:
    def __init__(self, app):
        self.app = app
        self.bird = Bird()
        self.pipes: List[PipePair] = []
        self.score = 0
        self.last_pipe_time = pygame.time.get_ticks()
        self.time_since_last = 0
        self.spawn_x = SCREEN_WIDTH + 50

    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.last_pipe_time = pygame.time.get_ticks()
        self.time_since_last = 0

    def update(self, dt):
        self.bird.update(dt)
        # spawn pipes using accumulator for dt (more stable across pause/jank)
        self.time_since_last += dt
        if self.time_since_last >= PIPE_INTERVAL:
            self.time_since_last -= PIPE_INTERVAL
            self.pipes.append(PipePair(self.spawn_x))
        for p in self.pipes:
            p.update(dt)
            # score when the pipe center passes the bird
            if not p.scored and (p.x + p.width * 0.5) < self.bird.x:
                p.scored = True
                self.score += 1
        self.pipes = [p for p in self.pipes if not p.off_screen()]
        # collisions
        if self.bird.y > SCREEN_HEIGHT - GROUND_HEIGHT or self.bird.y < 0:
            self.app.change_screen('end', self.score)
            return
        # mask-based collisions (more accurate)
        bird_mask = pygame.mask.from_surface(self.bird.image)
        bird_rect = self.bird.rect
        for p in self.pipes:
            top_mask, top_rect = p.get_top_mask()
            bottom_mask, bottom_rect = p.get_bottom_mask()
            off_top = (top_rect.x - bird_rect.x, top_rect.y - bird_rect.y)
            off_bottom = (bottom_rect.x - bird_rect.x, bottom_rect.y - bird_rect.y)
            if bird_mask.overlap(top_mask, off_top) or bird_mask.overlap(bottom_mask, off_bottom):
                self.app.change_screen('end', self.score)
                return

    def draw(self, surface):
        surface.blit(background_img, (0, 0))
        for p in self.pipes:
            p.draw(surface)
        # ground
        ground_y = SCREEN_HEIGHT - GROUND_HEIGHT
        pygame.draw.rect(surface, (120, 80, 40), (0, ground_y, SCREEN_WIDTH, GROUND_HEIGHT))
        self.bird.draw(surface)
        draw_text(surface, str(self.score), 48, SCREEN_WIDTH//2, 40, WHITE)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.bird.hold = True
                self.bird.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.bird.hold = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.bird.hold = True
            self.bird.jump()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.bird.hold = False

class EndScreen:
    def __init__(self, app):
        self.app = app
        self.final_score = 0
        self.restart_button = Button((SCREEN_WIDTH//2 - 140, SCREEN_HEIGHT - 140, 120, 44), 'Restart', self.on_restart)
        self.quit_button = Button((SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT - 140, 120, 44), 'Quit', self.on_quit)

    def enter(self, score):
        self.final_score = int(score)
        # save score
        try:
            self.app.leaderboard.save_score(self.app.player_name or 'Player', self.final_score)
        except Exception:
            pass

    def on_restart(self):
        self.app.change_screen('game')

    def on_quit(self):
        pygame.quit()
        sys.exit()

    def draw(self, surface):
        surface.blit(background_img, (0, 0))
        draw_text(surface, 'Game Over', 56, SCREEN_WIDTH//2, 120)
        draw_text(surface, f'Score: {self.final_score}', 28, SCREEN_WIDTH//2, 200)
        # leaderboard
        top = self.app.leaderboard.get_top_scores(5)
        draw_text(surface, 'Leaderboard', 24, SCREEN_WIDTH//2, 260)
        y = 300
        for i, (name, sc) in enumerate(top[:5]):
            draw_text(surface, f'{i+1}. {name} - {sc}', 20, SCREEN_WIDTH//2, y)
            y += 30
        self.restart_button.draw(surface)
        self.quit_button.draw(surface)

    def handle_event(self, event):
        self.restart_button.handle_event(event)
        self.quit_button.handle_event(event)

# Application
class App:
    def __init__(self):
        self.player_name = 'Player'
        self.leaderboard = Leaderboard()
        self.screens = {
            'start': StartScreen(self),
            'game': GameScreen(self),
            'end': EndScreen(self),
        }
        self.current = 'start'

    def change_screen(self, name, *args):
        # if switching to game, reset
        if name == 'game':
            self.screens['game'].reset()
        if name == 'end' and args:
            self.screens['end'].enter(args[0])
        self.current = name

    def run(self):
        running = True
        while running:
            dt = CLOCK.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                # global quick keys
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    break
                # dispatch
                screen = self.screens[self.current]
                if hasattr(screen, 'handle_event'):
                    screen.handle_event(event)
            # update
            screen = self.screens[self.current]
            if hasattr(screen, 'update'):
                screen.update(dt)
            # draw
            screen.draw(SCREEN)
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    app = App()
    try:
        app.run()
    except Exception as e:
        pygame.quit()
        print('An error occurred:', e)
        raise