# -*- coding: utf-8 -*-
from pyoptic import *
from PyQt4 import QtGui, QtCore
QtCore.Signal = QtCore.pyqtSignal

import pyqtgraph as pg
import pyqtgraph.canvas
import numpy as np
from pyqtgraph import Point

app = QtGui.QApplication([])

w = pg.GraphicsWindow()
view = w.addViewBox()

optics = []


view.setAspectLocked()
#view.aspectLocked = True
#view.invertY(False)
#grid = pg.GridItem()
#view.addItem(grid)
#view.setRange(QtCore.QRectF(200, -100, 500, 400))




## UV focus lenses
uvy = 50
uvl1 = Lens(r1=34.5, r2=0, d=4.4, pos=(0, uvy), glass='Corning7980') ## 75mm UVFS  (LA4725)
uvl2 = Lens(r1=0, r2=34.5, d=4.4, pos=(150,uvy), glass='Corning7980') ## 75mm UVFS  (LA4725) 

## UV mirrors
uvm1 = Mirror(d=0.001, pos=(225, uvy), angle=45)
uvm2 = Mirror(d=0.001, pos=(225, 0), angle=225)


## First system: 50mm scan lens
## IR beam expander
l1 = Lens(r1=23.0, r2=0, d=5.8, glass='Corning7980')  ## 50mm  UVFS  (LA4148)
l2 = Lens(r1=0, r2=69.0, d=3.2, pos=(200,0), glass='Corning7980')  ## 150mm UVFS  (LA4874)

## Scan mirrors
scanx = 250
scany = 10
m1 = Mirror(dia=4.2, d=0.001, pos=(scanx, 0), angle=315)
m2 = Mirror(dia=8.4, d=0.001, pos=(scanx, scany), angle=135)

## Scan lenses
#l3 = Lens(r1=46, r2=0, d=3.8, pos=(scanx+50, scany), glass='Corning7980') ## 100mm UVFS  (LA4380)
#l4 = Lens(r1=0, r2=46, d=3.8, pos=(scanx+250, scany), glass='Corning7980') ## 100mm UVFS  (LA4380)
l3 = Lens(r1=23.0, r2=0, d=5.8, pos=(scanx+50, scany), glass='Corning7980')  ## 50mm  UVFS  (LA4148)
l4 = Lens(r1=0, r2=69.0, d=3.2, pos=(scanx+250, scany), glass='Corning7980')  ## 150mm UVFS  (LA4874)

## Objective
obj = Lens(r1=15, r2=15, d=10, dia=8, pos=(scanx+400, scany), glass='Corning7980')

#IROptics = [l1, l2, m1, m2, l3, l4, obj]
IROptics = [m1, m2, l3, l4, obj]
UVOptics = [uvl1, uvl2, uvm1, uvm2, m1, m2, l3, l4, obj]



#### Second system: 100mm scan lens
## IR beam expander
l1a = Lens(r1=23.0, r2=0, d=5.8, pos=(0, 20), glass='Corning7980')  ## 50mm  UVFS  (LA4148)
l2a = Lens(r1=0, r2=69.0, d=3.2, pos=(200,20), glass='Corning7980')  ## 150mm UVFS  (LA4874)

## Scan mirrors
scanx = 250
scany = 30
m1a = Mirror(dia=4.2, d=0.001, pos=(scanx, 20), angle=315)
m2a = Mirror(dia=8.4, d=0.001, pos=(scanx, scany), angle=135)

## Scan lenses
l3a = Lens(r1=46, r2=0, d=3.8, pos=(scanx+50, scany), glass='Corning7980') ## 100mm UVFS  (LA4380)
l4a = Lens(r1=0, r2=46, d=3.8, pos=(scanx+250, scany), glass='Corning7980') ## 100mm UVFS  (LA4380)

## Objective
obja = Lens(r1=15, r2=15, d=10, dia=8, pos=(scanx+400, scany), glass='Corning7980')

#IROptics2 = [l1a, l2a, m1a, m2a, l3a, l4a, obja]
IROptics2 = [m1a, m2a, l3a, l4a, obja]



UVOptics = []
for o in set(IROptics+UVOptics+IROptics2):
    view.addItem(o)
    
IRRays = []
IRRays2 = []
UVRays = []

for dy in [-0.4, -0.15, 0, 0.15, 0.4]:
    IRRays.append(Ray(start=Point(-50, dy), dir=(1, 0), wl=780))
    IRRays2.append(Ray(start=Point(-50, dy+20), dir=(1, 0), wl=780))
    #UVRays.append(Ray(start=Point(-50, uvy+dy), dir=(1, 0), wl=355))
    
for r in set(IRRays+UVRays+IRRays2):
    view.addItem(r)

#UVTracer = Tracer(UVRays, UVOptics)
IRTracer = Tracer(IRRays, IROptics)
IRTracer2 = Tracer(IRRays2, IROptics2)

phase = 0.0
def update():
    global phase
    if phase % (8*np.pi) > 4*np.pi:
        m1['angle'] = 315 + 1.5*np.sin(phase)
        m1a['angle'] = 315 + 1.5*np.sin(phase)
    else:
        m2['angle'] = 135 + 1.5*np.sin(phase)
        m2a['angle'] = 135 + 1.5*np.sin(phase)
    phase += 0.2
    
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(40)

### 2V mirror deflection causes 5mm/40mm change in spot pos.
### typical deflections are up to 0.6V
#maxAngle = (1.0 / 2.0) * np.arctan(5./40.)

#for wl, dy in [(355, 0), (470, -20), (680, -40), (1040, -60)]:
    #rays = []
    #for a in [-maxAngle, 0, maxAngle]:
        #for y in [-1.25, 0, 1.25]:
            #ang = a
            #r = Ray(start=Point(-50 - y*np.sin(ang), dy+y*np.cos(ang)), dir=(np.cos(ang), np.sin(ang)), wl=wl)
            #rays.append(r)
            #view.addItem(r)
    #allRays.append(rays)

#for i in range(4):
    #trace(allRays[i], optics[i])

