import OpenGL.GL as gl
from modules.objLoader import OBJ

class Model(object):
    """Loading asteroids with objLoader module"""
    def __init__(self, filename, objsize, pos, rot_x=0, rot_y=0, rot_z=0, using_left=False, move_speed=[0,0,0], rot_speed=0):
        self.obj = OBJ(filename, objsize)
        self.radius = self.obj.max_vert()
        self.pos = pos[:]
        self.rot_x_init = rot_x
        self.rot_y_init = rot_y
        self.rot_z_init = rot_z
        self.rot_x = rot_x
        self.rot_y = rot_y
        self.rot_z = rot_z
        self.move_speed = move_speed[:]
        self.rot_speed = rot_speed
        self.rot_angle = 0
        self.using_left = using_left

    def rotate(self):
        self.rot_angle = (self.rot_angle + self.rot_speed) % 360

    def render(self):
        """Rendering asteroids on the screen"""
        gl.glPushMatrix()
        gl.glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        gl.glRotatef(self.rot_z, 0, 0, 1)
        gl.glRotatef(self.rot_y, 0, 1, 0)
        gl.glRotatef(self.rot_x, 1, 0, 0)
        gl.glRotatef(self.rot_angle, 0, 0, 1)
        gl.glCallList(self.obj.list_id)
        gl.glPopMatrix()
