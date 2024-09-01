import argparse
from pallas.utils.DeviceType import DeviceType
from pallas.utils.UAFAssets import UAFAssets
from pallas.utils.Audience import Audience
from pallas.utils.OSTrainDevicePair import OSTrainDevicePair

parser = argparse.ArgumentParser("PallasRequester", "pallasrequester --unified-asset-framework")
parser.add_argument("--unified-asset-framework", "-u", action="store_true", default=False, help="Fetches the active asset information for the UnifiedAssetFramework (UAF).")
parser.add_argument("--software-update", "-s", action="store_true", default=False, help="Fetches active software updates for iOS, macOS, tvOS, visionOS, and watchOS.")
parser.add_argument("--timezone", "-t", action="store_true", default=False, help="Fetches the timezone update property list from Pallas.")
parser.add_argument("--custom", "-c", default="", help="Fetches custom body data provided by you! 😁")

if __name__ == "__main__":
    args = parser.parse_known_args()
    # uaf = args['unified_asset_framework']
    # su = args['software_update']
    # tz = args['timezone']
    print(args)

    if args[0].unified_asset_framework:
        assets = {
            DeviceType.iPhone: {
                "OS": OSTrainDevicePair.DawnESeed,
                "Audience": Audience.ios_generic,
                "Assets": [
                    UAFAssets.SiriDialogAssets,
                    UAFAssets.SiriFindMy,
                    UAFAssets.SiriPlatformAssets,
                    UAFAssets.SiriUnderstanding,
                    UAFAssets.SiriUnderstandingASRHammer,
                    UAFAssets.SiriUnderstandingNLOverrides
                ]
            },
            DeviceType.Mac: {
                "OS": OSTrainDevicePair.GlowSeed,
                "Audience": Audience.macos_generic,
                "Assets": UAFAssets.all_assets()
            }
        }
        print("Fetching iOS 17-aligned Assets:")
        for asset in assets[DeviceType.iPhone]["Assets"]:
            print(f"\t- {asset.value}")
            #TODO: Make request
        print("\nFetching iOS 18-aligned Assets:", len(assets[DeviceType.Mac]["Assets"]))
        for asset in assets[DeviceType.Mac]["Assets"]:
            print(f"\t- {asset.value}")
        print("Done.")
    elif args[0].software_update:
        print("SOFTWARE UPDATE")
    elif args[0].timezone:
        print("TIMEZONE")