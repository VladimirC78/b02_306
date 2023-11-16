import math
from random import choice

import pygame

FPS = 30
points = 0
midscore = 0
angle0 = 0
flag = 'classic'

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.resting_timer = 0

    def move(self):
        self.vy -= 1.2
        self.x += self.vx
        self.y -= self.vy

        if self.x >= WIDTH - self.r and self.vx > 0:
            self.x = WIDTH - self.r
            self.vx = -self.vx * 0.5
        elif self.x <= self.r and self.vx < 0:
            self.x = self.r
            self.vx = -self.vx * 0.5
        elif self.y >= HEIGHT - self.r:
            self.y = HEIGHT - self.r
            self.vy = - self.vy * 0.5
            self.vx = self.vx * 0.5
            if abs(self.vy) <= 5:
                self.vy = 0

        if self.vx == 0 or self.vy == 0:
            self.resting_timer += 1
        if self.resting_timer > 0.3 * FPS:
            balls.remove(self)

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False


class Fireball(Ball):
    def move(self):
        self.x += self.vx
        self.y -= self.vy

        if self.x >= WIDTH - self.r and self.vx > 0:
            self.x = WIDTH - self.r
            self.vx = -self.vx * 0.5
        elif self.x <= self.r and self.vx < 0:
            self.x = self.r
            self.vx = -self.vx * 0.5
        elif self.y >= HEIGHT - self.r:
            self.y = HEIGHT - self.r
            self.vy = - self.vy * 0.5
            self.vx = self.vx * 0.5
        elif self.y <= self.r and self.vy > 0:
            self.y = self.r
            self.vy = -self.vy * 0.5
            self.vx = self.vx * 0.5
        if abs(self.vy) <= 5 and self.y > HEIGHT - 2*self.r:
            self.vy = 0

        if self.vx == 0 or self.vy == 0:
            self.resting_timer += 1
        if self.resting_timer > 0.3 * FPS:
            balls.remove(self)

# class FragGrenade(Ball):
#     def explode(self):
#
#         balls.remove(self)


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 40
        self.y = 450

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        if flag == 'classic':
            new_ball = Ball(self.screen)
        elif flag == 'fb':
            new_ball = Fireball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        angle0 = self.an
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1] - 450) / (event.pos[0] - 20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(self.screen, self.color, (self.x, self.y), (
        self.x + (self.f2_power + 10) * math.cos(self.an), self.y + (self.f2_power + 10) * math.sin(self.an)), 10)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.live = True
        self.x = choice(range(500, 750))
        self.y = choice(range(300, 550))
        self.r = choice(range(5, 40))
        self.color = RED
        self.vy = choice(range(-10, 10))
        self.vx = choice(range(-10, 10))
        self.timer = 0
        self.n = 1

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.timer += 1

        if self.timer >= 55 * self.n:
            self.vy = choice(range(-10, 10))
            self.vx = choice(range(-10, 10))
            self.n += 1

        if self.x >= WIDTH - self.r and self.vx > 0:
            self.x = WIDTH - self.r
            self.vx = -self.vx
        elif self.x <= self.r and self.vx < 0:
            self.x = self.r
            self.vx = -self.vx
        elif self.y >= HEIGHT - self.r:
            self.y = HEIGHT - self.r
            self.vy = - self.vy
            self.vx = self.vx
        elif self.y <= self.r:
            self.y = self.r
            self.vy = -self.vy

    def randomization(self):
        self.vx = choice(range(-10, 10))
        self.vy = choice(range(-10, 10))
        self.timer = 55 * (self.n - 1)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()

    score_text = font.render("Очки: " + str(points), True, BLACK)
    screen.blit(score_text, (10, 10))

    midscore_text = font.render("Количество попыток: " + str(midscore), True, BLACK)
    screen.blit(midscore_text, (270, 525))

    for b in balls:
        b.draw()
    pygame.display.update()

    target.move()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
            midscore += 1
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
            target.randomization()
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                flag = 'fb'
            if event.key == pygame.K_c:
                flag = 'classic'
            if event.key == pygame.K_g:
                flag = 'frag'

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            target.live = False
            points += 1
            target.new_target()
            midscore = 0
    gun.power_up()

pygame.quit()
