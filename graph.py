from itertools import count
import matplotlib.pyplot as plt
import random
from matplotlib.animation import FuncAnimation

x = []
b = [] #brightness
t = [] #temperature
m = [] #moisture

index = count()
fig = plt.figure()
fig.set_size_inches(11, 6)
temp = fig.add_subplot(2,2,1)
moist = fig.add_subplot(2,2,2)
bright = fig.add_subplot(2,2,3)
_all = fig.add_subplot(2,2,4)
plt.subplots_adjust(top=0.9, hspace = 0.4)

def makePlot(i):
	x.append(next(index))
	
	b.append(random.randrange(1,10,1))
	t.append(random.randrange(1,10,1))
	m.append(random.randrange(1,10,1))

	temp.cla()
	temp.plot(x,t, color = 'blue')
	temp.set_title('Temperature')

	bright.cla()
	bright.plot(x,b, color = 'red')
	bright.set_title('Brightness')

	moist.cla()
	moist.plot(x,m, color = 'green')
	moist.set_title('Moisture')

	_all.cla()
	_all.plot(x,t,label = 'Temperature', color = 'blue')
	_all.plot(x,b,label = 'Brightness', color = 'red')
	_all.plot(x,m,label = 'Moisture', color = 'green')
	_all.set_title('Everything')
	_all.legend(loc = 'upper right', prop = {'size': 8})

	# _plot(temp,x,t,"Temperature")
	# _plot(bright,x,b,"Brightness")
	# _plot(moist,x,m,"Moisture")
	# plotAll(_all,t,b,m)


def _plot(axes,x,y,name):
	axes.cla()
	axes.plot(x,y,label = name)
	axes.legend(loc = "upper right")

def plotAll(axes,x,y1,y2,y3):
	axes.cla()
	axes.plot(x,y1,label = "Temperature")
	axes.plot(x,y2,label = "Brightness")
	axes.plot(x,y3,label = "Moisture")
	axes.legend(loc = "upper right")

livePlot = FuncAnimation(plt.gcf(),makePlot,interval = 1000*1)

plt.show()
