import base64
import http.client
import urllib.parse
import ssl
import json
from io import BytesIO
from enum import Enum
import time
import os

import requests

class DeviceType(Enum):
    AudioAccessory = "AudioAccessory"
    HomeAccessory = "HomeAccessory"
    Homepod = "HomePod"
    iPhone = "iPhone"
    iPad = "iPad"
    Mac = "Mac"
    TV = "Apple TV"
    Vision_Pro = "Apple Vision"
    Vision_Pro_dup = "rProd Device"
    Watch = "Apple Watch"

class OSTrainDevicePair(Enum):
    DawnSeed = "DawnSeed", DeviceType.iPhone, DeviceType.iPad
    DawnBSeed = "DawnBSeed", DeviceType.iPhone, DeviceType.iPad
    DawnCSeed = "DawnCSeed", DeviceType.iPhone, DeviceType.iPad
    DawnDSeed = "DawnDSeed", DeviceType.iPhone, DeviceType.iPad
    DawnESeed = "DawnESeed", DeviceType.iPhone, DeviceType.iPad
    DawnFSeed = "DawnFSeed", DeviceType.iPhone, DeviceType.iPad
    DawnGSeed = "DawnGSeed", DeviceType.iPhone, DeviceType.iPad
    CrystalSeed = "CrystalSeed", DeviceType.iPhone, DeviceType.iPad
    CrystalBSeed = "CrystalBSeed", DeviceType.iPhone, DeviceType.iPad #Reasonable assumption there might be a B Seed
    CrystalCSeed = "CrystalCSeed", DeviceType.iPhone, DeviceType.iPad #Setting up based on past OSes..
    CrystalDSeed = "CrystalDSeed", DeviceType.iPhone, DeviceType.iPad
    CrystalESeed = "CrystalESeed", DeviceType.iPhone, DeviceType.iPad #Pausing at ESeed based on laziness
    LighthouseSeed = "LighthouseSeed", DeviceType.Watch
    LighthouseBSeed = "LighthouseBSeed", DeviceType.Watch
    LighthouseCSeed = "LighthouseCSeed", DeviceType.Watch
    LighthouseDSeed = "LighthouseDSeed", DeviceType.Watch
    LighthouseESeed = "LighthouseESeed", DeviceType.Watch
    LighthouseFSeed = "LighthouseFSeed", DeviceType.Watch
    LighthouseGSeed = "LighthouseGSeed", DeviceType.Watch
    LighthouseHSeed = "LighthouseHSeed", DeviceType.Watch
    MoonstoneSeed = "MoonstoneSeed", DeviceType.Watch
    MoonstoneBSeed = "MoonstoneBSeed", DeviceType.Watch
    MoonstoneCSeed = "MoonstoneCSeed", DeviceType.Watch
    MoonstoneDSeed = "MoonstoneDSeed", DeviceType.Watch
    MoonstoneESeed = "MoonstoneESeed", DeviceType.Watch
    SunburstSeed = "SunburstSeed", DeviceType.Mac
    SunburstBSeed = "SunburstBSeed", DeviceType.Mac
    SunburstCSeed = "SunburstCSeed", DeviceType.Mac
    SunburstDSeed = "SunburstDSeed", DeviceType.Mac
    SunburstESeed = "SunburstESeed", DeviceType.Mac
    SunburstFSeed = "SunburstFSeed", DeviceType.Mac
    SunburstGSeed = "SunburstGSeed", DeviceType.Mac
    SunburstHSeed = "SunburstHSeed", DeviceType.Mac
    GlowSeed = "GlowSeed", DeviceType.Mac
    GlowBSeed = "GlowBSeed", DeviceType.Mac
    GlowCSeed = "GlowCSeed", DeviceType.Mac
    GlowDSeed = "GlowDSeed", DeviceType.Mac
    GlowESeed = "GlowESeed", DeviceType.Mac
    BorealisSeed = "BorealisSeed", DeviceType.Vision_Pro
    BorealisESeed = "BorealisESeed", DeviceType.Vision_Pro
    BorealisFSeed = "BorealisFSeed", DeviceType.Vision_Pro
    BorealisGSeed = "BorealisGSeed", DeviceType.Vision_Pro
    ConstellationSeed = "ConstellationSeed", DeviceType.Vision_Pro
    ConstellationBSeed = "ConstellationBSeed", DeviceType.Vision_Pro
    ConstellationCSeed = "ConstellationCSeed", DeviceType.Vision_Pro
    ConstellationDSeed = "ConstellationDSeed", DeviceType.Vision_Pro
    ConstellationESeed = "ConstellationESeed", DeviceType.Vision_Pro
    Null = "Null", DeviceType.TV

class AudienceLookups(Enum):
    macos_generic = "02d8e57e-dd1c-4090-aa50-b4ed2aef0062", OSTrainDevicePair.SunburstSeed, OSTrainDevicePair.SunburstBSeed, OSTrainDevicePair.SunburstCSeed, OSTrainDevicePair.SunburstDSeed, OSTrainDevicePair.SunburstESeed, OSTrainDevicePair.SunburstFSeed, OSTrainDevicePair.SunburstGSeed, OSTrainDevicePair.GlowSeed
    ios_generic = "0c88076f-c292-4dad-95e7-304db9d29d34", OSTrainDevicePair.DawnSeed, OSTrainDevicePair.DawnBSeed, OSTrainDevicePair.DawnCSeed, OSTrainDevicePair.DawnDSeed, OSTrainDevicePair.DawnESeed, OSTrainDevicePair.DawnFSeed, OSTrainDevicePair.DawnGSeed, OSTrainDevicePair.CrystalSeed
    tvos_generic = "fe6f26f9-ec98-46d2-8faf-565375a83ba7", OSTrainDevicePair.Null # TODO: Needs a sysdiagnose for tvOS (Shipping & Prerelease)..
    visionpro_generic = "5cb41593-0f8a-45ba-89c6-52928b9caaae", OSTrainDevicePair.BorealisSeed, OSTrainDevicePair.BorealisESeed, OSTrainDevicePair.BorealisFSeed, OSTrainDevicePair.BorealisGSeed, OSTrainDevicePair.ConstellationSeed
    watchos_generic = "fe4c7f1c-f44c-4c00-b3df-eef225a1ac9d", OSTrainDevicePair.LighthouseBSeed, OSTrainDevicePair.LighthouseCSeed, OSTrainDevicePair.LighthouseDSeed, OSTrainDevicePair.LighthouseESeed, OSTrainDevicePair.LighthouseFSeed, OSTrainDevicePair.LighthouseGSeed, OSTrainDevicePair.LighthouseHSeed, OSTrainDevicePair.MoonstoneSeed, OSTrainDevicePair.MoonstoneBSeed, OSTrainDevicePair.MoonstoneBSeed, OSTrainDevicePair.MoonstoneCSeed, OSTrainDevicePair.MoonstoneDSeed, OSTrainDevicePair.MoonstoneESeed

class Assets(Enum):
    UAFFMOverrides = "com.apple.MobileAsset.UAF.FM.Overrides"
    UAFFMCodeLM = "com.apple.MobileAsset.UAF.FM.CodeLM"
    UAFFMGenerativeModels = "com.apple.MobileAsset.UAF.FM.GenerativeModels"
    UAFHandwritingSynthesis = "com.apple.MobileAsset.UAF.Handwriting.Synthesis"
    UAFSafariBrowsingAssistant = "com.apple.MobileAsset.UAF.SafariBrowsingAssistant"
    UAFSiriDialogAssets = "com.apple.MobileAsset.UAF.Siri.DialogAssets"
    UAFSiriFindMy = "com.apple.MobileAsset.UAF.Siri.FindMyConfigurationFiles"
    UAFSiriPlatformAssets = "com.apple.MobileAsset.UAF.Siri.PlatformAssets"
    UAFSiriUnderstanding = "com.apple.MobileAsset.UAF.Siri.Understanding"
    UAFSiriUnderstandingASRHammer = "com.apple.MobileAsset.UAF.Siri.UnderstandingASRHammer"
    UAFSiriUnderstandingNLOverrides = "com.apple.MobileAsset.UAF.Siri.UnderstandingNLOverrides"
    UAFSpeechASR = "com.apple.MobileAsset.UAF.Speech.AutomaticSpeechRecognition"
    UAFSummarizationKit = "com.apple.MobileAsset.UAF.SummarizationKitConfiguration"

class PallasRequest:
    def __init__(self, url:str = "https://gdmf.apple.com/v2/assets"):
        self.url = url
        self.headers = {
            "Content-Type": "application/json"
        }

    def _modify_response(self, resp):
        content_type = resp.getheader('content-type')
        if content_type and 'application/json' in content_type:
            body_bytes = resp.red()
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
            "AssetAudience": asset_audience.value[0], #This can be changed to fit other deviceTypes
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
            raise Exception("Unhandled Data format")
    
    def dump_json_to_file(self, data:dict, filename:str):
        with open(filename, 'w') as f:
            f.write(json.dumps(data, indent=4, separators=(',',':')))
    
    def remove_asset_receipts(self, data:dict) -> dict:
        if 'Assets' in data:
            for asset in data['Assets']:
                if '_AssetReceipt' in asset:
                    del asset['_AssetReceipt']
        return data

if __name__ == "__main__":
    pallas_url = 'https://gdmf.apple.com/v2/assets'
    pallas_request = PallasRequest(url=pallas_url)
    sleep_time = 3
    
    def get_all_names_for_type(enum_type):
        to_return = []
        for key in enum_type.__dict__:
            if type(key) is str and '_' not in key[0]:
                to_return.append(key)
        return to_return

    root_path = "UAFAssets/raw"

    audience = AudienceLookups.ios_generic
    device = DeviceType.iPhone
    # Only need to get A and E Trains for iPhone to get all asset info.
    # - This is len(asset_audience) * len(os_trains) = ~50 requests over about 3 minutes (Not including how long it takes for Pallas to respond)
    asset_audiences = [Assets.__dict__[name] for name in get_all_names_for_type(Assets)]
    os_trains = [OSTrainDevicePair.DawnSeed, OSTrainDevicePair.DawnESeed, OSTrainDevicePair.CrystalSeed, OSTrainDevicePair.CrystalESeed]

    for ostrain in os_trains:
        for asset in asset_audiences:
            if not os.path.exists(f"{root_path}/{ostrain.value[0]}"):
                os.mkdir(f"{root_path}/{ostrain.value[0]}")
            if not os.path.exists(f"{root_path}/{ostrain.value[0]}/{device.value}"):
                os.mkdir(f"{root_path}/{ostrain.value[0]}/{device.value}")
            resp = pallas_request.request(audience, asset, device, ostrain)
            resp = pallas_request.remove_asset_receipts(resp)
            #TODO: Reorganize data by directory tree
            #TODO: Publish to Github through the API
            pallas_request.dump_json_to_file(resp, f"{root_path}/{ostrain.value[0]}/{device.value}/{asset.value}")
            time.sleep(sleep_time)
