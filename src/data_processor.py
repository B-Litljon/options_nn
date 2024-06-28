
from src.alpaca_data import DataCollector 
import pandas as pd
import numpy as np



class DataProcessor:
    def __init__(self, api_key, secret_key, paper=True):
        self.dc = DataCollector(api_key, secret_key)
        self.stocks = {}
        # class attribute for for the symbols, timeframe, and days_back for modularity
     
    def get_top_assets (): 
        dc.get_most_active_stocks()
        dc.get_market_movers()
        # get the top assets from the screener data
        # we can use the screener api to filter for the most active stocks or market movers
        # then return a dictionary of whichever stocks we like
        # with the symbol as the key, and the ohlcv data as the values 
        # then we can request the options chain data for each stock in the dictionary

    def process_underlying_asset_data(self, symbol, days_back, timeframe):
        return 
        # days back is just a filler variable for now, I have to read the api docs some more to see how it works 
        # request the historical stock data using the method we created in the StockDataCollector class
        # organize the data into a pandas dataframe for processing
        # return the dataframe
        

    def process_option_chain_data(self, symbol, days_back, timeframe):
        return  #filler for now, same as above/below writing pseudocode for now
        # request the options chain data using the method we created in the OptionsDataCollector class
        # organize the data into a pandas dataframe for processing
        # return the dataframe
        # add expiration date filtering
        # strike price filtering, we can find the average price of all the contracts and filter out the ones that are too far from the average

    # now that the data is processed we can decide how to align the data. 

    def align_data(self, underlying_asset_data, option_chain_data):
        return 
        # align the dataframes based on the timestamp of the data
        # this will allow us to compare the data and see how the underlying asset data affects the option
        # we want to identify which options are the best to buy based on the underlying assets price movement 
        # -- as well as the correlation between the two eg: how the price movement of the underlying asset affects the option price
        # we can do so using the options greeks and implied volatility to determine the best options to buy
        # in the money calculations for both calls (and or puts) 
        # warning: we may need to do figure out some other method for aligning the data, this is just a start, the timestamps will most 
        # -- likely not be the same, so we may need to do some other method for aligning the data which is no issue, we can figure that out later
        # return the aligned dataframes




    # Add additional methods for processing, cleaning, or feature engineering here
    # For example: calculate implied volatility, Greeks, or other indicators from the raw data