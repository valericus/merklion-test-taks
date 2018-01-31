from common.currency_pair import CurrencyPair
from common.market_data import MarketData
from exchanges.abstract_exchange import AbstractExchange, AbstractExchangeError


class BittrexError(AbstractExchangeError):
    pass


class Bittrex(AbstractExchange):
    base_url = 'https://bittrex.com/api/v1.1/public'

    exception = BittrexError

    # Example of API response
    # {
    #     "success": true,
    #     "message": "",
    #     "result": {
    #         "Bid": 2.05670368,
    #         "Ask": 3.35579531,
    #         "Last": 3.35579531
    #     }
    # }

    async def get_market_data(self, pair: CurrencyPair) -> MarketData:
        result = await self.json(
            await self.get(
                '/getticker',
                {'market': f'{pair.base_currency}-{pair.currency}'}
            ),
            lambda x: x.get('success'),
            lambda x: x.get('message')
        )

        return self.get_md(
            pair=pair,
            best_bid=result['result']['Bid'],
            best_ask=result['result']['Ask'],
            last_trade=result['result']['Last']
        )
