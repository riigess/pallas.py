from enum import Enum

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
    UAFIFPlanner = "com.apple.if.planner"
    UAFIFPlannerOverrides = "com.apple.if.planner.overrides"

    def all_assets() -> dict:
        to_return = {}
        for item in Assets.__dict__:
            if "UAF" in item:
                to_return.update({item: Assets.__dict__[item]})
        return to_return
