import tweepy
import json
import random
import os
from boto.s3.connection import S3Connection


# Twitter authentication
auth = tweepy.OAuthHandler(S3Connection(os.environ['CONSUMER_KEY']), S3Connection(os.environ['CONSUMER_SECRET_KEY']))
auth.set_access_token(S3Connection(os.environ['ACCESS_TOKEN']), S3Connection(os.environ['ACCESS_SECRET_TOKEN']))

api = tweepy.API(auth)

try: 
	api.verify_credentials()
	print("Authentication Successful")
except:
	print("Authentication Error")
	
# Open the json file
with open('recommendations.json') as f:
	data = json.load(f)
	
# Generate a random value to choose a recommendation
recommendation = 0
index = set(range(len(data)))
print(index)
while data[recommendation]['appeared'] == "True" and len(index) > 0:
	recommendation = int(random.sample(index, 1)[0])
	index.remove(recommendation)
	
if len(index) == 0 and data[recommendation]['appeared'] == "True":
	print("No hay :(")
	for i in range(len(data)):
		print(i)
		data[i]['appeared'] = "False"
	recommendation = int(random.uniform(0,len(data)))
	
if data[recommendation]['appeared'] == "False":
	data[recommendation]['appeared'] = "True"
		
# Rewrite the file to change the status of the chosen recommendation
with open('recommendations.json', 'w') as f:
	f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',',': ')))
	
msg = f"The recommendation of the day is a {data[recommendation]['type']} named {data[recommendation]['title']}. {data[recommendation]['plot']}."
			
api.update_status_with_media(msg, data[recommendation]['img'])

