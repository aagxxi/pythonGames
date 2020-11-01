#!/usr/bin/python3 -B
# -*- coding: utf-8 -*-

import pygame


class Drawable(object):

    mygame = None
    maxx = 0
    maxy = 0
    posx = 0
    posy = 0

    def __init__(self, mygame):
        self.mygame = mygame
        self.maxx, self.maxy = mygame.screen_size()
        self.posx = self.maxx // 2
        self.posy = self.maxy // 2

    def set_pos(self, x, y):
        self.posx = x
        self.posy = y

    def tick(self):
        pass

    def draw(self):
        pass


class Target(Drawable):

    def draw(self):
        pygame.draw.line(self.mygame.screen, (255, 255, 255),
                         (0, self.posy), (self.maxx, self.posy), 2)
        pygame.draw.line(self.mygame.screen, (255, 255, 255),
                         (self.posx, 0), (self.posx, self.maxy), 2)


class Ball(Drawable):

    spd = 1
    spdx = 1
    spdy = 1

    def __init__(self, mygame, speed):
        super().__init__(mygame)
        self.spdx = speed
        self.spdy = speed
        self.spd = speed

    def set_pos(self, x, y):
        pass

    def tick(self):
        self.posx = self.posx + self.spdx
        self.posy = self.posy + self.spdy
        if self.posx < 0:
            self.posx = 0
            self.spdx = self.spd
        if self.posx > self.maxx:
            self.posx = self.maxx
            self.spdx = -self.spd
        if self.posy < 0:
            self.posy = 0
            self.spdy = self.spd
        if self.posy > self.maxy:
            self.posy = self.maxy
            self.spdy = -self.spd

    def draw(self):
        pygame.draw.circle(self.mygame.screen, (255, 255, 255),
                           (self.posx, self.posy), 3)
