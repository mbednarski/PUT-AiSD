__author__ = 'Mateusz Bednarski'


import prettyplotlib as ppl
from prettyplotlib import brewer2mpl
import matplotlib.pyplot as plt
import numpy as np
from analyzer import guard_percentages, sizes
import matplotlib.ticker as ticker
from matplotlib.colors import LogNorm

filename = 'museum_results'
f2 = 'museum_creations'


purples = brewer2mpl.get_map('Purples', 'Sequential', 9).mpl_colormap
fig, ax = plt.subplots(1)

time_formatter = ticker.FormatStrFormatter('%ds')
y_formatter = ticker.FormatStrFormatter('%.2f%%')

def x_func_format(x, p):
	return str(int(sizes[p]))

data1 = np.loadtxt(filename)
data2 = np.loadtxt(f2)

data = data1 + data2

sizes_integer = [int(i) for i in sizes]
#data = data.transpose()
cb = ppl.pcolormesh(fig, ax, data,
			   cmap=purples,
			   yticklabels=guard_percentages,
			   xticklabels=sizes_integer,
			  # norm=LogNorm(vmin=data.min(), vmax=data.max())
			   )

plt.title('Both phases')
cb.colorbar.set_label('Execution time')
cb.colorbar.formatter = time_formatter
cb.colorbar.update_ticks()
#ax.xaxis.set_major_formatter(ticker.FuncFormatter(x_func_format))
#ax.set_xticks(sizes)
ax.yaxis.set_major_formatter(y_formatter)
ax.set_xlabel('Size')
ax.set_ylabel('Percentage of guards')

plt.savefig('combined.png', facecolor='#BFBFBF')

plt.show()