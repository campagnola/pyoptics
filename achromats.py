# -*- coding: utf-8 -*-
from pyoptic import *
from PyQt4 import QtGui, QtCore
QtCore.Signal = QtCore.pyqtSignal

import pyqtgraph as pg
import numpy as np
from pyqtgraph import Point

app = QtGui.QApplication([])

w = pg.GraphicsWindow()
view = w.addViewBox()

optics = []


view.setAspectLocked()
grid = pg.GridItem()
view.addItem(grid)
#view.setRange(QtCore.QRectF(-150, 200, 500, 400))




optics = []
rays = []

for y in [0, -20, -40, -60]:
    l1 = Lens(r1=51.5, r2=0, d=3.6, glass='N-BK7')
    l2 = Lens(r1=0, r2=51.5, d=3.6, glass='N-BK7')
    l1.translate(0, y)
    l2.translate(200, y)
    optics.append([l1, l2])
    view.addItem(l1)
    view.addItem(l2)
    
allRays = []
for wl, dy in [(355, 0), (470, -20), (680, -40), (1040, -60)]:
    rays = []
    for a in [-2, 0, 2]:
        for y in [-0.5, -0.2, 0, 0.2, 0.5]:
            ang = a*np.pi/180.
            r = Ray(start=Point(-100 - y*np.sin(ang), dy+y*np.cos(ang)), dir=(np.cos(ang), np.sin(ang)), wl=wl)
            rays.append(r)
            view.addItem(r)
    allRays.append(rays)

for i in range(4):
    trace(allRays[i], optics[i])

