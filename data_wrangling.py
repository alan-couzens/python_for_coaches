#!usr/bin/env python

#Import the pandas library and call it pd
import pandas as pd

#Read the 'workouts.csv' that we exported from Training Peaks & list the column names
df = pd.read_csv('workouts.csv')
list(df.columns)

#Print the contents of the column called Title
print(df['Title'])

#Print the title of the 50th workout in the export
print(df['Title'][49])

#Read the 'metrics.csv' that we exported from Training Peaks (contains HRV data, sleep data, fatigue, soreness etc.)
metrics_df = pd.read_csv('metrics.csv')
print(metrics_df)

#Reformat so that we have all of the different metric types as individual columns across the top and each day as a row.
#Initially trying it on just the HRV metrics
HRV = metrics_df[metrics_df.Type=='HRV']
HRV = HRV.set_index('Timestamp')
HRV = HRV.drop('Type', axis=1)
HRV = HRV.rename(columns={'Value':'HRV'})
print(HRV)

#After seeing that it works, we built a function to apply it to the other metrics
def build_series(metric):
  new_df = metrics_df[metrics_df.Type==str(metric)]
  new_df = new_df.set_index('Timestamp')
  new_df = new_df.drop('Type', axis=1)
  new_df = new_df.rename(columns={'Value':str(metric)})
  return new_df 

HRV = build_series('HRV')
pulse = build_series('Pulse')
stress = build_series('Stress')
sleep_quality = build_series('Sleep Qualilty')
sleep_hours = build_series('Sleep Hours')
mood = build_series('Mood')
new_improved_metrics = pd.concat([HRV, pulse, stress, sleep_quality, sleep_hours, mood], axis=1)
print(new_improved_metrics)

#Back to the workouts csv to sum up the total training load (TSS) for each day so that we can add it to the same sheet as our metrics
workouts_df = pd.read_csv('workouts.csv')
TSS_day = workouts_df.groupby(['WorkoutDay'])['TSS'].sum()
print(TSS_day)

#Changing the index on our metrics csv so that it matches the same index as the workouts.csv
new_improved_metrics['Date'] = new_improved_metrics.index
new_improved_metrics['Date'].astype(str)
new_improved_metrics['Date'] = new_improved_metrics['Date'].str.slice(0,10)
print(new_improved_metrics['Date'])
new_improved_metrics = new_improved_metrics.set_index('Date')

#Joining the two dataframes together so we now have daily training load added to our metrics spreadsheet
new_improved_metrics = pd.concat([TSS_day, new_improved_metrics], axis=1)
print(new_improved_metrics)

#Visualizing what our dataframe fields consist of (type & count of data for each)
new_improved_metrics.info()

#Changing the data type from a string to a float (decimal number) so that we can perform some math on it.
metrics = ['HRV', 'Pulse', 'Stress', 'Sleep Qualilty', 'Sleep Hours', 'Mood']
for metric in metrics:
  new_improved_metrics[metric] = new_improved_metrics[metric].astype(float)
new_improved_metrics.info()

#Performing some of that math - getting basic statistics on our data
new_improved_metrics.describe()

#Visualizing a frequency histogram for each of our data fields - on the lookout for weirdness/outliers.
import matplotlib.pyplot as plt
new_improved_metrics.hist(figsize=(20,15))
plt.show()

#Adding a new field that gets the training load from yesterday (as it is more likely to have an effect on our metrics for today)
new_improved_metrics['yesterday_TSS'] = new_improved_metrics['TSS'].shift(1)
print(new_improved_metrics)

#Visualizing the correlations between HRV and all of the other features
corr_matrix = new_improved_metrics.corr()
corr_matrix['HRV'].sort_values(ascending=False)

#Adding long term training load metrics - CTL, ATL, TSB to our dataframe.
import math
def calc_ctl(TSS:list, start_ctl, exponent):
  ctl = [start_ctl]
  for i in range(len(TSS)):
    ctl_value = TSS[i] * (1-math.exp(-1/exponent)) + ctl[-1] * math.exp(-1/exponent)
    ctl.append(ctl_value)
  return ctl
ctl = calc_ctl(new_improved_metrics['TSS'], 103, 42)
atl = calc_ctl(new_improved_metrics['TSS'], 50, 7)
tsb = []
for i in range(len(ctl)):
  tsb.append(ctl[i]-atl[i])
print(ctl)
print(atl)
print(tsb)
new_improved_metrics['ctl'] = ctl[1:]
new_improved_metrics['atl'] = atl[1:]
new_improved_metrics['tsb'] = tsb[1:]
print(new_improved_metrics)

#Visualizing statistics for these new metrics
new_improved_metrics.describe()

#Visualizing correlations for these new metrics
corr_matrix = new_improved_metrics.corr()
corr_matrix['HRV'].sort_values(ascending=False)

#Exporting our new, improved dataframe to a new improved csv so that we can apply the data to some machine learning in future posts.
new_improved_metrics.to_csv('new_improved_metrics.csv')











