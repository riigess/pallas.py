import argparse
import os

from pallas.utils.DeviceType import DeviceType
from pallas.utils.Assets import Assets
from pallas.utils.UAFAssets import UAFAssets
from pallas.utils.Audience import Audience
from pallas.utils.OSTrainDevicePair import OSTrainDevicePair
from pallas.actions.Fetching import Fetching
from pallas.actions.Saving import Saving

def main_argparse():
    parser = argparse.ArgumentParser("PallasRequester", "pallasrequester --unified-asset-framework")
    parser.add_argument("--unified-asset-framework", "-u", action="store_true", default=False, help="Fetches the active asset information for the UnifiedAssetFramework (UAF).")
    parser.add_argument("--software-update", "-s", action="store_true", default=False, help="Fetches active software updates for iOS, macOS, tvOS, visionOS, and watchOS.")
    parser.add_argument("--timezone", "-t", action="store_true", default=False, help="Fetches the timezone update property list from Pallas.")
    parser.add_argument("--custom", "-c", default="", help="Fetches custom body data provided by you! 😁")
    parser.add_argument("--ios", "-i", default=False, action="store_true", help="--custom (-c) is required for this flag to be available | ")
    parser.add_argument("--mac", "-m", default=False, action="store_true", help="")
    parser.add_argument("--apple-tv", "-t", default=False, action="store_true", help="")
    parser.add_argument("--vision-pro", "--vision-os", "--xros", "-p", default=False, action="store_true", help="")
    parser.add_argument("--apple-watch", "-w", default=False, action="store_true", help="")
    return parser.parse_known_args()

def get_uaf_assets() -> dict:
    return {
        DeviceType.iPhone: {
            "OS": OSTrainDevicePair.DawnESeed,
            "Audience": Audience.ios_generic,
            "Assets": [
                Assets.SiriDialogAssets,
                Assets.SiriFindMy,
                Assets.SiriPlatformAssets,
                Assets.SiriUnderstanding,
                Assets.SiriUnderstandingASRHammer,
                Assets.SiriUnderstandingNLOverrides
            ]
        },
        DeviceType.Mac: {
            "OS": OSTrainDevicePair.GlowSeed,
            "Audience": Audience.macos_generic,
            "Assets": Assets.all_assets()
        }
    }

def append_assets(assets:list[Assets], file_name:str) -> bool:
    store = Saving(file_name)
    if not store.sqlite_exists():
        store.configure_sqlite()
    for asset in assets:
        store.append_asset_to_sqlite(asset=asset)
    return store.sqlite_exists()

if __name__ == "__main__":
    args = main_argparse()

    fetch = Fetching()
    sqlite_file = f"{os.getcwd()}/database.sqlite"
    if args[0].unified_asset_framework:
        #Setup Variables
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
        pallas_resp = []
        
        #Fetch Assets
        print("Fetching iOS 17-aligned Assets:", end=' ')
        pallas_resp += fetch.get_ios_asset_group(assets=assets[DeviceType.iPhone], os_train=OSTrainDevicePair.DawnESeed)
        temp = len(pallas_resp)
        print(f"{temp} assets.\n\nFetching iOS 18-aligned Assets:", end=' ')
        pallas_resp += fetch.get_macos_asset_group(assets=assets[DeviceType.Mac], os_train=OSTrainDevicePair.CrystalSeed)
        print(f"{len(pallas_resp) - temp} assets.\nDone.\n")

        #Store assets
        print(f"Adding assets to {sqlite_file}")
        append_assets(pallas_resp, sqlite_file)
    elif args[0].software_update:
        mac_su = Assets.MacSoftwareUpdate
        mac_su_asset = fetch.get_macos_asset(asset=mac_su, os_train=OSTrainDevicePair.GlowSeed)
        ios_su = Assets.iPhoneSoftwareUpdate
        ios_su_asset = fetch.get_ios_asset(asset=ios_su, os_train=OSTrainDevicePair.CrystalSeed)
        # tv_su = Assets.TVSoftwareUpdate
        # tv_su_asset = fetch.get_tvos_asset(asset=tv_su, os_train=OSTrainDevicePair.Null)
        watch_su = Assets.WatchSoftwareUpdate
        watch_su_asset = fetch.get_watchos_asset(asset=watch_su, os_train=OSTrainDevicePair.MoonstoneSeed)
        append_assets(assets=[mac_su_asset, ios_su_asset, watch_su_asset], file_name=sqlite_file)
    elif args[0].timezone:
        tz_update = Assets.TimeZoneUpdate
        tz_resp = fetch.get_macos_asset(asset=tz_update, os_train=OSTrainDevicePair.CrystalSeed)
        append_assets(assets=[tz_resp], file_name=sqlite_file)
        print()
    elif args[0].custom:
        print("This is curerntly a feature that remains in development. Intended use: \n\t`python -m pallas --custom --ios --train-name=crystalseed --asset=UAFSiriUnderstanding`")
