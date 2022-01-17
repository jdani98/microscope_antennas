#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 13:28:53 2021
@author: daniel

DIGITAL FILTER AND EVENT VIEWER
"""

import numpy as np
import matplotlib.pyplot as plt
import os
import microcodes_modules.functions as fc
from scipy.fft import fft, ifft, fftfreq
from microcodes_modules.events import Event
from microcodes_modules.CAENReader import WDReader
from microcodes_modules.CAENReader import readChannels
from microcodes_modules.auto_plots import histo_stats

import cmath


plt.close('all')


optin = {   'in_dir':       'waves_211125_1927_((4))i',
            'ADC_ch':       int(2**14),
            'nsamp':        1030,
            'deltaT':       4,
            'Vpp':          0.5,
            'ngroups':      1,
            'Nevents':      'ind',
            }

ich = 0 # !!! channel
#READ = readChannels('DATA/'+optin['in_dir'],Vpp=2.0)
READ = WDReader('DATA/'+optin['in_dir']+'/wave'+str(ich)+'.dat', Vpp=2.0)
#DATA = READ.data()
DATA = READ.autoread()
#nevents = READ.nevents()
#print('Number of events:', nevents)
#file_list = READ.files_list()


def make_filter(nsamp,dT,fmin,fmax):
    xf = fftfreq(nsamp,dT)
    print(xf)
    difsmin = [abs(fi-fmin) for fi in xf]
    difsmax = [abs(fi-fmax) for fi in xf]
    iminpos = np.argmin(difsmin); iminneg = nsamp - iminpos
    imaxpos = np.argmin(difsmax); imaxneg = nsamp - imaxpos
    dig_filter = np.array([0.01]*nsamp)
    for i in range(nsamp):
        if i>iminpos and i<imaxpos:
            dig_filter[i] = 1.0
        if i>imaxneg and i <iminneg:
            dig_filter[i] = 1.0
    dig_filter[0] = 1.0
    return dig_filter

def butterworth_filter(nsamp,dT,w0,wp,eps,N):
    """
    Parameters
    ----------
    nsamp : INTEGER
        Number of ADC samples.
    dT : FLOAT
        Time separation between two consecutive samples.
    w0 : FLOAT
        Central frequency of maximum gain.
    wp : FLOAT
        Width of filter.
    eps : FLOAT
        Epsilon parameter of the Butterworth filter (gain at wp is 1/sqrt(1+eps²))
    N : INTEGER
        Power of epsilon².

    Returns
    -------
    Array with gain for each frequency.

    """
    xf = fftfreq(nsamp,dT)
    gain = 1.0/np.sqrt(1.0 + eps**2*((np.abs(xf)-w0)/wp)**(2*N))
    gain[0] = 1.0
    return gain
    
xf = fftfreq(optin['nsamp'],optin['deltaT']*1e-9)
gain = butterworth_filter(optin['nsamp'],optin['deltaT']*1e-9,55e6,15e6,0.2,20)
#gain = make_filter(optin['nsamp'],optin['deltaT']*1e-9,30e6,80e6)
plt.plot(xf,gain)



ev = 46 # !!! introduce number of event to plot

ADC_counts = {}
#for ich in range(8):
#event0 = DATA[ich][ev]
event0 = DATA[1][ev]
ADC_counts = event0[1]
FFT = fft(ADC_counts)

###############################################################################
fig1, ax1 = plt.subplots(1,1)
evento_inicial = Event(ADC_counts,ich)
evento_inicial.evn_display(ax1)
#ax1.set_ylim(0,2**14)

fig2, ax2 = plt.subplots(1,1)
evento_inicial.evn_display_fourier(ax2)
ax2.set_xlim(1,110)
ax2.set_yscale('log')
###############################################################################



filt_FFT = []
for i in range(optin['nsamp']):
    sample = FFT[i]
    mod = np.abs(sample)
    phs = cmath.phase(sample)
    filt_mod = gain[i] * mod
    filt_sample = cmath.rect(filt_mod,phs)
    filt_FFT.append(filt_sample)

filt_counts = ifft(filt_FFT)

###############################################################################
fig3, ax3 = plt.subplots(1,1)
evento_final = Event(filt_counts,ich)
evento_final.evn_display(ax3)
#ax3.set_ylim(0,2**14)

fig4, ax4 = plt.subplots(1,1)
evento_final.evn_display_fourier(ax4)
ax4.set_xlim(1,110)
ax4.set_yscale('log')
###############################################################################
