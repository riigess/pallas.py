import argparse
from typing import Union
import os

from pallas.asset import Asset
from pallas.utils.DeviceType import DeviceType
from pallas.utils.Assets import Assets, UAFAssets, EnumUtils
from pallas.utils.Audience import Audience
from pallas.utils.OSTrainDevicePair import OSTrainDevicePair
from pallas.actions.Fetching import Fetching
from pallas.actions.Saving import Saving


def main_argparse():
    parser = argparse.ArgumentParser(
        "PallasRequester", "pallasrequester --unified-asset-framework")
    parser.add_argument("--unified-asset-framework", "-u", action="store_true", default=False,
                        help="Fetches the active asset information for the UnifiedAssetFramework (UAF).")
    parser.add_argument("--software-update", "-s", action="store_true", default=False,
                        help="Fetches active software updates for iOS, macOS, tvOS, visionOS, and watchOS.")
    parser.add_argument("--timezone", "-t", action="store_true", default=False,
                        help="Fetches the timezone update property list from Pallas.")
    # parser.add_argument("--custom", "-c", default="", help="Fetches custom request using additional args")
    parser.add_argument("--ios", "-i", default=False, action="store_true",
                        help="--custom (-c) is required for this flag to be available | ")
    parser.add_argument("--mac", "-m", default=False,
                        action="store_true", help="")
    parser.add_argument("--apple-tv", "--tv", default=False,
                        action="store_true", help="")
    parser.add_argument("--vision-pro", "--vision-os", "--xros",
                        "-p", default=False, action="store_true", help="")
    parser.add_argument("--apple-watch", "--watch", "-w",
                        default=False, action="store_true", help="")
    parser.add_argument("--list-identifiers", "-ids", default=False, action="store_true",
                        help="Lists all available asset identifiers (ex. com.apple.MobileAsset.MacSoftwareUpdate)")
    parser.add_argument("--identifier", default=[], action="extend",
                        help="Specifies a specific identifier to fetch")
    parser.add_argument("--os-ver", "-os", default="", action="store_const")
    return parser.parse_known_args()


def get_uaf_assets() -> dict:
    DawnESeed_Assets = [
        UAFAssets.SiriDialogAssets,
        UAFAssets.SiriFindMy,
        UAFAssets.SiriPlatformAssets,
        UAFAssets.SiriUnderstanding,
        UAFAssets.SiriUnderstandingASRHammer,
        UAFAssets.SiriUnderstandingNLOverrides
    ]
    CrystalSeed_Assets = EnumUtils().list_members(UAFAssets)
    del CrystalSeed_Assets['FMVisual']
    del CrystalSeed_Assets['FMVisual']
    return {
        OSTrainDevicePair.DawnESeed: {
            "Device": DeviceType.iPhone,
            "Audience": Audience.ios_generic,
            "Assets": DawnESeed_Assets
        },
        OSTrainDevicePair.CrystalSeed: {
            "Device": DeviceType.Mac,
            "Audience": Audience.macos_generic,
            "Assets": CrystalSeed_Assets
        },
        OSTrainDevicePair.CrystalESeed: {
            "Device": DeviceType.Mac,
            "Audience": Audience.macos_generic,
            "Assets": EnumUtils().list_members(Assets)
        }
    }


def get_assets(assets: dict, key: OSTrainDevicePair):
    otdp = assets[key]
    device = otdp["Device"]
    if device == DeviceType.iPhone or DeviceType.iPad:
        return fetch.get_ios_asset_group(assets=otdp["Assets"], os_train=key)
    elif device == DeviceType.Mac:
        return fetch.get_macos_asset_group(assets=otdp["Assets"], os_train=key)
    elif device == DeviceType.TV:
        return fetch.get_tvos_asset_group(assets=otdp["Assets"], os_train=key)
    elif device == DeviceType.Watch:
        return fetch.get_watchos_asset_group(assets=otdp["Assets"], os_train=key)
    else:
        raise RuntimeError(
            "Error, unknown device provided please review __main__.py:get_assets(list[Assets],OSTrainDevicePair)")


def append_assets(assets: list[Asset], file_name: str) -> bool:
    store = Saving(file_name)
    if not store.sqlite_exists():
        store.configure_sqlite()
    for asset in assets:
        store.append_asset_to_sqlite(asset=asset)
    return store.sqlite_exists()


if __name__ == "__main__":
    args = main_argparse()
    print("ARGS:", args)

    fetch = Fetching()
    # This is caching logic, I need to add better invalidation logic to handle what happens before noon PT vs after here
    sqlite_file = f"{os.getcwd()}/database.sqlite"
    if args[0].unified_asset_framework:
        # Setup Variables
        assets = get_uaf_assets()
        pallas_resp = []

        # Fetch Assets
        latest = [OSTrainDevicePair.CrystalFSeed, OSTrainDevicePair.CheerSeed]
        for train in latest:
            print(f"Fetching iOS {OSTrainDevicePair.lookup(train)}-aligned Assets: ", end=' ')
            temp = len(pallas_resp)
            pallas_resp += get_assets(assets, train)
            print(f"{len(pallas_resp)-temp} Assets.")

        # Store assets
        print(f"Adding assets to {sqlite_file} for asset caching.")
        append_assets(pallas_resp, sqlite_file)
    elif args[0].software_update:
        mac_su = Assets.MacSoftwareUpdate
        mac_su_asset = fetch.get_macos_asset(
            asset=mac_su, os_train=OSTrainDevicePair.LuckSeed).assets[0]
        ios_su = Assets.iPhoneSoftwareUpdate
        ios_su_asset = fetch.get_ios_asset(
            asset=ios_su, os_train=OSTrainDevicePair.CheerSeed).assets[0]
        # tv_su = Assets.TVSoftwareUpdate
        # tv_su_asset = fetch.get_tvos_asset(asset=tv_su, os_train=OSTrainDevicePair.Null)
        watch_su = Assets.WatchSoftwareUpdate
        watch_su_asset = fetch.get_watchos_asset(
            asset=watch_su, os_train=OSTrainDevicePair.NepaliSeed).assets[0]
        append_assets(assets=[mac_su_asset, ios_su_asset,
                      watch_su_asset], file_name=sqlite_file)
    elif args[0].timezone:
        tz_update = Assets.TimeZoneUpdate
        tz_resp = fetch.get_macos_asset(
            asset=tz_update, os_train=OSTrainDevicePair.CrystalSeed).assets[0]
        append_assets(assets=[tz_resp], file_name=sqlite_file)
        print()
    elif 'custom' in args[0] and args[0].custom:
        print("This is curerntly a feature that remains in development. Intended use: \n\t`python -m pallas --custom --ios --train-name=crystalseed --asset=UAFSiriUnderstanding`")
