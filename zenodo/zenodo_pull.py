import os
import csv
from datetime import datetime
import requests

FIELDS = 'id created revision stats/downloads stats/views stats/unique_downloads stats/unique_views'.split()

def get_field(json, field):
    subtree = json
    for part in field.split('/'):
        subtree = subtree[part]
    return subtree

def filter_fields(json, fields):
    return {key.split('/')[-1]: get_field(json, key) for key in fields}

def get_collection(collection):
    url = 'https://zenodo.org/api/records'
    params = {'communities': collection, 'size': 100, 'page': 1}
    headers = {'User-Agent': 'restud-report-zenodo-pull'}
    
    # Add authentication if token is available
    token = os.environ.get('ZENODO_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    rows = []
    while True:
        r = requests.get(url, params=params, headers=headers, timeout=60)
        if not r.ok:
            raise RuntimeError(f'Zenodo API error {r.status_code}: {r.text[:500]}')
        hits = r.json()['hits']['hits']
        if not hits:
            break
        rows += [filter_fields(row, FIELDS) for row in hits]
        if len(hits) < params['size']:
            break
        params['page'] += 1
    return rows

def main():
    zenodo_data = get_collection('restud-replication')
    fname = 'zenodo_data.csv'
    current_time = datetime.now().isoformat()
    fieldnames = list(zenodo_data[0].keys()) + ['update_time']
    new_file = not os.path.exists(fname)
    with open(fname, 'at', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if new_file:
            writer.writeheader()
        for row in zenodo_data:
            row['update_time'] = current_time
            writer.writerow(row)

if __name__ == '__main__':
    main()#need an empirical distribution of download and view numbers for zenodo packages
import os
from datetime import datetime
import requests
import csv
FIELDS = 'id created revision stats/downloads stats/views stats/unique_downloads stats/unique_views'.split()

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
    fname = 'zenodo_data_test.csv'
    current_time = datetime.now().isoformat()
    if not os.path.exists(fname):
        zenodo = csv.DictWriter(open(fname,'wt'), fieldnames=list(zenodo_data[0].keys()) + ['update_time'])
        zenodo.writeheader()
    else:    
        zenodo = csv.DictWriter(open(fname,'at'), fieldnames=list(zenodo_data[0].keys()) + ['update_time'])
    for row in zenodo_data:
        row['update_time'] = current_time
        zenodo.writerow(row)


if __name__== '__main__':
    main()
