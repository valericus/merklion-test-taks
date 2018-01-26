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

    def __init__(self, session: ClientSession = ClientSession()):
        self.session = session

    async def get_market_data(self, pair: CurrencyPair) -> MarketData:
        raise NotImplementedError

    async def get(self, method: str, params: dict) -> ClientResponse:
        url = f'{self.base_url}{method}'
        try:
            result = await self.session.get(url, params=params)
            result.raise_for_status()
            return result
        except:
            logging.exception(
                f'Error while retrieving data from {self.__class__.__name__}. '
                f'URL {url}, params {params}'
            )

    async def json(self, response: ClientResponse, verify: Callable[..., bool]) -> dict:
        result = await response.json(loads=self.loads)
        logging.debug(result)
        if verify(result):
            return result
        else:
            raise self.exception(result)
