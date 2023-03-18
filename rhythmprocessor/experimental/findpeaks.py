import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def random():
    #defining the x and y arrays
    x = np.linspace(0,10, 100)
    y = x*np.random.randn(100)**2

    #Find peaks
    peaks = find_peaks(y, height = 1, threshold = 1, distance = 1)
    height = peaks[1]['peak_heights'] #list of the heights of the peaks
    peak_pos = x[peaks[0]] #list of the peaks positions

    #Finding the minima
    y2 = y*-1
    minima = find_peaks(y2)
    min_pos = x[minima[0]] #list of the minima positions
    min_height = y2[minima[0]] #list of the mirrored minima heights

    #Plotting
    fig = plt.figure()
    ax = fig.subplots()
    ax.plot(x,y)
    ax.scatter(peak_pos, height, color = 'r', s = 15, marker = 'D', label = 'Maxima')
    ax.scatter(min_pos, min_height*-1, color = 'gold', s = 15, marker = 'X', label = 'Minima')
    ax.legend()
    ax.grid()
    plt.show()
