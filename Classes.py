import math
import pygame
import numpy as np
ini_pos = (100,360)
screen = pygame.display.set_mode((1080,720))
class Ray:
    def __init__(self,dir,size=10.0,pos=ini_pos):
        self.dir = [dir[0]/math.sqrt(dir[0]*dir[0]+dir[1]*dir[1]),dir[1]/math.sqrt(dir[0]*dir[0]+dir[1]*dir[1])]
        self.speed = 60
        self.size = size
        self.start = [pos[0],pos[1]]
        self.end = [pos[0] + self.dir[0]*self.size,pos[1] + self.dir[1]*self.size]
        self.mid = [(self.end[0]+self.start[0])/2,(self.end[1]+self.start[1])/2]

    def move(self,dt):
        self.start[0] = self.start[0] + (self.dir[0]*self.speed*dt)
        self.start[1] = self.start[1] + (self.dir[1]*self.speed*dt)
        self.end[0] = self.end[0] + (self.dir[0]*self.speed*dt)
        self.end[1] = self.end[1] + (self.dir[1]*self.speed*dt)
        self.mid[0] = self.mid[0] + (self.dir[0]*self.speed*dt)
        self.mid[1] = self.mid[1] + (self.dir[1]*self.speed*dt)

    def change_dir(self,dir):
        if(dir is None):
            return
        self.dir = dir
        self.start = [self.end[0],self.end[1]]
        self.end = [self.start[0]+dir[0]*self.size,self.start[1]+dir[1]*self.size]

    def draw(self):
        pygame.draw.line(screen,(255,0,0),self.start,self.end,3)

    def lerp(self,t):
        x = self.start[0] + t*(self.end[0]-self.start[0])
        y = self.start[1] + t*(self.end[1]-self.start[1])
        return [x,y]

    def change_size(self,ds):
        rate = 3
        self.start = [self.mid[0] + self.dir[0]*(self.size+ds)/2*rate,self.mid[1] + self.dir[1]*(self.size+ds)/2*rate]
        self.end = [self.mid[0] - self.dir[0]*(self.size+ds)/2*rate,self.mid[1] - self.dir[1]*(self.size+ds)/2*rate]
        self.size += ds*rate

class Arc:
    def __init__(self,angle,rad,pos=ini_pos,start=None):
        self.rad = rad
        if(start is None):
            self.start_angle = (angle/2) % (2 * math.pi)
            self.end_angle = (-angle/2) % (2 * math.pi)
        else:
            self.start_angle = start % (2*math.pi)
            self.end_angle = (start+angle) % (2*math.pi)
        self.mid = [pos[0],pos[1]]
        self.size = rad

    def draw(self):
        pygame.draw.arc(screen,(0,50,255),(self.mid[0]-self.rad,self.mid[1]-self.rad,self.rad*2,self.rad*2),self.start_angle,self.end_angle)

    def is_colliding(self,ray):
        n = 20
        for t in range(0,n+1):
            t=t/n
            point = ray.lerp(t)
            dis = math.sqrt((point[0]-self.mid[0])**2 + (point[1]-self.mid[1])**2)
            ob = Dragable(Ray((1,0),10))
            dir = [point[0]-self.mid[0],point[1]-self.mid[1]]
            di = [1,0]
            angle = (-ob.angle_bet(dir,di))%(2*math.pi)
            if(abs(dis-self.rad)<0.5):
               if(self.start_angle<self.end_angle and angle>self.start_angle and angle<self.end_angle):
                   return True,point
               elif(self.start_angle>self.end_angle and (angle>self.start_angle or angle<self.end_angle)):
                   return True,point
        return False,None

class Dragable:
    def __init__(self,drag):
        self.drag = drag
        self.dragging = False
        self.rotating = False

    def is_close(self,point,dis=5):
        dis += self.drag.size
        dist = math.sqrt((point[0]-self.drag.mid[0])**2 + (point[1]-self.drag.mid[1])**2)
        if (dist<dis):
            return True
        else:
            return False
        
    def move_to(self,point):
        mid = self.drag.mid
        if(isinstance(self.drag,Ray)):
            self.drag.start[0] += point[0]-mid[0]
            self.drag.start[1] += point[1]-mid[1]
            self.drag.end[0] += point[0]-mid[0]
            self.drag.end[1] += point[1]-mid[1]
        self.drag.mid[0] = point[0]
        self.drag.mid[1] = point[1]

    def is_colliding(self,ray):
        if(isinstance(self.drag,Ray)):
            return self.segmentIntersect(self.drag.start[0],self.drag.start[1],self.drag.end[0],self.drag.end[1],ray.start[0],ray.start[1],ray.end[0],ray.end[1]),None
        else:
            return self.drag.is_colliding(ray)
        
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
    def reflect(self,dir,point):
        dir1 = np.array(dir,dtype=float)
        if(isinstance(self.drag,Ray)):
            dir2 = np.array(self.drag.dir,dtype=float)
            nor = np.array([-dir2[1],dir2[0]],dtype=float)
        elif(isinstance(self.drag,Arc)):
            nor = np.array([self.drag.mid[0]-point[0],self.drag.mid[1]-point[1]],dtype=float)
        nsq = np.dot(nor,nor)
        r = dir1 - 2 * np.dot(dir1,nor) / nsq * nor
        return r
    def angle_bet(self,dir,di):
        dir1 = np.array(dir,dtype=float)
        dir2 = np.array(di,dtype=float)
        nor1 = np.linalg.norm(dir1)
        nor2 = np.linalg.norm(dir2)
        cross_product = dir1[0] * dir2[1] - dir1[1] * dir2[0]
        if nor1==0 or nor2==0:
            return 0.0
        dot_product = np.dot(dir1,dir2)
        cos = np.clip(dot_product/(nor1*nor2),-1.0,1.0)
        angle_val = np.arccos(cos)
        angle_val = -1*np.arctan2(cross_product, dot_product)
        return float(angle_val)

    def rotate_point(self,angle,p1,p2=0):
        if p2==0:
            p2 = [0,0]
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        x = (dx * np.cos(angle) - dy * np.sin(angle)) + p2[0]
        y = (dx * np.sin(angle) + dy * np.cos(angle)) + p2[1]
        return [x,y]

    def rotate(self,angle):
        if(isinstance(self.drag,Ray)):
            new_start = self.rotate_point(angle,self.drag.start,p2=self.drag.mid)
            self.drag.end = self.rotate_point(angle,self.drag.end,p2=self.drag.mid)
            self.drag.start = new_start
            self.rotate_dir(angle)
        elif(isinstance(self.drag,Arc)):
            self.drag.start_angle = (self.drag.start_angle-angle)%(2*math.pi)
            self.drag.end_angle = (self.drag.end_angle-angle)%(2*math.pi)
            

    def rotate_dir(self,angle):
        x,y = self.drag.dir
        cos = math.cos(angle)
        sin = math.sin(angle)
        nx = x*cos-y*sin
        ny = x*sin+y*cos
        self.drag.dir = [nx,ny]

    def draw(self):
        self.drag.draw()

class Ray_Shooter(Dragable):
    def __init__(self):
        self.rad = 15
        self.mid = [ini_pos[0],ini_pos[1]]
        self.dragging = False

    def draw(self):
        pygame.draw.circle(screen,(255,0,0),self.mid,self.rad)

    def is_close(self,point):
            dis = self.rad
            dist = math.sqrt((point[0]-self.mid[0])**2 + (point[1]-self.mid[1])**2)
            if (dist<dis):
                return True
            else:
                return False

    def move_to(self,point):
        self.mid[0] = point[0]
        self.mid[1] = point[1]

class Material:
    def __init__(self,index):
        self.index = index
        self.surface = Arc(0.0001,50)
        self.dragging = False

    def draw(self):
        t_sur = pygame.Surface((100,100),pygame.SRCALPHA)
        col = (0,0,0,255*(1-1/self.index))
        pygame.draw.circle(t_sur,col,(50,50),50)
        screen.blit(t_sur,(self.surface.mid[0]-50,self.surface.mid[1]-50))
        self.surface.draw()

    def change_index(self,change):
        self.index += change
        if(self.index<1):
            self.index=1

    def move_to(self,point):
        self.surface.mid[0] = point[0]
        self.surface.mid[1] = point[1]

    def is_inside(self,ray:Ray):
        return self.is_point_inside(ray.start) or self.is_point_inside(ray.end)

    def is_point_inside(self,point):
        mid = self.surface.mid
        dis = math.sqrt((mid[0]-point[0])**2+(mid[1]-point[1])**2)
        if(dis<self.surface.rad):
            return True
        return False

    def refract(self,ray):
        point = self.get_collision_point(ray)
        if(point==None):
            return 
        nor = np.array((self.surface.mid[0]-point[0],self.surface.mid[1]-point[1]))
        nor = nor/np.linalg.norm(nor)
        inc = np.array((ray.dir[0],ray.dir[1]))
        inc = inc/np.linalg.norm(inc)
        cos1 = -1*np.dot(nor,inc)
        meu = self.index
        if(cos1<0):
            nor = -nor
            cos1 = -cos1
            meu = 1.0/meu
        k = 1 - (meu**2)*(1-cos1**2)
        if(k<0):
            ob = Dragable(Arc(2*math.pi,self.surface.rad))
            return ob.reflect(inc,point)
        refrac = meu*inc+(meu*cos1-math.sqrt(k))*nor
        return refrac

    def get_collision_point(self,ray):
        n = 20
        for t in range(n+1):
            t = t/n
            point = self.lerp(ray,t)
            dis = math.sqrt((self.surface.mid[0]-point[0])**2+(self.surface.mid[1]-point[1])**2)
            rad = self.surface.rad
            diff = abs(dis-rad)
            if(diff<0.3):
                return [point[0],point[1]]
        return None
    
    def lerp(self,ray,t):
        x = ray.start[0] + t*(ray.end[0]-ray.start[0])
        y = ray.start[1] + t*(ray.end[1]-ray.start[1])
        return [x,y]

class Button:
    def __init__(self,text,x,y,width,height):
        font = pygame.font.SysFont("Arial", 24)
        self.text = text
        self.rect = pygame.Rect(x,y,width,height)
        self.color = (233,22,100)
        self.text_surf = font.render(text,True,(255,255,255))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self):
        pygame.draw.rect(screen,self.color,self.rect,border_radius=5)
        screen.blit(self.text_surf,self.text_rect)

    def is_close(self,pos):
        return self.rect.collidepoint(pos)

class Label:
    def __init__(self,text,x,y,width,height,color=(255,255,255)):
        self.text = text
        self.rect = pygame.Rect(x,y,width,height)
        font = pygame.font.SysFont("Arial", int(height/5))
        self.text_surf = font.render(text,True,color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self):
        screen.blit(self.text_surf,self.text_rect)

class Player:
    def __init__(self,pos,col=(23,50,100)):
        self.pos = pos
        self.step = 4
        self.color = col

    def move(self,event):
        move = [0,0]
        keys = pygame.key.get_pressed()
        if(keys[pygame.K_w]):
            move[1] = -self.step
        elif(keys[pygame.K_a]):
            move[0] = -self.step
        elif(keys[pygame.K_s]):
            move[1] = self.step
        elif(keys[pygame.K_d]):
            move[0] = self.step
        mag = math.sqrt(move[0]**2+move[1]**2)
        if(mag==0):
            return
        move[0] = move[0]/mag*self.step
        move[1] = move[1]/mag*self.step
        self.pos[0] += move[0]
        self.pos[1] += move[1]

    def draw(self):
        pygame.draw.circle(screen,self.color,self.pos,50)