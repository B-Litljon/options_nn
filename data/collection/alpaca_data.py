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
    def __init__(self, api_key, secret_key):
        self.historical_client = StockHistoricalDataClient(api_key, secret_key)

    
