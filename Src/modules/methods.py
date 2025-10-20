import os
import sys

import pygame
import numpy as np
import OpenGL.GL as gl

from config import *

pygame.init()


def init_window():
    os.environ['SDL_VIDEO_CENTERED'] = '1'


def quit_program():
    """Function for program abort"""
    pygame.quit()
    sys.exit()


def load_texture(path):
    """Function for loading texture"""
    surface = pygame.image.load(path)
    data = pygame.image.tostring(surface, "RGBA", True)

    ix = surface.get_width()
    iy = surface.get_height()

    gl.glEnable(gl.GL_TEXTURE_2D)
    tex_id = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, tex_id)

    gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, 3, ix, iy, 0,
                    gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, data)

    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_R, gl.GL_CLAMP_TO_EDGE)
    gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE)

    return tex_id


def ship_update(ship, ship_speed, tilt_speed, delta_time, x_limit=SCENE_SIZE_LIMIT, z_limit=SCENE_SIZE_LIMIT):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if ship.pos[0] > -x_limit:
            ship.pos[0] -= ship_speed * delta_time

        if ship.using_left:
            if ship.rot_y <= ship.rot_y_init - MAX_TILT_ANGLE_Y:
                ship.rot_y = ship.rot_y_init - MAX_TILT_ANGLE_Y
            else:
                ship.rot_y -= tilt_speed * delta_time
        else:
            if ship.rot_y >= ship.rot_y_init + MAX_TILT_ANGLE_Y:
                ship.rot_y = ship.rot_y_init + MAX_TILT_ANGLE_Y
            else:
                ship.rot_y += tilt_speed * delta_time

    if keys[pygame.K_d]:
        if ship.pos[0] < x_limit:
            ship.pos[0] += ship_speed * delta_time

        if ship.using_left:
            if ship.rot_y >= ship.rot_y_init + MAX_TILT_ANGLE_Y:
                ship.rot_y = ship.rot_y_init + MAX_TILT_ANGLE_Y
            else:
                ship.rot_y += tilt_speed * delta_time
        else:
            if ship.rot_y <= ship.rot_y_init - MAX_TILT_ANGLE_Y:
                ship.rot_y = ship.rot_y_init - MAX_TILT_ANGLE_Y
            else:
                ship.rot_y -= tilt_speed * delta_time

    if keys[pygame.K_w]:
        if ship.pos[2] < z_limit:
            ship.pos[2] += ship_speed * delta_time

        if ship.using_left:
            if ship.rot_x >= ship.rot_x_init + MAX_TILT_ANGLE_X:
                ship.rot_x = ship.rot_x_init + MAX_TILT_ANGLE_X
            else:
                ship.rot_x += tilt_speed * delta_time
        else:
            if ship.rot_x <= ship.rot_x_init - MAX_TILT_ANGLE_X:
                ship.rot_x = ship.rot_x_init - MAX_TILT_ANGLE_X
            else:
                ship.rot_x -= tilt_speed * delta_time

    if keys[pygame.K_s]:
        if ship.pos[2] > -z_limit:
            ship.pos[2] -= ship_speed * delta_time

        if ship.using_left:
            if ship.rot_x <= ship.rot_x_init - MAX_TILT_ANGLE_X:
                ship.rot_x = ship.rot_x_init - MAX_TILT_ANGLE_X
            else:
                ship.rot_x -= tilt_speed * delta_time
        else:
            if ship.rot_x >= ship.rot_x_init + MAX_TILT_ANGLE_X:
                ship.rot_x = ship.rot_x_init + MAX_TILT_ANGLE_X
            else:
                ship.rot_x += tilt_speed * delta_time

    if not keys[pygame.K_a] and not keys[pygame.K_d]:  # Restore
        if ship.rot_y < ship.rot_y_init - tilt_speed * delta_time:
            ship.rot_y += tilt_speed * delta_time
        elif ship.rot_y > ship.rot_y_init + tilt_speed * delta_time:
            ship.rot_y -= tilt_speed * delta_time
        else:
            ship.rot_y = ship.rot_y_init

    if not keys[pygame.K_w] and not keys[pygame.K_s]:  # Restore
        if ship.rot_x < ship.rot_x_init - tilt_speed * delta_time:
            ship.rot_x += tilt_speed * delta_time
        elif ship.rot_x > ship.rot_x_init + tilt_speed * delta_time:
            ship.rot_x -= tilt_speed * delta_time
        else:
            ship.rot_x = ship.rot_x_init


def collision_detection(first, second):
    """Function to detect collision between two spheres"""
    distance = ((first.pos[0] - second.pos[0])**2 + (first.pos[1] - \
        second.pos[1])**2 + (first.pos[2] - second.pos[2])**2) ** 0.5

    if distance < first.radius + second.radius:
        return True
    else:
        return False


def draw_text(pos, text_string, size=50, from_center=False, color=(255, 255, 255), back_color=None):
    """Function for drawing text on screen"""
    font = pygame.font.SysFont('timesnewroman', size)
    text_surface = font.render(text_string, True, color, back_color)
    img_data = pygame.image.tostring(text_surface, "RGBA", True)
    ix, iy = text_surface.get_width(), text_surface.get_height()
    x = 20
    if from_center:
        x = pos[0] - int(ix / 2)
    else:
        x = pos[0]
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glWindowPos2i(x, pos[1])
    gl.glDrawPixels(ix, iy, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, img_data)
    gl.glDisable(gl.GL_BLEND)
