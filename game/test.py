import sys, pygame

pygame.init()

window_size = width, height = 640, 480
black = 0, 0, 0

speed = [2, 2]

screen = pygame.display.set_mode(window_size)

player = pygame.image.load("models/Player-test-model.png")

playerRect = player.get_rect()

while True:
    # bullshit starts here
    playerRect = playerRect.move(speed)
    if playerRect.left < 0 or playerRect.right > width:
        speed[0] = -speed[0]
    if playerRect.top < 0 or playerRect.bottom > height:
        speed [1] = -speed[1]
    # bullshit ends here
    screen.fill(black)
    screen.blit(player, playerRect)
    pygame.display.flip()