#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Lately, I've been playing with the  World Population Prospects data that
are available on the [UN website](https://esa.un.org/unpd/wpp/Download/Standard/Population/).
I decided to check when I'll be older than half of the people on the planet,
which might be considered as one boundary of getting old.
"""
import pandas, numpy, matplotlib.pyplot, matplotlib.ticker, scipy.interpolate

# Script controls.
FNAME='WPP2015_POP_F05_MEDIAN_AGE.XLS' # What file to read the UN data from.

# Various font sizes.
ticksFontSize=18
labelsFontSizeSmall=20
labelsFontSize=30
titleFontSize=34
legendFontSize=20
matplotlib.rc('xtick',labelsize=ticksFontSize) 
matplotlib.rc('ytick',labelsize=ticksFontSize)

matplotlib.pyplot.xkcd()

def extractUNData(datFrm,countryCode):
    """ Extract UN Population Outlook data for a country from a dataframe.
    
    Get both historical or forecast data from the given sheet in the data file
    from the [UN website](https://esa.un.org/unpd/wpp/Download/Standard/Population/).
    Different data sets are located in different sheets of the Excel workbooks,
    so they can be selected by changing the sheet name. Countries are selected
    using the country codes.
    
    Args
    --------
    * dataFrm (:class:`pandas.Dataframe`): dataframe with country codes and
      UN prognoses. See :func:`getUNData` to see how to read the `dataFrm`
      from an Excel workbook as avaialble from the UN website.
    * countryCode (int): the code of the country for which to reac the data.
    
    Returns
    --------
    2-tuple of numpy.ndarrays with population data in the original units and
    the corresponding years. Shapes are (N,).
    """
    # Not generic! But works for the UN World Outlook 2015 data.
    countryData=datFrm[datFrm['Country code']==countryCode]
    x=numpy.array(countryData[datFrm.columns[1:]],dtype=float).reshape(-1,)
    t=numpy.array(datFrm.columns[1:].tolist(),dtype=float)
    return x,t

def getUNData(fName,sheetName,countryCode,trimYear=None):
    """ Get UN Population Outlook data for a given country.
    
    Get both historical or forecast data from the given sheet in the data file
    from the [UN website](https://esa.un.org/unpd/wpp/Download/Standard/Population/).
    Different data sets are located in different sheets of the Excel workbooks,
    so they can be selected by changing the sheet name. Countries are selected
    using the country codes.
    
    Can also choose to return only a subset of the data older than a given year
    by specifying `trimYear`.
    
    Args
    --------
    * fName: string or file-like object accepted by :func:`pandas.read_excel`
      from which the data will be read.
    * sheetName: string with the sheet name in `fName` workbook or an int.
      Defines the UN prognosis to be read.
    * countryCode (int): the code of the country for which to reac the data.
    * trimYear (int): whether to return only data older than a given year.
    
    Returns
    --------
    2-tuple of numpy.ndarrays with population data in the original units and
    the corresponding years. Shapes are (N,).
    """
    # Not generic! But works for the UN World Outlook 2015 data.
    df=pandas.read_excel(fName,sheetname=sheetName,header=0,skiprows=16)
    # Could use parse_cols in read_excel to ignore the unwanted columns, but
    # then it'd be tricky not to risk unintentionally trimming the data by
    # selecting only some of the columns. So read everything and drop what we
    # don't need.
    df.drop('Index',axis=1,inplace=True)
    df.drop('Variant',axis=1,inplace=True)
    df.drop('Major area, region, country or area *',axis=1,inplace=True)
    df.drop('Notes',axis=1,inplace=True)
    x,t=extractUNData(df,countryCode)
    if not trimYear is None: # Trim the data by year.
        return x[t<=trimYear],t[t<=trimYear]
    else: # No trimming, return everything.
        return x,t

# Analyse combined historical and predicted data for the whole world.
xHistory,tHistory=getUNData(FNAME,'ESTIMATES',900,trimYear=2200)
xLow,tLow=getUNData(FNAME,'LOW VARIANT',900,trimYear=2200)
xHigh,tHigh=getUNData(FNAME,'HIGH VARIANT',900,trimYear=2200)
xMedium,tMedium=getUNData(FNAME,'MEDIUM VARIANT',900,trimYear=2200)

# Interpolate the predictions close to the region of itnerest.
fLow=scipy.interpolate.interp1d(tLow,xLow)
fHigh=scipy.interpolate.interp1d(tHigh,xHigh)
fMedium=scipy.interpolate.interp1d(tMedium,xMedium)
tInterp=numpy.linspace(2015,2040,25)
xLowInterp=fLow(tInterp)
xHighInterp=fHigh(tInterp)
xMediumInterp=fMedium(tInterp)

# Plot the historical data.
fig,ax=matplotlib.pyplot.subplots(1,1,figsize=(14,8))
ax.scatter(tHistory,xHistory,c='indigo',marker='o',s=50,
           label=r'$Historical\ estimates$')

# Plot the age and predictions interpolated close to the cross-over.
ax.plot(tInterp,xLowInterp,ls='-',c='deepskyblue',lw=2.,
        label=r'$UN\ low\ variant\ forecast$')
ax.plot(tInterp,xHighInterp,ls='-',c='crimson',lw=2.,
        label=r'$UN\ high\ variant\ forecast$')
ax.plot(tInterp,xMediumInterp,ls='-',c='gold',lw=2.,
        label=r'$UN\ medium\ variant\ forecast$')
ax.plot([1990,2040],[0,50],ls='--',c='k',lw=3.,label=r'$My\ approx.\ age$')

# Zoom to the area of interest.
ax.set_xlim(1990,2040)
ax.set_ylim(bottom=0)
minorLocator=matplotlib.ticker.MultipleLocator(1)
ax.xaxis.set_minor_locator(minorLocator)

# Misc. formatting.
ax.set_axisbelow(True)
ax.set_xlabel(r'$Year$',fontsize=labelsFontSize)
ax.set_ylabel(r'$Median\ age$',fontsize=labelsFontSize)
matplotlib.pyplot.subplots_adjust(left=0.1,right=0.95,bottom=0.15,top=0.84)
ax.grid(linewidth=1,linestyle=':',which='major')
ax.grid(linewidth=0.1,linestyle='--',which='minor')
ax.legend(bbox_to_anchor=(0.5,1.23),loc='upper center',
          prop={'size':legendFontSize},fancybox=True,shadow=True,ncol=3)
ax.tick_params(axis='both',reset=False,which='both',length=5,width=1.5)
fig.show()