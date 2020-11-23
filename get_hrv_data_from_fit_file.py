#!/usr/bin/env python

#Import libraries
import numpy as np
from fitparse import FitFile
import plotly.graph_objects as go


#Instantiate our HRV file
fit_file = FitFile('my_hrv_file.fit')

#Print out our HRV data
for record in fit_file.get_messages('hrv'):
        for record_data in record:
          print(record_data)

#Put out HRV RR interval data into one big list called RRs
RRs = []
for record in fit_file.get_messages('hrv'):
        for record_data in record:
          for RR_interval in record_data.value:
            if RR_interval is not None:
              RRs.append(RR_interval)
print(RRs)

#Plot our RR data
x = []
total = 0
for i in range(len(RRs)):
  total = total+RRs[i]
  x.append(total)
fig = go.Figure(data=go.Scatter(x=x, y=RRs))
fig.show()

#Remove interference and ectopic beats from our data
filtered_RRs = []
for i in range(len(RRs)):
  if RRs[(i-1)]*0.75 < RRs[i] < RRs[(i-1)]*1.25:
    filtered_RRs.append(RRs[i])
print(filtered_RRs)

#Plot our filtered data
x = []
total = 0
for i in range(len(filtered_RRs)):
  total = total+filtered_RRs[i]
  x.append(total)
fig = go.Figure(data=go.Scatter(x=x, y=filtered_RRs))
fig.show()

#Remove the standing part of the test
laying_down_bit = []
totals = 0
for i in range(len(filtered_RRs)):
  totals = totals + filtered_RRs[i]
  if totals < 60:
    laying_down_bit.append(filtered_RRs[i])
print(laying_down_bit)

#Build a function to plot the list of HRV values and pass my list of supine only values to the function
def plot_my_list(my_list):
  x = []
  total = 0
  for i in range(len(my_list)):
    total = total+my_list[i]
    x.append(total)
  fig = go.Figure(data=go.Scatter(x=x, y=my_list))
  fig.show()
plot_my_list(laying_down_bit)

#Convert the RR intervals to milliseconds (ms)
laying_down_bit_ms = []
for i in range(len(laying_down_bit)):
  laying_down_bit_ms.append(laying_down_bit[i] * 1000)
print(laying_down_bit_ms)

#Do the same thing as above but more efficiently with a list comprehension
laying_down_bit_ms = [RR_interval * 1000 for RR_interval in laying_down_bit]
print(laying_down_bit_ms)

#Calculate SDNN
SDNN = np.std(laying_down_bit_ms)
print(SDNN)

#Calculate successive differences, i.e. the SD part in rmsSD
successive_differences = [laying_down_bit_ms[i+1] - laying_down_bit_ms[i] for i in range(len(laying_down_bit_ms)-1)]
print(successive_differences)

#Calculate squared successive differences, i.e. the SSD part in rmSSD
squared_successive_differences = [successive_difference**2 for successive_difference in successive_differences]
print(squared_successive_differences)

#Calculate the mean of the squared successive differences (rMSSD)
mean = np.mean(squared_successive_differences)
print(mean)

#Calculate the root of the mean squared successive differences
rMSSD = mean**0.5
print(rMSSD)




