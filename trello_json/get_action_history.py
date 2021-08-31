# This code uses Trello API to get all the action history.
import requests
import json
from argparse import ArgumentParser
from dateutil.parser import isoparse

with open('secrets.json', 'r') as secrets:
	keys = json.load(secrets)

key = keys['key']
token = keys['token']

def create_query(time):
	url = "https://api.trello.com/1/boards/7YNdeENt/actions"
	query = {
	'key': key,
	'token': token,
	'filter': 'updateCard,createCard',
	'actions_limit': '1000',
	'before': time,
	}
	return url,query

def create_response(url,query):
	response = requests.request("GET", url,params=query)
	return response.text

def main():
	ap = ArgumentParser()
	ap.add_argument("-t", "--today", required=True, help="Today's date in ISO-Formatted Date eg.:2021-08-31T08:00:00.977.")
	ap.add_argument("-s", "--since", required=True, help="The last date you want in the query in ISO-Formatted Date eg.:2020-08-01T08:00:00.977.")
	today = vars(ap.parse_args())['today']
	since = vars(ap.parse_args())['since']
	
	url, query = create_query(today)
	file = create_response(url,query)
	last_date = json.loads(file)[-1]['date'].rstrip('Z')
	
	while isoparse(last_date) > isoparse(since):
		url, query = create_query(last_date)
		aux_file = create_response(url,query)
		file = file.rstrip(']') + ',' + aux_file.lstrip('[')
		last_date = json.loads(aux_file)[-1]['date'].rstrip('Z')
		print(last_date)
	
	
	with open("actions.json", "w") as table:
		table.write(file)

if __name__ =='__main__':
	main()

