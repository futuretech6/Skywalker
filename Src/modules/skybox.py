from modules.methods import *
import OpenGL.GL as gl

class Skybox(object):
    """Skybox class (background image)"""

    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.skybox = []
        self.sky_position = [0.0, 0.0, 0.0]
        self.sky_planes = [
            [(-10, -10, -10), (-10, -10, +10),
             (-10, +10, +10), (-10, +10, -10)],  # Naorijed
            [(-10, -10, +10), (+10, -10, +10),
             (+10, +10, +10), (-10, +10, +10)],  # Lijevo
            [(+10, -10, +10), (+10, -10, -10),
             (+10, +10, -10), (+10, +10, +10)],  # Natrag
            [(+10, -10, -10), (-10, -10, -10),
             (-10, +10, -10), (+10, +10, -10)],  # Desno
            [(-10, +10, -10), (-10, +10, +10),
             (+10, +10, +10), (+10, +10, -10)],  # Gore
            [(-10, -10, -10), (-10, -10, +10),
             (+10, -10, +10), (+10, -10, -10)]]  # Dolje

        self.sky_tex_coord = [[(0, 0), (1, 0), (1, 1), (0, 1)],
                              [(0, 0), (1, 0), (1, 1), (0, 1)],
                              [(0, 0), (1, 0), (1, 1), (0, 1)],
                              [(0, 0), (1, 0), (1, 1), (0, 1)],
                              [(0, 0), (1, 0), (1, 1), (0, 1)],
                              [(0, 1), (1, 1), (1, 0), (0, 0)]]

    def render(self):
        """Drawing skybox"""
        gl.glPushMatrix()
        gl.glDisable(gl.GL_CULL_FACE)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glTranslatef(*self.sky_position)
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

        self.skybox = [load_texture('materials/sky/nasa.jpg'),
                       load_texture('materials/sky/nasa.jpg'),
                       load_texture('materials/sky/nasa.jpg'),
                       load_texture('materials/sky/nasa.jpg'),
                       load_texture('materials/sky/nasa.jpg'),
                       load_texture('materials/sky/nasa.jpg')]

        # self.skybox = [load_texture('materials/sky/front.jpg'),
        #                load_texture('materials/sky/left.jpg'),
        #                load_texture('materials/sky/back.jpg'),
        #                load_texture('materials/sky/right.jpg'),
        #                load_texture('materials/sky/top.jpg'),
        #                load_texture('materials/sky/bottom.jpg')]

        # self.skybox = [load_texture('materials/sky/Front_MauveSpaceBox.png'),
        #                load_texture('materials/sky/Left_MauveSpaceBox.png'),
        #                load_texture('materials/sky/Back_MauveSpaceBox.png'),
        #                load_texture('materials/sky/Right_MauveSpaceBox.png'),
        #                load_texture('materials/sky/Up_MauveSpaceBox.png'),
        #                load_texture('materials/sky/Down_MauveSpaceBox.png')]
