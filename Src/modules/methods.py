"""Module which contains frequently used functions ans classes"""

import os
import sys

import pygame
import numpy as np
import OpenGL.GL as gl

pygame.init()


# Prozor centriran na sredinu ekrana
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


def arrows_movement(obj, speed, d_time):
    """Arrow movement, supports diagonal movement"""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or (keys[pygame.K_LEFT] and keys[pygame.K_UP]) or (keys[pygame.K_LEFT] and keys[pygame.K_DOWN]):
        obj.position[0] -= speed * d_time
    if keys[pygame.K_RIGHT] or (keys[pygame.K_RIGHT] and keys[pygame.K_UP]) or (keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]):
        obj.position[0] += speed * d_time
    if keys[pygame.K_UP] or (keys[pygame.K_LEFT] and keys[pygame.K_UP]) or (keys[pygame.K_RIGHT] and keys[pygame.K_UP]):
        obj.position[2] -= speed * d_time
    if keys[pygame.K_DOWN] or (keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]) or (keys[pygame.K_LEFT] and keys[pygame.K_DOWN]):
        obj.position[2] += speed * d_time


def wasd_xy_movement(obj, speed, d_time):
    """wasd buttons movement along x and y axis (forward-backward, up-down), supports diagonal movement"""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or (keys[pygame.K_a] and keys[pygame.K_w]) or (keys[pygame.K_a] and keys[pygame.K_s]):
        obj.position[0] -= speed * d_time
    if keys[pygame.K_d] or (keys[pygame.K_d] and keys[pygame.K_w]) or (keys[pygame.K_d] and keys[pygame.K_s]):
        obj.position[0] += speed * d_time
    if keys[pygame.K_w] or (keys[pygame.K_a] and keys[pygame.K_w]) or (keys[pygame.K_d] and keys[pygame.K_w]):
        obj.position[1] -= speed * d_time
    if keys[pygame.K_s] or (keys[pygame.K_d] and keys[pygame.K_s]) or (keys[pygame.K_a] and keys[pygame.K_s]):
        obj.position[1] += speed * d_time


def wasd_xz_movement(obj, speed, d_time):
    """wasd buttons movement along x and z axis (forward-backward, left-right)"""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or (keys[pygame.K_a] and keys[pygame.K_w]) or (keys[pygame.K_a] and keys[pygame.K_s]):
        obj.position[0] -= speed * d_time
    if keys[pygame.K_d] or (keys[pygame.K_d] and keys[pygame.K_w]) or (keys[pygame.K_d] and keys[pygame.K_s]):
        obj.position[0] += speed * d_time
    if keys[pygame.K_w] or (keys[pygame.K_a] and keys[pygame.K_w]) or (keys[pygame.K_d] and keys[pygame.K_w]):
        obj.position[2] -= speed * d_time
    if keys[pygame.K_s] or (keys[pygame.K_d] and keys[pygame.K_s]) or (keys[pygame.K_a] and keys[pygame.K_s]):
        obj.position[2] += speed * d_time


def ship_movement(player, move_speed, lean_speed, delta_time, x_limit, y_limit):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if player.position[0] > -x_limit:
            player.position[0] -= move_speed * delta_time * 1.2
        if player.rot_z < -39:
            player.rot_z = -40
        else:
            player.rot_z -= lean_speed * delta_time
    if keys[pygame.K_d]:
        if player.position[0] < x_limit:
            player.position[0] += move_speed * delta_time * 1.2
        if player.rot_z > 39:
            player.rot_z = 40
        else:
            player.rot_z += lean_speed * delta_time
    if keys[pygame.K_w]:
        if player.position[1] < y_limit:
            player.position[1] += move_speed * delta_time
        if player.rot_x > 24:
            player.rot_x = 25
        else:
            player.rot_x += lean_speed * delta_time
    if keys[pygame.K_s]:
        if player.position[1] > -y_limit:
            player.position[1] -= move_speed * delta_time
        if player.rot_x < -24:
            player.rot_x = -25
        else:
            player.rot_x -= lean_speed * delta_time
    if not keys[pygame.K_a] and not keys[pygame.K_d]:
        if player.rot_z < -1 - lean_speed * delta_time:
            player.rot_z += lean_speed * delta_time
        elif player.rot_z > 1 + lean_speed * delta_time:
            player.rot_z -= lean_speed * delta_time
        else:
            player.rot_z = 0
    if not keys[pygame.K_w] and not keys[pygame.K_s]:
        if player.rot_x < -1 - lean_speed * delta_time:
            player.rot_x += lean_speed * delta_time
        elif player.rot_x > 1 + lean_speed * delta_time:
            player.rot_x -= lean_speed * delta_time
        else:
            player.rot_x = 0


# def simple_zoom(fov, button):
#     """View zoom, gets called when scrolling, calls mousebuttondown event"""
#     if button == 4:
#         fov *= 0.9
#     elif button == 5:
#         fov /= 0.9

#     if fov > 100:
#         fov = 100
#     elif fov < 15:
#         fov = 15
#     return fov


def collision_detection(first, second):
    """Function to detect collision between two spheres"""
    distance_array = distance_between_two_objects(first, second)
    distance = distance_array[0]
    r1, r2 = distance_array[1], distance_array[2]

    # ako je udaljenost manja od zbroja radijusa imamo sudar
    if distance < r1 + r2:
        return True
    else:
        return False


# def basic_AI(first, second, danger_zone, dtime, ai_speed):
#     """Simple AI, start to follow a player if it is inside its danger_zone"""
#     distance_array = distance_between_two_objects(first, second)
#     distance = distance_array[0]
#     size_first = distance_array[1]
#     size_second = distance_array[2]
#     x_dist, y_dist, z_dist = distance_array[3:6]

#     if (distance < danger_zone and distance > size_first + size_second):
#         second.position[1] += dtime * ai_speed * \
#             (y_dist / distance)  # normaliziran vektor
#         second.position[0] += dtime * ai_speed * (x_dist / distance)
#         second.position[2] += dtime * ai_speed * (z_dist / distance)


def distance_between_two_objects(first, second):
    """Returns distance between objects, used for collision detection"""
    # x pozicija
    x1 = first.position[0]
    x2 = second.position[0]

    # y pozicija
    y1 = first.position[1]
    y2 = second.position[1]

    # z pozicija
    z1 = first.position[2]
    z2 = second.position[2]

    # njihov radijus
    if hasattr(first, 'radius'):
        r1 = first.radius
    else:
        r1 = abs(first.size)
    if hasattr(second, 'radius'):
        r2 = second.radius
    else:
        r2 = abs(second.size)

    # formula za udaljenost između dviju točaka
    distance = np.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1)
                       * (y2 - y1) + (z2 - z1) * (z2 - z1))

    x_dist = x1 - x2
    y_dist = y1 - y2
    z_dist = z1 - z2

    return [distance, r1, r2, x_dist, y_dist, z_dist]


def draw_text(position, text_string, size=50, from_center=False, color=(255, 255, 255), back_color=None):
    """Function for drawing text on screen"""
    font = pygame.font.SysFont('times', size)
    text_surface = font.render(text_string, True, color, back_color)
    img_data = pygame.image.tostring(text_surface, "RGBA", True)
    ix, iy = text_surface.get_width(), text_surface.get_height()
    x = 20
    if from_center:
        x = position[0] - int(ix / 2)
    else:
        x = position[0]
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glWindowPos2i(x, position[1])
    gl.glDrawPixels(ix, iy, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, img_data)
    gl.glDisable(gl.GL_BLEND)










