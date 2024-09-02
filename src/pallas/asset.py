import requests

from pallas.utils.DeviceType import DeviceType

class VersionIdentifier:
        def __init__(self, version:str="1.0.0"):
            parts = version.split(".")
            self.major = int(parts[0]) if len(parts) > 0 else 1
            self.minor = int(parts[1]) if len(parts) > 1 else 0
            self.sub = int(parts[2]) if len(parts) > 2 else 0
        
        def __eq__(self, other):
            return self.major == other.major and self.minor == other.minor and self.sub == other.sub
    
        def __gt__(self, other):
            return self.major > other.major or self.minor > other.minor or self.sub > other.sub

        def __lt__(self, other):
            return self.major < other.major or self.minor < other.minor or self.sub < other.sub


class VersionCompatibilities:
    def __init__(self, vers:dict={}):
        self.mac = [Asset.VersionIdentifier(vers.get("Mac", {}).get("_MinOSVersion", "")),
                    Asset.VersionIdentifier(vers.get("Mac", {}).get("_MaxOSVersion", ""))]
        self.ipad = [Asset.VersionIdentifier(vers.get("iPad", {}).get("_MinOSVersion", "")),
                     Asset.VersionIdentifier(vers.get("iPad", {}).get("_MaxOSVersion", ""))]
        self.iphone = [Asset.VersionIdentifier(vers.get("iPhone", {}).get("_MinOSVersion", "")),
                        Asset.VersionIdentifier(vers.get("iPhone", {}).get("_MaxOSVersion", ""))]
        self.homepod = [Asset.VersionIdentifier(vers.get("HomePod", {}).get("_MinOSVersion", "")),
                        Asset.VersionIdentifier(vers.get("HomePod", {}).get("_MaxOSVersion", ""))]
        self.apple_tv = [Asset.VersionIdentifier(vers.get("Apple TV", {}).get("_MinOSVersion", "")),
                         Asset.VersionIdentifier(vers.get("Apple TV", {}).get("_MaxOSVersion", ""))]
        self.apple_watch = [Asset.VersionIdentifier(vers.get("Apple Watch", {}).get("_MinOSVersion", "")),
                            Asset.VersionIdentifier(vers.get("Apple Watch", {}).get("_MaxOSVersion", ""))]
        vp_low = max(Asset.VersionIdentifier(vers.get("Apple Vision", {}).get("_MinOSVersion", "")),
                     Asset.VersionIdentifier(vers.get("rProd Device", {}).get("_MinOSVersion", "")))
        vp_high = max(Asset.VersionIdentifier(vers.get("Apple Vision", {}).get("_MaxOSVersion", "")),
                      Asset.VersionIdentifier(vers.get("rProd Device", {}).get("_MaxOSVersion", "")))
        self.vision_pro = [vp_low, vp_high]
        self.home_accessory = [Asset.VersionIdentifier(vers.get("HomeAccessory", {}).get("_MinOSVersion", "")),
                               Asset.VersionIdentifier(vers.get("HomeAccessory", {}).get("_MaxOSVersion", ""))]
    
    def is_compatible(self, device:DeviceType=DeviceType.iPhone, version:str="1.0.0") -> bool:
        return self.is_compatible(device=device, version=VersionIdentifier(version=version))
    
    def is_compatible(self, device:DeviceType=DeviceType.iPhone, version:VersionIdentifier=VersionIdentifier()) -> bool:
        if device == DeviceType.iPhone:
            return version <= self.iphone[1] and version >= self.iphone[0]
        elif device == DeviceType.iPad:
            return version <= self.ipad[1] and version >= self.ipad[0]
        elif device == DeviceType.Mac:
            return version <= self.mac[1] and version >= self.mac[0]
        elif device == DeviceType.TV:
            return version <= self.apple_tv[1] and version >= self.apple_tv[0]
        elif device == DeviceType.Homepod:
            return version <= self.homepod[1] and version >= self.homepod[0]
        elif device == DeviceType.Vision_Pro:
            return version <= self.vision_pro[1] and version >= self.vision_pro[0]
        elif device == DeviceType.Watch:
            return version <= self.apple_watch[1] and version >= self.apple_watch[0]
        else: #HomeAccessory
            return version <= self.home_accessory[1] and version >= self.home_accessory[0]

class Asset:
    def __init__(self, a_dict:dict={}):
        self.decryption_key = a_dict.get("ArchiveDecryptionKey", None)
        self.decryption_key_file = a_dict.get("ArchiveDecryptionKeyFile", None)
        self.archive_id = a_dict.get("ArchiveID", None)
        self.asset_format = a_dict.get("AssetFormat", None)
        self.asset_specifier = a_dict.get("AssetSpecifier", a_dict.get("Factor", ""))
        self.asset_type = a_dict.get("AssetType", "")
        self.asset_version = a_dict.get("AssetVersion", "") #I should build an AssetVersion object that's able to store more fields compared to the above VersionIdentifier object
        self.build = a_dict.get("Build", "")
        self._DownloadSize = a_dict.get("_DownloadSize", 1)
        self._ISMAAutoAsset = a_dict.get("_ISMAAutoAsset", False)
        self._BaseURL = a_dict.get("_BaseURL", "")
        self._RelativePath = a_dict.get("_RelativePath", "")
        self.url = self._BaseURL + ("/" if self._BaseURL[-1] != "/" else "") + self._RelativePath
        self.version = VersionIdentifier(a_dict.get("version", "1.0.0"))
        self.ramp = a_dict.get("Ramp", False)
        self._OSVersionCompatibilities = VersionCompatibilities(a_dict.get("_OSVersionCompatibilities", {}))
    
    def download(self, to_file:str=None) -> str:
        req = requests.get(self.url)
        if to_file and req.status_code == 200:
            with open(to_file, 'wb') as f:
                f.write(req.content)
        elif req.status_code != 200:
            raise RuntimeError(f"Status Code {req.status_code} - please validate the URL provided for asset. {self.url}")
        elif not to_file:
            return req.text
