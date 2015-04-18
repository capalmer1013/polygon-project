import sys, pygame
from pygame.locals import *

pygame.init()

window_size = width, height = 640, 480
black = 0, 0, 0

speed = [0, 0]

screen = pygame.display.set_mode(window_size)

player = pygame.image.load("models/Player-test-model.png")

playerRect = player.get_rect()

while True:
    # bullshit starts here
    playerRect = playerRect.move(speed)
    if playerRect.left < 0 or playerRect.right > width:
        speed[0] = -speed[0]
    if playerRect.top < 0 or playerRect.bottom > height:
        speed[1] = -speed[1]
    # bullshit ends here
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_LEFT:
            player = pygame.transform.rotate(player, 10)
        if event.type == KEYDOWN and event.key == K_RIGHT:
            player = pygame.transform.rotate(player, -10)
        if event.type == QUIT:
            exit()

    screen.fill(black)
    screen.blit(player, playerRect)
    pygame.display.flip()