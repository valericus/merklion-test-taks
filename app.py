#!/usr/bin/env python3.6

import asyncio
import logging
from typing import Callable, Sequence

import aiohttp

from common.currency_pair import CurrencyPair
from common.market_data import MarketData
from exchanges import Livecoin, Bittrex, Poloniex, Bitfinex

logging.basicConfig(level=logging.CRITICAL)

exchange_classes = [Livecoin, Bittrex, Poloniex, Bitfinex]

ltc_btc = CurrencyPair('LTC', 'BTC')
ltc_eth = CurrencyPair('LTC', 'ETH')
eth_btc = CurrencyPair('ETH', 'BTC')


def report(result_desc: str, pair: CurrencyPair, md: Sequence[MarketData], fltr: Callable, key: Callable):
    if md is not None:
        proper_md = fltr(md, key=key)
        print(f'{result_desc} for {pair.currency}/{pair.base_currency} is '
              f'{key(proper_md)} ({proper_md.source}). {len(md)} pairs found')
    else:
        print(f'{result_desc} for {pair.currency}/{pair.base_currency} not found')


async def main(loop: asyncio.AbstractEventLoop, pairs: Sequence[CurrencyPair]):
    async with aiohttp.ClientSession(loop=loop) as session:
        exchanges = [e(session) for e in exchange_classes]

        futures = list()
        for exchange in exchanges:
            for pair in pairs:
                futures.append(
                    asyncio.ensure_future(
                        exchange.get_market_data(pair),
                        loop=loop
                    )
                )

        market_data = dict()
        for item in await asyncio.gather(*futures, loop=loop, return_exceptions=True):
            if isinstance(item, MarketData):
                market_data.setdefault(item.pair, list())
                market_data[item.pair].append(item)
            else:
                logging.error(f'{item.__class__.__name__}: {item}')

        return market_data

loop = asyncio.get_event_loop()
result = loop.run_until_complete(main(loop, (ltc_btc, ltc_eth, eth_btc)))

report('Minimal bid', ltc_btc, result.get(ltc_btc), min, lambda x: x.best_bid)
report('Minimal bid', ltc_eth, result.get(ltc_eth), min, lambda x: x.best_bid)
report('Maximal ask', eth_btc, result.get(eth_btc), max, lambda x: x.best_ask)
