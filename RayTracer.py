import pygame
import Classes
import asyncio
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Classes import *
default_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
motion_cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZEALL)


pygame.init()
screen = pygame.display.set_mode((1080,720),DOUBLEBUF | OPENGL)
Classes.screen = screen
clock = pygame.time.Clock()
def main():
    running = True
    dt=0.0
    prev = 0
    scene = 1
    rays = []
    drags = []
    shooters = []
    mats = []
    player = Classes.Player([230,240])
    glClearColor(0.1,0.5,0.4,1.0)
    start_button = Classes.Button("START",440,510,100,50)
    restart_button = Classes.Button("PLAY AGAIN",440,510,150,80)
    welcome_text = Classes.Label("WELCOME TO RAY TRACER",50,50,1000,400)
    game_over_text = Classes.Label("GAME OVER",50,50,800,400)
    while running:
        mouse_pos = pygame.mouse.get_pos()
        glClear(GL_COLOR_BUFFER_BIT)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                running = False
            elif(event.type == pygame.MOUSEWHEEL):
                if(scene==1):
                    for drag_test in drags:
                        if drag_test.is_close(mouse_pos):
                            if(isinstance(drag_test.drag,Classes.Arc)):
                                keys = pygame.key.get_pressed()
                                if(keys[pygame.K_r]):
                                    drag_test.drag.rad += event.y*3
                                else:
                                    drag_test.drag.start_angle = (drag_test.drag.start_angle+event.y/5)
                                    drag_test.drag.end_angle = (drag_test.drag.end_angle-event.y/5)
                            elif(isinstance(drag_test.drag,Classes.Ray)):
                                drag_test.drag.change_size(event.y)
                    for mat in mats:
                        if(mat.is_point_inside(mouse_pos)):
                            mat.change_index(event.y)
            elif(event.type == pygame.MOUSEBUTTONDOWN):
                if(scene==0):
                    if(start_button.is_close(mouse_pos)):
                        scene = 1
                elif(scene==1):
                    if(event.button in (4,5,6,7)):
                        continue
                    for drag_test in drags:
                        if drag_test.is_close(event.pos):
                            if event.button == 1:
                                drag_test.dragging = True
                                break
                            elif event.button == 3:
                                drag_test.rotating = True
                                prev = [mouse_pos[0]-drag_test.drag.mid[0],mouse_pos[1]-drag_test.drag.mid[1]]
                                break
                    else:
                        for shooter in shooters:
                            if shooter.is_close(event.pos):
                                shooter.dragging = True
                                break
                        else:
                            for mat in mats:
                                if(mat.is_point_inside(event.pos)):
                                    mat.dragging = True
                                    break
                            else:
                                for shooter in shooters:
                                    rays.append(Classes.Ray((event.pos[0]-shooter.mid[0],event.pos[1]-shooter.mid[1]),pos=shooter.mid))
                elif(scene==2):
                     if(restart_button.is_close(mouse_pos)):
                         scene=1
            elif event.type == pygame.MOUSEMOTION:
                if(scene==1):
                    for shooter in shooters:
                        if(shooter.dragging):
                            shooter.move_to(mouse_pos)
                    for mat in mats:
                        if(mat.dragging):
                            mat.move_to(mouse_pos)
                    for drag_test in drags:
                        if drag_test.dragging:
                            drag_test.move_to(mouse_pos)
                        if drag_test.rotating:
                            angle = drag_test.angle_bet([mouse_pos[0]-drag_test.drag.mid[0],mouse_pos[1]-drag_test.drag.mid[1]],prev)
                            drag_test.rotate(angle)
                            prev = [mouse_pos[0]-drag_test.drag.mid[0],mouse_pos[1]-drag_test.drag.mid[1]]
            elif(event.type==pygame.MOUSEBUTTONUP):
                if(scene==1):
                    for drag_test in drags:
                        drag_test.dragging = False
                        drag_test.rotating = False
                    for shooter in shooters:
                        shooter.dragging = False
                    for mat in mats:
                        mat.dragging = False
            elif event.type == pygame.KEYDOWN:
                if(scene==1):
                    if event.key == pygame.K_f:
                        drags.append(Classes.Dragable(Classes.Ray((1,0),100)))
                    elif event.key == pygame.K_g:
                        drags.append(Classes.Dragable(Classes.Arc(1.5,100)))
                    elif event.key == pygame.K_h:
                        shooters.append(Classes.Ray_Shooter())
                    elif event.key == pygame.K_j:
                        mats.append(Classes.Material(1.33))
                    elif event.key == pygame.K_DELETE:
                        for drag in drags:
                            if(drag.is_close(mouse_pos)):
                                drags.remove(drag)
                        for shooter in shooters:
                            if(shooter.is_close(mouse_pos)):
                                shooters.remove(shooter)
                        for mat in mats:
                            if(mat.is_point_inside(mouse_pos)):
                                mats.remove(mat)
        if(scene==0):
            start_button.draw()
            welcome_text.draw()

        elif(scene==1):
            player.move()
            for mat in mats:
                mat.draw()
            for drag_test in drags:
                if drag_test.is_close(mouse_pos):
                    pygame.mouse.set_cursor(motion_cursor)
                    break
            else:
                for shooter in shooters:
                    if shooter.is_close(mouse_pos):
                        pygame.mouse.set_cursor(motion_cursor)
                        break
                else:
                    for mat in mats:
                        if(mat.is_point_inside(mouse_pos)):
                            pygame.mouse.set_cursor(motion_cursor)
                            break
                    else:
                        pygame.mouse.set_cursor(default_cursor)
            dt = clock.tick(60)/1000.0
            for ray in rays:
                if(not screen.get_rect().collidepoint(ray.mid[0],ray.mid[1])):
                    rays.remove(ray)
                    continue
                pygame.draw.line(screen,(255,0,0),ray.start,ray.end,3)
                for drag_test in drags:
                    res = drag_test.is_colliding(ray)
                    if(res[0]):
                        ray.change_dir(drag_test.reflect(ray.dir,res[1]))
                for mat in mats:
                    if(mat.is_point_inside(ray.start)!=mat.is_point_inside(ray.end)):
                        ray.change_dir(mat.refract(ray))
                ray.move(dt)
            player.draw()
            for shooter in shooters:
                shooter.draw()
            for drag in drags:
                drag.draw()
        elif scene==2:
            restart_button.draw()
            game_over_text.draw()
        pygame.display.flip()
main()
pygame.quit()