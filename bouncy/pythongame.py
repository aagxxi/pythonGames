#!/usr/bin/python3 -B
# -*- coding: utf-8 -*-

import pygame

from drawables import Target, Ball


class PythonGame(object):

    clock = None
    screen = None
    debug = False

    def __init__(self, debug=False):
        # init pygame object
        # super().__init__()

        if self.debug:
            print("PythonGame.__init__")

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption('Bouncy')
#        icon = pygame.image.load('controller-pad.png')
#        pygame.display.set_icon(icon)
#        self.font64 = pygame.font.Font('freesansbold.ttf', 64)
#        self.font84 = pygame.font.Font('freesansbold.ttf', 84)
#        self.errorimage = pygame.image.load('error-256.png')
#        self.winimage = pygame.image.load('win-256.png')
        self.debug = debug

        self.objects = []
        self.objects.append(Target(self))
        self.objects.append(Ball(self, 2))

    def __del__(self):
        if self.debug:
            print("PythonGame.__del__")
        pygame.quit()

    def debug(self):
        return self.debug

    def screen_size(self):
        return self.screen.get_size()

    def main_loop(self):
        running = True

        for event in pygame.event.get():
            if self.debug:
                print("event = {}".format(event))
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                for obj in self.objects:
                    obj.set_pos(x, y)

        self.screen.fill((50, 50, 50))
        for obj in self.objects:
            obj.tick()
            obj.draw()
        pygame.display.update()

        return running

    def tick_clock(self):
        self.clock.tick(240)
