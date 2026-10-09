import pygame
pygame.init()
screen = pygame.display.set_mode((1000,640))
screen.fill((0,0,0))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit() 