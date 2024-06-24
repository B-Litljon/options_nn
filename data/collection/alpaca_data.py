import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import alpaca
from alpaca.data.historical.screener import ScreenerClient
from alpaca.data.live.stock import StockDataStream
from alpaca.data.historical.stock import (
    StockHistoricalDataClient,
    StockBarsRequest,
    StockTradesRequest,
    StockQuotesRequest,
)
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.live.option import OptionDataStream
from alpaca.data.historical.option import (
    OptionHistoricalDataClient,
    OptionBarsRequest,
    OptionSnapshotRequest,
    OptionChainRequest,
)
from alpaca.data.requests import GetAssetsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOptionContractsRequest
from alpaca.trading.enums import AssetStatus, ExerciseStyle
from alpaca.common.exceptions import APIError


class DataCollector:
    def __init__(self, api_key, secret_key, symbol, timeframe, days_back):
        self.historical_client = StockHistoricalDataClient(api_key, secret_key)
        self.historical_option_client = OptionHistoricalDataClient(api_key, secret_key)
        self.asset_screener = ScreenerClient(api_key, secret_key)
        self.live_client = StockDataStream(api_key, secret_key)
        self.option_live_client = OptionDataStream(api_key, secret_key)
        self.symbol = symbol
    

    # we can use the screener api to filter for the most active stocks or market movers
    # then return a dictionary of whichever stocks we like
    # with the symbol as the key, and the ohlcv data as the values 
    # then we can request the options chain data for each stock in the dictionary

    def get_stock_data(self, symbol, timeframe, days_back):
        end = datetime.now(ZoneInfo("America/Pacific"))
        start = end - timedelta(days=days_back)
        data = StockBarsRequest(symbol, timeframe, start, end)
        return self.historical_client.get_bars(data)
    
    def most_active_stocks(self):
        data = self.asset_screener.get_most_actives()
        return data
    
    def market_movers(self):
        data = self.asset_screener.get_market_movers()
        return data