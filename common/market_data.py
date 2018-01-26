from collections import namedtuple

MarketData = namedtuple(
    'MarketData',
    ('source', 'pair', 'best_bid', 'best_ask', 'last_trade', 'vwap')
)