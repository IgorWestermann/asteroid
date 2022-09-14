from os import remove
import pygame
import sys
from settings import *
from random import randint, uniform


def bullet_update(bullet_list, speed=800):
    for rect in bullet_list:
        rect.y -= speed * dt
        if rect.bottom < 0:
            bullet_list.remove(rect)


def bullet_timer(can_shoot, duration=500):
    if not can_shoot:
        ct = pygame.time.get_ticks()
        if ct - shoot_time > duration:
            can_shoot = True
    return can_shoot


def meteor_update(meteor_list, speed):
    for meteor in meteor_list:

        direction = meteor[1]
        meteor_rect = meteor[0]
        meteor_rect.center += direction * speed * dt
        if meteor_rect.top > WINDOW_HEIGHT:
            meteor_list.remove(meteor)


global speed
speed = 300
ja_ficou_rapido = False
speed_timer = None

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Asteroid')

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
background_surface = pygame.image.load(
    './graphics/background.png').convert_alpha()
# ship
ship_surface = pygame.image.load('./graphics/ship.png').convert_alpha()
ship_rect = ship_surface.get_rect(center=(640, 360))

# font


# bullet
bullet_surface = pygame.image.load('./graphics/laser.png').convert_alpha()
bullet_list = []
# bullet timer
can_shoot = True
shoot_time = None

# meteor
meteor_surface = pygame.image.load('./graphics/meteor.png').convert_alpha()
meteor_list = []
# meteor timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 500)

# sound

laser = pygame.mixer.Sound('./sounds/laser.ogg')
explosion = pygame.mixer.Sound('./sounds/explosion.wav')

# score
score = 0
font = pygame.font.Font('./graphics/subatomic.ttf', 50)

while True:
    text_surface = font.render(f'Score {score}', True, ('White'))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        ship_rect.y -= 4
    if keys[pygame.K_DOWN]:
        ship_rect.y += 4
    if keys[pygame.K_LEFT]:
        ship_rect.x -= 4
    if keys[pygame.K_RIGHT]:
        ship_rect.x += 4
    if keys[pygame.K_SPACE] and can_shoot:
        bullet_rect = bullet_surface.get_rect(midbottom=ship_rect.midtop)
        bullet_list.append(bullet_rect)

        can_shoot = False
        shoot_time = pygame.time.get_ticks()

        laser.play()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == meteor_timer:
            rand_x = randint(-100, WINDOW_WIDTH + 100)
            rand_y = randint(-100, -50)

            meteor_rect = meteor_surface.get_rect(center=(rand_x, rand_y))

            direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)

            meteor_list.append((meteor_rect, direction))
    if score % 5 == 0 and score > 0 and ja_ficou_rapido:
        ct = pygame.time.get_ticks()
        if ct - shoot_time > 500:
            speed += 10
            if ct - shoot_time < 500:
                meteor_update(meteor_list, speed)
                ja_ficou_rapido = False
                print(speed)
    else:
        meteor_update(meteor_list, speed)
        if score % 5 == 0:
            ja_ficou_rapido = True

    bullet_update(bullet_list)
    can_shoot = bullet_timer(can_shoot, 500)

    for meteor in meteor_list:
        meteor_rect = meteor[0]
        if ship_rect.colliderect(meteor_rect):
            pygame.quit()
            sys.exit()

    for meteor in meteor_list:
        for bullet in bullet_list:
            meteor_rect = meteor[0]
            bullet_rect = bullet
            if bullet_rect.colliderect(meteor_rect):
                meteor_list.remove(meteor)
                bullet_list.remove(bullet)
                score += 1
                explosion.play()

    dt = clock.tick(120) / 1000

    display_surface.fill((0, 0, 0))
    display_surface.blit(background_surface, (0, 0))

    for bullet in bullet_list:
        display_surface.blit(bullet_surface, bullet)
    for meteor in meteor_list:
        display_surface.blit(meteor_surface, meteor[0])

    display_surface.blit(ship_surface, ship_rect)
    display_surface.blit(text_surface, (500, 200))

    pygame.display.update()
