import OpenGL.GL as gl

class Cube(object):
    """Class for making a cube"""

    def __init__(self, size, position, color, visible=True):
        self.position = position
        self.size = size
        self.color = color
        self.visible = visible
        self.color.append(self.visible)
        self.vertices = [[+size, -size, -size], [+size, +size, -size],
                         [-size, +size, -size], [-size, -size, -size],
                         [+size, -size, +size], [+size, +size, +size],
                         [-size, -size, +size], [-size, +size, +size]]
        self.cube_sides = [[0, 1, 2, 3], [3, 2, 7, 6], [6, 7, 5, 4],
                           [4, 5, 1, 0], [1, 5, 7, 2], [4, 0, 3, 6]]

    def render(self):
        """Drawing a cube"""
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        v = self.visible

        gl.glPushMatrix()
        # these two function below allow object transparency
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
        gl.glTranslatef(x, y, z)
        gl.glBegin(gl.GL_QUADS)
        self.color = [self.color[0], self.color[1], self.color[2], v]
        gl.glColor4f(*self.color)
        for side in self.cube_sides:
            for vert in side:
                gl.glVertex3fv(self.vertices[vert])
        gl.glEnd()
        gl.glDisable(gl.GL_BLEND)
        gl.glPopMatrix()
