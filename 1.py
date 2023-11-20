import math
from random import choice

import pygame

FPS = 30
points = 0
midscore = 0
flag = 'classic'
planes = []

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
BROWN = (160, 128, 96)

GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
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
        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r + 2)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            balls.remove(self)
            return True
        else:
            return False


class Fireball(Ball):
    def move(self):
        self.x += self.vx
        self.y -= self.vy

        if self.x >= WIDTH:
            balls.remove(self)


# class Missile(Ball):
#     def move(self):
#         self.angle = math.acos((self.x - target.x) / ((self.x - target.x) ** 2 + (self.y - target.y)) ** 0.5)
#         self.vx = 10 * math.cos(self.angle)
#         self.vy = 10 * math.sin(self.angle)


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 40
        self.y = 450
        self.vx = 0
        self.moving = False
        self.hp = 5

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
            new_ball = Ball(self.screen, gun.x, gun.y)
        elif flag == 'fb':
            new_ball = Fireball(self.screen, gun.x, gun.y)
        # elif flag == 'missile':
        #     new_ball = Missile(self.screen, gun.x, gun.y)
        if event.pos[1] < self.y:
            self.an = math.atan((event.pos[0] - self.x) / (event.pos[1] - self.y))
        new_ball.vx = - self.f2_power * math.sin(self.an)
        new_ball.vy = self.f2_power * math.cos(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        if event and (event.pos[1] < self.y):
            self.an = math.atan((event.pos[0]-self.x) / (event.pos[1]-self.y))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        y11 = self.y + 5 * math.sin(self.an)
        x11 = self.x - 5 * math.cos(self.an)
        y12 = self.y - 5 * math.sin(self.an)
        x12 = self.x + 5 * math.cos(self.an)

        y21 = self.y - (self.f2_power + 20) * math.cos(self.an) - 5 * math.sin(self.an)
        x21 = self.x - (self.f2_power + 20) * math.sin(self.an) + 5 * math.cos(self.an)
        y22 = self.y - (self.f2_power + 20) * math.cos(self.an) + 5 * math.sin(self.an)
        x22 = self.x - (self.f2_power + 20) * math.sin(self.an) - 5 * math.cos(self.an)
        pygame.draw.polygon(self.screen, self.color, [[x11, y11], [x12, y12], [x21, y21], [x22, y22]])
        pygame.draw.circle(self.screen, BLACK, [self.x, self.y], 22)
        pygame.draw.circle(self.screen, [29, 150, 20], [self.x, self.y], 20)
        x1 = self.x - 32
        y1 = self.y
        x2 = self.x - 32
        y2 = self.y + 10
        x3 = self.x - 20
        y3 = self.y + 20
        x4 = self.x + 32
        y4 = self.y
        x5 = self.x + 32
        y5 = self.y + 10
        x6 = self.x + 20
        y6 = self.y + 20

        pygame.draw.polygon(self.screen, BLACK, [[x1 - 2, y1 - 2], [x2 - 2, y2], [x3 - 2, y3], [x6 + 2, y6], [x5 + 2, y5], [x4 + 2, y4 - 2]])
        pygame.draw.polygon(self.screen, [29, 100, 20], [[x1, y1], [x2, y2], [x3, y3], [x6, y6], [x5, y5], [x4, y4]])

        pygame.draw.circle(self.screen, BLACK, (x1, y6), 8)
        pygame.draw.circle(self.screen, BROWN, (x1, y6), 6)
        pygame.draw.circle(self.screen, BLACK, (x4, y6), 8)
        pygame.draw.circle(self.screen, BROWN, (x4, y6), 6)
        pygame.draw.circle(self.screen, BLACK, (x1 + 16, y6), 8)
        pygame.draw.circle(self.screen, BROWN, (x1 + 16, y6), 6)
        pygame.draw.circle(self.screen, BLACK, (x1 + 32, y6), 8)
        pygame.draw.circle(self.screen, BROWN, (x1 + 32, y6), 6)
        pygame.draw.circle(self.screen, BLACK, (x1 + 48, y6), 8)
        pygame.draw.circle(self.screen, BROWN, (x1 + 48, y6), 6)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    def move(self):
        self.x += self.vx


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.new_target()
        global targets

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
        self.hp = 1
        self.color = RED
        targets.append(self)

    def draw(self):
        if self.hp == 1:
            self.color = RED
        elif self.hp == 2:
            self.color = GREEN

        pygame.draw.circle(self.screen, BLACK, (self.x, self.y), self.r + 2)
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


class RestingTarget(Target):
    def __init__(self, screen):
        self.screen = screen
        self.new_target()
        global targets

    def new_target(self):
        self.live = True
        self.x = choice(range(300, 750))
        self.y = choice(range(200, 550))
        self.r = choice(range(5, 40))
        self.color = GREEN
        self.vy = 0
        self.vx = 0
        self.timer = 0
        self.n = 1
        self.hp = 2
        self.color = GREEN
        targets.append(self)

    def move(self):
        pass

    def randomization(self):
        pass

class Bomber:
    def __init__(self, screen):

        self.x = 0
        self.y = choice(range(200, 400))
        self.vx = choice(range(3, 8))
        self.screen = screen
        self.timer = 0
        self.color = GREY
        self.timer = 0
        self.forward = True
        planes.append(self)

    def drop_bomb(self):
        return Bomb(self.screen, self.x, self.y, self.vx)

    def move(self):
        self.x += self.vx
        if self.x >= WIDTH - 80:
            self.x = WIDTH - 80
            self.vx = -self.vx
            self.forward = False

        if self.x <= 80:
            self.x = 80
            self.vx = -self.vx
            self.forward = True

    def draw(self):

        if self.forward:
            xc = self.x + 70
            yc = self.y
            rc = 10
            x1 = self.x
            y1 = self.y - 20
            x2 = self.x + 20
            y2 = self.y - 10
            x3 = self.x + 20
            y3 = self.y + 10
            x4 = self.x
            y4 = self.y + 20

            x5 = self.x + 20
            y5 = self.y - 10

            x6 = self.x + 35
            y6 = self.y - 10
            x7 = x6
            y7 = self.y - 45
            x8 = x7 + 15
            y8 = y7
            x9 = x8 + 5
            y9 = self.y - 10

            x10 = x6
            y10 = self.y + 10
            x11 = x10
            y11 = self.y + 45
            x12 = x11 + 15
            y12 = y11
            x13 = x12 + 5
            y13 = self.y + 10
        else:
            xc = self.x - 10
            yc = self.y
            rc = 12
            x1 = self.x - 60
            y1 = self.y - 10
            x2 = x1 - 20
            y2 = self.y - 20
            x3 = x2
            y3 = self.y + 20
            x4 = x1
            y4 = self.y + 10

            x5 = self.x + 10
            y5 = self.x - 10

            x6 = self.x + 25
            y6 = self.y - 10
            x7 = self.x + 30
            y7 = self.y - 45
            x8 = x7 + 15
            y8 = y7
            x9 = x8
            y9 = y6

            x10 = x6
            y10 = self.y + 10
            x11 = x7
            y11 = self.y + 45
            x12 = x8
            y12 = y11
            x13 = x9
            y13 = y10

        pygame.draw.polygon(self.screen, self.color, [[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
        pygame.draw.rect(self.screen, self.color, (x5, y5, 50, 20))
        pygame.draw.circle(self.screen, self.color, (xc, yc), rc)
        pygame.draw.polygon(self.screen, self.color, [[x6, y6], [x7, y7], [x8, y8], [x9, y9]])
        pygame.draw.polygon(self.screen, self.color, [[x10, y10], [x11, y11], [x12, y12], [x13, y13]])

class Bomb(Ball):
    def __init__(self, screen, x, y, v):
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = v
        self.vy = 0
        self.r = choice(range(5, 12))


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
targets = []
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
gun = Gun(screen)
finished = False

Target(screen)
RestingTarget(screen)
RestingTarget(screen)
time = 0
counter = 0

while not finished:
    screen.fill(WHITE)
    gun.draw()
    gun.move()

    score_text = font.render("Очки: " + str(points), True, BLACK)
    screen.blit(score_text, (10, 10))

    midscore_text = font.render("Количество попыток: " + str(midscore), True, BLACK)
    screen.blit(midscore_text, (270, 525))

    if time % 200 == 0 and counter <= 3:
        Bomber(screen)
        counter += 1

    for b in balls:
        b.draw()

    time += 1

    for t in targets:
        t.draw()
        t.move()

    for plane in planes:
        plane.draw()
        plane.move()

    pygame.display.update()

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
            midscore += 1
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
            for t in targets:
                t.randomization()
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                flag = 'fb'
            if event.key == pygame.K_c:
                flag = 'classic'
            if event.key == pygame.K_m:
                flag = 'missile'
            if event.key == pygame.K_a:
                gun.vx = -5
            if event.key == pygame.K_d:
                gun.vx = 5
                gun.moving = True
        elif event.type == pygame.KEYUP:
            gun.vx = 0
            gun.moving = False

    for b in balls:
        b.move()
        for t in targets:
            if b.hittest(t) and t.live:
                t.hp -= 1
                if t.hp == 0:
                    t.live = False
                    targets.remove(t)
                    t.new_target()
                    points += 1
                    midscore = 0
    gun.power_up()

pygame.quit()