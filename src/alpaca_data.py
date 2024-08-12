from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import json
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


class AlpacaData:
    """
    this class will handle all data retrieval from the Alpaca API, including historical stock data, option chain data

    AlpacaData methods:
    .request_most_actives,
    .request_candlesticks,
    .request_option_chain,
    .request_option_historical_data

    each method is related to eachother and will be used together.

    data flow:
    1. request_most_actives; this method is from the alpaca-py api wrapper, 
    and will return a list of the most active stocks by volume (or tradecount, but I plan on using the volume as a req parameter)
    we can include some more parameters to filter the list, but for now we will just use the default parameters. 

    2. request_candlesticks; this method will take the list of most active stocks and request the historical data for each stock, 
    returning the open high low close volume for each stock. we will also include the timeframe as a parameter, this way
    each instance of the class can be used for different timeframes.

    3. request_option_chain; this method will take the list of most active stocks and request the option chain data for each stock,
    

    when the data is neat and formatted the way we want, we can then use the data for training the model.

    """
    def __init__(self, api_key: str, secret_key: str, timeframe: str): # timeframe may need to be int
        self.stock_historical_data_client = StockHistoricalDataClient(api_key, secret_key)
        self.option_historical_data_client = OptionHistoricalDataClient(api_key, secret_key)
        self.screener_client = ScreenerClient(api_key, secret_key)
        self.watchlist = [] # this will be a list of the most active stocks and/or user inputted stocks

    # needs to get user input for tickers, timeframe, and start/end dates
    def request_most_actives(self):
        """
        this method will return a list of the most active stocks by volume and update the watchlist variable
        """
        most_actives_request = MostActivesRequest()
        most_actives = self.screener_client.get_most_actives(most_actives_request)
        return most_actives

    # get historical stock data
    def request_candlesticks(self, watchlist: list, timeframe: str):
        """
        this method will return the historical stock data for each stock in the watchlist
        """
        for stock in watchlist:
            stock_bars_request = StockBarsRequest(
                symbol=stock, # this variable name may be wrong
                timeframe=timeframe,
                limit=1000 # this may need to be a user input, and or may not be needed
            )
            stock_bars = self.stock_historical_data_client.get_stock_bars(stock_bars_request)
            return stock_bars

    # get option chain data
    def request_option_chain(self, watchlist: list):
        """
        this method will return the option chain data for each stock in the watchlist
        """
        for stock in watchlist:
            option_chain_request = OptionChainRequest(
                symbol=stock,
                limit=1000
            )
            option_chain = self.stock_historical_data_client.get_option_chain(option_chain_request)
            return option_chain