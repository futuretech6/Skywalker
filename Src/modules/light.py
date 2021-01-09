import OpenGL.GL as gl

class Light(object):
    def __init__(self, direction):
        self.intensity = [1.0, 1.0, 1.0, 1.0]
        self.direction = direction
        self.ambient_intensity = [0.2, 0.2, 0.2, 1.0]
        self.specular_intensity = [0.6, 0.6, 0.6, 1.0]
        self.enable_specular = True

    def render(self):
        gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.ambient_intensity)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, self.direction)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, self.intensity)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_CONSTANT_ATTENUATION, 0.1)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_LINEAR_ATTENUATION, 0.05)
        # Ovo ispod je za reflektirajuće svjetlo
        if self.enable_specular:
            gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR,
                            self.specular_intensity)
            gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SHININESS, 15.0)
            gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, self.specular_intensity)

    def enable(self):
        """Enable light"""
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)

    def disable(self):
        """Disable light"""
        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_LIGHT0)
