import csv
import random
import time
import threading
#import graph as gr

# x_value = 0
# bright = 0
# temp = 0
# humid = 0

# fieldnames = ["Time", "Temperature", "Brightness","Humidity"]


# with open('data.csv', 'w') as csv_file:
#     csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     csv_writer.writeheader()

# while True:

#     with open('data.csv', 'a') as csv_file:
#         csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#         info = {
#             "Time": x_value,
#             "Temperature": temp,
#             "Brightness":bright,
#             "Humidity": humid
#         }

#         csv_writer.writerow(info)
#         print(x_value, temp, bright, humid)

#         x_value += 1
#         temp = random.randint(0, 100)
#         bright = random.randint(0, 100)
#         humid = random.randint(0, 100)
    
#     time.sleep(1)

ti = -1
def getVal():
    return x,temp,bright,humid

def genVal():
    global x,temp,bright,humid,ti
    while True:
        temp.append(random.randint(0, 100))
        bright.append(random.randint(0, 100))
        humid.append(random.randint(0, 100))
        ti+=1
        x.append(ti)
        time.sleep(1)

temp = []
bright = []
humid =[]
x = []
threading.Thread(target=genVal,daemon=True).start()
# while True:
#     a,b,c,d = getVal()
#     print(a,b,c,d)
#     time.sleep(1)

