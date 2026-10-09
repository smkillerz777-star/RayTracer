import pygame
import sys
pygame.init()
screen = pygame.display.set_mode((1080,720))
time = 0
vel = pygame.math.Vector2(2,3)
running = True
while running:
    screen.fill((0,255,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.draw.circle(screen,(255,0,0),(100,100)+vel*time,50)
    pygame.display.flip()
    time += 0.1
pygame.quit()