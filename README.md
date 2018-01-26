The script pulls four crypto-currency exchanges (Livecoin, Bittrex, Bitfinex, Poloniex)
in asynchronous ways and reports best prices for following pairs:

* minimal bid for BTC/LTC,
* minimal bid for LTC/ETH,
* maximal ask for ETH/BTC.

List of currencies is hardcoded to avoid inventing of complex data extracting language.

To run script you need Python 3.6 or higher and aiohttp.

```
pip install -r requirements
$ ./app.py
Minimal bid for BTC/LTC pair is 0.01575899 (Bittrex)
Minimal bid for LTC/ETH pair is 0.01575899 (Poloniex)
Maximal ask for ETH/BTC pair is 0.09358797 (Livecoin)
```