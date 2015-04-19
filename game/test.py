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

def point_pos(x0, y0, d, theta):
    theta_rad = pi/2 - radians(theta)
    return x0 + d*cos(theta_rad), y0 + d*sin(theta_rad)


def point_position(x0, y0, dist, theta):
    return dist*sin(theta), dist*cos(theta)

pygame.init()

window_size = width, height = 640, 480
black = 0, 0, 0

speed = [0, 0]
yChange = 50
xChange = 50
screen = pygame.display.set_mode(window_size)

rotate_left = False
rotate_right = False
rotate_counter_start = 20
rotate_counter = rotate_counter_start
player = pygame.image.load("models/Player-test-model.png")

player.set_alpha(0)

playerRect = player.get_rect()
rot_tuple = (player, playerRect)

while True:
    # bullshit starts here
    playerRect = playerRect.move(speed)
    if playerRect.left < 0 or playerRect.right > width:
        speed[0] = -speed[0]
    if playerRect.top < 0 or playerRect.bottom > height:
        speed[1] = -speed[1]
    if rotate_right:
        rotate_counter -= 1
        if rotate_counter == 0:
            player = rot_center(player, -10)
            rotate_counter = rotate_counter_start
    if rotate_left:
        rotate_counter -= 1
        if rotate_counter == 0:
            player = rot_center(player, 10)
            rotate_counter = rotate_counter_start

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
            yChange -= 10

        if event.type == QUIT:
            exit()

    screen.fill(black)
    screen.blit(player, (xChange, yChange))
    pygame.display.flip()