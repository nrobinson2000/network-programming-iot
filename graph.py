from itertools import count
import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation

x = []
y = []

index = count()

def _plot(i):
	x.append(next(index))
	y.append(random.randint(1,5))

	plt.cla()
	plt.plot(x,y)

livePlot = FuncAnimation(plt.gcf(),_plot,interval = 1000)

plt.tight_layout()
plt.show()
