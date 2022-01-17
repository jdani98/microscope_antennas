#!usr/bin/python3
"""
Date of creation: Wed  6 Oct 2021
# Author: Jose Daniel Viqueira Cao
#         josedaniel.viqueira@rai.usc.es
# Project: ANALYSING DATA FROM AN ARRAY OF ANTENNAS
"""

"""
INSTRUCTIONS:
Program prepared to read files with name formatted as 'filter[f]_r[r]_(no)sparks.txt', where [f]
is the number of filter (1,2,3 or 4) and [r] the number of ring 1 or 2).
If name format is different, change lines > nfilter = int(fname[6]) >nring   = int(fname[9])
> Ch = 2*(nfilter-1) + (nring-1)

It divides all the samples in several groups with <Nevents> each one, being each event a set of
<nsamp> samples. For each group, it returns the mean, std, max and min (simple stats) of the
samples and the gaussian parameters from a fit to the points of the histogram (gaussian).

=> In CONFIGURATION (variable 'options'):
   * fname: Name of file to read the data
   * outname: Name of file to write the outputs: simple statistics and gaussian parameters. New 
     data are appended to previous. Two files are created: one .txt and one .csv
   * options:
       - in_dir: directory to work, where input file is read and outputs are written
       - ADC_ch: number of ADC channels of the digitizer
       - deltaT: time between successive samples in nanoseconds, see specifications of digitizer
       - Vpp: voltage peak-peak set in the digitizer
       - ngroups: number of groups of events to generate.Can be string to stay as free parameter
         provided that <Nevents> is a integer.
       - Nevents: number of events per group. Can be string to stay as free parameter provided
         that <ngroups> is a integer.
       - Show_plots: True to show plots of histograms
"""

import os
os.chdir('..')
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sco
import os
from collections import Counter
import csv

import microcodes_modules.functions as fc

### CONFIGURATION #############################################################
fname = 'wave0.dat'  # FILENAME
outname = 'summary'
nbins = 2**7

options = {	'in_dir':		'prueba_ext_211001_14h',
			'ADC_ch':		int(2**14),
			'nsamp':		1030,
            'deltaT':       4,
            'Vpp':          0.5,
            'ngroups':      1,
            'Nevents':      'ind',
            'Show_plots':   True,
            'Save_stats':   False
			}
###############################################################################


cwd = os.getcwd()  # main current working directory
os.chdir(cwd+'/'+'DATA/'+options['in_dir'])
list_dir = os.listdir()

Ch = int(fname[4])

g = 0
i = 0
ng = options['ngroups']
Ne = options['Nevents']

print("Number of bins: ", nbins)


print(' Reading file ' + fname + '...')
if fname[-4:] == '.txt':
    file = open(fname)
    data = [int(row[:-1]) for row in file]
    file.close()
if fname[-4:] == '.dat':
    data  = np.fromfile(fname, dtype='<i2')


if type(ng) == str:
    i = len(data)
    Ns = Ne*options['nsamp']
    ng=i//Ns
    print(' Number of lines in file:', i)
    print(' Number of groups automatically set to '+str(ng))

if type(Ne) == str:
    i = len(data)
    Ne=i//(ng*options['nsamp'])
    print(' Number of lines in file:', i)
    print(' Number of events per group automatically set to '+str(Ne))

Ns = Ne*options['nsamp']

#####################################################
DATA = []
i=0
for line in data:
    if i%Ns == 0:
        g+=1
        if g>ng: break
        print('Group '+str(g)+' created')
        DATA.append([])
    DATA[g-1].append(line)
    i+=1
#####################################################


colors = ['b','g','r','c','m','y','k','tab:gray']

def gaussian(x,A,x0,sgm):
	return A*np.exp(-(x-x0)**2/(2*sgm**2))

if options['Save_stats']:
	file2 = open(outname+'.txt',"a")
	header = ('\n \n# STATISTICS OF FILE '+str(fname))
	parheader = ('\n# ADC_ch: %i, nsamp: %i, deltaT: %.2f, Vpp: %.2f' 
	             %(options['ADC_ch'],options['nsamp'],options['deltaT'],options['Vpp']))
	tag =       ('\n#--------------Simple statistics-------------------|----------Gaussian----------')
	subheader = ('\n#    Gr  Ch     N     MEAN     STD     MAX    MIN  |   A         X0     SIGMA   ')
	file2.write(header+parheader+tag+subheader)

	file3 = open(outname+'.csv',"a")
	writer = csv.writer(file3)


plt.close('all')
for i,group in enumerate(DATA):
	counts = Counter(group)
	rango  = np.arange(0,options['ADC_ch'])
	histo  = np.array([0.]*options['ADC_ch'])
	rango2 = np.array([0.]*nbins)
	histo2 = np.array([0.]*nbins)
	for j in range(len(rango)):
		histo[j] = counts[j]
	
	width = int(options['ADC_ch']/nbins)
	#print(width)
	totalcount = sum(histo)
	#npoints = options['ADC_ch']
	rango2l = fc.agrupar(rango,width)
	rango2 = np.array([np.mean(item) for item in rango2l])
	histo2l = fc.agrupar(histo,width)
	histo2 = np.array([np.mean(item)  for item in histo2l])
	shisto2 = np.array([np.std(item)  for item in histo2l])
	print(len(rango2),len(histo2),len(shisto2))
	#print(shisto2)
	#print(npoints)
	print(sum(histo2))
	
	Norm = sum(histo2)*width
	
	histo2  = histo2/Norm
	shisto2 = shisto2/Norm
	
	print('Norm?: ', sum(histo2)*width)
	
	media = np.mean(group)
	desvs = np.std(group)
	maxim = np.max(group)
	minim = np.min(group)
    #popt, pcov = sco.curve_fit(gaussian, rango,histo, p0 = [max(histo),media,desvs])
	
    #A,x0,sgm = popt
	
	line = ('\n  %5i  %2i  %5i  %7.1f  %7.1f  %5i  %5i' 
	%(i+1,Ch,Ne,media,desvs,maxim,minim))
	
	if options['Save_stats']:
		file2.write(line)
		#writer.writerow([i+1,Ch,Ne,media,desvs,maxim,minim,A,x0,sgm])
		writer.writerow([i+1,Ch,Ne,media,desvs,maxim,minim])
	
	if options['Show_plots']:
        #fig = plt.figure('histo_Ch'+str(Ch)+'_Gr'+str(i+1),figsize=(10,8))
		fig, ax = plt.subplots()
		plt.title('Histogram of Ch'+str(Ch)+' g'+str(i+1))
        #plt.plot(rango,histo,'.',color=colors[Ch],label='Ch'+str(Ch))
		#plt.semilogy(rango2,histo2,'.',color=colors[Ch],label='Ch'+str(Ch))
		plt.errorbar(rango2,histo2,yerr=shisto2,marker='.',ls='',color=colors[Ch],ecolor='gray', elinewidth=0.5,label='Ch'+str(Ch))
		#plt.bar(rango2,histo2,64,color=colors[Ch],label='Ch'+str(Ch))
		plt.yscale("log")
        #plt.plot(rango,gaussian(rango,A,x0,sgm),'--',color=colors[Ch-1])
		plt.xlabel('ADC channels')
		plt.ylim(1e-9,1e-3)
    
		header1 = ('SIMPLE STATS \n')
		texto1 = ((' N. events: %i \n' %Ne)+
                  (' Mean: %.1f \n' %media)+
                  (' Std.:  %.1f \n' %desvs)+
                  (' Max.: %i \n' %maxim)+
                  (' Min.: %i \n' %minim))
        
		#header2 = ('\nFIT PARAMS \n')
		#texto2 = ((' $x_0=$ %.1f \n' %x0)+
        #          (' $\sigma=$ %.1f \n' %sgm)+
        #          (' $A=$  %.2f') %A)
		texto = header1+texto1#+header2+texto2
    
		props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
		plt.text(0.78, 0.40, texto, transform=ax.transAxes, fontsize=8, verticalalignment='top', bbox=props)
		plt.legend()
		plt.grid()
        #plt.savefig('histo'+str(Ch)+'A.png')
		plt.savefig('histo'+str(nbins)+'_'+str(Ch)+'.png')
		plt.show()
        #plt.savefig('histo_'+fname[-4]+str(i+1)+'.png')
		
if options['Save_stats']:
	file2.close()
	file3.close()
