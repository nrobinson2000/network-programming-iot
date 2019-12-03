from itertools import count
import matplotlib.pyplot as plt
import random
import json
from matplotlib.animation import FuncAnimation

def makePlot(i):
	time.append(next(index))
	
	b.append(random.randrange(1,10,1))
	t.append(random.randrange(1,10,1))
	m.append(random.randrange(1,10,1))
	
	_plot(axes=temp,x=time,y=t,name = 'Temperature',_color='red')
	_plot(axes=bright,x=time,y=b,name = 'Brightness',_color= 'orange')
	_plot(axes=moist,x=time,y=m,name = 'Moisture',_color= 'blue')


	_all.cla()
	_all.plot(time,t,label = 'Temperature', color = 'blue')
	_all.plot(time,b,label = 'Brightness', color = 'red')
	_all.plot(time,m,label = 'Moisture', color = 'green')
	_all.set_title('Everything')
	_all.legend(framealpha = 0.2, loc = 'upper right', prop = {'size': 6})


def _plot(axes,x,y,name,_color):
	axes.cla()
	axes.plot(x,y,color = _color)
	axes.set_title(name)


fig = plt.figure()
fig.set_size_inches(11, 6)

temp = fig.add_subplot(2,2,1)
moist = fig.add_subplot(2,2,2)
bright = fig.add_subplot(2,2,3)
_all = fig.add_subplot(2,2,4)

plt.tight_layout()
plt.subplots_adjust(top=0.9, hspace = 0.4)

time = [] #time
b = [] #brightness
t = [] #temperature
m = [] #moisture
index = count()

livePlot = FuncAnimation(plt.gcf(),makePlot,interval = 1000*1)
plt.show()
