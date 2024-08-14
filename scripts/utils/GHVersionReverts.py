import yaml
import requests

from enum import Enum

"""
Task List
- Build out Repository class
- Finish fetching PRs
- Compare PR files to files in main branch using PyYAML (which I can probably reimplement as-needed)
"""

class RequestType(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"

class ConvertParamsToVars:
    def convert(self, d:dict):
        for key in d:
            self.__setattr__(key, d[key])

class Auth:
    def __init__(self, base_url:str="https://api.github.com", access_token=""):
        self.base_url = base_url
        self.access_token = access_token
        

class Repository(ConvertParamsToVars):
    def __init__(self, auth:Auth=Auth(), name:str="", org:str=""):
        self.name = name
        self.org = org
        self.headers = {
            "Authorization": f"Bearer {auth.access_token}"
        }
        req = requests.get(f"{auth.base_url}/repos/{org}/{name}", headers=self.headers)
        if req.status_code == 200:
            self.convert(req.json())
        else:
            raise Exception(f"Error when trying to request repo information. Message: {req.text}") #TODO: Provide a better name for this Exception

class Github:
    def __init__(self, base_url="https://api.github.com", access_token=""):
        self.base_url = base_url
        self.pat = access_token
    
    def __fetch__(self, url:str, request_type:RequestType, headers:dict, body:str="", json={}) -> tuple[int, str]:
        req = None
        if request_type == RequestType.POST or request_type == RequestType.PUT or request_type == RequestType.PATCH:
            req = requests.request(request_type.value, url, headers=headers, body=body, json=json)
        else:
            req = requests.request(request_type.value, url, headers=headers)
        ret = (req.status_code, "")
        if req.json():
            ret[1] = json.dumps(req.json())
        else:
            ret[1] = req.text
        return ret

    def fetch_pr(self, repo:Repository, pr:int):