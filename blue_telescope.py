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
#view.invertY(False)
grid = pg.GridItem()
view.addItem(grid)
view.setRange(QtCore.QRectF(-150, -200, 500, 400))


l1 = Lens(r1=38.6, r2=0, d=4.1, glass='N-BK7')  ## 75mm
l2 = Lens(r1=0, r2=38.6, d=4.1, glass='N-BK7')  ## 75mm
l1.translate(0, 0)
l2.translate(200, 0)
view.addItem(l1)
view.addItem(l2)
    
## 2V mirror deflection causes 5mm/40mm change in spot pos.
## typical deflections are up to 0.6V
maxAngle = (1.0 / 2.0) * np.arctan(5./40.)

wl = 470
dy = 0
rays = []
for a in [-maxAngle, 0, maxAngle]:
    for y in [-1.25, 0, 1.25]:
        ang = a
        r = Ray(start=Point(-50 - y*np.sin(ang), dy+y*np.cos(ang)), dir=(np.cos(ang), np.sin(ang)), wl=wl)
        rays.append(r)
        view.addItem(r)

t = Tracer(rays, [l1, l2])
#trace(rays, [l1, l2])

