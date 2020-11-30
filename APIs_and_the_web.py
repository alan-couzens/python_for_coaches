#!/usr/bin/env python

#Introducing the requests library by pulling Slowtwitch's home page
import requests
response = requests.get('https://www.slowtwitch.com')
print(response.text)

#Introducing simple open API's - coindesk returns current bitcoin price in json format
response = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
print(response.text)

#Getting data from Strava's API (after signing up) 
# a) get the access token
response = requests.post(
    url = 'https://www.strava.com/oauth/token',
    data = {'client_id':YOUR_CLIENT_ID,
            'client_secret':'YOUR_CLIENT_SECRET',
            'code':'YOUR_CODE',
            'grant_type':'authorization_code'})
print(response.text)
# b) pass your access token to an API call
response = requests.get("https://www.strava.com/api/v3/athlete/activities?access_token=YOUR_ACCESS_TOKEN")
print(response.text)

#Login to Strava programatically
# a) Find the authenticity token
session = requests.Session()
login_response = session.get('https://strava.com/login')
print(login_response.text)
from bs4 import BeautifulSoup
soup = BeautifulSoup(login_response.text)
token = soup.find('input', {'name': 'authenticity_token'}).get('value')
print(f"Token {token}")
# b) Pass your login details and the token to Strava
response = session.post('https://www.strava.com/session', data={'email':'YOUR_EMAIL', 'password':'YOUR_PASSWORD', 'authenticity_token': token})
print(response)

#Get power data from one of Cam's rides
response = session.get('https://www.strava.com/activities/4385737177/power_data')
power_data = response.text
print(power_data)

#Get all of the cadence data from the same ride
response = session.get('https://www.strava.com/activities/4385737177/streams?stream_types%5B%5D=cadence')
print(response.text)

#Convert the json formatted ride data to a Python dictionary
import json
power_data_dictionary = json.loads(power_data)
print(power_data_dictionary['weighted_power'])

#Get all of Cam's rides with power for the past year
response = session.get('https://www.strava.com/athletes/430673#interval?interval=201922&interval_type=week&chart_type=miles&year_offset=0')
print(response.text)

#Get all activity name locations in the html text above
def get_location_of_string_in_response_text(string, response):
  activity_indices = [i for i in range(len(response.text)) if response.text.startswith(string, i)]
  return activity_indices
activity_indices = get_location_of_string_in_response_text('activity_id', response)
print(activity_indices)

#Get the corresponding activity number from each of these locations
def get_activity_ids(response, activity_indices):
  activity_ids = []
  for activity in activity_indices:
    if response.text[activity+13:activity+23] not in activity_ids:
      activity_ids.append(response.text[activity+13:activity+23])
  return activity_ids
activity_ids = get_activity_ids(response, activity_indices)
print(activity_ids)

#Get the power stats from each of these activities
def get_power_stats_from_each_activity(activity_ids):
  power_stats = []
  activities_with_power = []
  for i in range(len(activity_ids)):
    url = f"https://www.strava.com/activities/{activity_ids[i]}/power_data"
    response = session.get(url)
    if (response.text not in power_stats) and (len(response.text)>1):
      stats_dictionary = json.loads(response.text)
      stats_dictionary['activity_id'] = activity_ids[i]
      power_stats.append(stats_dictionary)
  return power_stats
power_stats = get_power_stats_from_each_activity(activity_ids)
for stat in power_stats:
  print(stat)

#Find the date for each of these activities and add it to the activity dictionary for the ride
def find_date_of_workout(activity_id):
  response = session.get(f"https://www.strava.com/activities/{activity_id}")
  soup = BeautifulSoup(response.text, features="lxml")
  workout_date = soup.find('time').getText()
  workout_date = workout_date.strip('\n')
  return workout_date
find_date_of_workout('4404163137')
for workout in power_stats:
  date = find_date_of_workout(workout['activity_id'])
  workout['date'] = date
print(power_stats)

#Save all of our data to a csv file (spreadsheet)
import csv

our_spreadsheet = open('our_spreadsheet.csv', 'w', newline='')
output_writer = csv.writer(our_spreadsheet)
headers = power_stats[0].keys()
output_writer.writerow(headers)
for workout in power_stats:
  output_writer.writerow(workout.values())




