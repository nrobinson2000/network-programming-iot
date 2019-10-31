import numpy as np
import matplotlib.pyplot as plt
import random

def getRandom():
    arr = []
    for i in range(10):
        arr.append(random.randint(i,10))
    return arr

def _plot(x,y):
    plt.plot(x, y)
    plt.show()
 
x = getRandom()
y = getRandom()

_plot(x,y)