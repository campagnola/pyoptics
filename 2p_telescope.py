# -*- coding: utf-8 -*-
from pyoptic import *
from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.canvas
import numpy as np
from pyqtgraph import Point

app = QtGui.QApplication([])

w = pg.GraphicsWindow()
view = w.addViewBox()

optics = []


view.setAspectLocked()
#view.invertY(False)
#grid = pg.GridItem()
#view.addItem(grid)
#view.setRange(QtCore.QRectF(-50, -100, 500, 400))




optics = []
rays = []

f1 = 50.
f2 = 150.
#f1 = 100.
#f2 = 100.

dtot = (f1+f2)*2
## Solve for d1 (distance from scan mirrors to scan lens)
## if we want the total distance to be 2 * (f1+f2)
if f1 == f2:
    d1 = (f1+f2)*0.5
else:
    d1 = (f1 * (-(f1 + f2)**2 + f1 * dtot)) / ((f1 - f2) * (f1 + f2))


for y in [0, -20, -40, -60]:
    #l1 = Lens(r1=51.5, r2=0, d=3.6, glass='N-BK7') ## 100mm
    if f1 == 50:
        l1 = Lens(r1=23.0, r2=0, d=5.8, pos=(d1, y), glass='Corning7980')  ## 50mm  UVFS  (LA4148)
        l2 = Lens(r1=0, r2=69.0, d=3.2, pos=(d1+f1+f2, y), glass='Corning7980')  ## 150mm UVFS  (LA4874)
    else:
        l1 = Lens(r1=46, r2=0, d=3.8, pos=(d1, y), glass='Corning7980') ## 100mm UVFS  (LA4380)
        l2 = Lens(r1=0, r2=46, d=3.8, pos=(d1+f1+f2, y), glass='Corning7980') ## 100mm UVFS  (LA4380)
    #l1.translate(0, y)
    #l2.translate(200, y)
    optics.append([l1, l2])
    view.addItem(l1)
    view.addItem(l2)
    
allRays = []

## 2V mirror deflection causes 5mm/40mm change in spot pos.
## typical deflections are up to 0.6V
maxAngle = (1.0 / 2.0) * np.arctan(5./40.)

for wl, dy in [(355, 0), (470, -20), (680, -40), (1040, -60)]:
    rays = []
    for a in [-maxAngle, 0, maxAngle]:
        for y in [-1, -0.4, 0, 0.4, 1]:
            for x in [0]:
                ang = a
                r = Ray(start=Point(x - y*np.sin(ang), dy+y*np.cos(ang)), dir=(np.cos(ang), np.sin(ang)), wl=wl)
                rays.append(r)
                view.addItem(r)
    allRays.append(rays)

tracers = []
for i in range(4):
    tracers.append(Tracer(allRays[i], optics[i]))



def shift(x):
    global f1, f2
    d1 = optics[0][0]['pos'][0] + x
    d3 = (- d1 + f1**2/f2 + f1) / (f1**2/f2**2)
    
    for s,t in optics:
        s['pos'] = (d1, s['pos'][1])
        t['pos'] = (d3, s['pos'][1])


import sys
if sys.flags.interactive == 0:
    app.exec_()
