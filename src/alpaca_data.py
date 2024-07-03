from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from alpaca.data import (
    StockHistoricalDataClient,
    StockBarsRequest,
    OptionChainRequest
)
from alpaca.data.historical.option import OptionHistoricalDataClient
from alpaca.data.historical.screener import ScreenerClient

class StockDataCollector:
    def __init__(self, api_key, secret_key, timeframe, days_back):
        self.historical_asset = StockHistoricalDataClient(api_key, secret_key)
        self.asset_screener = ScreenerClient(api_key, secret_key)
        self.timeframe = timeframe
        self.days_back = days_back
        self.watchlist = {}

    def stocks_to_watch(self):
        active_stock_data = self.asset_screener.get_most_actives()["most_actives"]
        for stock_info in active_stock_data:
            symbol = stock_info['symbol']
            self.watchlist[symbol] = {
                'trade_count': stock_info['trade_count'],
                'volume': stock_info['volume']
            }

    def get_stock_data(self, symbol):
        end = datetime.now(ZoneInfo("America/Los_Angeles"))
        start = end - timedelta(days=self.days_back)
        data = StockBarsRequest(symbol, self.timeframe, start, end)
        return self.historical_asset.get_bars(data)

class OptionDataCollector:
    def __init__(self, api_key, secret_key):
        self.historic_options = OptionHistoricalDataClient(api_key, secret_key)

    def get_option_chain_data(self, symbol):
        request_params = OptionChainRequest(symbol=symbol)
        option_chain_snapshot = self.historic_options.get_option_chain(request_params)
        return option_chain_snapshot

class MarketDataCollector:
    def __init__(self, api_key, secret_key, timeframe, days_back):
        self.stock_collector = StockDataCollector(api_key, secret_key, timeframe, days_back)
        self.option_collector = OptionDataCollector(api_key, secret_key)

    def populate_watchlist(self):
        self.stock_collector.stocks_to_watch()

    def collect_data_for_watchlist(self):
        self.populate_watchlist()
        collected_data = {}
        for symbol in self.stock_collector.watchlist:
            collected_data[symbol] = {
                'stock_data': self.stock_collector.get_stock_data(symbol),
                'option_chain_data': self.option_collector.get_option_chain_data(symbol),
            }
        return collected_data