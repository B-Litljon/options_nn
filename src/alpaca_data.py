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
    def __init__(self, api_key, secret_key, timeframe, days_back):
        self.historical_asset = StockHistoricalDataClient(api_key, secret_key)
        self.asset_screener = ScreenerClient(api_key, secret_key)
        self.timeframe = timeframe
        self.days_back = days_back
        self.watchlist = {}  # Initialize the watchlist attribute

    def stocks_to_watch(self):
        active_stock_data = self.asset_screener.get_most_actives()["most_actives"]

        for stock_info in active_stock_data:
            symbol = stock_info['symbol']
            self.watchlist[symbol] = {
                'trade_count': stock_info['trade_count'],
                'volume': stock_info['volume']
            }

    def get_stock_data(self, symbol):
        end = datetime.now(ZoneInfo("America/Pacific"))
        start = end - timedelta(days=self.days_back)
        data = StockBarsRequest(symbol, self.timeframe, start, end)
        return self.historical_asset.get_bars(data)
    
    def get_option_chain_data(self, symbol, expiration_date=None):
        # this method should be used to get the 
        pass

    def get_option_contracts(self, symbol):
        request_params = GetOptionContractsRequest(
            underlying_symbols=list(symbol),  # assuming watchlist is a dict with stock names as keys
            status=AssetStatus.ACTIVE,  # default status
            expiration_date=None,  # default expiration date
            expiration_date_gte=None,
            expiration_date_lte=None,
            root_symbol=None,
            type=None,
            style=None,
            strike_price_gte=None,
            strike_price_lte=None,
            limit=None,
            page_token=None
        )
        return self.trade_client.get_option_contracts(request_params)
    
    def collect_data_for_watchlist(self, watchlist):
        collected_data = {}
        # this is a fugly, slow implementation, but it'll work for now while we iron out the kinks
        # gemini wrote this, but it should iterate through the watchlist, then call each of the data request methods, using the symbol from the watchlist as the input (untested)
        for symbol in watchlist:
            collected_data[symbol] = {
                'stock_data': self.get_stock_data(symbol),
                'option_chain_data': self.get_option_chain_data(symbol),  # Replace with your actual implementation
                'option_contracts': self.get_option_contracts([symbol]), # Pass a single symbol
            }

        return collected_data