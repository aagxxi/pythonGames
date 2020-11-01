#!/usr/bin/python3 -B
# -*- coding: utf-8 -*-

from pythongame import PythonGame

DEBUG = True

mygame = PythonGame(DEBUG)

while mygame.main_loop():
    mygame.tick_clock()
