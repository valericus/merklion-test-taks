from common.currency_pair import CurrencyPair
from common.market_data import MarketData
from exchanges.abstract_exchange import AbstractExchange, AbstractExchangeError


class LivecoinError(AbstractExchangeError):
    pass


class Livecoin(AbstractExchange):
    base_url = 'https://api.livecoin.net'

    exception = LivecoinError

    # Example of API response
    # {
    #     "last": 431.15098,
    #     "high": 447,
    #     "low": 420,
    #     "volume": 491.24533286,
    #     "vwap": 440.11749153148,
    #     "max_bid": 447,
    #     "min_ask": 420,
    #     "best_bid": 429.21,
    #     "best_ask": 431.14998
    # }

    async def get_market_data(self, pair: CurrencyPair) -> MarketData:
        result = await self.json(
            await self.get(
                '/exchange/ticker',
                {'currencyPair': f'{pair.currency}/{pair.base_currency}'}
            ),
            lambda x: x.get('best_bid'),
            lambda x: x.get('errorMessage')
        )

        return self.get_md(
            pair=pair,
            best_bid=result['best_bid'],
            best_ask=result['best_ask'],
            last_trade=result['last'],
            vwap=result['vwap']
        )
