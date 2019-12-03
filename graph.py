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

	plotIndividual()
	plotAll()
	plotText()
	
def plotText():
	txt.cla()
	txt.text(0.1,0.95,"[Temperature]", fontsize = 10)
	txt.text(0.4,0.95,"Mean: "+str(np.round(np.mean(t),decimals=2)))
	txt.text(0.4,0.85,"Standard Deviation: "+str(np.round(np.std(t),decimals=2)), fontsize = 10)

	txt.text(0.1,0.6,"[Brightness]", fontsize = 10)
	txt.text(0.4,0.6,"Mean: "+str(np.round(np.mean(b),decimals=2)))
	txt.text(0.4,0.5,"Standard Deviation: "+str(np.round(np.std(b),decimals=2)), fontsize = 10)

	txt.text(0.1,0.25,"[Moisture]", fontsize = 10)
	txt.text(0.4,0.25,"Mean: "+str(np.round(np.mean(m),decimals=2)))
	txt.text(0.4,0.1,"Standard Deviation: "+str(np.round(np.std(m),decimals=2)), fontsize = 10)

def plotIndividual():
	_plot(axes=temp,x=time,y=t,name = 'Temperature',_color='red')
	_plot(axes=bright,x=time,y=b,name = 'Brightness',_color= 'orange')
	_plot(axes=moist,x=time,y=m,name = 'Moisture',_color= 'blue')

def plotAll():
	_all.cla()
	_all.plot(time,t,label = 'Temperature', color = 'red')
	_all.plot(time,b,label = 'Brightness', color = 'orange')
	_all.plot(time,m,label = 'Moisture', color = 'blue')
	_all.set_title('Everything')
	_all.legend(loc = (1.01,0.78), prop = {'size': 6})
	if (len(time)>15):
		_all.set_xlim(len(time)-16,len(time)-1)
		_all.set_xticks(range(len(time)-16,len(time)))
	else:
		_all.set_xlim(0,15)
		_all.set_xticks(range(0,16))
	_all.grid()

def _plot(axes,x,y,name,_color):
	axes.cla()
	axes.plot(x,y,color = _color)
	axes.set_title(name+': '+str(y[len(y)-1]))
	axes.set_xlabel('Time')
	axes.set_ylabel(name)
	if (len(x)>10):
		axes.set_xlim(len(x)-11,len(x)-1)
		axes.set_xticks(range(len(x)-11,len(x)))
	else:
		axes.set_xlim(0,10)
		axes.set_xticks(range(0,11))
	axes.grid()
	
def graph():
	livePlot = FuncAnimation(fig,makePlot,interval = 1000*1)
	plt.show()

time = [] #time
b = [] #brightness
t = [] #temperature
m = [] #moisture
index = count()

fig = plt.figure()
fig.set_size_inches(11, 6)
temp = fig.add_subplot(2,3,4)
bright = fig.add_subplot(2,3,5)
moist = fig.add_subplot(2,3,6)
_all = fig.add_subplot(2,2,1)
txt = fig.add_subplot(2,2,2)

txt.get_xaxis().set_visible(False)
txt.get_yaxis().set_visible(False)
for i in txt.spines:
	txt.spines[i].set_visible(False)
plt.subplots_adjust(top=0.9, hspace = 0.4,left=0.05,right=0.95)
graph()