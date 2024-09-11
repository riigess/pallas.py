from pallas.utils.PallasRequest import PallasRequest
from pallas.utils.Audience import Audience
from pallas.utils.Assets import UAFAssets
from pallas.utils.DeviceType import DeviceType
from pallas.utils.OSTrainDevicePair import OSTrainDevicePair

def test_pallasrequest():
    pr = PallasRequest()
    pallas_resp = pr.request(asset_audience=Audience.ios_generic,
                             asset_type=UAFAssets.SiriPlatformAssets,
                             device_type=DeviceType.iPhone,
                             train_name=OSTrainDevicePair.CrystalSeed)
