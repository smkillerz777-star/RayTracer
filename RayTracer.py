import pygame
import math
ini_pos = (100,360)
class Ray:
    def __init__(self,dir):
        self.dir = [dir[0]/math.sqrt(dir[0]*dir[0]+dir[1]*dir[1]),dir[1]/math.sqrt(dir[0]*dir[0]+dir[1]*dir[1])]
        self.speed = 60
        self.slope = self.dir[1]/self.dir[0]
        self.size = 10
        self.start = [ini_pos[0],ini_pos[1]]
        self.end = [ini_pos[0] + self.dir[0]*self.size,ini_pos[1] + self.dir[1]*self.size]
    def move(self,dt):
        self.start[0] = self.start[0] + (self.dir[0]*self.speed*dt)
        self.start[1] = self.start[1] + (self.dir[1]*self.speed*dt)
        self.end[0] = self.end[0] + (self.dir[0]*self.speed*dt)
        self.end[1] = self.end[1] + (self.dir[1]*self.speed*dt)
class Dragable:
    def __init__(self,drag):
        self.drag = drag
        self.dragging = False
    def is_close(self,point,dis=5):
        size = math.sqrt((self.drag.end[0]-self.drag.start[0])**2 + (self.drag.end[1]-self.drag.start[1])**2)
        mid = [(self.drag.end[0]+self.drag.start[0])/2,(self.drag.end[1]+self.drag.start[1])/2]
        dist = math.sqrt((point[0]-mid[0])**2 + (point[1]-mid[1])**2)
        if (dist<(size+dis)):
            return True
        else:
            return False
    def move(self,dis):
        self.drag.start[0] += dis[0]
        self.drag.start[1] += dis[1]
        self.drag.end[0] += dis[0]
        self.drag.end[1] += dis[1]
    def move_to(self,point):
        mid = [(self.drag.end[0]+self.drag.start[0])/2,(self.drag.end[1]+self.drag.start[1])/2]
        self.drag.start[0] += point[0]-mid[0]
        self.drag.start[1] += point[1]-mid[1]
        self.drag.end[0] += point[0]-mid[0]
        self.drag.end[1] += point[1]-mid[1]
    def is_colliding(self,ray):
        max_x_drag = max(self.drag.end[0],self.drag.start[0])
        max_y_drag = max(self.drag.end[1],self.drag.start[1])
        min_x_drag = min(self.drag.end[0],self.drag.start[0])
        min_y_drag = min(self.drag.end[1],self.drag.start[1])
        max_x_ray = max(ray.end[0],ray.start[0])
        max_y_ray = max(ray.end[1],ray.start[0])
        min_x_ray = min(ray.end[0],ray.start[0])
        min_y_ray = min(ray.end[1],ray.start[1])
        return self.segmentIntersect(self.drag.start[0],self.drag.start[1],self.drag.end[0],self.drag.end[1],ray.start[0],ray.start[1],ray.end[0],ray.end[1])
    def segmentIntersect(self,x1,y1,x2,y2,x3,y3,x4,y4):
        denom = (y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)
        if(denom==0):
            cross = (x3-x3)*(y2-y1)-(y3-y1)*(x2-x1)
            if(cross != 0): return False
            dx = x2-x1
            dy = y2-y1
            lensq = dx*dx+dy*dy
            t3 = ((x3-x1)*dx+(y3-y1)*dy)/lensq
            t4 = ((x4-x1)*dx+(y4-y1)*dy)/lensq
            tMin = min(t3,t4)
            tMax = max(t3,t4)
            return (max(0,tMin) <= min(1,tMax))
        s = ((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/denom
        t = ((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/denom
        return (s>=0 and s<=1) and (t>=0 and t<=1)

pygame.init()
screen = pygame.display.set_mode((1080,720))
clock = pygame.time.Clock()
vel = pygame.math.Vector2(2,3)
running = True
dt=0.0
screen.fill((0,255,0))
rays = []
drag_test = Dragable(Ray((1,1)))
while running:
    screen.fill((0,255,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            rays.append(Ray((event.pos[0]-ini_pos[0],event.pos[1]-ini_pos[1])))
            if drag_test.is_close(event.pos):
                drag_test.dragging = True
        elif event.type == pygame.MOUSEMOTION:
            if drag_test.dragging:
                drag_test.move_to(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            drag_test.dragging = False
    dt = clock.tick(60)/1000.0
    for ray in rays:
        pygame.draw.line(screen,(255,0,0),ray.start,ray.end,3)
        if(drag_test.is_colliding(ray)):
            print(ray)
        ray.move(dt)
    pygame.draw.line(screen,(0,0,0),(0,360),(1080,360))
    pygame.draw.line(screen,(255,0,0),drag_test.drag.start,drag_test.drag.end,3)
    pygame.display.flip()
pygame.quit()