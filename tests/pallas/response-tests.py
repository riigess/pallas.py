from datetime import datetime

from pallas.response import Response
from pallas.utils.Assets import UAFAssets
from pallas.utils.Audience import Audience

def test_response():
    example_response = {
        "Nonce": "abc123",
        "PallasNonce": "def456",
        "SessionId": "ghi789",
        "LegacyXmlUrl": "jkl012",
        "PostingDate": datetime.now().strftime("%Y-%m-%d"),
        "Assets": [],
        "AssetSetId": "75cfb472-8fe2-4c35-8e2d-5e59fc97af03",
        "AssetAudience": "d0854246-c9d0-456e-a2c7-7183c5bf11d1"
    }
    resp = Response(response=example_response)
    assert resp.asset_audience == example_response["AssetAudience"]
    assert resp.asset_set_id == example_response["AssetSetId"]
    assert resp.assets == example_response["Assets"]
    assert resp.posting_date == example_response["PostingDate"]
    assert resp.legacy_xml_url == example_response["LegacyXmlUrl"]
    assert resp.session_id == example_response["SessionId"]
    assert resp.pallas_nonce == example_response["PallasNonce"]
    assert resp.nonce == example_response["Nonce"]
