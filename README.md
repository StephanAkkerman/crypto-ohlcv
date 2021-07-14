# Crypto_OHLCV
Crypto_OHLCV is a simple Python script that lets you fetch historical OHLCV data from ccxt supported exchanges.
I wrote this script, because my other script focussed solely on Binance, whereas this one supports many exchanges.
It consists of one simple function called fetchData, that returns a pandas Dataframe, readible by TensorTrade.

How to use:
- Add the Crypto_OHLCV.py to same directory you're working in.
- Write: from Crypto_OHLCV import fetchData.
- To get the latest 500 daily data points of OHLCV on the BTC/USDT pair from Binance, write: fetchData(exchange='binance', symbol="BTC/USDT", timeframe='1d', limit=500)

Exchange should be one of the exchanges supported by ccxt, currently these are:
-'binance'
-'bitfinex'
-'bytetrade'
-'ftx'
-'kraken'
-'poloniex'
-'upbit'
-'acx'
-'bequant'
-'bigone'
-'bitforex'
-'bitkk'
-'bitz'
-'btcalpha'
-'coinex'
-'crex24'
-'digifinex'
-'gateio'
-'hitbtc2'
-'huobipro'
-'huobiru'
-'kucoin'
-'lbank'
-'okex'
-'okex3'
-'stex'
-'upbit'
-'whitebit'
-'zb'

Symbol can be any pair availble on the specified exchange. 
Supported time frames are: '1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'.
Limit is the number of rows you would like to have returned, leaving this unspecified will return most available.
Using since as parameter will change the starting point of gathering the data, this is an integer consisting of UTC timestamp in milliseconds.
