import sys, pygame

pygame.init()

window_size = width, height = 640, 480
black = 0, 0, 0

screen = pygame.display.set_mode(window_size)

while True:
    screen.fill(black)
    pygame.display.flip()