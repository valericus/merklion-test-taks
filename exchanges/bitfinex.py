from common.currency_pair import CurrencyPair
from common.market_data import MarketData
from exchanges.abstract_exchange import AbstractExchange, AbstractExchangeError


class BitfinexError(AbstractExchangeError):
    pass


class Bitfinex(AbstractExchange):
    base_url = 'https://api.bitfinex.com'

    exception = BitfinexError

    async def get_market_data(self, pair: CurrencyPair) -> MarketData:
        result = await self.json(
            await self.get(
                f'/v1/pubticker/'
                f'{pair.currency.lower()}{pair.base_currency.lower()}'
            ),
            lambda x: x.get('bid')
        )

        return self.get_md(
            pair=pair,
            best_bid=result['bid'],
            best_ask=result['ask'],
            last_trade=result['last_price']
        )
