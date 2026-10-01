from datetime import datetime, timedelta

import pandas as pd
import pytest

from FinanceDataReader.krx import data, listing


@pytest.fixture(params=["index", "stock", "delisting"])
def reader(request, monkeypatch):
    windows = []

    def fetch(*args):
        start, end = args[-2:]
        windows.append((start, end))
        dates = pd.date_range(start, end)
        if request.param == "index":
            frame = pd.DataFrame({"TRD_DD": dates.strftime("%Y-%m-%d")})
            for column in (
                "CLSPRC_IDX", "FLUC_TP_CD", "PRV_DD_CMPR", "UPDN_RATE",
                "OPNPRC_IDX", "HGPRC_IDX", "LWPRC_IDX", "ACC_TRDVOL",
                "ACC_TRDVAL", "MKTCAP",
            ):
                frame[column] = "1"
            return frame
        if request.param == "stock":
            return pd.DataFrame({"Date": dates, "Close": 1})
        return pd.DataFrame({"DelistingDate": dates, "Name": "stock"})

    if request.param == "index":
        monkeypatch.setattr(data, "_krx_index_price_2years", fetch)
        read, args = data._krx_index_price, ("1", "001")
    elif request.param == "stock":
        monkeypatch.setattr(data, "_krx_stock_price_2years", fetch)
        read, args = data._krx_stock_price, ("KR7005930003",)
    else:
        monkeypatch.setattr(listing, "_krx_delisting_2years", fetch)
        read, args = listing._krx_delisting, ()

    def read_dates(start, end):
        frame = read(*args, start, end)
        if request.param == "delisting":
            return pd.DatetimeIndex(frame["DelistingDate"])
        return frame.index

    return read_dates, windows


@pytest.mark.parametrize(
    "start,end,first_window_end,window_count",
    [
        (datetime(2020, 2, 29), datetime(2020, 3, 1), datetime(2022, 2, 27), 1),
        (datetime(2024, 2, 29), datetime(2024, 3, 1), datetime(2026, 2, 27), 1),
        (datetime(2024, 2, 29), datetime(2028, 3, 1), datetime(2026, 2, 27), 3),
        (datetime(2024, 1, 1), datetime(2026, 1, 2), datetime(2025, 12, 31), 2),
    ],
)
def test_krx_date_windows(reader, start, end, first_window_end, window_count):
    read_dates, windows = reader

    dates = read_dates(start, end)

    pd.testing.assert_index_equal(dates, pd.date_range(start, end), check_names=False)
    assert len(windows) == window_count
    assert windows[0] == (start, first_window_end)
    for previous, current in zip(windows, windows[1:]):
        assert current[0] == previous[1] + timedelta(days=1)
    assert dates.is_unique
