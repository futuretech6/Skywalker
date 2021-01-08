import pygame
import numpy as np

class MouseClass(object):
    """Class for mouse controls"""

    def __init__(self, mouse_speed, move_speed):
        self.move_speed = move_speed
        self.mouse_speed = mouse_speed
        self.up = [0.0, 0.0, 0.0]
        self.right = [0.0, 0.0, 0.0]
        self.direction = [0.0, 0.0, 0.0]
        self.position = [0, 0, 0]
        self.hor_angle = 0.0
        self.vert_angle = 0.0

    def update_view(self):
        """Refreshes direction of view based on right and up vector"""
        self.direction = np.array([
            np.cos(self.vert_angle) * np.sin(self.hor_angle),
            np.sin(self.vert_angle),
            np.cos(self.vert_angle) * np.cos(self.hor_angle)])

        self.right = np.array([
            np.sin(self.hor_angle - np.pi / 2.0),
            0,
            np.cos(self.hor_angle - np.pi / 2.0)])

        # rezultantni vektor dvaju vektora
        self.up = np.cross(self.right, self.direction)

        # spremiti zbroj dvaju vektora, to nam je smjer gledanja u odnosu na trenutnu poziciju
        look_here = np.add(self.position, self.direction)

        look_at = (self.position[0], self.position[1], self.position[2],
                   look_here[0], look_here[1], look_here[2],
                   self.up[0], self.up[1], self.up[2])

        # vraćamo lookAt varijablu koju u glavnom programu proslijedimo u gluLookAt funkciju
        return look_at

    def limit_vert_view(self):
        """Limits vertical view to 90 degress up and down"""
        if self.vert_angle > 0.9:
            self.vert_angle = 0.9
        elif self.vert_angle < -0.9:
            self.vert_angle = -0.9

    def limit_hor_view(self):
        """Limits horizontal view to 90 degress left and right"""
        if self.hor_angle > 0.9:
            self.hor_angle = 0.9
        elif self.hor_angle < -0.9:
            self.hor_angle = -0.9

    def move_player(self, delta_time):
        """Player movement based on direction of view"""
        keys = pygame.key.get_pressed()
        # pomnožiti vektor smjera i desni vektor sa brzinom kretanja i vremenom između dva updatea
        self.direction = np.multiply(
            self.direction, delta_time * self.move_speed)
        self.right = np.multiply(self.right, delta_time * self.move_speed)

        if keys[pygame.K_w]:
            # zbroji trenutnu poziciju i vektor smjera
            self.position = np.add(self.position, self.direction)
        if keys[pygame.K_s]:
            self.position = np.subtract(self.position, self.direction)
        if keys[pygame.K_a]:
            self.position = np.subtract(self.position, self.right)
        if keys[pygame.K_d]:
            self.position = np.add(self.position, self.right)

    def angle(self, width, height, delta_time, mouse_position):
        """Refreshes angle of view, depends on a sensitivity of a mouse (mouse_speed)"""
        self.hor_angle += self.mouse_speed * \
            delta_time * (width / 2 - mouse_position[0])
        self.vert_angle += self.mouse_speed * \
            delta_time * (height / 2 - mouse_position[1])
