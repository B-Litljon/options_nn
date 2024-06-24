import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from alpaca.data import (
    StockHistoricalDataClient, OptionHistoricalDataClient, 
    StockBarsRequest, OptionChainRequest, OptionContractsRequest
)
from alpaca.data.live import StockDataStream, OptionDataStream
from alpaca.data.historical.screener import ScreenerClient

from alpaca.trading.requests import GetOptionContractsRequest
from alpaca.trading.enums import AssetStatus, ContractType, ContractStyle



class DataCollector:
    def __init__(self, api_key, secret_key, symbol, timeframe, days_back):
        self.historical_asset = StockHistoricalDataClient(api_key, secret_key)
        self.historical_options = OptionHistoricalDataClient(api_key, secret_key)
        self.asset_screener = ScreenerClient(api_key, secret_key)
        self.stream_stock = StockDataStream(api_key, secret_key)
        self.stream_options = OptionDataStream(api_key, secret_key)
        self.symbol = symbol
        self.timeframe = timeframe
        self.days_back = days_back
    

    # we can use the screener api to filter for the most active stocks or market movers
    # then return a dictionary of whichever stocks we like
    # with the symbol as the key, and the ohlcv data as the values 
    # then we can request the options chain data for each stock in the dictionary

    def get_most_active_stocks(self):
        data = self.asset_screener.get_most_actives()
        return data
    
    def get_market_movers(self):
        data = self.asset_screener.get_market_movers()
        return data
    
    def get_stock_data(self, symbol, timeframe, days_back):
        end = datetime.now(ZoneInfo("America/Pacific"))
        start = end - timedelta(days=days_back)
        data = StockBarsRequest(symbol, timeframe, start, end)
        return self.historical_asset.get_bars(data)
    
    def get_option_chain_data(self, symbol, expiration_date=None):
        # this method should be used to get the 
        pass

    def get_contracts(self, symbol, strike_price, put_call=None, expiration_date=None):
        pass