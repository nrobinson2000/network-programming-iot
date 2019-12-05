import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation

import test
import pyClient as pc

def animate(i):
	global time,t,b,m
	# data = pd.read_csv(fileName)
	# time = data['Time']
	# t = data['Temperature']
	# b = data['Brightness']
	# m = data['Humidity']
	
	# time,t,b,m = test.getVal()
	time,t,b,m = pc.getData()
	plotIndividual()
	plotAll()
	plotText()

#make annotations	
def plotText():
	txt.cla()
	txt.text(0.1,0.95,"[Temperature]", fontsize = 10)
	txt.text(0.4,0.95,"Mean: "+str(np.round(np.mean(t),decimals=2)))
	txt.text(0.4,0.85,"Standard Deviation: "+str(np.round(np.std(t),decimals=2)), fontsize = 10)

	txt.text(0.1,0.6,"[Brightness]", fontsize = 10)
	txt.text(0.4,0.6,"Mean: "+str(np.round(np.mean(b),decimals=2)))
	txt.text(0.4,0.5,"Standard Deviation: "+str(np.round(np.std(b),decimals=2)), fontsize = 10)

	txt.text(0.1,0.25,"[Humidity]", fontsize = 10)
	txt.text(0.4,0.25,"Mean: "+str(np.round(np.mean(m),decimals=2)))
	txt.text(0.4,0.1,"Standard Deviation: "+str(np.round(np.std(m),decimals=2)), fontsize = 10)

#plot each plot individually
def plotIndividual():
	_plot(axes=temp,x=time,y=t,name = 'Temperature',_color='red')
	_plot(axes=bright,x=time,y=b,name = 'Brightness',_color= 'orange')
	_plot(axes=moist,x=time,y=m,name = 'Humidity',_color= 'green')

#plot every plot together 
def plotAll():
	try:
		_all.cla()
		_all.plot(time,t,label = 'Temperature', color = 'red')
		b1=[]
		for i in b:
			b1.append(i/100)
		_all.plot(time,b1,label = 'Brightness \n  1:100', color = 'orange')
		_all.plot(time,m,label = 'Humidity', color = 'green')
		_all.set_title('Everything')
		_all.legend(loc = (1.01,0.715), prop = {'size': 7})
		_all.set_xticks(np.arange(len(time)))
		_all.tick_params(axis = 'x', rotation = -30)
		if (len(time)>7):
			_all.set_xlim(len(time)-8,len(time)-1)
		else:
			_all.set_xlim(0,time[len(time)-1])
		_all.grid()
	except ValueError:
		return

#plot driver
def _plot(axes,x,y,name,_color):
	axes.cla()
	axes.plot(x,y,'o-',color = _color)
	axes.set_title(name+': '+str(y[len(y)-1]))
	axes.set_xlabel('Time')
	axes.set_ylabel(name)
	axes.set_xticks(np.arange(len(x)))
	axes.tick_params(axis = 'x', rotation = -30)
	
	if (len(x)>4):
		axes.set_xlim(len(x)-5,len(x)-1)
	else:
		axes.set_xlim(0,x[len(x)-1])
	axes.grid()
	
def graph(file):
	global fileName
	fileName = file
	livePlot = FuncAnimation(fig,animate,interval = 1000*1)
	plt.show()
	

time = [-1] #time
b = [-100] #brightness
t = [-1] #temperature
m = [-1] #moisture
fileName = ''

plt.style.use('dark_background')
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
plt.subplots_adjust(top=0.95,bottom = 0.18,wspace=0.25, hspace = 0.69,left=0.07,right=0.97)

graph('data.csv')
