import pygame
import sys
pygame.init()
screen = pygame.display.set_mode((1080,720))
clock = pygame.time.Clock()
vel = pygame.math.Vector2(20,30)
running = True
dt=0.0
p_ball = (100,100)
while running:
    screen.fill((0,255,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            p_ball = event.pos
    dt += clock.tick(60)/1000.0
    p_ball += (dt*vel)
    pygame.draw.circle(screen,(255,0,0),p_ball,50)
    pygame.display.flip()
pygame.quit()