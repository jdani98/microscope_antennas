import numpy as np

def agrupar(X,ngroup):
	return [X[x:x+ngroup] for x in range(0, len(X), ngroup)]


def mean_ch(DAT,ngroup):
	"""
	returns the mean value of each event for all the channels separated
	"""
	mean_ch_DAT = []
	for channel in DAT:
		loe = []
		for event in channel:
			med = sum(event)/ngroup
			loe.append(med)
		mean_ch_DAT.append(loe)
	return mean_ch_DAT


def max_ch(DAT):
	"""
	returns the maximum of each event for all the channels separated
	"""
	max_ch_DAT = []
	for channel in DAT:
		loe = []
		for event in channel:
			maxi = max(event)
			loe.append(maxi)
		max_ch_DAT.append(loe)
	return max_ch_DAT
	

def first_mm(x,n):
    """
    returns the first n maxima and minima of array x
    """
    first_mm = []
    media = np.mean(x)
    desv  = np.abs(x-media)
    for i in range(n):
        imax = np.argmax(desv)
        desv[imax] = 0
        first_mm.append((imax,x[imax]))
    return first_mm


def sqdev(x,mean):
	"""
	'square deviation': square root of sum of square deviations from a given mean value
	"""
	devs = [(xi-mean)**2 for xi in x]
	return np.sqrt(sum(devs)/len(x))
	

def median_method(X,Y,s=3):
	"""
	median method for noise suppression. Y is array with data and s the number of samples to apply
	the median
	"""
	nX = []
	nY = []
	for i in range(s//2,len(Y)-s//2):
		part = Y[i-s//2:i+s//2+1]
		nX.append(X[i])
		nY.append(np.median(part))
	return np.array(nX),np.array(nY)


def half_Hann(y,portion=10,baseline=0):
    """
    Parameters
    ----------
    y : LIST
        Data to which apply half-Hann window.
    portion : FLOAT
        Portion (in percentage!) at the starting and at the end of y at which
        apply half-Hann window. Default: 10. This means that the first 10 per
        cent is atenuated as a sine and the last 10 per cent, the same.

    Returns
    -------
    Attenuated signal in the extremes with sinusoidal form.
    """
    L = len(y)
    l = int((portion/100)*L)
    ini_factor = np.array([0.5*(1-np.cos(i*np.pi/l)) for i in range(l)])
    end_factor = np.array([0.5*(1+np.cos(i*np.pi/l)) for i in range(l)])
    tot_factor = np.array([1.0]*L)
    tot_factor[:l] = ini_factor
    tot_factor[-l:] = end_factor
    y_new = np.array([baseline + tot_factor[i] * (y[i]-baseline) for i in range(L)])
    return y_new
