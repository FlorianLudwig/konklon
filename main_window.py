#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

import pyglet
from pyglet.window import key, mouse

import model

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

KEYBOARD_SCROLL = 50 #px

MAX_NUMBER_OF_STARS = 1000

class GameWindow(pyglet.window.Window):
    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)
        self.dragging = False
        self.camera_offset = [0, 0]
        self.zoom = 10
        self.star_coords = []
        self.star_count = 1
        self.randomize_stars()
        self.update_stars()

    def on_key_press(self, symbol, modifiers):
        super(GameWindow, self).on_key_press(symbol, modifiers)
        if symbol == key.F:
            self.set_fullscreen(not self.fullscreen)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            self.dragging = True
            self.camera_offset[0] += dx
            self.camera_offset[1] += dy
            self.update_stars()

    def on_mouse_release(self, x, y, buttons, modifiers):
        if buttons & mouse.LEFT and self.dragging:
            self.dragging = False

    def update_stars(self):
        x_offset = self.camera_offset[0] / 10
        y_offset = self.camera_offset[1] / 10
        verts = []
        for i, vert in enumerate(self.star_coords):
            if i%2:
                new = vert + y_offset * (max(1, ((i-1)/2)%5))
                verts.append(new % self.height)
            else:
                new = vert + x_offset * (max(1, (i/2)%5))
                verts.append(new % self.width)
        self.stars.vertices = verts
        self.on_draw()

    def randomize_stars(self):
        self.star_coords = []
        for i in xrange(self.star_count):
            self.star_coords.append(random.randint(0, self.width))
            self.star_coords.append(random.randint(0, self.height))
        self.stars = pyglet.graphics.vertex_list(len(self.star_coords) / 2,
                                                 ('v2i', tuple(self.star_coords)))
    def on_resize(self, width, height):
        self.star_count = self.width*self.height/1000
        self.star_count = MAX_NUMBER_OF_STARS if self.star_count > MAX_NUMBER_OF_STARS else self.star_count
        self.randomize_stars()
        self.update_stars()
        super(GameWindow, self).on_resize(width, height)


    def on_draw(self):
        self.clear()

        self.stars.draw(pyglet.gl.GL_POINTS)
        ### draw planets
        z = self.zoom
        min_x = -self.camera_offset[0]/z
        min_y = -self.camera_offset[1]/z
        max_x = min_x + (self.width/z)
        max_y = min_y + (self.height/z)
        planets = model.get_planets(min_x, min_y, max_x, max_y)
        pl = []
        for planet in planets:
            p_x = planet.x*z + self.camera_offset[0]
            p_y = planet.y*z + self.camera_offset[1]
            pl.extend([p_x,   p_y,
                       p_x,   p_y+z,
                       p_x+z, p_y+z,
                       p_x+z, p_y])
        if pl:
            planets_v = pyglet.graphics.vertex_list(len(planets)*4,
                                                    ('v2i', tuple(pl)))
            planets_v.draw(pyglet.gl.GL_QUADS)


if __name__ == '__main__':
    window = GameWindow(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, resizable=True)
    pyglet.app.run()
