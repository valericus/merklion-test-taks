import logging

from common.currency_pair import CurrencyPair
from common.market_data import MarketData
from exchanges.abstract_exchange import AbstractExchange, AbstractExchangeError


class BittrexError(AbstractExchangeError):
    pass


class Bittrex(AbstractExchange):
    base_url = 'https://bittrex.com/api/v1.1/public'

    exception = BittrexError

    async def get_market_data(self, pair: CurrencyPair) -> MarketData:
        response = await self.get(
            '/getticker',
            {'market': f'{pair.currency}-{pair.base_currency}'}
        )
        try:
            result = await self.json(response, lambda x: x.get('success'))
            md = MarketData(
                source=self.__class__.__name__,
                pair=pair,
                best_bid=result['result']['Bid'],
                best_ask=result['result']['Ask'],
                last_trade=result['result']['Last'],
                vwap=None
            )
            logging.debug(md)
            return md
        except self.exception as e:
            logging.error(e)
