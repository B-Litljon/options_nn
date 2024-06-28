import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from alpaca.data import (
    StockHistoricalDataClient, OptionHistoricalDataClient, 
    StockBarsRequest, OptionChainRequest
)
from alpaca.data.live import StockDataStream, OptionDataStream
from alpaca.data.historical.screener import ScreenerClient


class DataCollector:
    """
    Collects and stores historical stock data and option chain data for a watchlist of stocks.

    Provides methods to populate a watchlist, retrieve historical stock data and option chain data, and collect data for a watchlist of stocks.
    """
    def __init__(self, api_key, secret_key, timeframe, days_back):
        self.historical_asset = StockHistoricalDataClient(api_key, secret_key)
        self.asset_screener = ScreenerClient(api_key, secret_key)
        # perhaps include the top movers as well, there is some output that includes the losers, which may be useful for training the model to learn  up and down trends
        self.historic_options = OptionHistoricalDataClient(api_key, secret_key)
        self.timeframe = timeframe
        self.days_back = days_back
        self.watchlist = {}  # Initialize the watchlist attribute

    def stocks_to_watch(self):
        """
        Populates the watchlist attribute with the most active stocks and their corresponding trade count and volume.

        Returns:
        None
        """
        active_stock_data = self.asset_screener.get_most_actives()["most_actives"]

        for stock_info in active_stock_data:
            symbol = stock_info['symbol']
            self.watchlist[symbol] = {
                'trade_count': stock_info['trade_count'],
                'volume': stock_info['volume']
            }

    def get_stock_data(self, symbol):
        """
        Retrieves historical stock data for a given symbol.

        Parameters:
        symbol (str): The stock symbol for which to retrieve data.

        Returns:
        StockBarsResponse: A StockBarsResponse object containing the historical stock data.
        """
        end = datetime.now(ZoneInfo("America/Pacific"))
        start = end - timedelta(days=self.days_back)
        data = StockBarsRequest(symbol, self.timeframe, start, end)
        return self.historical_asset.get_bars(data)
    
    def get_option_chain_data(self, symbol):
        """
        Retrieves option chain data for a given symbol.

        Parameters:
        symbol (str): The stock symbol for which to retrieve option chain data.

        Returns:
        OptionChainSnapshot: An OptionChainSnapshot object containing the option chain data.
        """
        request_params = OptionChainRequest(symbol=symbol)
        option_chain_snapshot = self.historic_options.get_option_chain(request_params)

        
        return option_chain_snapshot

    def collect_data_for_watchlist(self, watchlist):
        """
        Collects historical stock data and option chain data for each symbol in the watchlist.

        Parameters:
        watchlist (dict): A dictionary of stock symbols and their corresponding trade count and volume.

        Returns:
        dict: A dictionary where each key is a stock symbol and the value is another dictionary containing the historical stock data and option chain data.
        """
        collected_data = {}

        for symbol in watchlist:
            collected_data[symbol] = {
                'stock_data': self.get_stock_data(symbol),
                'option_chain_data': self.get_option_chain_data(symbol),
            }

        return collected_data