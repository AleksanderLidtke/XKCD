# -*- coding: utf-8 -*-
"""

With special dedication to my favourite anarchist ;) Also, thanks to my friend
Sophia for the inspiration.

Created on Sun Apr 10 14:47:16 2016

@author: alek
@version: 1.0.0
@since: Sun Apr 10 14:47:16 2016

CHANGELOG:
Sun Apr 10 13:02:16 2016 - 1.0.0 - alek - Issued the first draft version.
"""

import matplotlib.pyplot, numpy
matplotlib.pyplot.xkcd()

x = numpy.linspace(-2,2,40) # X coordinates of the lines.
y1 = 0.1*x + 1 # Horizontal line.
y2 = 4*x - 0.5 # Rising edge of the A
y3 = -4*x + 6 # Falling edge of the A

t = numpy.linspace(0,2*numpy.pi,500) # Curvilinear coordinates around the circle around A
radius = 2
xc = radius*numpy.cos(t)+1 # Circle's Xes.
yc = radius*numpy.sin(t)+1.2 # And Ys.

fig = matplotlib.pyplot.figure(figsize=(12, 8))
ax = fig.gca()
ax.set_aspect("equal")

ax.set_title("Because I draw my lines the way I want!")
ax.set_xlabel("X (dimensionless)",size=16)
ax.set_ylabel("Y (dimensionless)",size=16)

ax.set_xlim([-5,5])
ax.set_ylim([-5,5])

ax.plot(x,y1,c='k',lw='4',ls='-')
ax.plot(x,y2,c='k',lw='4',ls='-')
ax.plot(x,y3,c='k',lw='4',ls='-')
ax.plot(xc,yc,c='k',lw='4',ls='-')

ax.annotate('Misalignments intentional', xy=(2, 1.2), xytext=(3, -1.5),
	arrowprops=dict(facecolor='0.5', shrink=0.05))

matplotlib.pyplot.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1)

fig.show()
