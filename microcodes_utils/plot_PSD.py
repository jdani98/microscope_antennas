#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 13:08:11 2021
@author: daniel

PLOT OF THE MEAN POWER SPECTRAL DENSITY OF ONE FILE
"""

# http://www.fmlist.org/eafm2.php?smode=C&localidad=Santiago%20de%20Compostela/Monte%20Pedroso

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
import os
import csv

from microcodes_modules.CAENReader import WDReader
from microcodes_modules.events import Event
import microcodes_modules.functions as fc

colors = ['b','g','r','c','m','y','k','tab:gray']

###### Settings to read data (options in)
""" Legend:
	* in_dir -> name of input directory
	* ADC_ch -> number of ADC channels, equal to 2^Nbits
	* nsamp -> number of samples per event
	* deltaT -> real time separation between two samples
	* Vpp -> voltage peak to peak
	* ngroups -> number of groups to study data
	* Nevents -> number of events per group
"""
optin = {	'in_dir':		'wavesh_211124_1620_merged',
            #'in_dir':		'wavesh_211029_1300_92h00',
			'ADC_ch':		int(2**14),
			'nsamp':		1030,
            'deltaT':       4,
            'Vpp':          0.5,
            'ngroups':      1,
            'Nevents':      'ind',
			}

###### Settings to show results (options out)
optot = {	'savefig':      False,
            'savepts':      False
		}
######

fname = 'wave0.dat'

READER = WDReader('DATA/'+optin['in_dir']+'/'+fname,channel=int(fname[4]))
print('.')
channel, data = READER.autoread()

Fs = 250.e6

R = 50 # ohm (impedance of the oscilloscope)
A = 0
for iev, event in data.items():
    yC = 2 / 2**14 # counts to V converter
    xC = 1.e-6     # Hz to MHz converter
    counts = [yC*count for count in event[1]]
    n = len(counts)
    
    PSD = (2.0/(n*Fs)) * (np.abs(fft(counts)[:n//2]))**2  # V^2 / Hz
    xF = xC * fftfreq(n,4.0*1.e-9)[:n//2]
    
    A += 10 * np.log10(PSD/(R*Fs))

print('Nev=', iev)
A = A/iev + 30

print('Channel ', channel)

ss = 5
xF_smooth, A_smooth = fc.median_method(xF,A,ss)

print(len(xF))
print(len(xF_smooth))

Ap = [(A[i+ss//2]-A_smooth[i]) for i in range(len(A_smooth))]

########################## PLOTS ##############################################
plt.close('all')
fig3 = plt.figure(3,figsize=(6,7.5))
fig3.subplots_adjust(hspace=0.4)

ax1 = fig3.add_subplot(5,1,(1,4))
minx = 5; maxx = 110
ax1.axvline(x=88.9,color='red',linewidth=0.5,linestyle='dashed')
for x in np.arange(minx,maxx): ax1.axvline(x=x,color='lightgray',linewidth=0.3)
ax1.plot(xF,A,color=colors[channel],linewidth=0.5)
ax1.plot(xF_smooth,A_smooth,color=colors[channel],linewidth=0.5,linestyle='dashed',alpha=0.5)
#ax1.set_xlabel('$f$ (MHz)')
ax1.set_ylabel('$A$ (dBm/Hz)')
ax1.set_xlim(minx,maxx)
ax1.set_ylim(-220,-100)
ax1.set_xticks(np.arange(minx+5,maxx+5,10))
ax1.grid()

ax2 = fig3.add_subplot(5,1,5)
ax2.axvline(x=88.9,color='red',linewidth=0.5,linestyle='dashed')
for x in np.arange(minx,maxx): ax2.axvline(x=x,color='lightgray',linewidth=0.3)
ax2.plot(xF_smooth,Ap,color=colors[channel],linewidth=0.5,alpha=0.8)
ax2.set_xlabel('$f$ (MHz)')
ax2.set_ylabel(r'$\Delta A$ (dBm/Hz)')
ax2.set_xlim(minx,maxx)
ax2.set_ylim(-10,20)
ax2.set_xticks(np.arange(minx+5,maxx+5,10))
ax2.grid()

##############################################################################


if optot['savefig'] or optot['savepts']:
    os.chdir('OUTPUTS')
    fileslist = os.listdir()
    if optin['in_dir'] not in fileslist:
        os.mkdir(optin['in_dir'])
        print('Created new directory ' + optin['in_dir'])

if optot['savefig']:
    plt.savefig(optin['in_dir']+'/'+'AAp_wave'+str(channel)+'.png',dpi=300)

if optot['savepts']:
    outdata = open(optin['in_dir']+'/'+'AAp_data.csv','a')
    writer = csv.writer(outdata)
    writer.writerow(['#Ch'+str(channel)])
    writer.writerow(xF)
    writer.writerow(A)
    writer.writerow(xF_smooth)
    writer.writerow(A_smooth)
    writer.writerow(Ap)
    outdata.close()

"""
#evento = Event(data[0][1],channel=channel)
#fig, ax = plt.subplots()
#evento.evn_display(ax)

evento = data[0][1]
evento = [count/2**13 for count in evento]
plt.figure(1)
plt.plot(evento,color=colors[channel],linewidth=0.5)
"""