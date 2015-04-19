import sys, pygame
from pygame.locals import *
from character import Character

# function definitions here


def rot_center(image, angle):
    # rotate an image while keeping its center and size
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


# Main starts here

# setup the screen stuff
pygame.init()
window_size = width, height = 800, 600
white = 255, 255, 255
screen = pygame.display.set_mode(window_size)

# test stuff for using character class

player1 = Character(123, 'cpalmer', 5, 100, 50, 50, 50, 0)
playerList = []
playerList.append(player1)

# get list of characters from server
# append self

while True:
    for player in playerList:
        player.cycle()
        if player.xPos < 0:
            player.xPos = 0
        if player.xPos + player.playerRect.right > width:
            player.xPos = width - player.playerRect.right

        if player.yPos < 0:
            player.yPos = 0
        if player.yPos + player.playerRect.bottom > height:
            player.yPos = height - player.playerRect.bottom
        # event handler
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_LEFT:
                player.rotate_left = True

            if event.type == KEYUP and event.key == K_LEFT:
                player.rotate_left = False

            if event.type == KEYUP and event.key == K_RIGHT:
                player.rotate_right = False

            if event.type == KEYDOWN and event.key == K_RIGHT:
                player.rotate_right = True

            if event.type == KEYDOWN and event.key == K_UP:
                player.move = True

            if event.type == KEYUP and event.key == K_UP:
                player.move = False

            if event.type == QUIT:
                exit()
        player.orientation %= 360
        screen.fill(white)

        tempPlayer = rot_center(player.sprite, player.orientation)

        screen.blit(tempPlayer, (player.xPos, player.yPos))
    pygame.display.flip()

