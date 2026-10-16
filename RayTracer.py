import pygame
import math
ini_pos = (100,360)
class Ray:
    def __init__(self,dir):
        self.dir = [dir[0]/math.sqrt(dir[0]*dir[0]+dir[1]*dir[1]),dir[1]/math.sqrt(dir[0]*dir[0]+dir[1]*dir[1])]
        self.speed = 60
        self.size = 10
        self.start = [ini_pos[0],ini_pos[1]]
        self.end = [ini_pos[0] + self.dir[0]*self.size,ini_pos[1] + self.dir[1]*self.size]
    def move(self,dt):
        self.start[0] = self.start[0] + (self.dir[0]*self.speed*dt)
        self.start[1] = self.start[1] + (self.dir[1]*self.speed*dt)
        self.end[0] = self.end[0] + (self.dir[0]*self.speed*dt)
        self.end[1] = self.end[1] + (self.dir[1]*self.speed*dt)
pygame.init()
screen = pygame.display.set_mode((1080,720))
clock = pygame.time.Clock()
vel = pygame.math.Vector2(2,3)
running = True
dt=0.0
screen.fill((0,255,0))
rays = []
while running:
    screen.fill((0,255,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
            rays.append(Ray((event.pos[0]-ini_pos[0],event.pos[1]-ini_pos[1])))
    dt = clock.tick(60)/1000.0
    for ray in rays:
        pygame.draw.line(screen,(255,0,0),ray.start,ray.end,3)
        ray.move(dt)
    pygame.draw.line(screen,(0,0,0),(0,360),(1080,360))
    pygame.display.flip()
pygame.quit()