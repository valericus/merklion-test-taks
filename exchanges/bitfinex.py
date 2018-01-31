from aiohttp import ClientResponse

from common.currency_pair import CurrencyPair
from common.market_data import MarketData
from exchanges.abstract_exchange import AbstractExchange, AbstractExchangeError


class BitfinexError(AbstractExchangeError):
    pass


class Bitfinex(AbstractExchange):
    base_url = 'https://api.bitfinex.com'

    exception = BitfinexError

    # Example of API response
    # {
    #     "mid": "244.755",
    #     "bid": "244.75",
    #     "ask": "244.76",
    #     "last_price": "244.82",
    #     "low": "244.2",
    #     "high": "248.19",
    #     "volume": "7842.11542563",
    #     "timestamp": "1444253422.348340958"
    # }

    @staticmethod
    def raise_for_status(result: ClientResponse):
        # 400 Bad Request status is used by Bitfinex to indicate wrong ticker
        if result.status > 400:
            result.raise_for_status()

    async def get_market_data(self, pair: CurrencyPair) -> MarketData:
        pair_str = f'{pair.currency.lower()}{pair.base_currency.lower()}'

        result = await self.json(
            await self.get(f'/v1/pubticker/{pair_str}'),
            lambda x: x.get('bid'),
            lambda x: f'Error with {pair} ({pair_str}): {x.get("message")}'
        )

        return self.get_md(
            pair=pair,
            best_bid=result['bid'],
            best_ask=result['ask'],
            last_trade=result['last_price']
        )
