import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import alpaca
from alpaca.data.live.stock import StockDataStream
from alpaca.data.historical.stock import (
    StockHistoricalDataClient,
    StockBarsRequest,
    StockTradesRequest,
    StockQuotesRequest,
)
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

class StockDataCollector:
    def __init__(self, api_key, secret_key):
        self.historical_client = StockHistoricalDataClient(api_key, secret_key)

    def get_historical_bars(self, symbols, timeframe, days_back=5, limit=None):
        now = datetime.now(ZoneInfo("America/New_York"))
        req = StockBarsRequest(
            symbol_or_symbols=symbols,
            timeframe=timeframe,
            start=now - timedelta(days=days_back),
            limit=limit,
        )
        return self.historical_client.get_stock_bars(req).df

    def get_historical_trades(self, symbols, days_back=5, limit=None):
        now = datetime.now(ZoneInfo("America/New_York"))
        req = StockTradesRequest(
            symbol_or_symbols=symbols,
            start=now - timedelta(days=days_back),
            limit=limit,
        )
        return self.historical_client.get_stock_trades(req).df

    def get_historical_quotes(self, symbols, days_back=5, limit=None):
        now = datetime.now(ZoneInfo("America/New_York"))
        req = StockQuotesRequest(
            symbol_or_symbols=symbols,
            start=now - timedelta(days=days_back),
            limit=limit,
        )
        return self.historical_client.get_stock_quotes(req).df

    def get_latest_quote(self, symbols):
        req = StockQuotesRequest(symbol_or_symbols=symbols)
        return self.historical_client.get_stock_latest_quote(req)
    
    def stream_stock_data(self, symbols, quote_handler=None, trade_handler=None):
        stock_data_stream_client = StockDataStream(self.api_key, self.secret_key)

        if quote_handler:
            stock_data_stream_client.subscribe_quotes(quote_handler, *symbols)
        if trade_handler:
            stock_data_stream_client.subscribe_trades(trade_handler, *symbols)

        stock_data_stream_client.run()



# Example Usage:
api_key = "YOUR_API_KEY" 
secret_key = "YOUR_SECRET_KEY"  
collector = StockDataCollector(api_key, secret_key)

# Get hourly bars for AAPL for the past 5 days
aapl_bars = collector.get_historical_bars(["AAPL"], TimeFrame(1, TimeFrameUnit.Hour))

# Get latest quote for AAPL and GOOG
latest_quotes = collector.get_latest_quote(["AAPL", "GOOG"]) 