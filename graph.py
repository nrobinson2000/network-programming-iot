from itertools import count
import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation

x = []
y1 = []
y2 = []

index = count()

def _plot(i):
	x.append(next(index))
	y1.append(random.randrange(1,10,1))
	y2.append(random.randrange(1,10,1))

	plt.cla()
	plt.plot(x,y1,label = 'Temperature')
	plt.plot(x,y2,label = 'Moisture')
	plt.legend(loc = 'upper right') 

livePlot = FuncAnimation(plt.gcf(),_plot,interval = 1000*2)

plt.tight_layout()

plt.show()
