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

    def get_option_contracts(self, underlying_symbols, **kwargs):
        request_params = GetOptionContractsRequest(
            underlying_symbols=underlying_symbols,
            status=kwargs.get('status', AssetStatus.ACTIVE),
            expiration_date=kwargs.get('expiration_date'),
            expiration_date_gte=kwargs.get('expiration_date_gte'),
            expiration_date_lte=kwargs.get('expiration_date_lte'),
            root_symbol=kwargs.get('root_symbol'),
            type=kwargs.get('type'),
            style=kwargs.get('style'),
            strike_price_gte=kwargs.get('strike_price_gte'),
            strike_price_lte=kwargs.get('strike_price_lte'),
            limit=kwargs.get('limit'),
            page_token=kwargs.get('page_token')
        )
        return self.trade_client.get_option_contracts(request_params)