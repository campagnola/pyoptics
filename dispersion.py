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
w.show()

optics = []


view.setAspectLocked()
grid = pg.GridItem()
view.addItem(grid)
view.setRange(QtCore.QRectF(-10, -50, 90, 60))

optics = []
rays = []
#l1 = Lens(r1=0, r2=0, d=10)
l1 = Lens(r1=20, r2=20, d=10, angle=12, glass='Corning7980')
optics.append(l1)
#l1.rotate(45)
#l1.translate(5,0)


allRays = []
for wl in np.linspace(355,1040, 25):
    for y in [10]:
        r = Ray(start=Point(-100, y), wl=wl)
        view.addItem(r)
        allRays.append(r)

for o in optics:
    view.addItem(o)

t = Tracer(allRays, optics)

