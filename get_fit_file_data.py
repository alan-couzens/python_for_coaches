#!/usr/bin/env python

#import the libraries
import matplotlib.pyplot as plt
from fitparse import FitFile

fit_file = FitFile('KonaBike.fit')

#Show all record data from the file.
for record in fit_file.get_messages("record"):
    #Records can contain multiple pieces of data (e.g. timestamp, lat, long etc)
    for data in record:
        #Print the name and value of the data (& the units if it has any)
        if data.units:
            print(f"{data.name}, {data.value}, {data.units}")
        else:
            print(f"{data.name} {data.value}")


#Filter the file to show only power data
for record in fit_file.get_messages("record"):
    # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
    for data in record:
        # Print the name and value of the data (and the units if it has any)
        if data.name == 'power':
            print(f"{data.name}, {data.value}, {data.units}")


#Build a big list of all power numbers for further analysis
power = []
for record in fit_file.get_messages("record"):
    # Records can contain multiple pieces of data (ex: timestamp, latitude, longitude, etc)
    for data in record:
        # Print the name and value of the data (and the units if it has any)
        if data.name == 'power':
            power.append(data.value)
print(power)

#Chart the power data
x = []
for i in range(len(power)):
  x.append(i)

plt.bar(x, power)
plt.show()
