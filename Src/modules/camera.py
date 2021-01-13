import OpenGL.GL as gl
import pygame
from math import sin, cos

from config import CAMERA_DIST, D2R, CAM_MOVE_STEP


class Camera:
    def __init__(self):
        self.eyex = 0
        self.eyey = -CAMERA_DIST
        self.eyez = 0
        self.upx = 0
        self.azimuthAngle = 90  # Counter-clock from x+
        self.polarAngle = 90    # Down from z+
        self.mouse_oldx = None
        self.mouse_oldy = None
        self.clicked = False

    def update(self, ship):
        self.eyex = ship.pos[0]
        self.eyey = ship.pos[1] - CAMERA_DIST
        self.eyez = ship.pos[2]

    def roam(self, even_list):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.eyex -= CAM_MOVE_STEP * sin(self.azimuthAngle * D2R)
            self.eyey += CAM_MOVE_STEP * cos(self.azimuthAngle * D2R)
        if keys[pygame.K_d]:
            self.eyex += CAM_MOVE_STEP * sin(self.azimuthAngle * D2R)
            self.eyey -= CAM_MOVE_STEP * cos(self.azimuthAngle * D2R)
        if keys[pygame.K_w]:
            self.eyex += CAM_MOVE_STEP * sin(self.polarAngle * D2R) * cos(self.azimuthAngle * D2R)
            self.eyey += CAM_MOVE_STEP * sin(self.polarAngle * D2R) * sin(self.azimuthAngle * D2R)
            self.eyez += CAM_MOVE_STEP * cos(self.polarAngle * D2R)
        if keys[pygame.K_s]:
            self.eyex -= CAM_MOVE_STEP * sin(self.polarAngle * D2R) * cos(self.azimuthAngle * D2R)
            self.eyey -= CAM_MOVE_STEP * sin(self.polarAngle * D2R) * sin(self.azimuthAngle * D2R)
            self.eyez -= CAM_MOVE_STEP * cos(self.polarAngle * D2R)
        if keys[pygame.K_l]:
            self.eyex -= cos(self.polarAngle * D2R) * cos(self.azimuthAngle * D2R)
            self.eyey -= cos(self.polarAngle * D2R) * sin(self.azimuthAngle * D2R)
            self.eyez += CAM_MOVE_STEP * sin(self.polarAngle * D2R)
        if keys[pygame.K_k]:
            self.eyex += cos(self.polarAngle * D2R) * cos(self.azimuthAngle * D2R)
            self.eyey += cos(self.polarAngle * D2R) * sin(self.azimuthAngle * D2R)
            self.eyez -= CAM_MOVE_STEP * sin(self.polarAngle * D2R)

        mouse_pos = pygame.mouse.get_pos()
        # if self.mouse_oldx == None and self.mouse_oldy == None:
        #     self.mouse_oldx, self.mouse_oldy = mouse_pos[0], mouse_pos[1]

        for e in even_list:
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.clicked = True
                self.mouse_oldx, self.mouse_oldy = mouse_pos[0], mouse_pos[1]
            if e.type == pygame.MOUSEBUTTONUP:
                self.clicked = False
        print(self.clicked)
        if self.clicked:
            self.azimuthAngle += (mouse_pos[0] - self.mouse_oldx) / 5
            self.polarAngle -= (mouse_pos[1] - self.mouse_oldy) / 5
            self.mouse_oldx, self.mouse_oldy = mouse_pos[0], mouse_pos[1]


        # mouse = pygame.