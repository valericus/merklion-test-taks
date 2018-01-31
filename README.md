The script pulls four crypto-currency exchanges (Livecoin, Bittrex, Bitfinex, Poloniex)
in asynchronous way and reports some info about following pairs:

* minimal bid for LTC/BTC,
* minimal bid for LTC/ETH,
* maximal ask for ETH/BTC.

List of currencies is hardcoded to avoid inventing of complex data extracting language.

To run script you need Python 3.6 or higher and aiohttp.

```
$ pip install -r requirements
$ ./app.py
Minimal bid for LTC/BTC is 0.01593537 (Livecoin). 4 pairs found
Minimal bid for LTC/ETH is 0.14661140 (Bittrex). 1 pairs found
Maximal ask for ETH/BTC is 0.110201 (Livecoin). 4 pairs found
```