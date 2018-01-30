import json
import logging
from typing import Callable

from aiohttp import ClientSession, ClientResponse
from decimal import Decimal

from common.currency_pair import CurrencyPair
from common.market_data import MarketData


class AbstractExchangeError(RuntimeError):
    pass


class AbstractExchange:

    @staticmethod
    def loads(data: str):
        return json.loads(data, parse_float=Decimal, parse_int=Decimal)

    @property
    def base_url(self) -> str:
        raise NotImplementedError

    @property
    def exception(self) -> RuntimeError:
        raise NotImplementedError

    def __init__(self, session: ClientSession):
        self.session = session

    async def get_market_data(self, pair: CurrencyPair) -> MarketData:
        raise NotImplementedError

    async def get(self, method: str, params: dict) -> ClientResponse:
        """
        Perfor HTTP GET request and raise if result status code is over 399

        :param method: path that should be added to `base_url`
        :param params: query params
        :return: server response
        """
        url = f'{self.base_url}{method}'
        result = await self.session.get(url, params=params)
        result.raise_for_status()
        return result

    async def json(self, response: ClientResponse, verify: Callable[[dict], bool]) -> dict:
        """
        Parse response from exchange as JSON and verify it with given callback.

        :param response: response that should be parsed
        :param verify: function that receives dictionary with response and
         returns true if it's valid exchange response
        :return: dictionary that can be serialized to MarketData item
        """
        result = await response.json(loads=self.loads)
        logging.debug(f'Raw exchange response: {result}')
        if verify(result):
            return result
        else:
            raise self.exception(result)

    def get_md(self, pair: CurrencyPair, best_bid: Decimal, best_ask: Decimal,
               last_trade: Decimal, vwap: Decimal=None):
        md = MarketData(
            source=self.__class__.__name__,
            pair=pair,
            best_bid=best_bid,
            best_ask=best_ask,
            last_trade=last_trade,
            vwap=vwap
        )
        logging.debug(f'Parsed MarketData: {md}')
        return md
