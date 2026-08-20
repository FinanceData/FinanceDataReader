import json

import pandas as pd

import FinanceDataReader as fdr
from FinanceDataReader.krx import listing as krx_listing


def test_krx_stock_listing_uses_correct_change_ratio_column(monkeypatch):
    class Response:
        text = json.dumps({"result": {"output": [{"max_work_dt": "20260329"}]}})

    cached_listing = pd.DataFrame(
        {
            "Code": ["005930"],
            "Name": ["Samsung"],
            "ChagesRatio": [0.14],
            "MarketId": ["STK"],
        }
    )

    monkeypatch.setattr(krx_listing.requests, "get", lambda *args, **kwargs: Response())
    monkeypatch.setattr(
        krx_listing.pd, "read_csv", lambda *args, **kwargs: cached_listing.copy()
    )

    result = fdr.StockListing("KRX")

    assert "ChangesRatio" in result.columns
    assert "ChagesRatio" not in result.columns


def test_krx_live_listing_uses_correct_change_ratio_column(monkeypatch):
    class Response:
        def __init__(self, text):
            self.text = text

    metadata = json.dumps({"result": {"output": [{"max_work_dt": "20260329"}]}})
    row = {
        "ISU_SRT_CD": "005930",
        "ISU_ABBRV": "Samsung",
        "TDD_CLSPRC": "70000",
        "SECT_TP_NM": "Electronics",
        "FLUC_TP_CD": "1",
        "CMPPREVDD_PRC": "100",
        "FLUC_RT": "0.14",
        "ACC_TRDVOL": "123",
        "ACC_TRDVAL": "8610000",
        "TDD_OPNPRC": "69900",
        "TDD_HGPRC": "70500",
        "TDD_LWPRC": "69500",
        "MKTCAP": "1000000",
        "LIST_SHRS": "1000",
        "MKT_NM": "KOSPI",
        "MKT_ID": "STK",
    }

    def fake_get(*args, **kwargs):
        return Response(metadata)

    def fake_post(*args, **kwargs):
        return Response(json.dumps({"OutBlock_1": [row]}))

    monkeypatch.setattr(krx_listing.requests, "get", fake_get)
    monkeypatch.setattr(krx_listing.requests, "post", fake_post)

    result = krx_listing.KrxMarcapListing("KRX").read()

    assert "ChangesRatio" in result.columns
    assert "ChagesRatio" not in result.columns
