from modules.camera import Camera
import os
import pygame
import random
import OpenGL.GL as gl
import OpenGL.GLU as glu


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
        self.asteroids = []
        self.light = Light([0, -3, 3])
        self.skybox = Skybox(self.win_w, self.win_h)
        self.center = Sphere(0.1, [1.0, 0.0, 1.0], [1, 1, 1])
        self.paused = False
        self.score = 0
        self.camera = Camera()

    def init_screen(self):
        """Creating screen and initializing objects"""
        pygame.init()
        size = [self.win_w, self.win_h]
        pygame.display.set_mode(size, pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption("Skywalker")
        pygame.mouse.set_visible(False)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)
        self.light.enable()
        self.init_properties()

        os.chdir('./materials/spaceship/')
        self.ship = Model("spaceship.obj", 0.4, [0.0, 0.0, 0.0], -270, 0, -180)
        os.chdir('../../')

        # os.chdir('./materials/Starship/')
        # self.ship = Model("Starship.obj", 0.01, [0.0, 0.0, 0.0], 90, 0, 180)
        # os.chdir('../../')

        # os.chdir('./materials/NCC-1701/')
        # self.ship = Model("NCC-1701_modified.obj", 1.2, [0.0, 0.0, 0.0], 90, 0, 180)
        # os.chdir('../../')

        # os.chdir('./materials/millenium-falcon/')
        # self.ship = Model("millenium-falcon_modified.obj", 1, [0.0, 0.0, 0.0], 90, 0, 0, using_left=True)
        # os.chdir('../../')

        for i in range(MAX_DISPLAY_AST):
            self.add_asteroid()
        self.ship_collider = Sphere(self.ship.radius, [0.0, 0.0, 0.0], [1, 1, 1], False)
        self.skybox.init_sky()

    def init_properties(self):
        """Initialization of game properties"""
        self.isplaying = False
        self.fps_view = False
        self.shield = HARD_INIT_SHIELD
        self.ast_speed = HARD_AST_INIT
        self.ship_speed = HARD_SHIP_INIT
        self.lean_speed = HARD_TILT_INIT

    def main_loop(self):
        """Main game loop"""
        self.init_screen()
        pygame.time.set_timer(pygame.USEREVENT + 1, HARD_ACC_TIME_SEP)  # accelerate
        pygame.time.set_timer(pygame.USEREVENT + 2, 1000)  # score++
        pygame.time.set_timer(pygame.USEREVENT + 3, 1000)  # refresh asts
        played_once = False
        clock = pygame.time.Clock()
        while True:
            delta_time = clock.tick(60) / 10
            fps = int(clock.get_fps())
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif e.type == pygame.KEYDOWN:
                    """ Keyboard """
                    if e.key == pygame.K_ESCAPE or e.key == pygame.K_q:
                        method.quit_program()
                    elif e.key == pygame.K_v:
                        self.fps_view = not self.fps_view
                    elif e.key == pygame.K_p:
                        self.paused = not self.paused
                    elif e.key == pygame.K_SPACE and not self.isplaying:
                        self.score = 0
                        for ast in self.asteroids:
                            ast.pos[0] = random.randint(-300, 300)
                            ast.pos[1] = random.randint(-300, 300)
                            ast.pos[2] = random.randint(-800, -300)
                        self.isplaying = True
                        played_once = True
                elif e.type == pygame.USEREVENT + 1 and self.isplaying and not self.paused:
                    self.ast_speed += HARD_AST_ACC
                    self.ship_speed += HARD_SHIP_ACC
                    self.lean_speed += HARD_TILT_ACC
                elif e.type == pygame.USEREVENT + 2 and self.isplaying and not self.paused:
                    self.score += 1
                elif e.type == pygame.USEREVENT + 3 and self.isplaying and fps > 24 and not self.paused:
                    self.add_asteroid()
            
            """ Display update """
            if not self.paused:
                if self.isplaying:
                    method.ship_movement(self.ship, self.ship_speed, self.lean_speed, delta_time)
                    self.ship_collider.pos = self.ship.pos[:]
                    self.display(delta_time, self.ast_speed)
                    method.draw_text([40, self.win_h - 50], str(self.score), 30)
                    method.draw_text(
                        [self.win_w - 130, self.win_h - 50], "FPS: " + str(fps), 30)
                    method.draw_text([int(self.win_w / 2), self.win_h - 30],
                                 "_" * self.shield, 80, True, (0, 255, 0))

                else:  # Game Over
                    self.start_screen_anim(delta_time, self.ast_speed)
                    method.draw_text([40, 40], "Esc to exit",
                                 25, False, (255, 0, 0))
                    if played_once:
                        method.draw_text([int(self.win_w / 2), int(self.win_h / 3)],
                                     "You scored: " + str(self.score), 40, True)
                    method.draw_text(
                        [int(self.win_w / 2), int(self.win_h / 2)], "Press space to start", 50, True)

                clock.tick(60)
                pygame.display.flip()

    def display(self, delta_time, speed):
        """Refreshing screen, clearing buffers, and redrawing objects"""  # Ciscenje medjuspremnika i ponovno crtanje objekata
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(90, self.win_w / self.win_h, 0.1, 10000)

        self.camera.update(self.ship)
        if self.fps_view:
            glu.gluLookAt(self.ship.pos[0], self.ship.pos[1], self.ship.pos[2],
                          self.ship.pos[0], self.ship.pos[1] + 100, self.ship.pos[2],
                          0, 0, 1)
        else:
            glu.gluLookAt(self.camera.eyex, self.camera.eyey, self.camera.eyez + 3,
                          self.ship.pos[0], self.ship.pos[1] + 100, self.ship.pos[2],
                          0, 0, 1)
        self.skybox.sky_pos = self.ship.pos
        self.light.disable()
        self.skybox.render()
        self.light.enable()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        """ Ast """
        for ast in self.asteroids:
            if method.collision_detection(self.ship_collider, ast):
                self.shield -= 1
                if self.shield <= 0:  # GAME OVER
                    self.init_properties()
                    self.ship.pos = [0.0, 0.0, 0.0]
            if ast.pos[1] < -20:  # Reset Ast Pos
                ast.pos[0] = random.uniform(
                    self.ship.pos[0] - 300, self.ship.pos[0] + 300)
                ast.pos[1] = random.randint(300, 800)
                ast.pos[2] = random.uniform(
                    self.ship.pos[2] - 300, self.ship.pos[2] + 300)
            else:
                ast.pos[1] -= speed * delta_time
                ast.render()
        
        """ Ship """
        self.center.pos = (self.ship.pos[0], self.ship.pos[1], self.ship.pos[2])
        if not self.fps_view:
            self.light.disable()
            self.ship.render()
            self.light.enable()
        else:
            self.center.render()
        self.ship_collider.render()
        self.light.render()

    def start_screen_anim(self, delta_time, speed):
        """Updating a welcome screen (like a screensaver)"""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(80, self.win_w / self.win_h, 0.1, 10000)
        self.skybox.sky_pos = self.ship.pos
        self.light.disable()
        self.skybox.render()
        self.light.enable()

        for ast in self.asteroids:
            if ast.pos[2] < - CAMERA_DIST - 10:
                ast.pos[0] = random.randint(self.ship.pos[0]-AST_RANGE, self.ship.pos[0]+AST_RANGE)
                ast.pos[1] = random.randint(self.ship.pos[1]+300, self.ship.pos[1]+700)
                ast.pos[2] = random.randint(self.ship.pos[2]-AST_RANGE, self.ship.pos[2]+AST_RANGE)
            else:
                ast.pos[1] -= speed * delta_time * 0.1
            ast.render()
        self.light.render()

    def add_asteroid(self):
        """Adding asteroids to a random pos near the ship"""
        size = random.randint(3, 20)
        pos_x = random.uniform(
            self.ship.pos[0] - AST_RANGE, self.ship.pos[0] + AST_RANGE)
        pos_z = random.uniform(
            self.ship.pos[2] - AST_RANGE, self.ship.pos[2] + AST_RANGE)
        if self.isplaying:
            pos_y = random.randint(300, 800)
        else:
            pos_y = random.randint(100, 500)
        self.asteroids.append(
            Model("materials/ast_lowpoly2/ast_lowpoly2.obj", size, [pos_x, pos_y, pos_z], random.randint(0, 360), random.randint(0, 360), random.randint(0, 360)))
        if len(self.asteroids) > MAX_DISPLAY_AST:
            self.asteroids.pop(0)
