#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 16:38:40 2021
@author: daniel

*** PLOT OF mPSD IN GROUPS***
This program reads CSV datafiles 'psd24h.dat' to plot:
    -> Mean PSD during time (ax1)
    -> Phase variance of Fourier transform during time (ax2)
    -> Total (integrated over frequencies) PSD during time (ax3)

How to run this file? # !!!
Type in terminal > python3 psd24h_plot.py [idr]
where [idr] is the directory with data to read
"""

import os
os.chdir('..')

import sys
idr = str(sys.argv[1])

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import csv

colors = cm.tab10(np.linspace(0,1,8))
orientations = {0:'EW', 1:'NS', 2:'NS', 3:'EW', 4:'EW', 5:'NS', 6:'NS', 7:'EW'}
### SETTINGS ##################################################################
###### Settings to read data (options in)
in_dir  =    idr                             # !!! name of input directory
nbits   =    14                              # !!! number of bits for ADC channels
nsamp   =    1030                            # !!! number of samples per event
deltaT  =    4                               # !!! real time separation between two samples
Vpp     =    2.0                             # !!! voltage peak to peak
ADC_ch  =    2**nbits                        # number of ADC_channels, equal to 2**nbits
Fs      =    1/deltaT * 1e9                  # sampling frequency (Hz)
R       =    50                              # input impedance

###### Settings of timing and agrupation of events
DeltaT  =    2                               # time between two events (in seconds)
nevnts  =    900                             # number of events per group
timegr  =    DeltaT*nevnts                   # duration of one group

###### Calculus settings
ss      =    11                              # number of samplings to apply median method

###### Settings to show results (options out)
ytiks = np.arange(0,23,1) # yticks for ax1 & ax2
day_times = [str((13+i)%24)+':45' for i in range(23)] # times of data for ytiks ax1 & ax2
minx = 5; maxx = 110; stp = 10 # !!! xlims and step of xticks
ax1_minz = -230; ax1_maxz = -180 # !!! lims of magnitude in 2D plot for ax1
ax2_minz = 0.98; ax2_maxz = 1.00 # !!! lims of magnitude in 2D plot for ax2
ax3_minx = 0; ax3_maxx = 23; ax3_stp = 5 # !!! xlims and step for ax3
showfigs = False
savefigs = {'Horizontal': {'mPSD':   False,
                           'sPHS':   False,
                           'tPSD':   False},
            'Vertical':   {'mPSD':   False,
                           'sPHS':   False,
                           'tPSD':   True}}

###############################################################################

# Reading data from csv
file = open('OUTPUTS/'+in_dir+'/'+'psd24h.dat','r')
data = csv.reader(file)

xF     = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
A      = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}}
sA     = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}}
m_phs  = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}}
s_phs  = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}}

min_if = 10 # !!! minimum index of frequency to read
for row in data:
    ch = int(row[0][3])
    if row[1] == 'xF':
        xF[ch] = [float(item) for item in row[min_if+3:]]
    if row[1] == 'A':
        tb = int(float(row[2]))
        A[ch][tb] = [float(item) for item in row[min_if+3:]]
    if row[1] == 'sA':
        tb = int(float(row[2]))
        sA[ch][tb] = [float(item) for item in row[min_if+3:]]
    if row[1] == 'm_phs':
        tb = int(float(row[2]))
        m_phs[ch][tb] = [float(item) for item in row[min_if+3:]]
    if row[1] == 's_phs':
        tb = int(float(row[2]))
        s_phs[ch][tb] = [float(item) for item in row[min_if+3:]]
        
file.close()

Ng = int(60*tb//timegr) + 1
print('Number of groups: ', Ng)

### PLOTS #####################################################################
plt.close('all')


# Content of PLOT OF MEAN POWER SPECTRAL DENSITY DURING TIME
def plot_psd(ax,ich):
    x = [freqi for freqi in xF[ich]]
    y = []
    V = np.zeros([Ng,len(x)])
    for tb,PSD in A[ich].items():
        ig = int(60*tb//timegr)
        for f in range(len(x)):
            V[ig,f] = PSD[f]
        y.append(tb/60)
    c = ax1.imshow(V,extent=[x[0],x[-1],y[0],y[-1]],vmin=ax1_minz,vmax=ax1_maxz,aspect='auto',cmap='inferno')
    return c

# Content of PLOT OF PHASE VARIANCE DURING TIME
def plot_phsvar(ax,ich):
    x = [freqi for freqi in xF[ich]]
    y = []
    V = np.zeros([Ng,len(x)])
    for tb,s_phsi in s_phs[ich].items():
        ig = int(60*tb//timegr)
        for f in range(len(x)):
            V[ig,f] = s_phsi[f]
        y.append(tb/60)
    c = ax2.imshow(V,extent=[x[0],x[-1],y[0],y[-1]],vmin=ax2_minz,vmax=ax2_maxz,aspect='auto',cmap='inferno')
    return c

# Content of PLOT OF TOTAL PSD DURING TIME
def plot_tpsd(ax,ich):
    x = []
    y = []
    for tb,PSD in A[ich].items():
        PSD_unlog = 50*250e6*10**(np.array(PSD)/10)
        TPSD_ig = np.sqrt(np.mean(PSD_unlog**2))
        x.append(tb/60)
        y.append(TPSD_ig)
    ax3.plot(x,y,'o')
    return


if showfigs:
    # PLOT OF MEAN POWER SPECTRAL DENSITY DURING TIME
    fig11 = plt.figure(1,figsize=(16,9))
    fig11.suptitle('Mean Power Spectral Density during 24h')
    fig11.subplots_adjust(hspace=0.2,wspace=0.2)


    for ich in range(8):
        row = (ich)//4 ;  col = (ich)%4
        ax1 = fig11.add_subplot(11,5,(5*6*row+col+1,5*6*row+col+21))
        c = plot_psd(ax1,ich)
        ax1.set_xlim(minx,maxx)
        ax1.set_xticks(np.arange(stp,maxx+1,stp))
        #ax1.set_ylabel('Hours')
        ax1.set_yticks(ytiks,labels = day_times)
        ax1.set_xlabel('$f$ (MHz)')

    axleg = fig11.add_subplot(11,5,(5,4+21),frame_on=False,visible=False)
    fig11.colorbar(c, ax=axleg,location='left')


    # PLOT OF PHASE VARIANCE DURING TIME
    fig21 = plt.figure(3,figsize=(16,9))
    fig21.suptitle('Phase variance of spectrum during 24h')
    fig21.subplots_adjust(hspace=0.2,wspace=0.2)

    for ich in range(8):
        row = (ich)//4 ;  col = (ich)%4
        ax2 = fig21.add_subplot(11,5,(5*6*row+col+1,5*6*row+col+21))
        c = plot_phsvar(ax2,ich)
    
        ax2.set_xlim(minx,maxx)
        ax2.set_xticks(np.arange(stp,maxx+1,stp))
        ax2.set_yticks(ytiks,labels = day_times)
        ax2.set_xlabel('$f$ (MHz)')

    axleg = fig21.add_subplot(11,5,(5,4+21),frame_on=False,visible=False)
    fig21.colorbar(c, ax=axleg,location='left')


    # PLOT OF TOTAL PSD DURING TIME
    fig31 = plt.figure(4,figsize=(16,9))
    fig31.suptitle('Total Power Spectral Density during 24h')
    fig31.subplots_adjust(hspace=0.2,wspace=0.2)

    for ich in range(8):
        row = (ich)//4 ;  col = (ich)%4
        ax3 = fig31.add_subplot(2,4,ich+1)
        plot_tpsd(ax3,ich)
        ax3.set_xticks(np.arange(ax3_minx,ax3_maxx,ax3_stp))
        #ax3.set_yticks()
        ax3.set_xlabel('Time (h)')
        ax3.set_ylabel('Total PSD')

    plt.show()



if savefigs['Horizontal']['mPSD']:
    # Horizontal figure to save PLOT OF MEAN POWER SPECTRAL DENSITY DURING TIME
    fig12 = plt.figure(4,figsize=(21.5,9))
    fig12.suptitle('Mean Power Spectral Density during 24h')
    fig12.subplots_adjust(hspace=0.1,wspace=0.3)

    for ich in range(8):
        row = (ich)//4 ;  col = (ich)%4
        ax1 = fig12.add_subplot(11,5,(5*6*row+col+1,5*6*row+col+21))
        c = plot_psd(ax1,ich)
        ax1.set_xlim(minx,maxx)
        ax1.set_xticks(np.arange(stp,maxx+1,stp))
        #ax1.set_ylabel('Hours')
        ax1.set_yticks(ytiks,labels = day_times)
        ax1.set_xlabel('$f$ (MHz)')

    axleg = fig12.add_subplot(11,5,(5,4+21),frame_on=False,visible=False)
    fig12.colorbar(c, ax=axleg,location='left')
    
    plt.savefig('OUTPUTS/'+in_dir+'/'+'psd24h_169.png',dpi=300,bbox_inches='tight')


if savefigs['Horizontal']['sPHS']:
    # Horizontal figure to save PLOT OF PHASE VARIANCE DURING TIME
    fig22 = plt.figure(5,figsize=(21.5,9))
    fig22.suptitle('Phase variance of spectrum during 24h')
    fig22.subplots_adjust(hspace=0.1,wspace=0.3)

    for ich in range(8):
        row = (ich)//4 ;  col = (ich)%4
        ax2 = fig22.add_subplot(11,5,(5*6*row+col+1,5*6*row+col+21))
        c = plot_phsvar(ax2,ich)
    
        ax2.set_xlim(minx,maxx)
        ax2.set_xticks(np.arange(stp,maxx+1,stp))
        ax2.set_yticks(ytiks,labels = day_times)
        ax2.set_xlabel('$f$ (MHz)')

    axleg = fig22.add_subplot(11,5,(5,4+21),frame_on=False,visible=False)
    fig22.colorbar(c, ax=axleg,location='left')
    
    plt.savefig('OUTPUTS/'+in_dir+'/'+'sphs24h_169.png',dpi=300,bbox_inches='tight')


if savefigs['Horizontal']['tPSD']:
    # Horizontal figure to save PLOT OF TOTAL PSD DURING TIME
    fig32 = plt.figure(6,figsize=(18.5,9))
    fig32.suptitle('Total Power Spectral Density during 24h')
    fig32.subplots_adjust(hspace=0.1,wspace=0.3)

    for ich in range(8):
        row = (ich)//4 ;  col = (ich)%4
        ax3 = fig32.add_subplot(2,4,ich+1)
        plot_tpsd(ax3,ich)
        ax3.set_xticks(np.arange(ax3_minx,ax3_maxx,ax3_stp))
        #ax3.set_yticks()
        ax3.set_xlabel('Time (h)')
        ax3.set_ylabel('Total PSD')
    
    plt.savefig('OUTPUTS/'+in_dir+'/'+'tpsd_169.png',dpi=300,bbox_inches='tight')



if savefigs['Vertical']['mPSD']:
    # Vertical figure to save PLOT OF MEAN POWER SPECTRAL DENSITY DURING TIME
    fig13 = plt.figure(7,figsize=(10.5,14.85))
    fig13.subplots_adjust(hspace=0.2,wspace=0.4)

    for ich in range(8):
        row = (ich)//2 ;  col = (ich)%2
        ax1 = fig13.add_subplot(4,13,(13*row+6*col+1,13*row+6*col+5))
        c = plot_psd(ax1,ich)
        ax1.set_xlim(minx,maxx)
        ax1.set_xticks(np.arange(stp,maxx+1,stp))
        #ax1.set_ylabel('Hours')
        ax1.set_yticks(ytiks,labels = day_times)
        ax1.tick_params(axis='y', labelsize=8)
        ax1.set_xlabel('$f$ (MHz)')

    axleg = fig13.add_subplot(4,13,13,frame_on=False,visible=False)
    fig13.colorbar(c, ax=axleg,location='left')
    
    plt.savefig('OUTPUTS/'+in_dir+'/'+'psd24h_A4.png',dpi=300,bbox_inches='tight')


if savefigs['Vertical']['sPHS']:
    # Vertical figure to save PLOT OF PHASE VARIANCE DURING TIME
    fig23 = plt.figure(8,figsize=(10.5,14.85))
    fig23.subplots_adjust(hspace=0.2,wspace=0.4)

    for ich in range(8):
        row = (ich)//2 ;  col = (ich)%2
        ax2 = fig23.add_subplot(4,13,(13*row+6*col+1,13*row+6*col+5))
        c = plot_phsvar(ax2,ich)
    
        ax2.set_xlim(minx,maxx)
        ax2.set_xticks(np.arange(stp,maxx+1,stp))
        ax2.set_yticks(ytiks,labels = day_times)
        ax2.tick_params(axis='y', labelsize=8)
        ax2.set_xlabel('$f$ (MHz)')

    axleg = fig23.add_subplot(4,13,13,frame_on=False,visible=False)
    fig23.colorbar(c, ax=axleg,location='left')
    
    plt.savefig('OUTPUTS/'+in_dir+'/'+'sphs24h_A4.png',dpi=300,bbox_inches='tight')


if savefigs['Vertical']['tPSD']:
    # Vertical figure to save PLOT OF TOTAL PSD DURING TIME
    fig33 = plt.figure(9,figsize=(10.5,14.85))
    fig33.subplots_adjust(hspace=0.2,wspace=0.2)

    for ich in range(8):
        row = (ich)//2 ;  col = (ich)%2
        ax3 = fig33.add_subplot(4,2,ich+1)
        plot_tpsd(ax3,ich)
        ax3.set_xticks(np.arange(ax3_minx,ax3_maxx,ax3_stp))
        #ax3.set_yticks()
        ax3.set_xlabel('Time (h)')
        ax3.set_ylabel('Total PSD')
    
    plt.savefig('OUTPUTS/'+in_dir+'/'+'tpsd_A4.png',dpi=300,bbox_inches='tight')