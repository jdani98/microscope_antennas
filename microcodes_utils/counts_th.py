#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 17:22:59 2021

@author: daniel

NUMBER OF SAMPLES OVER THRESHOLD
"""

import os
#os.chdir('..')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import csv
import scipy.optimize as sco
#from scipy.stats import chisquare

colors1 = cm.hot(np.linspace(0,1,8))
colors2 = cm.gnuplot(np.linspace(0,1,30))
orientations = {0:'EW', 1:'NS', 2:'NS', 3:'EW', 4:'EW', 5:'NS', 6:'NS', 7:'EW'}
### SETTINGS ##################################################################
###### Settings to read data (options in)
in_dis  =    ['wavesh_211105_1146_70h10',
              'wavesh_211029_1300_92h00',
              'wavesh_211102_0955_47h43',
              'wavesh_211104_1102_23h00',
              'wavesh_211108_1029_0h38']  # !!! names of input directories
              #''
tags    =    ['770 V','780 V', '800 V', '820 V', '900 V']
voltages=    [770,780,800,820,900]
nbits   =    14                              # !!! number of bits for ADC channels
nsamp   =    1030                            # !!! number of samples per event
deltaT  =    8                               # !!! real time separation between two samples
Vpp     =    2.0                             # !!! voltage peak to peak
ADC_ch  =    2**nbits                        # number of ADC_channels, equal to 2**nbits
Fs      =    1/deltaT * 1e9                  # sampling frequency (Hz)
R       =    50                              # input impedance
ngroups =    1                               # number of groups to study data
Nevents =    'ind'                           # number of events per group
###############################################################################

def recta(x,a,b):
    return a*x + b

rango = {}
histo = {}

counts_over = {}
counts_undr = {}
Counts = {}


baseline = ADC_ch//2
#thresholds = [0,250,500,750,1000,1250,1500,1750,2000,2250,2500,2750,3000,3250,
#              3500,3750,4000,4250,4500,4750,5000,5250,5500,5750,6000,6250,6500] # !!! only integers
thresholds = [0,500,1000,1500,2000,2500,3000,3500,4000,4250,4500,4750,5000,5250,5500,5750,6000,6250,6500]

NTcounts = []
# Reading data from csv
for in_dir in in_dis:
    print(' ... Reading ' + str(in_dir))
    file = open('OUTPUTS/'+in_dir+'/'+'data_for_plots.dat','r')
    data = csv.reader(file)

    rang =     {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
    hist =     {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}

    i = 0
    for row in data:
        if (i-0)%11 == 0:
            ch = int(row[0][3])
        if (i-4)%11 == 0:
            rango[ch] = [int(item) for item in row[2:]]
        if (i-5)%11 == 0:
            histo[ch] = [int(item) for item in row[2:]]
        i+=1
    
    rango[in_dir] = rang
    histo[in_dir] = hist

    file.close()
    
    ntcounts = sum(histo[0])
    NTcounts.append(ntcounts)
    print('     Total number of counts: ', ntcounts)

    counts_over_th = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}}
    counts_undr_th = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}}
    counts_th = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}}


    for ich in range(8):
        for th in thresholds:
            ith_over = baseline + th
            ith_undr = baseline - th
            counts_over_th[ich][th] = sum(histo[ich][ith_over:])/ntcounts
            counts_undr_th[ich][th] = sum(histo[ich][:ith_undr])/ntcounts
            counts_th[ich][th] = counts_over_th[ich][th] + counts_undr_th[ich][th]

    counts_over[in_dir] = counts_over_th
    counts_undr[in_dir] = counts_undr_th
    Counts[in_dir] = counts_th
#print(counts_over_th)
#print(counts_undr_th)



### PLOTS #####################################################################
plt.close('all')

# COUNTS VERSUS THRESHOLD
fig1 = plt.figure(1,figsize=(24,9))
fig1.suptitle('Counts versus threshold')
fig1.subplots_adjust(hspace=0.2,wspace=0.4)


for ich in range(8):
    ax = fig1.add_subplot(2,4,ich+1)
    for in_dir in in_dis:
        J = in_dis.index(in_dir)
        #print(' ... Plotting ch'+str(ich)+' '+in_dir)
        x_over = [] ;  y_over = []
        x_undr = [] ;  y_undr = []
        x = [] ;  y = []
        for th,counts in counts_over[in_dir][ich].items():
            x_over.append(th) ;  y_over.append(counts)
        for th,counts in counts_undr[in_dir][ich].items():
            x_undr.append(th) ;  y_undr.append(counts)
        #y = [yio+yiu for (yio,yiu) in zip(y_over,y_undr)]
        for th,counts in Counts[in_dir][ich].items():
            x.append(th) ;  y.append(counts)
        #ax.plot(x_over,y_over,'.-',color=colors[J],label='Ch'+str(ich)+' over bl '+tags[J])
        #ax.plot(x_undr,y_undr,'.-',color=colors[J],alpha=0.5,label='Ch'+str(ich)+' under bl '+tags[J])
        ax.plot(x,y,'.-',color=colors1[J],label='Ch'+str(ich)+' '+tags[J])
        ax.set_xlabel('Threshold (ADC)')
        ax.set_ylabel('Rate of Counts')
        ax.set_xlim(thresholds[0],thresholds[-1])
        ax.set_ylim(0,1)
        #ax.grid()
        ax.legend()
#plt.show()


# COUNTS VERSUS SCINTILLATOR VOLTAGE
fig2 = plt.figure(2,figsize=(24,9))
fig2.suptitle('Counts versus scintillator voltage')
fig2.subplots_adjust(hspace=0.2,wspace=0.4)

fit_params = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}}
fit_params2 = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}}
for ich in range(8):
    ax = fig2.add_subplot(2,4,ich+1)
    for th,counts in Counts[in_dir][ich].items():
        fit_params[ich][th] = {}   # fit params 1
        fit_params2[ich][th] = {}  # fit params 2
        J = thresholds.index(th)
        x = [] ;  y = []
        for i in range(len(voltages)):
            in_dir = in_dis[i]
            x.append(voltages[i])
            y.append(Counts[in_dir][ich][th])
        
        # (1) Fit to all points:
        popt, pcov = sco.curve_fit(recta,x,y)
        a,b = popt
        fit_params[ich][th]['a'] = a
        fit_params[ich][th]['b'] = b
        fit_result = recta(np.array(voltages),a,b)
        dof = len(y) - 2
        chisq = sum([(yi-fiti)**2/fiti for (yi,fiti) in zip(y,fit_result)])
        fit_params[ich][th]['chi2'] = chisq
        #ax.plot([voltages[0],voltages[-1]],[b+a*voltages[0],b+a*voltages[-1]],
        #        color=colors2[J],linewidth=0.5,linestyle='--')
        ax.plot(voltages,fit_result,color=colors2[J],linewidth=0.5,linestyle='--')
        
        # (2) Fit to points excluding the last:
        popt2, pcov2 = sco.curve_fit(recta,x[:-1],y[:-1])
        a2,b2 = popt2
        fit_params2[ich][th]['a'] = a2
        fit_params2[ich][th]['b'] = b2
        fit_result2 = recta(np.array(voltages[:-1]),a2,b2)
        dof2 = len(y[:-1]) - 2
        chisq2 = sum([(yi-fiti)**2/fiti for (yi,fiti) in zip(y[:-1],fit_result2)])
        fit_params[ich][th]['chi2'] = chisq2
        ax.plot(voltages[:-1],fit_result2,color=colors2[J],linewidth=0.5,linestyle='--')
        
        chi_str = (' %5.1e %5.1e' %(chisq,chisq2))
        ax.plot(x,y,'.-',color=colors2[J],label='Ch'+str(ich)+' '+str(thresholds[J])+' V'+' '+chi_str)
        ax.set_xlabel('Scintillator voltage (V)')
        ax.set_ylabel('Rate of Counts')
        #ax.set_xlim(thresholds[0],thresholds[-1])
        #ax.set_ylim(0,1)
        #ax.grid()
        ax.legend(prop={'size':5})
#plt.show()


# SLOPES VERSUS THRESHOLD
fig3 = plt.figure(3,figsize=(24,9))
fig3.suptitle('Slopes of fits versus threshold')
fig3.subplots_adjust(hspace=0.2,wspace=0.4)

for ich in range(8):
    ax = fig3.add_subplot(2,4,ich+1)
    x = [] ;  ya = [] ;  yb = []
    x2 = [] ;  ya2 = [] ;  yb2 = []
    for th,item in fit_params[ich].items():
        x.append(th)
        ya.append(item['a'])
        yb.append(item['b'])
    for th,item in fit_params2[ich].items():
        x2.append(th)
        ya2.append(item['a'])
        yb2.append(item['b'])
    ax.plot(x,ya,'.-',label='Ch'+str(ich)+str(' slope fit all'))
    #ax.plot(x,yb,'.-',label='Ch'+str(ich)+str(' b'))
    ax.plot(x2,ya2,'.-',label='Ch'+str(ich)+str(' slope fit all -1'))
    ax.set_xlabel('Threshold (ADC)')
    ax.set_ylabel('Rate of Counts')
    ax.set_xlim(thresholds[0],thresholds[-1])
    #ax.set_ylim(0,1e-5)
    #ax.grid()
    ax.legend()
