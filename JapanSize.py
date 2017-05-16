# -*- coding: utf-8 -*-
"""
Throughout my travels I've discovered that most people, including myself, do not
realise many things about our Planet's size. For example, the latitude and
longitude of certain regions (South America is much further east than the US)
or the relative size of countries (Japan is surprisingly long).

Thus, I've created this script to understand such things a bit better. It
compares the sizes of Japan and Europe, which is the most recent surprise
I came across.

The shape data were aquired from [Global Administrative Areas](http://www.gadm.org/country)
website. Thus, their **redistribution, or commercial use is not allowed without
prior permission**.


Created on Sun May 7 14:13:47 2017

@author: Alek
"""
from mpl_toolkits.basemap import Basemap
import numpy, shapefile, os, matplotlib.pyplot

matplotlib.pyplot.xkcd() # Here we go.

def plotPrefecture(*,shp,colour,bMap,axes,latOff=0,longOff=0,lwdth=0.5):
    """ Plot a prefecture from a shapefile.
    
    Kwargs
    -------
    * shp - shape as returned by :func:`shapefile.Reader.shapes`,
    * colour - colour accepted by :func:`matplotlib.pyplot.Axes.plot',
    * bMap - instance of :class:`mpl_toolkits.basemap.Basemap` used to project
      the shape onto a map,
    * axes - :class:`matplotlib.pyplot.Axes` instance where to plot,
    * latOff,longOff - deg, by how much to offset the `shp` lattitudes and
      longitudes before plotting,
    * lwdth - line width as accepted by :func:`matplotlib.pyplot.Axes.plot'.
    """
    if len(shp.parts)==1: # Only one region in this shape.
        vertices=numpy.array(shp.points)
        bMap.plot(vertices[:,0]+longOff,vertices[:,1]+latOff,color=colour,
                  lw=lwdth,ls='-',latlon=True,ax=axes)
    else: # This shape has islands, disjoint regions and what-not.
        for ip in range(len(shp.parts)): # For every part of the shape.
            # Indices that get the slice with this part of the shape.
            lower=shp.parts[ip]
            if ip==len(shp.parts)-1:
                upper=len(shp.points) # Last part.
            else:
                upper=shp.parts[ip+1] # Next part starts at idx parts[ip+1]
            partVertices=numpy.array(shp.points[lower:upper])
            bMap.plot(partVertices[:,0]+longOff,partVertices[:,1]+latOff,
                      color=colour,lw=lwdth,ls='-',latlon=True,ax=axes)

# Various font sizes.
ticksFontSize=18
labelsFontSizeSmall=20
labelsFontSize=30
titleFontSize=34
legendFontSize=20
matplotlib.rc('xtick',labelsize=ticksFontSize) 
matplotlib.rc('ytick',labelsize=ticksFontSize)
cm=matplotlib.pyplot.cm.get_cmap('viridis')

# Read a shapefile with Japan's cartography data.
shapeRdr0=shapefile.Reader(os.path.join('borders','JPN_adm0')) # Country.
shapeRdr1=shapefile.Reader(os.path.join('borders','JPN_adm1')) # Prefectures.
shapeRdr2=shapefile.Reader(os.path.join('borders','JPN_adm2')) # Towns.
shape=shapeRdr0.shapes()[0]
if shape.shapeType != shapefile.POLYGON:
    raise ValueError('Shape not polygon with shapeType={}'.format(shape.shapeType ))

vertices=numpy.array(shape.points) # 2D array of coordinates.

# Where to centre different maps and where to translate Japan to.
latJpn=37 # Where to centre one map, i.e. over Japan. Lat/lon in degrees.
lonJpn=138
latCtr=40 # Where to centre the Europe's map. Lat/lon in degrees.
lonCtr=10
dLonJ=10 # Plot Japan at these coordinates over the map of Europe.
dLatJ=50

' Mercator projection, a.k.a. "the things you learn in schools".'
fig,ax=matplotlib.pyplot.subplots(1,2,figsize=(16,8))

# The whole Planet.
mercMapP=Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,
                urcrnrlon=180,lat_ts=10,ax=ax[0],resolution='c')
mercMapP.drawcoastlines(linewidth=0.5)
mercMapP.drawcountries(linewidth=0.25)
mercMapP.drawparallels(numpy.arange(-90.,91.,30.))
mercMapP.drawmeridians(numpy.arange(-180.,181.,60.))
ax[0].set_title(r'$Our\ Planet$',fontsize=titleFontSize)
plotPrefecture(shp=shape,colour='gold',lwdth=1,bMap=mercMapP,axes=ax[0])

# Only Europe.
mercMapE=Basemap(projection='merc',llcrnrlat=30,urcrnrlat=75,llcrnrlon=-25,
                urcrnrlon=40,lat_ts=10,ax=ax[1],resolution='l')
mercMapE.drawcoastlines(linewidth=0.5)
mercMapE.drawcountries(linewidth=0.25)
mercMapE.drawparallels(numpy.arange(mercMapE.latmin,mercMapE.latmax,10.))
mercMapE.drawmeridians(numpy.arange(mercMapE.lonmin,mercMapE.lonmax,15.))
ax[1].set_title(r'$Europe$',fontsize=titleFontSize)
plotPrefecture(shp=shape,colour='gold',lwdth=2,bMap=mercMapE,axes=ax[1],
               latOff=dLatJ-latJpn,longOff=dLonJ-lonJpn)

fig.show()

' One figure with orthonormal maps centred on Japan and Europe.'
fig,ax=matplotlib.pyplot.subplots(1,2,figsize=(16,8))

# Centred on Japan.
ortnMapJ=Basemap(projection='ortho',lat_0=latJpn,lon_0=lonJpn,resolution='c',
                 ax=ax[0])
ortnMapJ.drawcoastlines(linewidth=0.5)
ortnMapJ.drawcountries(linewidth=0.25)
ortnMapJ.drawmeridians(numpy.arange(0,360,30))
ortnMapJ.drawparallels(numpy.arange(-90,90,30))
ax[0].set_title(r'${}$'.format(shapeRdr0.records()[0][4]),fontsize=titleFontSize)
plotPrefecture(shp=shape,colour='gold',lwdth=2,bMap=ortnMapJ,axes=ax[0])

# Plot all the prefectures.
cNorm=matplotlib.colors.Normalize(vmin=0,vmax=shapeRdr1.numRecords)
scalarMap=matplotlib.cm.ScalarMappable(norm=cNorm,cmap=cm)
prefectures=shapeRdr1.shapes()
prefRecords=shapeRdr1.records()
for i in range(shapeRdr1.numRecords):
    if prefRecords[i][9]=='Prefecture':
        plotPrefecture(shp=prefectures[i],colour=scalarMap.to_rgba(i),
                       lwdth=0.5,bMap=ortnMapJ,axes=ax[0])

# Centred on Europe.
ortnMapE=Basemap(projection='ortho',lat_0=latCtr,lon_0=lonCtr,resolution='c',
                 ax=ax[1])
ortnMapE.drawcoastlines(linewidth=0.5)
ortnMapE.drawcountries(linewidth=0.25)
ortnMapE.drawmeridians(numpy.arange(0,360,30))
ortnMapE.drawparallels(numpy.arange(-90,90,30))
ax[1].set_title(r'${}\ over\ Europe$'.format(shapeRdr0.records()[0][4]),
    fontsize=titleFontSize)
plotPrefecture(shp=shape,colour='gold',lwdth=2,bMap=ortnMapE,axes=ax[1],
               latOff=dLatJ-latJpn,longOff=dLonJ-lonJpn)

fig.show()
