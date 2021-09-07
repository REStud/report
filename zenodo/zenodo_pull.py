#need an empirical distribution of download and view numbers for zenodo packages
import requests
import json
import csv
import time
class Zenodo(object):
    URL = f'https://zenodo.org/api/records/'
    def __init__(self, id):
        self.id = id
        self.meta = requests.get(self.__class__.URL + f'/{self.id}').json()


def main():
    with open('zenodoid.json', 'r') as json_file:
            json_data = json.load(json_file)

    zenodo_data = {'zenodoid': "", 'downloads': "", 'unique_downloads': "", 'views': "", 'unique_views': "", 'revisions':""}
    zenodo = csv.DictWriter(open('zenodo_data.csv','w'), fieldnames=list(zenodo_data.keys()))
    zenodo.writeheader()

    for i in range(len(json_data)):
        zenodoid = json_data[i]['zenodoid']
        print(i)
        zenodo_pack = Zenodo(zenodoid)
        zenodo_data['zenodoid'] = zenodoid
        zenodo_data['downloads'] = zenodo_pack.meta['stats']['downloads']
        zenodo_data['unique_downloads'] = zenodo_pack.meta['stats']['unique_downloads']
        zenodo_data['views'] = zenodo_pack.meta['stats']['views']
        zenodo_data['unique_views'] = zenodo_pack.meta['stats']['unique_views']
        zenodo_data['revisions'] = zenodo_pack.meta['revision']
        zenodo.writerow(zenodo_data)

        # The api calls are limited to 60/min therefore we have to wait before continue.
        if (i+1)%60 == 0:
            time.sleep(65)
        else :
            pass


if __name__== '__main__':
    main()