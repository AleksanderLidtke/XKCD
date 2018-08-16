#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" My previous project seemed more or less impossible from the outset. I knew
that we had to do the best it gets to stand a chance of delivering it. I normally
read a lot about productivity, team work, leadership and the like. By chance, I'd
read of Slack, the communication tool a few weeks before joining that project.
So we gave it a shot. And it worked. Slack, the app that puts rovers on other
planets (or satellites in low-Earth orbit).
"""
import pandas, numpy, matplotlib.pyplot, matplotlib.ticker

# Various font sizes.
ticksFontSize=18
labelsFontSizeSmall=20
labelsFontSize=30
titleFontSize=34
legendFontSize=20
matplotlib.rc('xtick',labelsize=ticksFontSize) 
matplotlib.rc('ytick',labelsize=ticksFontSize)

matplotlib.pyplot.xkcd() # C'est le shit.

SAVEFIG=True # Automatically save figures to CWD?

# Read the data from the message, channel and user statistics files.
dfMsg=pandas.read_csv('SlackAnalytics03Aug2018.csv',sep=',',header=0,
                      # First column (date) should be the index to enable resampling.
                      index_col=0,
                      # Interpret column 0 as dates, which it is.
                      parse_dates=[0],infer_datetime_format=True)
dfMsg1WkSum=dfMsg.resample('1W').sum() # Weekly sum of messages.

dfCh =pandas.read_csv('ChannelAnalytics03Aug2018.csv',sep=',',header=0,index_col=1,
	parse_dates=[1],infer_datetime_format=True)
dfUsr=pandas.read_csv('UserAnalytics03Aug2018.csv',sep=',',header=0,index_col=0,
	parse_dates=[2],infer_datetime_format=True)

# Plot the message data.
public=dfMsg1WkSum['Messages in Public Channels']
private=dfMsg1WkSum['Messages in Private Channels']
direct=dfMsg1WkSum['Messages in DMs']

fig,ax=matplotlib.pyplot.subplots(1,1,figsize=(14,8))
ax.plot(dfMsg1WkSum.index,public,c='indigo',
	ls='-',lw=3,marker=None,label=r'$Public\ channel$')
ax.plot(dfMsg1WkSum.index,private,c='deepskyblue',
	ls='-',lw=3,marker=None,label=r'$Private\ channel$')
ax.plot(dfMsg1WkSum.index,direct,c='crimson',
	ls='-',lw=3,marker=None,label=r'$Direct\ messages$')
ax.set_axisbelow(True)
ax.set_xlabel(r'$Date\ (JST)$',fontsize=labelsFontSize)
ax.set_ylabel(r'$Weekly\ messages$',fontsize=labelsFontSize)
matplotlib.pyplot.subplots_adjust(left=0.1,right=0.95,bottom=0.15,top=0.84)
ax.legend(bbox_to_anchor=(0.5,1.23),loc='upper center',
          prop={'size':legendFontSize},fancybox=True,shadow=True,ncol=3)
ax.grid(linewidth=1,linestyle=':',which='major')
ax.grid(linewidth=0.1,linestyle='--',which='minor')
ax.tick_params(axis='both',reset=False,which='both',length=5,width=1.5)
ax.annotate(r'$FM\ AIT$',size=ticksFontSize,xy=('2018-7-7',875),
            xytext=('2018-3-1',800),arrowprops=dict(facecolor='black',shrink=0.05))
ax.annotate(r'$Bounenkai$',size=ticksFontSize,xy=('2018-1-4',70),
            xytext=('2017-10-1',500),arrowprops=dict(facecolor='black',shrink=0.05))
ax.annotate(r'$CDR$',size=ticksFontSize,xy=('2018-5-20',510),
            xytext=('2018-1-1',600),arrowprops=dict(facecolor='black',shrink=0.05))
ax.annotate(r'$Summer\ ends$',size=ticksFontSize,xy=('2017-10-28',210),
            xytext=('2017-6-1',400),arrowprops=dict(facecolor='black',shrink=0.05))
ax.annotate(r'$PDR$',size=ticksFontSize,xy=('2017-8-8',170),
            xytext=('2017-4-1',300),arrowprops=dict(facecolor='black',shrink=0.05))
fig.autofmt_xdate()
fig.show()
if SAVEFIG: fig.savefig('globalMessageHistory.png')

# Plot the user data. File data aren't so interesting.
fig,ax=matplotlib.pyplot.subplots(1,1,figsize=(14,8))
# Plot files uploaded per week - filr data (users as well) are too noisy to be
# interpreted on the time scale of days.
#ax.plot(dfMsg1WkSum.index,dfMsg1WkSum['Files Uploaded'],c='indigo',
#	ls='-',lw=3,marker=None,label=r'$Files\ uploaded$')
# Have weekly user data from Slack, so plot that w/o resampling.
ax.plot(dfMsg.index,dfMsg['Full Members'],c='deepskyblue',
	ls='-',lw=3,marker=None,label=r'$Registered$')
ax.plot(dfMsg.index,dfMsg['Weekly Active Users'],c='crimson',
	ls='-',lw=3,marker=None,label=r'$Active$')
ax.plot(dfMsg.index,dfMsg['Weekly Users Posting Messages'],c='gold',
	ls='-',lw=3,marker=None,label=r'$Posting$')
ax.set_axisbelow(True)
ax.set_xlabel(r'$Date\ (JST)$',fontsize=labelsFontSize)
ax.set_ylabel(r'$Weekly\ users$',fontsize=labelsFontSize)
matplotlib.pyplot.subplots_adjust(left=0.1,right=0.95,bottom=0.15,top=0.83)
ax.legend(bbox_to_anchor=(0.5,1.23),loc='upper center',
          prop={'size':legendFontSize},fancybox=True,shadow=True,ncol=3)
ax.grid(linewidth=1,linestyle=':',which='major')
ax.grid(linewidth=0.1,linestyle='--',which='minor')
ax.tick_params(axis='both',reset=False,which='both',length=5,width=1.5)
ax.set_ylim(bottom=-20)
ax.annotate(r'$Bounenkai$',size=ticksFontSize,xy=('2018-1-4',2),
            xytext=('2018-3-1',-10),arrowprops=dict(facecolor='black',shrink=0.05))
ax.annotate(r'$Obon$',size=ticksFontSize,xy=('2017-8-19',0),
            xytext=('2017-6-1',-15),arrowprops=dict(facecolor='black',shrink=0.05))
fig.autofmt_xdate()
fig.show()
if SAVEFIG: fig.savefig('userNumberHistory.png')

# Plot the inactive user numbers.
registered=dfMsg['Full Members']
active=dfMsg['Weekly Active Users']
posting=dfMsg['Weekly Users Posting Messages']
lower=min(registered.min(),active.min(),posting.min())
# Will only subtract, so won't exceed the original no. users in any series.
upper=min(registered.max(),active.max(),posting.max())

fig,ax=matplotlib.pyplot.subplots(1,1,figsize=(14,8))
ax.plot(dfMsg.index,registered-active,c='deepskyblue',
	ls='-',lw=3,marker=None,label=r'$Inactive$')
ax.plot(dfMsg.index,active-posting,c='crimson',
	ls='-',lw=3,marker=None,label=r'$Active\ not\ posting$')
ax.set_axisbelow(True)
ax.set_xlabel(r'$Date\ (JST)$',fontsize=labelsFontSize)
ax.set_ylabel(r'$Weekly\ users$',fontsize=labelsFontSize)
matplotlib.pyplot.subplots_adjust(left=0.1,right=0.95,bottom=0.15,top=0.84)
ax.legend(bbox_to_anchor=(0.5,1.23),loc='upper center',
          prop={'size':legendFontSize},fancybox=True,shadow=True,ncol=2)
ax.grid(linewidth=1,linestyle=':',which='major')
ax.grid(linewidth=0.1,linestyle='--',which='minor')
ax.tick_params(axis='both',reset=False,which='both',length=5,width=1.5)
ax.set_yticks(numpy.arange(numpy.floor(lower),numpy.ceil(upper),5))
ax.annotate(r'$Bounenkai$',size=ticksFontSize,xy=('2018-1-4',16),
            xytext=('2018-3-1',17),arrowprops=dict(facecolor='black',shrink=0.05))
ax.annotate(r'$Obon$',size=ticksFontSize,xy=('2017-8-19',17),
            xytext=('2017-6-1',15),arrowprops=dict(facecolor='black',shrink=0.05))
fig.autofmt_xdate()
fig.show()
if SAVEFIG: fig.savefig('activeSilentUserNumberHistory.png')

# Plot ratio of active and inactive users.
fig,ax=matplotlib.pyplot.subplots(1,1,figsize=(14,8))
ax.plot(dfMsg.index,(registered-active)/registered,c='deepskyblue',
	ls='-',lw=3,marker=None,label=r'$Inactive$')
ax.plot(dfMsg.index,(active-posting)/registered,c='crimson',
	ls='-',lw=3,marker=None,label=r'$Active\ not\ posting$')
ax.set_axisbelow(True)
ax.set_xlabel(r'$Date\ (JST)$',fontsize=labelsFontSize)
ax.set_ylabel(r'$Weekly\ user\ ratio$',fontsize=labelsFontSize)
matplotlib.pyplot.subplots_adjust(left=0.1,right=0.95,bottom=0.15,top=0.84)
ax.legend(bbox_to_anchor=(0.5,1.23),loc='upper center',
          prop={'size':legendFontSize},fancybox=True,shadow=True,ncol=2)
ax.grid(linewidth=1,linestyle=':',which='major')
ax.grid(linewidth=0.1,linestyle='--',which='minor')
ax.tick_params(axis='both',reset=False,which='both',length=5,width=1.5)
ax.annotate(r'$Bounenkai$',size=ticksFontSize,xy=('2018-1-4',0.67),
            xytext=('2018-3-1',0.8),arrowprops=dict(facecolor='black',shrink=0.05))
ax.annotate(r'$Obon$',size=ticksFontSize,xy=('2017-8-19',0.85),
            xytext=('2017-6-1',0.95),arrowprops=dict(facecolor='black',shrink=0.05))
ax.set_ylim(bottom=-0.1,top=1.1)
fig.autofmt_xdate()
fig.show()
if SAVEFIG: fig.savefig('activeSilentUserRatioHistory.png')

# Plot channel users & messages VS age (datetime.now()-date created)
fig,ax=matplotlib.pyplot.subplots(1,1,figsize=(14,8))
ax.plot( (pandas.Timestamp(2018,8,15)-dfCh.index).days, # Channel age.
           dfCh['Messages Posted'],c='indigo',lw=0,marker='o',ms=10)
ax.set_axisbelow(True)
ax.set_xlabel(r'$Channel\ age\ (days)$',fontsize=labelsFontSize)
ax.set_ylabel(r'$Messages\ posted$',fontsize=labelsFontSize)
matplotlib.pyplot.subplots_adjust(left=0.1,right=0.95,bottom=0.15,top=0.84)
ax.grid(linewidth=1,linestyle=':',which='major')
ax.grid(linewidth=0.1,linestyle='--',which='minor')
ax.tick_params(axis='both',reset=False,which='both',length=5,width=1.5)
ax.annotate(r'$random\ =\ we\ are\ to\ the\ point$',size=ticksFontSize,xy=(555,65),
            xytext=(250,200),arrowprops=dict(facecolor='black',shrink=0.05))
fig.show()
if SAVEFIG: fig.savefig('channelPopularityVSAge.png')

# User age VS activity. Don't blame anyone.
userAges=(pandas.Timestamp(2018,8,15)-dfUsr['Account Creation Date']).values/(1e9*24*3600)

fig,ax=matplotlib.pyplot.subplots(1,1,figsize=(14,8))
ax.plot(userAges,dfUsr['chats_sent'],c='indigo',lw=0,marker='o',ms=10,label=r'$User$')
ax.plot([userAges.min(),userAges.max()],
        [dfUsr['chats_sent'].mean(),dfUsr['chats_sent'].mean()],ls='--',lw=2,
        c='deepskyblue',label=r"$Mean$")
ax.plot([userAges.min(),userAges.max()],
        [dfUsr['chats_sent'].median(),dfUsr['chats_sent'].median()],ls='--',lw=2,
        c='crimson',label=r"$Median$")
ax.set_axisbelow(True)
ax.set_xlabel(r'$User\ age\ (days)$',fontsize=labelsFontSize)
ax.set_ylabel(r'$Chats\ sent$',fontsize=labelsFontSize)
matplotlib.pyplot.subplots_adjust(left=0.1,right=0.95,bottom=0.15,top=0.84)
ax.legend(bbox_to_anchor=(0.5,1.23),loc='upper center',
          prop={'size':legendFontSize},fancybox=True,shadow=True,ncol=3)
ax.grid(linewidth=1,linestyle=':',which='major')
ax.grid(linewidth=0.1,linestyle='--',which='minor')
ax.tick_params(axis='both',reset=False,which='both',length=5,width=1.5)
ax.text(x=100,y=550,s=r'${0:.2f}$'.format(dfUsr['chats_sent'].mean()),
        color='deepskyblue',size=ticksFontSize)
ax.text(x=100,y=250,s=r'${0:.2f}$'.format(dfUsr['chats_sent'].median()),
        color='crimson',size=ticksFontSize)
fig.show()
if SAVEFIG: fig.savefig('userVerboseness.png')

input()
