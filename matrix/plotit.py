from _threading_local import local
import csv
import itertools
import numpy as np
import matplotlib.pyplot as plt

#pasta:
def errorfill(x, y, yerr, name, color=None, alpha_fill=0.3, ax=None):
    ax = ax if ax is not None else plt.gca()
    if color is None:
        color = ax._get_lines.color_cycle.next()
    if np.isscalar(yerr) or len(yerr) == len(y):
        ymin = y - yerr
        ymax = y + yerr
    elif len(yerr) == 2:
        ymin, ymax = yerr
    ax.plot(x, y, color=color, label=name)
    ax.fill_between(x, ymax, ymin, color=color, alpha=alpha_fill)


def generator(plotname, filedir):
    lines = []
    series = []
    averages = []
    stddev = []

    with open(filedir) as plik:
        for line in csv.reader(plik, delimiter=' '):
            lines.append(map(float, line))  #floaty
    #print "wiersze:", lines
    #print "kolumny:"
    for column in itertools.izip(*lines):
        avg = np.average(column[1:])  #srednia bez serii
        std = np.std(column[1:])
        series.append(column[0])
        averages.append(avg)
        stddev.append(std)
    #print column[1:]        #bez serii danych
    #print srednia
    #print odchylenie
    #print seria

    #plt.errorbar(series,averages,std,label=plotname)

    errorfill(series, averages, std, plotname)
    plt.title('Hamiltonian. N = 15')
    plt.ylabel('Execution time [s]')
    plt.xlabel('Saturation ratio')
    plt.ylim([0,max(averages)*1.07])
    plt.yscale('linear')
    plt.legend(loc=2)

#print series
#print averages
#print stddev


generator('Single', 'hamilton_Single_15')
generator('Multiple', 'hamilton_Multi_15')
plt.savefig('hamiltonian_15.png')
plt.show()

