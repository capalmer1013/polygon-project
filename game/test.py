import sys, pygame
from pygame.locals import *
from math import sin, cos, radians, pi


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def point_position(x0, y0, dist, theta):
    return dist*sin(theta), dist*cos(theta)

pygame.init()

window_size = width, height = 640, 480
black = 255, 255, 255

speed = [0, 0]
playerMaxSpeed = 50
playerSpeed = playerMaxSpeed
distance = 20
playerY = 50
playerX = 50
screen = pygame.display.set_mode(window_size)

move = False
rotate_left = False
rotate_right = False
rotate_counter_start = 20
rotate_counter = rotate_counter_start
player = pygame.image.load("models/Player-Triangle-00.png")

angleChange = 0

player.set_alpha(255)

playerRect = player.get_rect()
rot_tuple = (player, playerRect)

while True:
    playerRect = playerRect.move(speed)
    if playerRect.left < 0 or playerRect.right > width:
        speed[0] = -speed[0]

    if playerRect.top < 0 or playerRect.bottom > height:
        speed[1] = -speed[1]

    if rotate_right:
        rotate_counter -= 1
        if rotate_counter == 0:
            angleChange -= 10
            rotate_counter = rotate_counter_start

    if rotate_left:
        rotate_counter -= 1
        if rotate_counter == 0:
            angleChange += 10
            rotate_counter = rotate_counter_start
    if move:
        xyTuple = point_position(0, 0, distance, radians(angleChange))
        playerSpeed -= 1
        if playerSpeed == 0:
            playerSpeed = playerMaxSpeed
            playerX -= xyTuple[0]
            playerY -= xyTuple[1]


    # bullshit ends here
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_LEFT:
            rotate_left = True

        if event.type == KEYUP and event.key == K_LEFT:
            rotate_left = False

        if event.type == KEYUP and event.key == K_RIGHT:
            rotate_right = False

        if event.type == KEYDOWN and event.key == K_RIGHT:
            rotate_right = True

        if event.type == KEYDOWN and event.key == K_UP:
            move = True

        if event.type == KEYUP and event.key == K_UP:
            move = False

        if event.type == QUIT:
            exit()
    angleChange = angleChange % 360

    tempPlayer = rot_center(player, angleChange)
    screen.fill(black)
    screen.blit(tempPlayer, (playerX, playerY))
    pygame.display.flip()