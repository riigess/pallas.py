# Documentation
I'm horrible at writing documentation so this is really a "how to" or "what does this do?" reference page.

## `__main__`
| argument | alias | store or toggle | description |
| :-- | :-- | :-- | :-- |
| --unified-asset-framework | -u | toggle (=true) | Fetches the active asset information for the UnifiedAssetFramework (UAF). |
| --software-update | -s | toggle (=true) | Fetches active software updates for iOS, macOS, tvOS, visionOS, and watchOS. |
| --timezone | -t | toggle (=true) | Fetches the timezone property list from Pallas. |
| --ios | -i | toggle (=true) | Requests assets for iOS using the ios_generic [(pallas/utils/Audience.py:L5)](../src/pallas/utils/Audience.py) Asset Audience |
| --mac | -m | toggle (=true) | Requests assets for macOS using the macos_generic [(pallas/utils/Audience.py:L4)](../src/pallas/utils/Audience.py) Asset Audience |
| --apple-tv | --tv | toggle (=true) | Requests assets for tvos using the tvos_generic Asset Audience |
| --vision-pro | -p | toggle (=true) | Requests assets for VisionOS using the visionpro_generic Asset Audience |
| --apple-watch | -w | toggle (=true) | Requests assets for WatchOS using the watchos_generic Asset Audience |
| --list-identifiers | -ids | toggle (=true) | Lists all available asset identifiers (ex. com.apple.MobileAsset.MacSoftwareUpdate) |
| --identifier | | store | Specifies a (or many) specific identifier(s) to fetch |
| --os-ver | -os | store | Specifies an OS version to use while making requests to Pallas. |

## Current state of testing
<details open>
<summary>
[ ] TODO: Add testing badges here
</summary>

- [ ] macOS Testing Badge

- [ ] Linux Testing Badge

- [ ] Successful requests for individual assets (independent of each OS, only needs to be accessible by 1 OS)
</details>
- [ ] TODO: Complete writing tests for src/pallas/response.py

- [ ] TODO: 