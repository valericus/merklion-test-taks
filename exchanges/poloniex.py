from common.currency_pair import CurrencyPair
from common.market_data import MarketData
from exchanges.abstract_exchange import AbstractExchange, AbstractExchangeError


class PoloniexError(AbstractExchangeError):
    pass


class Poloniex(AbstractExchange):
    base_url = 'https://poloniex.com'

    exception = PoloniexError

    @staticmethod
    def __pair_to_str(pair: CurrencyPair) -> str:
        return f'{pair.base_currency}_{pair.currency}'

    async def get_market_data(self, pair: CurrencyPair) -> MarketData:
        pair_str = self.__pair_to_str(pair)

        result = await self.json(
            response=await self.get('/public', {'command': 'returnTicker'}),
            verify=lambda x: x.get(pair_str)
        )

        return self.get_md(
            pair=pair,
            best_bid=result[pair_str]['highestBid'],
            best_ask=result[pair_str]['lowestAsk'],
            last_trade=result[pair_str]['last']
        )
