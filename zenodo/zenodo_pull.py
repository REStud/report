#need an empirical distribution of download and view numbers for zenodo packages
from webbrowser import get
import requests
import json
import csv
import time
class Zenodo(object):
    URL = f'https://zenodo.org/api/records/'
    def __init__(self, id):
        self.id = id
        self.meta = requests.get(self.__class__.URL + f'/{self.id}').json()

FIELDS = 'id revision stats/downloads stats/views stats/unique_downloads stats/unique_views'.split()

def get_field(json, field):
    parts = field.split('/')
    subtree = json
    for part in parts:
        subtree = subtree[part]
    return subtree

def filter_fields(json, fields):
    return {key.split('/')[-1]: get_field(json, key) for key in fields}

def get_collection(collection):
    URL = f'https://zenodo.org/api/records?communities={collection}&size=999'
    data = requests.get(URL).json()
    return [filter_fields(row, FIELDS) for row in data['hits']['hits']]

def main():
    zenodo_data = get_collection('restud-replication')
    zenodo = csv.DictWriter(open('zenodo_data_2022.csv','wt'), fieldnames=list(zenodo_data[0].keys()))
    zenodo.writeheader()
    
    for row in zenodo_data:
        zenodo.writerow(row)


if __name__== '__main__':
    main()