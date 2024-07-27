from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pandas as pd
import numpy as np

from alpaca.data import (
    StockHistoricalDataClient,
    StockBarsRequest,
    OptionChainRequest
)
from alpaca.data.requests import MostActivesRequest
from alpaca.data.historical.option import OptionHistoricalDataClient
from alpaca.data.historical.screener import ScreenerClient


class Watchlist:
    """
    this class uses the alpaca-py screener api reference:  `https://docs.alpaca.markets/reference/mostactives-1`
    the screener returns a json response containing a list 'most_actives' contains a list of dictionaries, each dictionary contains the following keys:
        - symbol: the stock symbol
        - volume: the volume of the stock
        - trade_count: the number of trades for the stock

        once the data has been requested, the class will store
         
        the data in a dictionary with the symbol as the key and the volume and trade_count as values

        the class will be used in other  classes, so that the data being requested is dynamic 
    """
    def __init__(self, api_key, secret_key):
        self.stock_screener = ScreenerClient(api_key, secret_key)
        self.active_stocks = {}

    def request_most_active_assets(self): 
        request_params = MostActivesRequest
        response = self.stock_screener.get_most_actives(request_params)
        high_volume_assets = response['most_actives'] 
        
        for asset in high_volume_assets:
            symbol = asset['symbol']
            volume = asset['volume']
            trade_count = asset['trade_count']
            self.active_stocks[symbol] = { # active_stocks = {[symbol]: {'volume': volume, 'trade_count': trade_count}}
                'volume': volume,
                'trade_count': trade_count
            }

    def get_watchlist(self):
        return self.active_stocks 
        
    

# I am refactoring the classes in this file to be more modular, each part should build upon the other. the watchlist collects the most actives
# candles data will collect the historical data for the watchlist assets, then the option data will collect the option data for the watchlist assets
# I will also make a class that cleans the data and prepares it for the model called prepare data with pandas and numpy.
class CandlestickData:
    def __init__(self, api_key, secret_key):
        self.historical_asset = StockHistoricalDataClient(api_key, secret_key)
    # timeframe will be a variable passed in from a higher level class via an attribute 
    # this allows for the data to be collected from different timeframes 
    def get_bars(self, symbol, timeframe, start, end):
        data = StockBarsRequest(symbol, timeframe, start, end)
        return self.historical_asset.get_bars(data)


# all this code is depricated now, I will be updating with cleaner more modular code soon. as of now, just using this as a reference to the api docs to save time

# class StockDataCollector:
#     def __init__(self, api_key, secret_key, timeframe, days_back):
#         self.historical_asset = StockHistoricalDataClient(api_key, secret_key)
#         self.asset_screener = ScreenerClient(api_key, secret_key)
#         self.timeframe = timeframe
#         self.days_back = days_back
#         self.watchlist = {}

#     def stocks_to_watch(self):
#         request_params = MostActivesRequest()
#         response = self.asset_screener.get_most_actives(request_params) 
#         active_stock_data = response.get("most_actives", [])

#         # Extract only the symbols and add them to the watchlist
#         self.watchlist = {stock['symbol']: None for stock in active_stock_data}

#     def get_watchlist(self):
#         return self.watchlist

#     def get_stock_data(self, symbol):
#         end = datetime.now(ZoneInfo("America/Los_Angeles"))
#         start = end - timedelta(days=self.days_back)
#         data = StockBarsRequest(symbol, self.timeframe, start, end)
#         return self.historical_asset.get_bars(data)

# class OptionDataCollector:
#     def __init__(self, api_key, secret_key):
#         self.historic_options = OptionHistoricalDataClient(api_key, secret_key)

#     def get_option_chain_data(self, symbol):
#         request_params = OptionChainRequest(symbol=symbol)
#         option_chain_snapshot = self.historic_options.get_option_chain(request_params)
#         return option_chain_snapshot

# class MarketDataCollector:
#     def __init__(self, api_key, secret_key, timeframe, days_back):
#         self.stock_collector = StockDataCollector(api_key, secret_key, timeframe, days_back)
#         self.option_collector = OptionDataCollector(api_key, secret_key)

#     def populate_watchlist(self):
#         self.stock_collector.stocks_to_watch()
#         print(f"Watchlist populated with {len(self.stock_collector.get_watchlist())} stock symbols.")

#     def collect_data_for_watchlist(self):
#         self.populate_watchlist()
#         collected_data = {}
#         for symbol in self.stock_collector.get_watchlist():
#             collected_data[symbol] = {
#                 'stock_data': self.stock_collector.get_stock_data(symbol),
#                 'option_chain_data': self.option_collector.get_option_chain_data(symbol),
#             }
#         return collected_data