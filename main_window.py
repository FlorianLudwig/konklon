#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

import pyglet
from pyglet.window import key, mouse

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

KEYBOARD_SCROLL = 50 #px

NUMBER_OF_STARS = 1000

class GameWindow(pyglet.window.Window):
    def __init__(self, **kwargs):
        super(GameWindow, self).__init__(**kwargs)
        self.star_coords = []
        #for i in xrange(NUMBER_OF_STARS):
        #    self.star_coords.append(random.randint(0, self.width))
        #    self.star_coords.append(random.randint(0, self.height))
        self.randomize_stars()
        self.stars = pyglet.graphics.vertex_list(len(self.star_coords) / 2,
                                                 ('v2i', tuple(self.star_coords)))
        self.dragging = False
        self.camera_offset = [0, 0]
        self.zoom = 0

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            self.dragging = True
            self.camera_offset[0] += dx
            self.camera_offset[1] += dy

    def on_mouse_release(self, x, y, buttons, modifiers):
        if buttons & mouse.LEFT and self.dragging:
            self.dragging = False
            self.update_stars()
                       
    def update_stars(self):
        x_offset = self.camera_offset[0] / 10
        y_offset = self.camera_offset[1] / 10
        verts = []
        x = True
        for vert in self.star_coords:
            if x:
                new = vert + x_offset
                verts.append(new if new <= self.width else new - self.width)
            else:
                new = vert + y_offset
                verts.append(new if new <= self.height else new - self.height)
            x = not x
        self.stars.vertices = verts
        self.on_draw()

    def randomize_stars(self):
        self.star_coords = []
        for i in xrange(NUMBER_OF_STARS):
            self.star_coords.append(random.randint(0, self.height))
            self.star_coords.append(random.randint(0, self.width))
            
    def on_resize(self, width, height):
        self.randomize_stars()
        super(GameWindow, self).on_resize(width, height)

    def on_key_press(self, symbol, modifiers):
        super(GameWindow, self).on_key_press(symbol, modifiers)

    def on_draw(self):
        self.clear()
        self.stars.draw(pyglet.gl.GL_POINTS)

if __name__ == '__main__':
    window = GameWindow(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, resizable=True)
    pyglet.app.run()
