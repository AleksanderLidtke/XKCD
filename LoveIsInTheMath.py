# -*- coding: utf-8 -*-
"""

:)

Created on Sun Feb 14 13:02:16 2016

@author: alek
@version: 1.0.0
@since: Sun Feb 14 13:02:16 2016

CHANGELOG:
Sun Feb 14 13:02:16 2016 - 1.0.0 - alek - Issued the first draft version.
"""

import matplotlib.pyplot, numpy
matplotlib.pyplot.xkcd()

t = numpy.linspace(0,2*numpy.pi,500) # Curvilinear coordinates (i.e. along the heart).
x = 16.*numpy.power( numpy.sin(t), 3 )
y1 = 13*numpy.cos(t) - 5.*numpy.cos(2*t) - 2.*numpy.cos(3*t) - numpy.cos(4*t)
y2 = 13*numpy.cos(t) - 5.*numpy.cos(2*t) - 2.*numpy.cos(3*t) # Remove some components, one by one...
y3 = 13*numpy.cos(t) - 5.*numpy.cos(2*t)
y4 = 13*numpy.cos(t)

fig = matplotlib.pyplot.figure(figsize=(12, 8))
ax = fig.gca()
ax.set_aspect("equal")

ax.set_title("What is love? Fourier decomposition")
ax.set_xlabel("X (dimensionless)",size=16)
ax.set_ylabel("Y (dimensionless)",size=16)

ax.set_xlim([-20,20])
ax.set_ylim([-20,20])

ax.plot(x,y1,c='r',lw='4',ls='-')
ax.plot(x,y2,c='0.7',lw='4',ls='--')
ax.plot(x,y3,c='0.5',lw='4',ls='--')
ax.plot(x,y4,c='0.2',lw='4',ls='--')

ax.annotate('It has many components', xy=(0, 13), xytext=(5, 17),
	arrowprops=dict(facecolor='0.5', shrink=0.05))

ax.text(-8, 0, "And you've got them all", size=20, rotation='horizontal', color='red')

matplotlib.pyplot.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1)

fig.show()
