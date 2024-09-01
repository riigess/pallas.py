from enum import Enum

class UAFAssets(Enum):
    FMOverrides = "com.apple.MobileAsset.UAF.FM.Overrides"
    FMCodeLM = "com.apple.MobileAsset.UAF.FM.CodeLM"
    FMGenerativeModels = "com.apple.MobileAsset.UAF.FM.GenerativeModels"
    HandwritingSynthesis = "com.apple.MobileAsset.UAF.Handwriting.Synthesis"
    SafariBrowsingAssistant = "com.apple.MobileAsset.UAF.SafariBrowsingAssistant"
    SiriDialogAssets = "com.apple.MobileAsset.UAF.Siri.DialogAssets"
    SiriFindMy = "com.apple.MobileAsset.UAF.Siri.FindMyConfigurationFiles"
    SiriPlatformAssets = "com.apple.MobileAsset.UAF.Siri.PlatformAssets"
    SiriUnderstanding = "com.apple.MobileAsset.UAF.Siri.Understanding"
    SiriUnderstandingASRHammer = "com.apple.MobileAsset.UAF.Siri.UnderstandingASRHammer"
    SiriUnderstandingNLOverrides = "com.apple.MobileAsset.UAF.Siri.UnderstandingNLOverrides"
    SpeechASR = "com.apple.MobileAsset.UAF.Speech.AutomaticSpeechRecognition"
    SummarizationKit = "com.apple.MobileAsset.UAF.SummarizationKitConfiguration"
    IFPlanner = "com.apple.if.planner"
    IFPlannerOverrides = "com.apple.if.planner.overrides"

    def all_assets() -> list:
        to_return = []
        for key in UAFAssets.__dict__["_member_names_"]:
            to_return.append(UAFAssets.__dict__[key])
        return to_return
