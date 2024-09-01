import requests

from pallas.asset import Asset

class Downloading:
    def __init__(self, asset:Asset):
        self.asset = asset
        self.url = self.asset.url
    
    def download(self):
        req = requests.get(self.url)
        return req.content
