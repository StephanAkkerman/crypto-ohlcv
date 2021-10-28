# Based on Gursel Karacor's LinkedIn article
# https://www.linkedin.com/pulse/download-historical-data-all-cryptocoins-ccxt-gursel-karacor/

import ccxt
import pandas as pd


def fetchData(exchange, symbol, timeframe, since=None, limit=None):
    """
    Pandas DataFrame with the latest OHLCV data from specified exchange.

    Parameters
    --------------
    exchange : string, check the exchange_list to see the supported exchanges. For instance "binance".
    symbol : string, combine the coin you want to get with the pair and add a / in between. For instance BTC/USDT.
    timeframe : string, the timeframe following guidelines from CCXT. For instance "4h" for the 4 hour candles.
    since: integer, UTC timestamp in milliseconds. Default is None.
    limit : integer, the amount of rows that should be returned. For instance 100, default is None.

    All the timeframe options are: '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'
    """

    # Supported exchanges
    exchange_list = [
        "binance",
        "bitfinex",
        "bytetrade",
        "ftx",
        "kraken",
        "poloniex",
        "upbit",
        "acx",
        "bequant",
        "bigone",
        "bitforex",
        "bitkk",
        "bitz",
        "btcalpha",
        "coinex",
        "crex24",
        "digifinex",
        "gateio",
        "hitbtc2",
        "huobipro",
        "huobiru",
        "kucoin",
        "lbank",
        "okex",
        "okex3",
        "stex",
        "upbit",
        "whitebit",
        "zb",
    ]

    # Get our Exchange
    try:
        exchange = getattr(ccxt, exchange)()

    # In case exchange is not supported by ccxt
    except AttributeError:
        print("-" * 36, " ERROR ", "-" * 35)
        print(
            'Exchange "{}" not found. Please check the exchange is supported.'.format(
                exchange
            )
        )
        print("Supported exchanges are:")
        print(exchange_list)
        print("-" * 80)
        quit()

    # Check if fetching of OHLC Data is supported
    if exchange.has["fetchOHLCV"] != True:
        print("-" * 36, " ERROR ", "-" * 35)
        print(
            "{} does not support fetching OHLC data. Please use another  exchange".format(
                exchange
            )
        )
        print("-" * 80)
        quit()

    # Check requested timeframe is available. If not return a helpful error.
    if (not hasattr(exchange, "timeframes")) or (timeframe not in exchange.timeframes):
        print("-" * 36, " ERROR ", "-" * 35)
        print(
            "The requested timeframe ({}) is not available from {}\n".format(
                timeframe, exchange
            )
        )
        print("Available timeframes are:")
        for key in exchange.timeframes.keys():
            print("  - " + key)
        print("-" * 80)
        quit()

    # Check if the symbol is available on the Exchange
    exchange.load_markets()
    if symbol not in exchange.symbols:
        print("-" * 36, " ERROR ", "-" * 35)
        print(
            "The requested symbol ({}) is not available from {}\n".format(
                symbol, exchange
            )
        )
        print("Available symbols are:")
        for key in exchange.symbols:
            print("  - " + key)
        print("-" * 80)
        quit()

    # Get data
    data = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
    header = ["Timestamp", "open", "high", "low", "close", "volume"]
    df = pd.DataFrame(data, columns=header)

    # Convert Timestamp to date
    df.Timestamp = (
        df.Timestamp / 1000
    )  # Timestamp is 1000 times bigger than it should be in this case
    df["date"] = pd.to_datetime(df.Timestamp, unit="s")

    # Drop timestamp and replace it by date
    df = df[["date", "open", "high", "low", "close", "volume"]]

    # The default values are string, so convert these to numeric values
    df["open"] = pd.to_numeric(df["open"])
    df["high"] = pd.to_numeric(df["high"])
    df["low"] = pd.to_numeric(df["low"])
    df["close"] = pd.to_numeric(df["close"])
    df["volume"] = pd.to_numeric(df["volume"])

    # Returned DataFrame should consists of columns: index starting from 0, date as datetime, open, high, low, close, volume in numbers
    return df
