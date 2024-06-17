# imports
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import alpaca
from alpaca.data.live.option import OptionDataStream
from alpaca.data.historical.option import OptionHistoricalDataClient, OptionBarsRequest, OptionSnapshotRequest, OptionChainRequest
from alpaca.data.requests import GetAssetsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOptionContractsRequest
from alpaca.trading.enums import AssetStatus, ExerciseStyle
from alpaca.common.exceptions import APIError

class OptionsDataCollector:
    def __init__(self, api_key, secret_key, paper=True):
        self.trade_client = TradingClient(api_key, secret_key, paper=paper)
        self.historical_client = OptionHistoricalDataClient(api_key, secret_key)

    def get_optionable_assets(self):
        req = GetAssetsRequest(attributes="options_enabled")
        return self.trade_client.get_all_assets(req)

    def get_option_contracts(self, underlying_symbols, **kwargs):
        req = GetOptionContractsRequest(underlying_symbols=underlying_symbols, **kwargs)
        return self.trade_client.get_option_contracts(req)

    def get_put_options(self, underlying_symbols, days_forward=(1, 60), limit=100):
        now = datetime.now(tz=ZoneInfo("America/New_York"))
        req = GetOptionContractsRequest(
            underlying_symbols=underlying_symbols,
            status=AssetStatus.ACTIVE,
            expiration_date_gte=now.date() + timedelta(days=days_forward[0]),
            expiration_date_lte=(now + timedelta(days=days_forward[1])).strftime("%Y-%m-%d"),
            type="put",
            style=ExerciseStyle.AMERICAN,
            limit=limit,
        )
        return self.trade_client.get_option_contracts(req).option_contracts

    def get_historical_option_data(self, symbol, days_back=5, timeframe=TimeFrame(1, TimeFrameUnit.Hour)):
        now = datetime.now(tz=ZoneInfo("America/New_York"))
        bars_req = OptionBarsRequest(symbol, timeframe, start=now - timedelta(days=days_back))
        return self.historical_client.get_option_bars(bars_req).df

    def get_option_snapshot(self, symbols):
        req = OptionSnapshotRequest(symbol_or_symbols=symbols)
        return self.historical_client.get_option_snapshot(req)

    def get_option_chain(self, underlying_symbol):
        req = OptionChainRequest(underlying_symbol=underlying_symbol)
        return self.historical_client.get_option_chain(req)

    # ... (Add other methods for streaming data or analysis as needed)

# Example Usage:
api_key = "YOUR_API_KEY"  
secret_key = "YOUR_SECRET_KEY"  
bot = OptionsDataCollector(api_key, secret_key)

# Get optionable assets
optionable_assets = bot.get_optionable_assets()

# Get put options for SPY within the next 1-60 days
spy_puts = bot.get_put_options(["SPY"])

# Get historical data for the first SPY put contract
historical_data = bot.get_historical_option_data(spy_puts[0].symbol)