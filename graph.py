from itertools import count
import matplotlib.pyplot as plt
import random
import numpy as np
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
	_all.plot(time,t,label = 'Temperature', color = 'red')
	_all.plot(time,b,label = 'Brightness', color = 'orange')
	_all.plot(time,m,label = 'Moisture', color = 'blue')
	_all.set_title('Everything')
	_all.legend(framealpha = 0.2, loc = 'upper right', prop = {'size': 6})
	if (len(time)>=16):
		_all.set_xlim(len(time)-17,len(time)-1)
		_all.set_xticks(range(len(time)-17,len(time)))
	
	_all.grid()

def _plot(axes,x,y,name,_color):
	axes.cla()
	axes.plot(x,y,color = _color)
	axes.set_title(name+': '+str(y[len(y)-1]))
	axes.set_xlabel('Time')
	axes.set_ylabel(name)
	if (len(x)>=10):
		axes.set_xlim(len(x)-11,len(x)-1)
		axes.set_xticks(range(len(x)-11,len(x)))
	

fig = plt.figure()
fig.set_size_inches(11, 6)

temp = fig.add_subplot(2,3,4)
moist = fig.add_subplot(2,3,5)
bright = fig.add_subplot(2,3,6)
_all = fig.add_subplot(2,2,1)
fig.text(10,10,s = 'testing text', fontsize = 13) 


plt.tight_layout()
plt.subplots_adjust(top=0.9, hspace = 0.4,left=0.05,right=0.95)

time = [] #time
b = [] #brightness
t = [] #temperature
m = [] #moisture
index = count()

livePlot = FuncAnimation(fig,makePlot,interval = 1000*1)
plt.show()
