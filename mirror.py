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
view.show()
optics = []


#view.enableMouse()
view.setAspectLocked()
#view.invertY(False)
grid = pg.GridItem()
view.addItem(grid)
view.setRange(QtCore.QRectF(-150, 200, 500, 400))

optics = []
rays = []
m1 = Mirror(r1=-100, pos=(5,0), angle=-15)
optics.append(m1)
m2 = Mirror(r1=-100, pos=(-40, 30), angle=180-15)
optics.append(m2)

allRays = []
for y in np.linspace(-10, 10, 21):
    r = Ray(start=Point(-100, y))
    view.addItem(r)
    allRays.append(r)

for o in optics:
    view.addItem(o)
    
view.autoRange()

t = Tracer(allRays, optics)

import sys
if sys.flags.interactive == 0:
    app.exec_()