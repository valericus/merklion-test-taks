#!/usr/bin/env python3.6

import logging

logging.basicConfig(level=logging.DEBUG)

import asyncio
from typing import Callable, Iterable

import aiohttp

from common.currency_pair import CurrencyPair
from common.market_data import MarketData
from exchanges import Livecoin, Bittrex

exchange_classes = [Livecoin, Bittrex]

btc_ltc = CurrencyPair('BTC', 'LTC')
ltc_eth = CurrencyPair('LTC', 'ETH')
eth_btc = CurrencyPair('ETH', 'BTC')


def report(message: str, md: Iterable[MarketData], fltr: Callable, key: Callable):
    proper_md = fltr(md, key=key)
    print(message.format(key(proper_md), proper_md.source))


def exception_handler(loop: asyncio.AbstractEventLoop, context):
    logging.error(context['exception'])


async def main(loop: asyncio.AbstractEventLoop, pairs: Iterable[CurrencyPair]):
    async with aiohttp.ClientSession(loop=loop) as session:
        exchanges = [e(session) for e in exchange_classes]

        futures = list()
        for exchange in exchanges:
            for pair in pairs:
                #task = loop.create_task(exchange.get_market_data(pair))
                futures.append(exchange.get_market_data(pair))

        market_data = dict()
        for md in await asyncio.gather(*futures, loop=loop):
            if md is not None:
                market_data.setdefault(md.pair, list())
                market_data[md.pair].append(md)

        return market_data

loop = asyncio.get_event_loop()
loop.set_exception_handler(exception_handler)
result = loop.run_until_complete(main(loop, (btc_ltc, ltc_eth, eth_btc)))


report('Minimal bid for BTC/LTC pair is {} ({})', result[btc_ltc], min, lambda x: x.best_bid)
#report('Minimal bid for LTC/ETH pair is {} ({})', result[ltc_eth], min, lambda x: x.best_bid)
report('Maximal ask for ETH/BTC pair is {} ({})', result[eth_btc], max, lambda x: x.best_ask)
