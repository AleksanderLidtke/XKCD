# -*- coding: utf-8 -*-
"""

:D

I was looking for some work material and came across http://sophia.estec.esa.int/gtoc_portal/?page_id=103
Look at the plot to understand the rest of the story.

Take a look at http://jakevdp.github.io/blog/2013/07/10/XKCD-plots-in-matplotlib/
for some examples.

Created on Tue Apr  7 07:46:47 2015

@author: Alek
"""

import matplotlib.pyplot, numpy
matplotlib.pyplot.xkcd() # :D Maybe I should add this to all my plots.

fig = matplotlib.pyplot.figure(figsize=(12, 8))
ax = fig.add_subplot(211)

ax.set_title("This is swesome!!!* ** ***")
ax.set_xlabel(("Time offest from the moment I discovered matplotlib.pyplot.xkcd()\n"
    "(months)"),size=16)
ax.set_ylabel(("How awesome I think Python\n"
    "is normalised to playing PC games\n"
    "(what are the units of satisfaction?)"),size=16)

ax.set_ylim([-2,100])

timeOffsetValue = numpy.linspace(-60, 5)
satisfaction = ( -1 + 10. / (1 + numpy.exp(0.6 * (-30 - timeOffsetValue))) +
    1000. / (1 + numpy.exp(0.9 * (5 - timeOffsetValue))) )
ax.plot(timeOffsetValue, satisfaction)

ax.annotate('I stopped playing computer games', xy=(-30, 4), xytext=(-55, 20),
	arrowprops=dict(facecolor='black', shrink=0.05))

ax.annotate('A few hours ago', xy=(-1, 13), xytext=(-20, 35),
	arrowprops=dict(facecolor='black', shrink=0.05))

ax.annotate('Still laughing now', xy=(2.5, 90), xytext=(-15, 80),
	arrowprops=dict(facecolor='black', shrink=0.05))

ax.text(-50, -40, "*Can't believe how much time I've spent on this", size=12)
ax.text(-50, -50, "**Funniest thing is I actually make this as accurate as possible", size=12)
ax.text(-50, -60, "***Why do people use Matlab again?", size=12)

ax.text(2, 140, "Will this ever end?", size=10, rotation='vertical', color='blue')

matplotlib.pyplot.subplots_adjust(left=0.1, right=0.95, top=0.8, bottom=0.0)

fig.show()
