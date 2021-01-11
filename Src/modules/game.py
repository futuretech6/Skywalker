from modules.camera import Camera
import os
import pygame
import random
import OpenGL.GL as gl
import OpenGL.GLU as glu
from collections import deque
from math import sin, cos


from config import *
from modules.model import Model
import modules.methods as method
from modules.light import Light
from modules.sphere import Sphere
from modules.skybox import Skybox
from modules.camera import Camera


class Game(object):
    """Main game class"""

    def __init__(self, width=1280, height=700):
        self.win_w = width
        self.win_h = height
        self.asteroids = deque()
        self.light = Light([0, -3, 3])
        self.skybox = Skybox(self.win_w, self.win_h)
        self.center = Sphere(0.1, [1.0, 0.0, 1.0], [1, 1, 1])
        self.paused = False
        self.score = 0
        self.camera = Camera()
        self.isRoaming = False

    def init_properties(self):
        """Initialization of game properties"""
        self.isplaying = False
        self.fps_view = False
        self.shield = HARD_INIT_SHIELD
        self.ast_speed = HARD_AST_INIT
        self.ship_speed = HARD_SHIP_INIT
        self.lean_speed = HARD_TILT_INIT

    def init_screen(self):
        self.init_properties()

        """Creating screen and initializing objects"""
        pygame.init()
        size = [self.win_w, self.win_h]
        pygame.display.set_mode(size, pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption("Skywalker")
        pygame.mouse.set_visible(False)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)
        self.light.enable()

        """ Load model """
        os.chdir('./materials/spaceship/')
        self.ship = Model("spaceship.obj", 0.4, [0, 0, 0], -270, 0, -180)
        os.chdir('../../')

        # os.chdir('./materials/Starship/')
        # self.ship = Model("Starship.obj", 0.01, [0, 0, 0], 90, 0, 180)
        # os.chdir('../../')

        # os.chdir('./materials/NCC-1701/')
        # self.ship = Model("NCC-1701_modified.obj", 1.2, [0, 0, 0], 90, 0, 180)
        # os.chdir('../../')

        # os.chdir('./materials/millenium-falcon/')
        # self.ship = Model("millenium-falcon_modified.obj", 1, [0, 0, 0], 90, 0, 0, using_left=True)
        # os.chdir('../../')

        for i in range(MAX_DISPLAY_AST):
            self.add_ast(isInit=True)
        self.ship_collider = Sphere(
            self.ship.radius, [0.0, 0.0, 0.0], [1, 1, 1], False)
        self.skybox.init_sky()

    def main_loop(self):
        """Main game loop"""
        self.init_screen()
        pygame.time.set_timer(pygame.USEREVENT + 1,
                              HARD_ACC_TIME_SEP)  # accelerate
        pygame.time.set_timer(pygame.USEREVENT + 2, 1000)  # score++
        # pygame.time.set_timer(pygame.USEREVENT + 3, 1000)  # refresh asts
        has_played = False
        clock = pygame.time.Clock()
        while True:
            delta_time = clock.tick(60) / 10
            fps = int(clock.get_fps())
            event_list = pygame.event.get()
            for e in event_list:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif e.type == pygame.KEYDOWN:
                    """ Keyboard(Not Controller) """
                    if e.key == pygame.K_ESCAPE or e.key == pygame.K_q:
                        method.quit_program()
                    elif e.key == pygame.K_r and self.paused:
                        self.isRoaming = not self.isRoaming
                    elif e.key == pygame.K_v:
                        self.fps_view = not self.fps_view
                    elif e.key == pygame.K_p:
                        self.paused = not self.paused
                    elif e.key == pygame.K_SPACE and not self.isplaying:
                        self.score = 0
                        self.isplaying = True
                        has_played = True
                # elif e.type == pygame.MOUSEMOTION:

                elif e.type == pygame.USEREVENT + 1 and self.isplaying and not self.paused:
                    self.ast_speed += HARD_AST_ACC
                    self.ship_speed += HARD_SHIP_ACC
                    self.lean_speed += HARD_TILT_ACC
                elif e.type == pygame.USEREVENT + 2 and self.isplaying and not self.paused:
                    self.score += 1
                # elif e.type == pygame.USEREVENT + 3 and self.isplaying and fps > 24 and not self.paused:
                #     self.add_ast()


            """ Control & Display update """
            if not self.paused:
                if self.isplaying:
                    for ast in self.asteroids:
                        if method.collision_detection(self.ship_collider, ast):
                            self.shield -= 1
                            if self.shield <= 0:  # GAME OVER
                                self.init_properties()
                                self.ship.pos = [0, 0, 0]
                        if ast.pos[1] < -20:  # Reset Ast Pos
                            ast.pos[0] = random.uniform(
                                self.ship.pos[0] - AST_RANGE, self.ship.pos[0] + AST_RANGE)
                            ast.pos[1] = random.randint(AST_Y_MIN, AST_Y_MAX)
                            ast.pos[2] = random.uniform(
                                self.ship.pos[2] - AST_RANGE, self.ship.pos[2] + AST_RANGE)
                        else:
                            ast.pos[1] -= HARD_AST_INIT * delta_time
                        if ENABLE_AST_MOVING:
                            ast.pos[0] += ast.jiggle_speed[0]
                            ast.pos[1] += ast.jiggle_speed[1]
                            ast.pos[2] += ast.jiggle_speed[2]
                        ast.rotate()

                    method.ship_update(self.ship, self.ship_speed, self.lean_speed, delta_time)
                    self.ship_collider.pos = self.ship.pos[:]
                    self.display(delta_time)
                    method.draw_text([40, self.win_h - 50], str(self.score), 30)
                    method.draw_text([self.win_w - 130, self.win_h - 50], "FPS: " + str(fps), 30)
                    method.draw_text([int(self.win_w / 2 - 200), self.win_h - 60],
                                     "Shield: " + ">" * self.shield, 30, False, (92, 207, 230))

                else:  # Start or Game Over
                    self.start_screen(delta_time, self.ast_speed)
                    method.draw_text([40, 40], "Esc to exit",
                                     25, False, (255, 0, 0))
                    if has_played:  # Game Over
                        method.draw_text([int(self.win_w / 2), int(self.win_h / 3 * 2)],
                                         "Game Over", 60, True, (255, 174, 87))
                        method.draw_text([int(self.win_w / 2), int(self.win_h / 3)],
                                         "You scored: " + str(self.score), 40, True)
                    method.draw_text(
                        [int(self.win_w / 2), int(self.win_h / 2)], "Press space to start", 50, True)
                clock.tick(CLK_TICK)
                pygame.display.flip()
            else:
                if self.isRoaming:  # Paused and Roaming
                    self.camera.roam(event_list)
                    self.display(delta_time)
                    method.draw_text([int(self.win_w / 2), int(self.win_h / 5 * 4)],
                                        "Roaming...", 40, True, (255, 174, 87))
                    clock.tick(CLK_TICK)
                    pygame.display.flip()
                else:  # Just paused
                    method.draw_text([int(self.win_w / 2), int(self.win_h / 3 * 2)],
                                        "Paused", 60, True, (255, 174, 87))



    def display(self, delta_time):
        """Refreshing screen, clearing buffers, and redrawing objects"""  # Ciscenje medjuspremnika i ponovno crtanje objekata
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(110, self.win_w / self.win_h, 0.1, 10000)

        if self.isRoaming:
            ctx = self.camera.eyex + sin(self.camera.polarAngle * D2R) * cos(self.camera.azimuthAngle * D2R)
            cty = self.camera.eyey + sin(self.camera.polarAngle * D2R) * sin(self.camera.azimuthAngle * D2R)
            ctz = self.camera.eyez + cos(self.camera.polarAngle * D2R);
            upx = -cos(self.camera.polarAngle * D2R) * cos(self.camera.azimuthAngle * D2R)
            upy = -cos(self.camera.polarAngle * D2R) * sin(self.camera.azimuthAngle * D2R)
            upz = sin(self.camera.polarAngle * D2R)
            glu.gluLookAt(self.camera.eyex, self.camera.eyey, self.camera.eyez,
                          ctx, cty, ctz,
                          upx, upy, upz)
        else:
            self.camera.update(self.ship)
            if self.fps_view:
                glu.gluLookAt(self.ship.pos[0], self.ship.pos[1], self.ship.pos[2],
                            self.ship.pos[0], self.ship.pos[1] +
                            100, self.ship.pos[2],
                            0, 0, 1)
            else:
                glu.gluLookAt(self.camera.eyex, self.camera.eyey, self.camera.eyez + 3,
                            self.ship.pos[0], self.ship.pos[1] +
                            100, self.ship.pos[2],
                            0, 0, 1)
        self.skybox.sky_pos = self.ship.pos

        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        """ Skybox """
        self.light.disable()
        self.skybox.render(self.camera)
        self.light.enable()

        """ Ship """
        self.light.enable()
        self.center.pos = (
            self.ship.pos[0], self.ship.pos[1], self.ship.pos[2])
        if not self.fps_view:
            self.light.disable()
            self.ship.render()
            self.light.enable()
        else:
            self.center.render()
        self.ship_collider.render()
        self.light.render()

        """ Ast """
        for ast in self.asteroids:
            ast.render()
        self.light.render()

    def start_screen(self, delta_time, speed):
        """Updating a welcome screen (like a screensaver)"""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(80, self.win_w / self.win_h, 0.1, 10000)
        glu.gluLookAt(0, 0, 0, 0, 100, 0, 0, 0, 1)
        self.skybox.sky_pos = self.ship.pos
        self.light.disable()
        self.skybox.render(self.camera)
        self.light.enable()

        for ast in self.asteroids:
            if ast.pos[2] < - CAMERA_DIST - 10:
                ast.pos[0] = random.randint(
                    (int)(self.ship.pos[0])-AST_RANGE, (int)(self.ship.pos[0])+AST_RANGE)
                ast.pos[1] = random.randint(
                    self.ship.pos[1]+AST_Y_MIN_INIT, self.ship.pos[1]+AST_Y_MAX_INIT)
                ast.pos[2] = random.randint(
                    self.ship.pos[2]-AST_RANGE, self.ship.pos[2]+AST_RANGE)
            else:
                ast.pos[1] -= speed * delta_time * 0.1
            ast.render()
        self.light.render()

    def add_ast(self, isInit=False):
        """Adding asteroids to a random pos near the ship"""
        size = random.randint(AST_MIN_SIZE, AST_MAX_SIZE)
        pos_x = random.randint(
            self.ship.pos[0] - AST_RANGE, self.ship.pos[0] + AST_RANGE)
        pos_y = random.randint(self.ship.pos[1]+AST_Y_MIN_INIT, self.ship.pos[1]+AST_Y_MAX_INIT) if isInit \
            else random.randint(self.ship.pos[1]+AST_Y_MIN, self.ship.pos[1]+AST_Y_MAX)
        pos_z = random.randint(
            self.ship.pos[2] - AST_RANGE, self.ship.pos[2] + AST_RANGE)

        self.asteroids.append(Model("materials/ast_lowpoly2/ast_lowpoly2.obj", size, [
                              pos_x, pos_y, pos_z], random.randint(0, 360), random.randint(0, 360), random.randint(0, 360), False,
                              [random.randint(-AST_MOVE_RANGE, AST_MOVE_RANGE), random.randint(-AST_MOVE_RANGE, AST_MOVE_RANGE),
                              random.randint(-AST_MOVE_RANGE, AST_MOVE_RANGE)], random.randint(-AST_ROT_RANGE, AST_ROT_RANGE)))
        if len(self.asteroids) > MAX_DISPLAY_AST:
            self.asteroids.popleft()
 