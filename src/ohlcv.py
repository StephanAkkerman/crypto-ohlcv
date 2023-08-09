import datetime
import time

import ccxt
import pandas as pd
from dateutil.parser import parse

# Save the exchanges that are useful
exchanges_with_ohlcv = []

for exchange_id in ccxt.exchanges:
    exchange = getattr(ccxt, exchange_id)()
    if exchange.has["fetchOHLCV"]:
        exchanges_with_ohlcv.append(exchange_id)


def get_candle_diff(timeframe):
    # ms calculations based on: http://convertlive.com/nl/u/converteren/minuten/naar/milliseconden
    # 1m = 60000 ms
    if timeframe == "1m":
        return 60000
    elif timeframe == "3m":
        return 3 * 60000
    elif timeframe == "5m":
        return 5 * 60000
    elif timeframe == "15m":
        return 15 * 60000
    elif timeframe == "30m":
        return 30 * 60000

    # 1h = 3600000 ms
    elif timeframe == "1h":
        return 3600000
    elif timeframe == "2h":
        return 2 * 3600000
    elif timeframe == "4h":
        return 4 * 3600000
    if timeframe == "6h":
        return 6 * 3600000
    elif timeframe == "8h":
        return 8 * 3600000
    elif timeframe == "12h":
        return 12 * 3600000

    # 1d = 86400000 ms
    elif timeframe == "1d":
        return 86400000
    elif timeframe == "3d":
        return 3 * 86400000
    elif timeframe == "1W":
        return 604800000
    elif timeframe == "1M":
        return 2629800000


def fetch_data(
    exchange: str = "binance",
    symbol: str = "BTC/USDT",
    timeframe: str = "1d",
    since=None,
    limit: int = None,
    file_name: str = None,
) -> pd.DataFrame:
    """
    Pandas DataFrame with the latest OHLCV data from specified exchange.

    Parameters
    --------------
    exchange : string, check the exchange_list to see the supported exchanges. For instance "binance".
    symbol : string, combine the coin you want to get with the pair and add a `/` in between. For instance BTC/USDT.
    timeframe : string, the timeframe following guidelines from CCXT. For instance "4h" for the 4 hour candles.
    since: integer, UTC timestamp in milliseconds. Default is None, which means will not take the start date into account.
    The behavior of this parameter depends on the exchange.
    limit : integer, the amount of rows that should be returned. For instance 100, default is None, which means 500 rows.

    All the timeframe options are: '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'
    """

    # If it is a string, convert it to a datetime object
    if isinstance(since, str):
        since = parse(since)

    if isinstance(since, datetime.datetime):
        since = int(since.timestamp() * 1000)

    # Always convert to lowercase
    exchange = exchange.lower()

    if exchange not in exchanges_with_ohlcv:
        raise ValueError(
            f"{exchange} is not a supported exchange. Please use one of the following: {exchanges_with_ohlcv}"
        )

    timeframes = [
        "1m",
        "3m",
        "5m",
        "15m",
        "30m",
        "1h",
        "2h",
        "4h",
        "6h",
        "8h",
        "12h",
        "1d",
        "3d",
        "1w",
        "1M",
    ]

    if timeframe not in timeframes:
        raise ValueError(
            f"{timeframe} is not supported. Please use one of the following: {timeframes}"
        )

    exchange = getattr(ccxt, exchange)()

    # Check requested timeframe is available.
    if timeframe not in exchange.timeframes:
        raise ValueError(
            f"{timeframe} is not supported by {exchange}. Please use one of the following: {exchange.timeframes}"
        )

    exchange.load_markets()
    # Check if the symbol is available on the Exchange
    if symbol not in exchange.symbols:
        raise ValueError(
            f"{symbol} is not supported by {exchange}. Please use one of the following: {exchange.symbols}"
        )

    # Convert ms to seconds, so we can use time.sleep() for multiple calls
    rate_limit = exchange.rateLimit / 1000

    # Get data
    data = exchange.fetch_ohlcv(symbol, timeframe, since, limit)

    while len(data) < limit:
        # If the data is less than the limit, we need to make multiple calls
        # Shift the since date to the last date of the data
        since = data[-1][0] + get_candle_diff(timeframe)

        # Sleep to prevent rate limit errors
        time.sleep(rate_limit)

        # Get the remaining data
        new_data = exchange.fetch_ohlcv(symbol, timeframe, since, limit - len(data))
        data += new_data

        if len(new_data) == 0:
            break

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

    if file_name:
        df.to_csv(file_name, index=False)

    # Returned DataFrame should consists of columns: index starting from 0, date as datetime, open, high, low, close, volume in numbers
    return df
