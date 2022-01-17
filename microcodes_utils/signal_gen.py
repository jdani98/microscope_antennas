#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 13:14:52 2021
@author: daniel

ARTIFICIAL SIGNAL GENERATOR
"""

import numpy as np
import matplotlib.pyplot as plt
import random as rnd
import os
import struct

#def white_noise()

def gauss_sine_pulse(n,f,bl,A,x0,s):
    x = np.arange(0,4*n,4)
    gaussian = np.exp(-(x-x0)**2/(2*s**2))
    sinusoid = np.sin(2*np.pi*f*(x-x0))
    return x, bl + A*gaussian*sinusoid

# GENERADOR DE SEÑALES ARTIFICIALES
nsamp = 1030
nev   = 10000
basel = 2**13
rango = 2**14

channel_stds = [3100,2350,250,2900,100,2200,2750,2600]
total_delays = [516.5, 514.8, 343.,  343.,  226.5, 224.7, 149.,  147.2] 

white_noise = [basel + 3000*(2*rnd.random()-1) for i in range(nsamp)]
x, pulso = gauss_sine_pulse(nsamp,0.05,2**13,3000,201,20)
#plt.plot(x,white_noise,linewidth=0.5,linestyle='solid',color='cyan')
# Hemos comprobado el teorema de Nyquist: para frecuencias altas, no se recupera la señal de entrada
#plt.plot(x,pulso,linewidth=0.5,linestyle='solid',color='r')
#plt.plot(x,white_noise+pulso-basel,color='purple')


# VAMOS A GENERAR EVENTOS EN OCHO CANALES, CON PULSO SOLO EN ALGUNOS EVENTOS
directory = 'DATA/Artificial_signal10000_h'
os.mkdir(directory)
events_with_peak = [20,40,69,101,534,1098,5003,7689]
for ch in range(8):
    fichero = open(directory+'/wave'+str(ch)+'.dat','wb')
    for ev in range(nev):
        WNA = 1.0 * channel_stds[ch] # white noise amplitude
        PA  = 1.5 * channel_stds[ch] + 0.05 * channel_stds[ch] * (2*rnd.random()-1) # pulse amplitude
        Pw  = 30 + 4*(2*rnd.random()-1) # pulse width
        x0  = nsamp*2 + Pw/2 + total_delays[ch] + 4*(2*rnd.random()-1) # center of the pulse
        f   = 0.05 + 0.005*(2*rnd.random()-1) # frequency of the pulse
        white_noise = [basel + WNA*(2*rnd.random()-1) for i in range(nsamp)]
        if ev in events_with_peak:
            x, pulso = gauss_sine_pulse(nsamp,f,basel,PA,x0,Pw)
            pulso_total = [int(white_noise[i]+pulso[i]) - basel for i in range(nsamp)]
            #plt.figure(ev)
            #plt.plot(x,pulso_total,linewidth=0.5)
        else:
            x = np.arange(0,4*nsamp,4)
            pulso_total = [int(white_noise[i]) for i in range(nsamp)]
            
        for number in pulso_total:
            fichero.write(struct.pack('h',number))
    fichero.close()