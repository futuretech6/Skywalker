from modules.methods import *
import OpenGL.GL as gl


class Skybox(object):
    """Skybox class (background image)"""

    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.skybox = []
        self.sky_planes = [
            [(-100, 100, 100), (100, 100, 100),
             (100, 100, -100), (-100, 100, -100)],  # Front
            [(100, -100, 100), (-100, -100, 100),
             (-100, -100, -100), (100, -100, -100)],  # Back
            [(-100, -100, 100), (-100, 100, 100),
             (-100, 100, -100), (-100, -100, -100)],  # Left
            [(100, 100, 100), (100, -100, 100),
             (100, -100, -100), (100, 100, -100)],  # Right
            [(-100, -100, 100), (100, -100, 100),
             (100, 100, 100), (-100, 100, 100)],  # Top
            [(-100, 100, -100), (100, 100, -100),
             (100, -100, -100), (-100, -100, -100)]  # Bottom
        ]

        self.sky_tex_coord = [[(0, 1), (1, 1), (1, 0), (0, 0)],
                              [(0, 1), (1, 1), (1, 0), (0, 0)],
                              [(0, 1), (1, 1), (1, 0), (0, 0)],
                              [(0, 1), (1, 1), (1, 0), (0, 0)],
                              [(0, 1), (1, 1), (1, 0), (0, 0)],
                              [(0, 1), (1, 1), (1, 0), (0, 0)]]

    def render(self, camera):
        """Drawing skybox"""
        gl.glPushMatrix()
        gl.glDisable(gl.GL_CULL_FACE)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glTranslatef(camera.eyex, camera.eyey, camera.eyez)
        for i in range(len(self.sky_planes)):
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.skybox[i])
            gl.glBegin(gl.GL_QUADS)
            for j in range(len(self.sky_planes[i])):
                gl.glTexCoord2f(*self.sky_tex_coord[i][j])
                gl.glVertex3f(*self.sky_planes[i][j])
            gl.glEnd()
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glPopMatrix()

    def init_sky(self):
        """Loading skybox with help of load_texture function"""

        self.skybox = [load_texture(SKY_FRONT),
                       load_texture(SKY_BACK),
                       load_texture(SKY_LEFT),
                       load_texture(SKY_RIGHT),
                       load_texture(SKY_TOP),
                       load_texture(SKY_BOTTOM)]
