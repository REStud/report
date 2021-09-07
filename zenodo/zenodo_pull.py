#need an empirical distribution of download and view numbers for zenodo packages
import requests
import json

class Zenodo(object):
    URL = f'https://zenodo.org/api/records/'
    def __init__(self, id):
        self.id = id
        self.meta = requests.get(self.__class__.URL + f'/{self.id}').json()
        self.version = int(self.meta['metadata']['relations']['version'][0]['index']) + 1
        self.num_versions = int(self.meta['metadata']['relations']['version'][0]['count'])

if __name__== '__main__':
    zenodo = Zenodo(5338362)
    print(zenodo.meta)