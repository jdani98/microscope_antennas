#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 17:23:54 2021
@author: daniel

*** PLOT OF MEAN POWER SPECTRAL DENSITY (II)***
This program reads CSV datafiles 'fullchar.dat' to plot:
    -> Mean PSD, deviation & phase variance (ax1, ax2 & ax3 in fig1)
    -> Mean phase and phase variance (ax1 & ax2 in fig2)
    -> List of peaks

How to run this file? # !!!
Type in terminal > python3 psd2_plot.py [idr]
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
import microcodes_modules.functions as fc

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

###### Calculus settings
ss      =    11                              # number of samplings to apply median method

###### Settings to show results (options out)
minx = 5; maxx = 110; stp = 10 # !!! limits of frequency & step of xticks
ax1_miny = -220; ax1_maxy = -140  # !!! limits of y axis in ax1
ax2_miny = -20; ax2_maxy = 30; ax2_stp = 20 # !!! limits & step of y axis in ax2
ax3_miny1 = 0.80; ax3_maxy1 = 1.05; ax3_stp1 = 0.1 # !!! limits of y axis in ax3 in fig1
ax3_miny2 = 0.80; ax3_maxy2 = 1.05; ax3_stp2 = 0.05 # !!! limits of y axis in ax3 in fig2
showfigs = False
savefigs = {'Horizontal': {'PSDs':         True,
                           'PHSs':         True},
            'Vertical':   {'PSDs':         True,
                           'PHSs':         True}}

savepks = True
###############################################################################

# Reading data from csv
file = open('OUTPUTS/'+in_dir+'/'+'fullchar.dat','r')
data = csv.reader(file)

xF     = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
A      = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
sA     = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
m_phs  = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
s_phs  = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}

A_p_sA    = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
A_m_sA    = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
xF_smooth = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
A_smooth  = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
Ap        = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
Ap_p_sA   = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
Ap_m_sA   = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}


for row in data:
    ch = int(row[0][3])
    if row[1] == 'xF':
        xF[ch] = [float(item) for item in row[3:]]
    if row[1] == 'A':
        A[ch] = [float(item) for item in row[3:]]
    if row[1] == 'sA':
        sA[ch] = [float(item) for item in row[3:]]
    if row[1] == 'm_phs':
        m_phs[ch] = [float(item) for item in row[3:]]
    if row[1] == 's_phs':
        s_phs[ch] = [float(item) for item in row[3:]]

file.close()

for ich in range(8):
    A_p_sA[ich] = np.array(A[ich]) + np.array(sA[ich])
    A_m_sA[ich] = np.array(A[ich]) - np.array(sA[ich])
    xF_smooth[ich], A_smooth[ich] = fc.median_method(xF[ich],A[ich],ss)
    Ap[ich] = [(A[ich][i+ss//2]-A_smooth[ich][i]) for i in range(len(A_smooth[ich]))]
    Ap_p_sA[ich] = np.array(Ap[ich]) + np.array(sA[ich][ss//2:-ss//2+1])
    Ap_m_sA[ich] = np.array(Ap[ich]) - np.array(sA[ich][ss//2:-ss//2+1])

### PLOTS #####################################################################
plt.close('all')

# Content of PLOT PSDs:
def plot_psd(ax,ich):
    ax.fill_between(xF[ich],A_m_sA[ich],A_p_sA[ich],color=colors[ich],edgecolor=None,alpha=0.25)
    ax.plot(xF[ich],A[ich],color=colors[ich],linewidth=0.5,label='Ch'+str(ich)+' '+orientations[ich])
    ax.plot(xF_smooth[ich],A_smooth[ich],color=colors[ich],linewidth=0.5,linestyle='dashed',alpha=0.5)
    return

# Content of PLOT PEAKS:
def plot_pks(ax,ich):
    ax.fill_between(xF_smooth[ich],Ap_m_sA[ich],Ap_p_sA[ich],color=colors[ich],edgecolor=None,alpha=0.25)
    ax.plot(xF_smooth[ich],Ap[ich],color=colors[ich],linewidth=0.5,alpha=0.8)
    return

# Content of PHASE VARIANCE:
def plot_phsvar(ax,ich):
    ax.plot(xF[ich],s_phs[ich],color=colors[ich],linewidth=0.5,label='Ch'+str(ich)+' '+orientations[ich])
    return

# Content of MEAN PHASE:
def plot_phsavg(ax,ich):
    ax.plot(xF[ich],m_phs[ich],color=colors[ich],linewidth=0.5)
    return

# Set of x axis
def xtik_psd(ax,ich):
    for x in np.arange(minx,maxx): ax.axvline(x=x,color='lightgray',linewidth=0.3)
    ax.set_xlim(minx,maxx)
    ax.set_xticks(np.arange(stp,maxx+1,stp))
    return
    
if showfigs:
    # Interactive figures for PLOT PSD
    fig11 = plt.figure(1,figsize=(16,9))
    fig11.suptitle('Mean Power Spectral Density')
    fig11.subplots_adjust(hspace=0.4,wspace=0.4)

    for ich in range(8):
        row = (ich)//4 ;  col = (ich)%4
        ax1 = fig11.add_subplot(11,4,(4*6*row+col+1,4*6*row+col+9))
        ax2 = fig11.add_subplot(11,4,4*6*row+col+13)
        ax3 = fig11.add_subplot(11,4,4*6*row+col+17)
        
        xtik_psd(ax1,ich)
        plot_psd(ax1,ich)
        #ax1.set_xlabel('$f$ (MHz)')
        #ax1.set_xticklabels([])
        ax1.tick_params(axis='x', labelsize=5)
        ax1.set_ylabel('$A$ (dBm/Hz)')
        ax1.set_ylim(-230,-150)
        #ax1.set_yticks([-230,-210,-190,-170,-150])
        ax1.grid()
        ax1.legend()
    
        xtik_psd(ax2,ich)
        plot_pks(ax2,ich)
        #ax2.set_xlabel('$f$ (MHz)')
        #ax2.set_xticklabels([])
        ax2.tick_params(axis='x', labelsize=5)
        ax2.set_ylabel(r'$\Delta A$')
        ax2.set_ylim(ax2_miny,ax2_maxy)
        ax2.set_yticks(np.arange(ax2_miny,ax2_maxy,ax2_stp))
        ax2.grid()
        
        xtik_psd(ax3,ich)
        plot_phsvar(ax3,ich)
        ax3.set_xlabel('$f$ (MHz)')
        ax3.set_ylabel(r'$\Delta \varphi$')
        ax3.set_ylim(ax3_miny1,ax3_maxy1)
        ax3.set_yticks(np.arange(ax3_miny1,ax3_maxy1,ax3_stp1))
        ax3.grid()

    # Interactive figures for PLOT MEAN PHASES
    fig21 = plt.figure(2,figsize=(16,9))
    fig21.suptitle('Relative phases of power spectrum')
    fig21.subplots_adjust(hspace=0.4,wspace=0.4)

    for ich in range(8):
        row = (ich)//4 ;  col = (ich)%4
        ax4 = fig21.add_subplot(11,4,(4*6*row+col+1,4*6*row+col+9))
        ax3 = fig21.add_subplot(11,4,(4*6*row+col+13,4*6*row+col+17))
        
        xtik_psd(ax4,ich)
        plot_phsavg(ax4,ich)
        #ax1.set_xlabel('$f$ (MHz)')
        #ax1.set_xticklabels([])
        ax4.tick_params(axis='x', labelsize=5)
        ax4.set_ylabel('Phase (rad)')
        ax4.set_ylim(-np.pi-0.3,np.pi+0.3)
        ax4.set_yticks(ticks=[-np.pi,-np.pi/2,0,np.pi/2,np.pi],labels=('$-\pi$','$-\pi/2$','0','$\pi/2$','$\pi$'))
        ax4.grid()
        
        xtik_psd(ax3,ich)
        plot_phsvar(ax3,ich)
        ax3.set_xlabel('$f$ (MHz)')
        ax3.set_ylabel(r'$\Delta \varphi$')
        ax3.set_ylim(ax3_miny2,ax3_maxy2)
        ax3.set_yticks(np.arange(ax3_miny2,ax3_maxy2,ax3_stp2))
        ax3.grid()
        ax3.legend()

    plt.show()


if savefigs['Horizontal']['PSDs']:
    # Horizontal figure to save of PLOT OF PSDs
    fig12 = plt.figure(3,figsize=(18,9))
    fig12.suptitle('Mean Power Spectral Density')
    fig12.subplots_adjust(hspace=0.1,wspace=0.2)

    for ich in range(8):
        row = (ich)//4 ;  col = (ich)%4
        ax1 = fig12.add_subplot(11,4,(4*6*row+col+1,4*6*row+col+9))
        ax2 = fig12.add_subplot(11,4,4*6*row+col+13)
        ax3 = fig12.add_subplot(11,4,4*6*row+col+17)
        
        xtik_psd(ax1,ich)
        plot_psd(ax1,ich)
        #ax1.set_xlabel('$f$ (MHz)')
        ax1.set_xticklabels([])
        if ich%4==0: ax1.set_ylabel('$A$ (dBm/Hz)')
        ax1.set_ylim(ax1_miny,ax1_maxy)
        #ax1.set_yticks([-230,-210,-190,-170,-150])
        ax1.grid()
        ax1.legend()
        
        xtik_psd(ax2,ich)
        plot_pks(ax2,ich)
        #ax2.set_xlabel('$f$ (MHz)')
        ax2.set_xticklabels([])
        if ich%4==0: ax2.set_ylabel(r'$\Delta A$')
        ax2.set_ylim(ax2_miny,ax2_maxy)
        ax2.set_yticks(np.arange(ax2_miny,ax2_maxy,ax2_stp))
        ax2.grid()
        
        xtik_psd(ax3,ich)
        plot_phsvar(ax3,ich)
        if ich//4==1: ax3.set_xlabel('$f$ (MHz)')
        if ich%4==0:  ax3.set_ylabel(r'$\Delta \varphi$')
        ax3.set_xlim(minx,maxx)
        ax3.set_ylim(ax3_miny1,ax3_maxy1)
        ax3.set_yticks(np.arange(ax3_miny1,ax3_maxy1,ax3_stp1))
        ax3.grid()
        
    plt.savefig('OUTPUTS/'+in_dir+'/'+'psd2_169.png',dpi=300,bbox_inches='tight')


if savefigs['Horizontal']['PHSs']:
    # Horizontal figure to save of PLOT OF MEAN PHASES
    fig22 = plt.figure(4,figsize=(18,9))
    fig22.suptitle('Relative phases of power spectrum')
    fig22.subplots_adjust(hspace=0.1,wspace=0.2)

    for ich in range(8):
        row = (ich)//4 ;  col = (ich)%4
        ax4 = fig22.add_subplot(11,4,(4*6*row+col+1,4*6*row+col+9))
        ax3 = fig22.add_subplot(11,4,(4*6*row+col+13,4*6*row+col+17))
        
        xtik_psd(ax4,ich)
        plot_phsavg(ax4,ich)
        #ax1.set_xlabel('$f$ (MHz)')
        ax4.set_xticklabels([])
        if ich%4==0:  ax4.set_ylabel('Phase (rad)')
        ax4.set_ylim(-np.pi-0.3,np.pi+0.3)
        ax4.set_yticks(ticks=[-np.pi,-np.pi/2,0,np.pi/2,np.pi],labels=('$-\pi$','$-\pi/2$','0','$\pi/2$','$\pi$'))
        ax4.grid()
        
        xtik_psd(ax3,ich)
        plot_phsvar(ax3,ich)
        if ich//4==1: ax3.set_xlabel('$f$ (MHz)')
        if ich%4==0:  ax3.set_ylabel(r'$\Delta \varphi$')
        ax3.set_ylim(ax3_miny2,ax3_maxy2)
        ax3.set_yticks(np.arange(ax3_miny2,ax3_maxy2,ax3_stp2))
        ax3.grid()
        ax3.legend()
        
    plt.savefig('OUTPUTS/'+in_dir+'/'+'phs2_169.png',dpi=300,bbox_inches='tight')


if savefigs['Vertical']['PSDs']:
    # Horizontal figure to save of PLOT OF PSDs
    fig13 = plt.figure(5,figsize=(10.5,14.85))
    fig13.subplots_adjust(hspace=0.2,wspace=0.2)

    for ich in range(8):
        row = (ich)//2 ;  col = (ich)%2
        ax1 = fig13.add_subplot(23,2,(2*6*row+col+1,2*6*row+col+5))
        ax2 = fig13.add_subplot(23,2,2*6*row+col+7)
        ax3 = fig13.add_subplot(23,2,2*6*row+col+9)
        
        xtik_psd(ax1,ich)
        plot_psd(ax1,ich)
        #ax1.set_xlabel('$f$ (MHz)')
        ax1.set_xticklabels([])
        if ich%2==0: ax1.set_ylabel('$A$ (dBm/Hz)')
        ax1.set_ylim(ax1_miny,ax1_maxy)
        #ax1.set_yticks([-230,-210,-190,-170,-150])
        ax1.grid()
        ax1.legend()
        
        xtik_psd(ax2,ich)
        plot_pks(ax2,ich)
        #ax2.set_xlabel('$f$ (MHz)')
        ax2.set_xticklabels([])
        if ich%2==0: ax2.set_ylabel(r'$\Delta A$')
        ax2.set_ylim(ax2_miny,ax2_maxy)
        ax2.set_yticks(np.arange(ax2_miny,ax2_maxy,ax2_stp))
        ax2.grid()
        
        xtik_psd(ax3,ich)
        plot_phsvar(ax3,ich)
        if ich//2==3: ax3.set_xlabel('$f$ (MHz)')
        if ich%2==0:  ax3.set_ylabel(r'$\Delta \varphi$')
        ax3.set_ylim(ax3_miny1,ax3_maxy1)
        ax3.set_yticks(np.arange(ax3_miny1,ax3_maxy1,ax3_stp1))
        ax3.grid()
        
    plt.savefig('OUTPUTS/'+in_dir+'/'+'psd2_A4.png',dpi=300,bbox_inches='tight')


if savefigs['Vertical']['PHSs']:
    # Horizontal figure to save of PLOT OF MEAN PHASES
    fig23 = plt.figure(6,figsize=(10.5,14.85))
    fig23.subplots_adjust(hspace=0.2,wspace=0.2)

    for ich in range(8):
        row = (ich)//2 ;  col = (ich)%2
        ax4 = fig23.add_subplot(23,2,(2*6*row+col+1,2*6*row+col+5))
        ax3 = fig23.add_subplot(23,2,(2*6*row+col+7,2*6*row+col+9))
    
        xtik_psd(ax4,ich)
        plot_phsavg(ax4,ich)
        #ax4.set_xlabel('$f$ (MHz)')
        ax4.set_xticklabels([])
        if ich%2==0:  ax4.set_ylabel('Phase (rad)')
        ax4.set_ylim(-np.pi-0.3,np.pi+0.3)
        ax4.set_yticks(ticks=[-np.pi,-np.pi/2,0,np.pi/2,np.pi],labels=('$-\pi$','$-\pi/2$','0','$\pi/2$','$\pi$'))
        ax4.grid()
        
        xtik_psd(ax3,ich)
        plot_phsvar(ax3,ich)
        if ich//2==3: ax3.set_xlabel('$f$ (MHz)')
        if ich%2==0:  ax3.set_ylabel(r'$\Delta \varphi$')
        ax3.set_ylim(ax3_miny2,ax3_maxy2)
        ax3.set_yticks(np.arange(ax3_miny2,ax3_maxy2,ax3_stp2))
        ax3.grid()
        ax3.legend()
        
    plt.savefig('OUTPUTS/'+in_dir+'/'+'phs2_A4.png',dpi=300,bbox_inches='tight')


# DETECTION OF FREQUENCY PEAKS
peak_th = 2 #dBm/Hz
fpeaks = {}
mpeaks = {}
mstars = {}
npeaks = []

# Searching peaks in 8 channels
fpeaks = []
ipeaks = []
for ich in range(8):
    freq = xF_smooth[ich]
    magn = Ap[ich]
    for i in range(len(freq)):
        if freq[i] not in fpeaks:
            if magn[i]>=peak_th and magn[i]>=magn[i-1] and magn[i]>=magn[i+1]:
                fpeaks.append(freq[i])
                ipeaks.append(i)
fpeaks = sorted(fpeaks)
ipeaks = sorted(ipeaks)

# Saving in memory magnitudes of all peaks
for ich in range(8):
    magn = Ap[ich]
    mpeaks[ich] = []
    mstars[ich] = []
    for i in ipeaks:
        (mpeaks[ich]).append(magn[i])
        nstars = int(magn[i]//2)
        stars = ''
        for i in range(nstars):
            stars += '*'
        (mstars[ich]).append(stars)


# Saving in file peaks and coincidences of peaks
if savepks:
    peaksfile = open('OUTPUTS/'+in_dir+'/'+'psd_peaks.csv','w')
    writer = csv.writer(peaksfile)
    permutas2 = []
    for i in range(8):
        for j in range(i):
            permutas2 += [str(i)+str(j)]
    writer.writerow(['Ch0','','','Ch1','','','Ch2','','','Ch3','','','Ch4','','',
                     'Ch5','','','Ch6','','','Ch7','','', '','CC:']+
                     permutas2)
    for ip in range(len(fpeaks)):
        line = []
        per2 = []
        for ich in range(8):
            line += [fpeaks[ip],mpeaks[ich][ip],mstars[ich][ip]]
            for jch in range(ich):
                if mstars[ich][ip] == mstars[jch][ip] != '': per2 += [1]
                else: per2 += [0]
        line += ['',''] + per2
        writer.writerow(line)
    peaksfile.close()
