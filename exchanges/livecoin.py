import logging

from common.currency_pair import CurrencyPair
from common.market_data import MarketData
from exchanges.abstract_exchange import AbstractExchange, AbstractExchangeError


class LivecoinError(AbstractExchangeError):
    pass


class Livecoin(AbstractExchange):
    base_url = 'https://api.livecoin.net'

    exception = LivecoinError

    async def get_market_data(self, pair: CurrencyPair) -> MarketData:
        response = await self.get(
            '/exchange/ticker',
            {'currencyPair': f'{pair.currency}/{pair.base_currency}'}
        )
        result = await self.json(response, lambda x: x.get('best_bid'))
        return MarketData(
            source=self.__class__.__name__,
            pair=pair,
            best_bid=result['best_bid'],
            best_ask=result['best_ask'],
            last_trade=result['last'],
            vwap=result['vwap']
        )

