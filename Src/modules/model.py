import OpenGL.GL as gl
from modules.objLoader import OBJ

class Model(object):
    """Loading asteroids with objLoader module"""
    def __init__(self, filename, objsize, position, rot_x=0, rot_y=0, rot_z=0, scale=1):
        self.obj = OBJ(filename, objsize)
        self.size = self.obj.max_vert()
        self.position = position
        self.rot_x = rot_x
        self.rot_y = rot_y
        self.rot_z = rot_z
        self.scale = scale

    def render(self):
        """Rendering asteroids on the screen"""
        gl.glPushMatrix()
        gl.glTranslatef(self.position[0], self.position[1], self.position[2])
        gl.glRotatef(self.rot_x, 1, 0, 0)
        gl.glRotatef(self.rot_y, 0, 1, 0)
        gl.glRotatef(self.rot_z, 0, 0, 1)
        gl.glScalef(self.scale, self.scale, self.scale)
        gl.glCallList(self.obj.list_id)
        gl.glPopMatrix()