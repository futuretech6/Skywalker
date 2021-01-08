import OpenGL.GL as gl
import OpenGL.GLU as glu

class Sphere(object):
    """Class for making a sphere"""

    def __init__(self, radius, position, color, visible=True):
        self.radius = radius
        self.position = position
        self.visible = visible
        self.color = color
        self.slices = 25  # meridijani
        self.stacks = 15  # paralele
        self.quadric = glu.gluNewQuadric()

    def render(self):
        """Drawing a sphere"""
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        v = self.visible
        gl.glPushMatrix()
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
        self.color = (self.color[0], self.color[1], self.color[2], v)
        gl.glColor4f(*self.color)
        gl.glTranslatef(x, y, z)
        glu.gluSphere(self.quadric, self.radius, self.slices, self.stacks)
        gl.glDisable(gl.GL_BLEND)
        gl.glPopMatrix()
