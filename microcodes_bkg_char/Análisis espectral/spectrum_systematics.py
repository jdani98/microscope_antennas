#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 11:37:06 2021

@author: daniel
"""

import os
print(os.getcwd())
os.chdir('/home/daniel/Documentos/HYBRID/Antenas')
import modules_for_python.functions as fc
import csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import scipy.stats as sct
import scipy.optimize as sco

colors = cm.tab10(np.linspace(0,1,8))
orientations = {0:'EW', 1:'NS', 2:'NS', 3:'EW', 4:'EW', 5:'NS', 6:'NS', 7:'EW'}


def mean_method(X,Y,s=3):
	"""
	mean method for noise suppression. Y is array with data and s the number of samples to apply
	the mean
	"""
	nX = []
	nY = []
	for i in range(s//2,len(Y)-s//2):
		part = Y[i-s//2:i+s//2+1]
		nX.append(X[i])
		nY.append(np.mean(part))
	return np.array(nX),np.array(nY)

def polinomio(x,a0,a1,a2,a3,a4,a5):
    return a0 + a1*x + a2*x**2 + a3*x**3 + a4*x**4 + a5*x**5

in_dir = 'waves_211108_without_filter'

ff =        {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
A =         {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}

file = open('OUTPUTS/'+in_dir+'/'+'data_for_plots.dat','r')
data = csv.reader(file)

i = 0
for row in data:
    if (i-0)%11 == 0:
        ch = int(row[0][3])
    if (i-2)%11 == 0:
        ff[ch] = [float(item) for item in row[2:]]
    if (i-7)%11 == 0:
        A[ch] = [float(item) for item in row[2:]]
    i+=1
        
file.close()

x_env = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
y_env = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
x_bas = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
y_bas = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}

env_maxs = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
popts = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
ifm = 11 # interval for maximum
for ich in range(8):
    x_env[ich],y_env[ich] = mean_method(ff[ich],A[ich],11)
    x_bas[ich],y_bas[ich] = fc.median_method(x_env[ich],y_env[ich],31)
    for i in range(ifm//2,len(y_env[ich])-ifm//2-1):
        group = y_env[ich][i-ifm//2:i+ifm//2+1]
        if y_env[ich][i] == np.max(group): env_maxs[ich].append(x_env[ich][i+ifm//2])
    popt,pcov = sco.curve_fit(polinomio,x_bas[ich],y_bas[ich])
    popts[ich] = popt


plt.close('all')
fig3 = plt.figure(3)          
print('Envelope maximums:')
for ich in range(8):
    print('Channel '+str(ich))
    env_maxs_ich = [np.round(item,0) for item in env_maxs[ich]]
    print(env_maxs_ich)
    diffs = [env_maxs_ich[i+1]-env_maxs_ich[i] for i in range(len(env_maxs_ich)-1)]
    period = sct.mode(diffs)[0]
    period2 = np.median(diffs)
    print(period)
    print(period2)
    #for i in range(len(env_maxs_ich)): plt.axvline(x=(env_maxs_ich[0]+i*period),color=colors[ich])
    
for i in range(len(env_maxs_ich)): plt.axvline(x=(env_maxs[0][0]+i*period),color=colors[0])
plt.grid()

# PLOT OF POWER SPECTRAL DENSITY
fig4 = plt.figure(4,figsize=(24,9))
fig4.suptitle('Mean Power Spectral Density')
fig4.subplots_adjust(hspace=0.4,wspace=0.2)

minx = 5; maxx = 110
for ich in range(8):
    row = (ich)//4 ;  col = (ich)%4
    ax1 = fig4.add_subplot(2,4,ich+1)
    
    for x in np.arange(minx,maxx): ax1.axvline(x=x,color='lightgray',linewidth=0.3)
    ax1.plot(x_env[ich],y_env[ich],color=colors[ich])
    ax1.plot(x_bas[ich],y_bas[ich],color=colors[ich],linewidth=0.5,linestyle='dashed')
    ax1.plot(env_maxs[ich],[ich for i in range(len(env_maxs[ich]))],'o',color=colors[ich])
    ax1.plot(x_bas[ich],polinomio(x_bas[ich],*popts[ich]))
    #ax1.set_xlabel('$f$ (MHz)')
    #ax1.set_xticklabels([])
    ax1.set_ylabel('$A$ (dBm/Hz)')
    ax1.set_xlim(minx,maxx)
    ax1.set_ylim(-240,-140)
    ax1.set_xticks(np.arange(minx+5,maxx+5,10))
    ax1.grid()
    ax1.legend()