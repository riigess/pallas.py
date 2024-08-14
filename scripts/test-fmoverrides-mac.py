import importlib
import json

PallasRequest = importlib.import_module("pallas-get-UAFAssets").__dict__["PallasRequest"]
from utils.Assets import Assets
from utils.AudienceLookups import AudienceLookups
from utils.DeviceType import DeviceType
from utils.OSTrainDevicePair import OSTrainDevicePair

if __name__ == "__main__":
    pallas_request = PallasRequest()
    export_dir = "."

    request_body = {
        "AssetAudience": AudienceLookups.macos_generic.value,
        "AssetType": Assets.UAFIFPlanner.value,
        "ClientVersion":2,
        "CertIssuanceDay": "2023-12-10",
        "DeviceName": DeviceType.Mac.value,
        "TrainName": OSTrainDevicePair.GlowBSeed.value[0], #This should be "GlowBSeed"
        "InternalBuild": True,
        "RestoreVersion": "24.2.9.15.12,0", #This will need to be regularly updated :(
        "OSVersion": "15.1",
        "HWModelStr": "J516cAP"
    }

    resp = pallas_request.make_post_request(body=json.dumps(request_body))
    pallas_request.save_json_to_file(resp, "test-IFPlanner.json")
