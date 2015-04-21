import sys, pygame, random
from pygame.locals import *
from character import Character, npc
from server import MySocket
# function definitions here

playerList = []

def rot_center(image, angle):
    # rotate an image while keeping its center and size
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def make_npc():
    # magic
    vertexNumber = (random.randint(1, 9) + 2) % 11
    npcX = random.randint(50, 750)
    npcY = random.randint(50, 550)
    npcOr = random.randint(0, 359)
    playerList.append(npc(vertexNumber, npcX, npcY, npcOr))

# Main starts here

# setup the screen stuff
pygame.init()
window_size = width, height = 800, 600
white = 255, 255, 255
screen = pygame.display.set_mode(window_size)

# test stuff for using character class

userID = 123
player1 = Character(userID, 'cpalmer', 3, 100, 100, 200, 200, 0)
make_npc()
game_running = True
playerList.append(player1)

'''
player1.to_string()
mySocket = MySocket.MySocket()

mySocket.connect("54.149.175.19", 1337)
print player1.serialize_class()
mySocket.mysend(player1.serialize_class())

temp_buffer = mySocket.myreceive()
print temp_buffer
'''

# get list of characters from server
# append self

while game_running:
    screen.fill(white)
    for player in playerList:
        player.cycle()
        if player.xPos < 0:
            player.xPos = 0
            player.wall = True
        if player.xPos + player.Rect.right > width:
            player.xPos = width - player.Rect.right
            player.wall = True
        if player.yPos < 0:
            player.yPos = 0
            player.wall = True
        if player.yPos + player.Rect.bottom > height:
            player.yPos = height - player.Rect.bottom
            player.wall = True
        for otherPlayer in playerList:
            if otherPlayer is not player:
                a = pygame.Rect((player.xPos+20,player.yPos+20),(60,60))
                b = pygame.Rect((otherPlayer.xPos+20,otherPlayer.yPos+20),(60,60))
                if a.colliderect(b) == 1:
                    player.moveBack(player.playerSpeed)
                    if player.attack:
                        if otherPlayer.current_health > 0:
                            otherPlayer.current_health -= player.vertex_count * .05
                        otherPlayer.updateHealth()
                    #otherPlayer.moveBack(otherPlayer.playerSpeed)

        if player.current_health <= 0:
            player.dieTimer -= 1
            if player.dieTimer == 0:
                playerList.remove(player)
                break
        # event handler
        if player.user_id == userID:
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
                if event.type == KEYDOWN and event.key == K_SPACE:
                    player.attack = True
                if event.type == QUIT:
                    exit()
        player.orientation %= 360

        tempPlayer = rot_center(player.sprite, player.orientation)

        screen.blit(tempPlayer, (player.xPos, player.yPos))

    pygame.display.flip()

