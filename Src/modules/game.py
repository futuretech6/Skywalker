import os
import pygame
import random
import OpenGL.GL as gl
import OpenGL.GLU as glu


from config import *
from modules.model import Model
import modules.methods as method
from modules.light import Light
# from modules.cube import Cube
from modules.sphere import Sphere
# from modules.controller import MouseClass
from modules.skybox import Skybox

class Game(object):
    """Main game class"""

    def __init__(self, width=1280, height=700):
        self.width = width
        self.height = height
        self.asteroids = []
        self.light = Light([0, 3, 3])
        self.skybox = Skybox(self.width, self.height)
        self.center = Sphere(0.02, [0.0, 0.0, 0.0], [1, 1, 1])
        self.paused = False
        self.score = 0

    def init_screen(self):
        """Creating screen and initializing objects"""
        pygame.init()
        size = [self.width, self.height]
        pygame.display.set_mode(size, pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption("Skywalker")
        pygame.mouse.set_visible(False)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)
        self.light.enable()
        self.init_properties()

        os.chdir('./materials/spaceship/')
        self.player = Model("spaceship.obj", 0.4, [0.0, 0.0, 0.0], 0, 180, 0)
        os.chdir('../../')

        # os.chdir('./materials/Starship/')
        # self.player = Model("Starship.obj", 0.4, [0.0, 0.0, 0.0], 0, 180, 0)
        # os.chdir('../../')

        # os.chdir('./materials/X-Wing-OBJ/')
        # self.player = Model("X-Wing-wingsopened.obj", 0.4, [0.0, 0.0, 0.0], 0, 180, 0)
        # os.chdir('../../')

        # os.chdir('./materials/NCC-1701/')
        # self.player = Model("NCC-1701.obj", 0.4, [0.0, 0.0, 0.0], 0, 180, 0, 3)
        # os.chdir('../../')

        # os.chdir('./materials/millenium-falcon/')
        # self.player = Model("millenium-falcon.obj", 0.4, [0.0, 0.0, 0.0], 0, 0, 0, 0.008)
        # os.chdir('../../')

        for i in range(150):
            self.add_asteroid()
        self.ship_collider = Sphere(1.6, [0.0, 0.0, 0.0], [1, 1, 1])
        self.ship_collider.visible = False
        self.skybox.init_sky()

    def init_properties(self):
        """Initialization of game properties"""
        self.isplaying = False
        self.fps_view = False
        self.shield = 10
        self.lean_speed = 4  # brzina rotacije broda
        self.move_speed = 3  # brzina kretanja broda
        self.ast_speed = 6   # brzina asteroida

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
                    if e.key == pygame.K_ESCAPE:
                        method.quit_program()
                    elif e.key == pygame.K_v:
                        self.fps_view = not self.fps_view
                    elif e.key == pygame.K_p:
                        self.paused = not self.paused
                    elif e.key == pygame.K_SPACE and not self.isplaying:
                        self.score = 0
                        for ast in self.asteroids:
                            ast.position[0] = random.randint(-300, 300)
                            ast.position[1] = random.randint(-300, 300)
                            ast.position[2] = random.randint(-800, -300)
                        self.isplaying = True
                        played_once = True
                elif e.type == pygame.USEREVENT + 1 and self.isplaying and not self.paused:
                    self.ast_speed += HARD_AST_ACC
                    self.move_speed += HARD_SHIP_ACC
                    self.lean_speed += HARD_TILT_ACC
                elif e.type == pygame.USEREVENT + 2 and self.isplaying and not self.paused:
                    self.score += 1
                elif e.type == pygame.USEREVENT + 3 and self.isplaying and fps > 24 and not self.paused:
                    self.add_asteroid()

            if not self.paused:
                if self.isplaying:
                    method.ship_movement(self.player, self.move_speed,
                                     self.lean_speed, delta_time, 2000, 2000)
                    self.display(delta_time, self.ast_speed)
                    method.draw_text([40, self.height - 50], str(self.score), 30)
                    method.draw_text(
                        [self.width - 130, self.height - 50], "FPS: " + str(fps), 30)
                    method.draw_text([int(self.width / 2), self.height - 20],
                                 "_" * self.shield, 80, True, (0, 255, 0))
                else:
                    self.start_screen_anim(delta_time, self.ast_speed)
                    method.draw_text([40, 40], "Esc to exit",
                                 25, False, (255, 0, 0))
                    if played_once:
                        method.draw_text([int(self.width / 2), int(self.height / 3)],
                                     "You scored: " + str(self.score), 40, True)
                    method.draw_text(
                        [int(self.width / 2), int(self.height / 2)], "Press space to start", 50, True)
                clock.tick(60)
                pygame.display.flip()

    def display(self, delta_time, speed):
        """Refreshing screen, clearing buffers, and redrawing objects"""  # Ciscenje medjuspremnika i ponovno crtanje objekata
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(90, self.width / self.height, 0.1, 10000)
        if self.fps_view:
            glu.gluLookAt(self.player.position[0], self.player.position[1], self.player.position[2] + 1,
                          self.player.position[0], self.player.position[1], self.player.position[2] - 100,
                          0, 1, 0)
        else:
            glu.gluLookAt(self.player.position[0], self.player.position[1] + 3, self.player.position[2] + 10,
                          self.player.position[0], self.player.position[1], self.player.position[2] - 100,
                          0, 1, 0)
        self.skybox.sky_position = self.player.position
        self.ship_collider.position = self.player.position
        self.light.disable()
        self.skybox.render()
        self.light.enable()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        for ast in self.asteroids:
            if method.collision_detection(self.ship_collider, ast):
                self.shield -= 1
                if self.shield <= 0:  # GAME OVER
                    self.init_properties()
                    self.player.position = [0.0, 0.0, 0.0]
            if ast.position[2] > 20:
                ast.position[0] = random.uniform(
                    self.player.position[0] - 300, self.player.position[0] + 300)
                ast.position[1] = random.uniform(
                    self.player.position[1] - 300, self.player.position[1] + 300)
                ast.position[2] = random.randint(-800, -300)
            else:
                ast.position[2] += speed * delta_time
                ast.render()

        self.center.position = self.player.position
        if not self.fps_view:
            self.light.disable()
            self.player.render()
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
        glu.gluPerspective(80, self.width / self.height, 0.1, 10000)
        self.skybox.sky_position = self.player.position
        self.light.disable()
        self.skybox.render()
        self.light.enable()

        for obj in self.asteroids:
            if obj.position[2] > 30:
                obj.position[0] = random.randint(-200, 200)
                obj.position[1] = random.randint(-200, 200)
                obj.position[2] = random.randint(-700, -300)
            else:
                obj.position[2] += speed * delta_time * 0.1
                obj.render()
        self.light.render()

    def add_asteroid(self):
        """Adding asteroids to a random position near the ship"""
        size = random.randint(3, 20)
        pos_x = random.uniform(
            self.player.position[0] - 200, self.player.position[0] + 200)
        pos_y = random.uniform(
            self.player.position[1] - 200, self.player.position[1] + 200)
        if self.isplaying:
            pos_z = random.randint(-800, -300)
        else:
            pos_z = random.randint(-500, -100)
        self.asteroids.append(
            Model("materials/ast_lowpoly2/ast_lowpoly2.obj", size, [pos_x, pos_y, pos_z]))
        if len(self.asteroids) > MAX_DISPLAY_AST:
            self.asteroids.pop(0)
