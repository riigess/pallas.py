import base64
import http.client
import urllib.parse
import ssl
import json
from io import BytesIO
from enum import Enum
import time
import os
import zipfile

import yaml

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
    DawnSeed = "DawnSeed", "17.0", DeviceType.iPhone, DeviceType.iPad
    DawnBSeed = "DawnBSeed", "17.1", DeviceType.iPhone, DeviceType.iPad
    DawnCSeed = "DawnCSeed", "17.2", DeviceType.iPhone, DeviceType.iPad
    DawnDSeed = "DawnDSeed", "17.3", DeviceType.iPhone, DeviceType.iPad
    DawnESeed = "DawnESeed", "17.4", DeviceType.iPhone, DeviceType.iPad
    DawnFSeed = "DawnFSeed", "17.5", DeviceType.iPhone, DeviceType.iPad
    DawnGSeed = "DawnGSeed", "17.6", DeviceType.iPhone, DeviceType.iPad
    CrystalSeed = "CrystalSeed", "18.0", DeviceType.iPhone, DeviceType.iPad
    CrystalBSeed = "CrystalBSeed", "18.1", DeviceType.iPhone, DeviceType.iPad #Reasonable assumption there might be a B Seed
    CrystalCSeed = "CrystalCSeed", "18.2", DeviceType.iPhone, DeviceType.iPad #Setting up based on past OSes..
    CrystalDSeed = "CrystalDSeed", "18.3", DeviceType.iPhone, DeviceType.iPad
    CrystalESeed = "CrystalESeed", "18.4", DeviceType.iPhone, DeviceType.iPad #Pausing at ESeed based on laziness
    LighthouseSeed = "LighthouseSeed", "10.0", DeviceType.Watch
    LighthouseBSeed = "LighthouseBSeed", "10.1", DeviceType.Watch
    LighthouseCSeed = "LighthouseCSeed", "10.2", DeviceType.Watch
    LighthouseDSeed = "LighthouseDSeed", "10.3", DeviceType.Watch
    LighthouseESeed = "LighthouseESeed", "10.4", DeviceType.Watch
    LighthouseFSeed = "LighthouseFSeed", "10.5", DeviceType.Watch
    LighthouseGSeed = "LighthouseGSeed", "10.6", DeviceType.Watch
    LighthouseHSeed = "LighthouseHSeed", "10.7", DeviceType.Watch
    MoonstoneSeed = "MoonstoneSeed", "11.0", DeviceType.Watch
    MoonstoneBSeed = "MoonstoneBSeed", "11.1", DeviceType.Watch
    MoonstoneCSeed = "MoonstoneCSeed", "11.2", DeviceType.Watch
    MoonstoneDSeed = "MoonstoneDSeed", "11.3", DeviceType.Watch
    MoonstoneESeed = "MoonstoneESeed", "11.4", DeviceType.Watch
    SunburstSeed = "SunburstSeed", "14.0", DeviceType.Mac
    SunburstBSeed = "SunburstBSeed", "14.1", DeviceType.Mac
    SunburstCSeed = "SunburstCSeed", "14.2", DeviceType.Mac
    SunburstDSeed = "SunburstDSeed", "14.3", DeviceType.Mac
    SunburstESeed = "SunburstESeed", "14.4", DeviceType.Mac
    SunburstFSeed = "SunburstFSeed", "14.5", DeviceType.Mac
    SunburstGSeed = "SunburstGSeed", "14.6", DeviceType.Mac
    SunburstHSeed = "SunburstHSeed", "14.7", DeviceType.Mac
    GlowSeed = "GlowSeed", "15.0", DeviceType.Mac
    GlowBSeed = "GlowBSeed", "15.1", DeviceType.Mac
    GlowCSeed = "GlowCSeed", "15.2", DeviceType.Mac
    GlowDSeed = "GlowDSeed", "15.3", DeviceType.Mac
    GlowESeed = "GlowESeed", "15.4", DeviceType.Mac
    BorealisSeed = "BorealisSeed", "1.0", DeviceType.Vision_Pro
    BorealisESeed = "BorealisESeed", "1.1", DeviceType.Vision_Pro
    BorealisFSeed = "BorealisFSeed", "1.2", DeviceType.Vision_Pro
    BorealisGSeed = "BorealisGSeed", "1.3", DeviceType.Vision_Pro
    ConstellationSeed = "ConstellationSeed", "2.0", DeviceType.Vision_Pro
    ConstellationBSeed = "ConstellationBSeed", "2.1", DeviceType.Vision_Pro
    ConstellationCSeed = "ConstellationCSeed", "2.2", DeviceType.Vision_Pro
    ConstellationDSeed = "ConstellationDSeed", "2.3", DeviceType.Vision_Pro
    ConstellationESeed = "ConstellationESeed", "2.4", DeviceType.Vision_Pro
    Null = "Null", DeviceType.TV

    def lookup(ostdp):
        return ostdp.value[1]

class AudienceLookups(Enum):
    macos_generic = "02d8e57e-dd1c-4090-aa50-b4ed2aef0062"
    ios_generic = "0c88076f-c292-4dad-95e7-304db9d29d34"
    tvos_generic = "fe6f26f9-ec98-46d2-8faf-565375a83ba7"
    visionpro_generic = "5cb41593-0f8a-45ba-89c6-52928b9caaae"
    watchos_generic = "fe4c7f1c-f44c-4c00-b3df-eef225a1ac9d"

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
            raise Exception("Unhandled Data format")
    
    def save_json_to_file(self, data:dict, filename:str):
        with open(filename, 'w') as f:
            f.write(json.dumps(data, indent=4, separators=(',',':')))
    
    def remove_asset_receipts(self, data:dict) -> dict:
        if 'Assets' in data:
            for asset in data['Assets']:
                if '_AssetReceipt' in asset:
                    del asset['_AssetReceipt']
        return data
    
class Util:
    def create_new_zip(self, zip_filename:str="zipfile.zip"):
        if os.path.exists(zip_filename):
            os.remove(zip_filename)
        with zipfile.ZipFile(zip_filename, 'w') as zip_f:
            zip_f.writestr("UAFAssets/start.txt", "\n")

    def write_str_to_zipfile(self, zip_filename:str="zipfile.zip", dest_filename:str="Test.txt", data:str="\n"):
        with zipfile.ZipFile(zip_filename, 'a') as zip_f:
            zip_f.writestr(dest_filename, data)

if __name__ == "__main__":
    pallas_url = 'https://gdmf.apple.com/v2/assets'
    pallas_request = PallasRequest(url=pallas_url)
    sleep_time = 3
    data_store = {}
    export_dir = "/Users/riigess/Downloads"
    
    def get_all_names_for_type(enum_type):
        to_return = []
        for key in enum_type.__dict__:
            if type(key) is str and '_' not in key[0]:
                to_return.append(key)
        return to_return

    os_train_lookup = {}
    for train in OSTrainDevicePair.__dict__:
        if type(train) is str and '_' not in train and 'lookup' != train:
            pair = OSTrainDevicePair.__dict__[train]
            os_train_lookup.update({pair.value[1]: pair.value[0]})

    root_path = "raw"

    audience = AudienceLookups.ios_generic
    device = DeviceType.iPhone
    # Only need to get A and E Trains for iPhone to get all asset info.
    # - This is len(asset_audience) * len(os_trains) = ~50 requests over about 3 minutes (Not including how long it takes for Pallas to respond)
    asset_audiences = [Assets.__dict__[name] for name in get_all_names_for_type(Assets)]
    os_trains = [OSTrainDevicePair.DawnSeed, OSTrainDevicePair.DawnESeed, OSTrainDevicePair.CrystalSeed, OSTrainDevicePair.CrystalESeed]

    for ostrain in os_trains:
        for asset in asset_audiences:
            print(f"Now checking for {asset.value} on OS {ostrain.value[0]}")
            # if not os.path.exists(f"{root_path}/{ostrain.value[0]}"):
            #     os.mkdir(f"{root_path}/{ostrain.value[0]}")
            # if not os.path.exists(f"{root_path}/{ostrain.value[0]}/{device.value}"):
            #     os.mkdir(f"{root_path}/{ostrain.value[0]}/{device.value}")
            resp = pallas_request.request(audience, asset, device, ostrain)
            resp = pallas_request.remove_asset_receipts(resp)
            #TODO: Reorganize data by directory tree
            """
            Dictionary structure to organize everything before moving this into a directory tree in a zipfile to push to Github
            {
                "AssetType": {
                    "TrainName": {
                        "DeviceName": {
                            "AssetSpecifier": <payload-data>
                        }
                    }
                }
            }
            """
            asset_type_no_periods = asset.value.split('.')[3:]
            asset_type_no_periods = ''.join(asset_type_no_periods)
            if asset_type_no_periods not in data_store:
                data_store.update({asset_type_no_periods: {}})
            
            if 'Assets' in resp:
                for resp_asset in resp['Assets']:
                    #Get SupportedDeviceName (if not generic)
                    if 'SupportedDeviceNames' in resp_asset:
                        if 'Apple Vision' in resp_asset['SupportedDeviceNames'] or 'rProd Device' in resp_asset['SupportedDeviceNames']:
                            device_name = 'Apple Vision'
                        elif 'iPhone' in resp_asset['SupportedDeviceNames']:
                            device_name = 'iPhone'
                        elif 'Mac' in resp_asset['SupportedDeviceNames']:
                            device_name = 'Mac'
                        elif 'Apple TV' in resp_asset['SupportedDeviceNames']:
                            device_name = 'HomeAccessory'
                        elif 'Apple Watch' in resp_asset['SupportedDeviceNames']:
                            device_name = 'Apple Watch'
                    else:
                        device_name = 'generic'
                    #Determine OS Train name (device-specific train name)
                    if '_OSVersionCompatibilities' in resp_asset:
                        if device_name != 'generic':
                            version_number = resp_asset['_OSVersionCompatibilities'][device_name]['_MinOSVersion'].split('.')
                            if len(version_number) > 2:
                                version_number = version_number[:2]
                            version_number = '.'.join(version_number)
                            train_name = os_train_lookup[version_number]
                        else:
                            version_number = resp_asset['_OSVersionCompatibilities']['iPhone']['_MinOSVersion'].split('.')
                            if len(version_number) > 2:
                                version_number = version_number[:2]
                            version_number = '.'.join(version_number)
                            train_name = os_train_lookup[version_number]
                    else:
                        train_name = ostrain.value[0]
                    train_name = train_name.replace("Seed", "")
                    #Update data_store to add train_name
                    if train_name not in data_store[asset_type_no_periods]:
                        data_store[asset_type_no_periods].update({train_name: {}})
                    #Update data_store to add device_name (for targeting rules)
                    if device_name not in data_store[asset_type_no_periods][train_name]:
                        data_store[asset_type_no_periods][train_name].update({device_name: {}})
                    #Store data in data_store
                    specifier = resp_asset['AssetSpecifier']
                    dup_asset = resp_asset.copy()
                    keep_keys = ["ArchiveDecryptionKey", "ArchiveID", "AssetFormat", "AssetVersion", "Build", "__BaseURL", "_PreSoftwareUpdateAssetStaging", "__RelativePath"]
                    for key in resp_asset:
                        if key not in keep_keys and key in dup_asset:
                            del dup_asset[key]
                    if specifier not in data_store[asset_type_no_periods][train_name][device_name]:
                        dup_asset_yaml = yaml.dump(dup_asset)
                        line_count = len(dup_asset_yaml.split('\n'))
                        data_store[asset_type_no_periods][train_name][device_name].update({specifier: dup_asset_yaml})
            else:
                print(resp)
            
            #TODO: Publish to Github through the API given the zip file
            # if 'Status' not in resp:
            #     pallas_request.save_json_to_file(resp, f"{root_path}/{ostrain.value[0]}/{device.value}/{asset.value}.json")
            time.sleep(sleep_time)

    util = Util()
    util.create_new_zip(f"{export_dir}/UAFAssets.zip")
    #Create ZIP file with everything in it
    for asset_type_store in data_store:
        for train in data_store[asset_type_store]:
            for device in data_store[asset_type_store][train]:
                for specifier in data_store[asset_type_store][train][device]:
                    data = data_store[asset_type_store][train][device][specifier]
                    filepath = f"UAFAssets/{asset_type_store}/{train}/{device}/{specifier}/payload.yml"
                    util.write_str_to_zipfile(f"{export_dir}/UAFAssets.zip", filepath, data)
    print("Done.")
    #TODO: Upload ZIP to repo
