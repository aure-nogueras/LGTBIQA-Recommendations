import tweepy
import json
import os
from datetime import date

# Twitter authentication
auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET_KEY'])
auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_SECRET_TOKEN'])

api = tweepy.API(auth)

try: 
	api.verify_credentials()
	print("Authentication Successful")
except:
	print("Authentication Error")
	
# Open the json file
with open('recommendations.json') as f:
	data = json.load(f)
	
# Generate a value to choose a recommendation based in the day of the year
todays_date = date.today()
year = todays_date.year
month = todays_date.month
day = todays_date.day

days_each_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
leap_year = year % 4 == 0

if leap_year:
	days_each_month[1] = 29
	
day_of_the_year = 0	
	
for i in range(0, month-1, 1):
	day_of_the_year += days_each_month[i]
	
day_of_the_year += day

recommendation = day_of_the_year % len(data)

# Message the bot is going to tweet
msg = f"The recommendation of the day is a {data[recommendation]['type']} named {data[recommendation]['title']}. {data[recommendation]['plot']}."

# Tweet			
api.update_status_with_media(msg, data[recommendation]['img'])

