import ssl
import urllib
import json
from io import BytesIO
import base64
import http.client
import urllib.parse

from utils.Assets import Assets
from utils.AudienceLookups import AudienceLookups
from utils.DeviceType import DeviceType
from utils.OSTrainDevicePair import OSTrainDevicePair

class PallasRequest:
    def __init__(self, url:str = "https://gdmf.apple.com/v2/assets"):
        self.url = url
        self.headers = {
            "Content-Type": "application/json"
        }

    def _modify_response(self, resp):
        content_type = resp.getheader('content-type')
        if content_type and 'application/json' in content_type:
            body_bytes = resp.read()
            body_str = body_bytes.decode('utf-8')
            if body_str.startswith('e'):
                jwt_body = body_str.split('.')[1]
                decoded_jwt_body = base64.urlsafe_b64decode(jwt_body + '==')
                body_bytes = decoded_jwt_body
            resp_body = BytesIO(body_bytes)
            return resp_body, len(body_bytes)
        else:
            return BytesIO(resp.read()), resp.length

    def make_post_request(self, body:str):
        url_parts = urllib.parse.urlsplit(self.url)
        conn = http.client.HTTPSConnection(url_parts.netloc, context=ssl._create_unverified_context())

        headers = {
            "Host": "gdmf.apple.com",
            "Content-Length": str(len(body))
        }
        headers.update(self.headers) #Update with existing headers

        conn.request("POST", url_parts.path, body=body, headers=headers)
        resp = conn.getresponse()

        resp_body, length = self._modify_response(resp)

        to_return = resp_body.read().decode('utf-8')
        conn.close()
        return to_return
    
    def request(self, asset_audience:AudienceLookups, asset_type:Assets, device_type:DeviceType, train_name:OSTrainDevicePair) -> dict:
        body = {
            "AssetAudience": asset_audience.value, #This can be changed to fit other deviceTypes
            "ClientVersion": 2,
            "AssetType": asset_type.value, #This can be changed to other Assets
            "CertIssuanceDay": "2023-12-10",
            "DeviceName": device_type.value, #Can be changed to other DeviceTypes
            "TrainName": train_name.value[0] #Can be changed to other OSTrainDevicePair names (Useful at a quick glance)
        }
        body_dump = json.dumps(body)

        resp = self.make_post_request(body_dump)
        if '{' in resp[0]:
            if type(resp) is str:
                resp = json.loads(resp)
            if type(resp) is dict:
                return resp
            else:
                raise Exception(f"Error: unformatted type for resp {type(resp)}")
        else:
            print(resp)
            raise Exception("Unhandled data format")
    
    def save_json_to_file(self, data:dict, filename:str):
        with open(filename, 'w') as f:
            f.write(json.dumps(data, indent=4, separators=(',',':')))
    
    def remove_asset_receipts(self, data:dict) -> dict:
        if 'Assets' in data:
            for asset in data['Assets']:
                if '_AssetReceipt' in asset:
                    del asset['_AssetReceipt']
        return data
