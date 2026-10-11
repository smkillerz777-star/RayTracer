import pygame
import sys
class Ray:
    def __init__(self,dir):
        self.dir = dir
        self.speed = 5
        self.pos = [100,360]
    def move(self,dt):
        self.pos[0] = self.pos[0] + (self.dir[0]*self.speed*dt)
        self.pos[1] = self.pos[1] + (self.dir[1]*self.speed*dt)
pygame.init()
screen = pygame.display.set_mode((1080,720))
clock = pygame.time.Clock()
vel = pygame.math.Vector2(2,3)
running = True
dt=0.0
screen.fill((0,255,0))
p_ball = (100,100)
r = Ray((1,0))
print(r.pos)
r.move(1)
print(r.pos)
while running:
    #screen.fill((0,255,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            p_ball = event.pos
    dt += clock.tick(60)/1000.0
    p_ball += (dt*vel)
    pygame.draw.circle(screen,(255,0,0),p_ball,3)
    pygame.draw.line(screen,(0,0,0),(0,360),(1080,360))
    pygame.display.flip()
pygame.quit()
