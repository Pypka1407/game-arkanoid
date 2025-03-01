import pygame
from random import randrange as rnd

s = w, h = 720, 550
fps = 60

pw = 200
ph = 10
pspeed = 15
p = pygame.Rect(w // 2 - pw // 2, h - ph - 10, pw, ph)

ballr = 20
initial_ballspeed = 6
ballspeed = initial_ballspeed
ball1 = int(ballr * 2 ** 0.5)
ball = pygame.Rect(rnd(ball1, w - ball1), h // 2, ball1, ball1)
dx, dy = 1, -1

pygame.init()
screen = pygame.display.set_mode(s)
pygame.display.set_caption("Арканоид")
clock = pygame.time.Clock()
img = pygame.image.load('data/ФОН1.jpg').convert()

score = 0
level = 1
blocks_per_level = 24


def create_blocks():
    return [pygame.Rect(10 + 120 * i, 10 + 60 * j, 100, 50) for i in range(6) for j in range(4)], \
           [(rnd(30, 256), rnd(30, 256), rnd(20, 256)) for i in range(6)
            for j in range(4)]


blocklist, colorlist = create_blocks()


def show_intro():
    font = pygame.font.SysFont(None, 75)
    start_text = font.render('чтобы играть', True, (255, 255, 255))
    title_text = font.render('Нажмите на пробел', True, (255, 255, 255))

    screen.fill((160, 32, 255))
    screen.blit(title_text, (w // 2 - title_text.get_width() // 2, h // 2 - title_text.get_height() // 2 - 30))
    screen.blit(start_text, (w // 2 - start_text.get_width() // 2, h // 2 + 20))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


def show_game_over():
    font = pygame.font.SysFont(None, 75)
    text = font.render('GAME OVER ;(', True, (255, 96, 208))
    screen.fill((64, 64, 64))
    screen.blit(text, (w // 2 - text.get_width() // 2, h // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)


def show_victory():
    font = pygame.font.SysFont(None, 75)
    text = font.render('YOU WIN ;)', True, (160, 32, 255))
    screen.fill((80, 208, 255))
    screen.blit(text, (w // 2 - text.get_width() // 2, h // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)


def hit(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


def draw_score_level():
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Очки: {score}', True, pygame.Color('indigo'))
    level_text = font.render(f'Уровень: {level}', True, pygame.Color('indigo'))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (w - level_text.get_width() - 10, 10))


def reset_game():
    global level, blocklist, colorlist, ball, ballspeed
    level += 1
    ballspeed = initial_ballspeed + level
    ball = pygame.Rect(rnd(ball1, w - ball1), h // 2, ball1, ball1)
    blocklist, colorlist = create_blocks()


show_intro()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.blit(img, (0, 0))
    [pygame.draw.rect(screen, colorlist[color], block) for color, block in enumerate(blocklist)]
    pygame.draw.rect(screen, pygame.Color('darkgreen'), p)
    pygame.draw.circle(screen, pygame.Color('purple4'), ball.center, ballr)

    # Ball movement
    ball.x += ballspeed * dx
    ball.y += ballspeed * dy

    # Ball hit
    if ball.centerx < ballr or ball.centerx > w - ballr:
        dx = -dx
    if ball.centery < ballr:
        dy = -dy
    if ball.colliderect(p) and dy > 0:
        dx, dy = hit(dx, dy, ball, p)
    hit_index = ball.collidelist(blocklist)
    if hit_index != -1:
        hit_rect = blocklist.pop(hit_index)
        hit_color = colorlist.pop(hit_index)
        dx, dy = hit(dx, dy, ball, hit_rect)

        score += 1

        # Game over
    if ball.bottom > h:
        show_game_over()
        exit()

        # chek victory
    if not len(blocklist):
        show_victory()
        reset_game()

    draw_score_level()

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and p.left > 0:
        p.left -= pspeed
    if key[pygame.K_RIGHT] and p.right < w:
        p.right += pspeed

    pygame.display.flip()
    clock.tick(fps)
