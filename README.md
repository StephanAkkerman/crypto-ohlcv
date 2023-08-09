# Crypto OHLCV (Open High Low Close Volume)
[![Python 3.8](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![MIT License](https://img.shields.io/github/license/StephanAkkerman/Crypto_OHLCV.svg?color=brightgreen)](https://opensource.org/licenses/MIT)

---

crypto-ohlcv is a simple Python script that lets you fetch historical OHLCV data from ccxt supported exchanges.
I wrote this script, because my other script focussed solely on Binance, whereas this one supports many exchanges.
It consists of one simple function called `fetch_data()`, that returns a pandas Dataframe, readible by TensorTrade.

## How to use
- Add `ohlcv.py` located in src to same directory you're working in.
- Write: `from ohlcv import fetch_data`.
- To get the latest 500 daily data points of OHLCV on the BTC/USDT pair from Binance, write: `fetch_data(exchange='binance', symbol="BTC/USDT", timeframe='1d', limit=500)`.
- The result will be a pandas DataFrame consisting of the latest 500 daily candles of BTC/USDT on Binance.

## Supported exchanges
The `exchange` parameter should be one of the exchanges supported by ccxt, currently these are:
- 'binance'
- 'bitfinex'
- 'bytetrade'
- 'ftx'
- 'kraken'
- 'poloniex'
- 'upbit'
- 'acx'
- 'bequant'
- 'bigone'
- 'bitforex'
- 'bitkk'
- 'bitz'
- 'btcalpha'
- 'coinex'
- 'crex24'
- 'digifinex'
- 'gateio'
- 'hitbtc2'
- 'huobipro'
- 'huobiru'
- 'kucoin'
- 'lbank'
- 'okex'
- 'okex3'
- 'stex'
- 'upbit'
- 'whitebit'
- 'zb'

## Symbols
`Symbol` can be any pair available on the specified exchange.

## Time frames
Supported time frames are: '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'.

## Limit
`Limit` is the number of rows you would like to have returned, leaving this unspecified will return most available.
Using `since` as parameter will change the starting point of gathering the data, this is an integer consisting of UTC timestamp in milliseconds. You can also specify it as a string or datetime object, it will automatically be converted to the right format.
