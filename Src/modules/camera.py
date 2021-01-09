import OpenGL.GL as gl
from config import CAMERA_DIST

class Camera:
    def __init__(self):
        self.eyex = 0
        self.eyey = -CAMERA_DIST
        self.eyez = 0
        
    def update(self, ship):
        self.eyex = ship.pos[0]
        self.eyey = ship.pos[1] - CAMERA_DIST
        self.eyez = ship.pos[2]