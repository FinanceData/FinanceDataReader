"""
FinanceDataReader CLI

Usage:
    fdr price SYMBOL [--start START] [--end END] [--format FORMAT]
    fdr snap TICKER [--format FORMAT]
    fdr listing MARKET [--format FORMAT]
    fdr --version
"""
import argparse
import sys

import pandas as pd


def _format_output(df: pd.DataFrame, fmt: str) -> str:
    """Format DataFrame for CLI output."""
    if fmt == "csv":
        return df.to_csv()
    elif fmt == "json":
        return df.to_json(orient="records", force_ascii=False, indent=2, date_format="iso")
    elif fmt == "markdown":
        return df.to_markdown()
    else:  # table
        return df.to_string()


def cmd_price(args):
    """Fetch price data (timeseries)."""
    from FinanceDataReader import DataReader

    df = DataReader(args.symbol, start=args.start, end=args.end)
    print(_format_output(df, args.format))


def cmd_snap(args):
    """Fetch snapshot data."""
    from FinanceDataReader import SnapDataReader

    df = SnapDataReader(args.ticker)
    print(_format_output(df, args.format))


def cmd_listing(args):
    """Fetch stock listing."""
    from FinanceDataReader.data import StockListing

    df = StockListing(args.market)
    print(_format_output(df, args.format))



def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="fdr",
        description="FinanceDataReader - Financial data from the command line",
    )
    from FinanceDataReader import __version__
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"FinanceDataReader {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ── price ──────────────────────────────────────────────────
    p_price = subparsers.add_parser(
        "price",
        help="Fetch price timeseries (DataReader)",
        description=(
            "Fetch OHLCV price data.\n"
            "Examples:\n"
            "  fdr price 005930 --start 2024-01-01\n"
            "  fdr price AAPL --start 2024 --end 2024-06-30 --format csv\n"
            "  fdr price FRED:DEXKOUS --start 2020\n"
            "  fdr price KRX:KOSPI --start 2023\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_price.add_argument("symbol", help="Symbol or code (e.g. 005930, AAPL, FRED:DEXKOUS)")
    p_price.add_argument("-s", "--start", default=None, help="Start date (e.g. 2024-01-01)")
    p_price.add_argument("-e", "--end", default=None, help="End date (e.g. 2024-12-31)")
    p_price.add_argument(
        "-f", "--format", default="table",
        choices=["table", "csv", "json", "markdown"],
        help="Output format (default: table)",
    )
    p_price.set_defaults(func=cmd_price)

    # ── snap ───────────────────────────────────────────────────
    p_snap = subparsers.add_parser(
        "snap",
        help="Fetch data snapshot (SnapDataReader)",
        description=(
            "Fetch snapshot data.\n"
            "Examples:\n"
            "  fdr snap KRX/INDEX/LIST\n"
            "  fdr snap NAVER/STOCK/005930/FINSTATE\n"
            "  fdr snap ECOS/KEYSTAT/LIST\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_snap.add_argument("ticker", help="Snapshot ticker path (e.g. KRX/INDEX/LIST)")
    p_snap.add_argument(
        "-f", "--format", default="table",
        choices=["table", "csv", "json", "markdown"],
        help="Output format (default: table)",
    )
    p_snap.set_defaults(func=cmd_snap)

    # ── listing ────────────────────────────────────────────────
    p_listing = subparsers.add_parser(
        "listing",
        help="Fetch stock listing (StockListing)",
        description=(
            "Fetch stock listing for a market.\n"
            "Examples:\n"
            "  fdr listing KRX\n"
            "  fdr listing KOSPI --format csv\n"
            "  fdr listing NASDAQ --format json\n"
            "  fdr listing S&P500\n"
            "  fdr listing ETF/KR\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_listing.add_argument(
        "market",
        help="Market code (KRX, KOSPI, KOSDAQ, NASDAQ, NYSE, S&P500, ETF/KR, ...)",
    )
    p_listing.add_argument(
        "-f", "--format", default="table",
        choices=["table", "csv", "json", "markdown"],
        help="Output format (default: table)",
    )
    p_listing.set_defaults(func=cmd_listing)


    args = parser.parse_args(argv)
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
