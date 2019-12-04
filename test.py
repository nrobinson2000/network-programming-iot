import csv
import random
import time
#import graph as gr

x_value = 0
bright = 0
temp = 0
humid = 0

fieldnames = ["Time", "Temperature", "Brightness","Humidity"]


with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:

    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "Time": x_value,
            "Temperature": temp,
            "Brightness":bright,
            "Humidity": humid
        }

        csv_writer.writerow(info)
        print(x_value, temp, bright, humid)

        x_value += 1
        temp = random.randint(0, 100)
        bright = random.randint(0, 100)
        humid = random.randint(0, 100)
    
    time.sleep(1)

