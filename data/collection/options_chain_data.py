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

class OptionDataCollector:
    def __init__(self, api_key, secret_key):
        self.trade_client = TradingClient(api_key, secret_key)
        self.historical_client = OptionHistoricalDataClient(api_key, secret_key)

    def get_optionable_assets(self):
        """Retrieves a list of assets that have options available."""
        req = GetAssetsRequest(attributes="options_enabled")
        return self.trade_client.get_all_assets(req)

    def get_option_contracts(self, underlying_symbols, **kwargs):
        """Fetches option contracts for the specified underlying symbols.

        Args:
            underlying_symbols: A list of underlying asset symbols (e.g., ["AAPL", "SPY"]).
            **kwargs: Additional parameters for filtering contracts (status, expiration date range, etc.).
        """
        req = GetOptionContractsRequest(underlying_symbols=underlying_symbols, **kwargs)
        return self.trade_client.get_option_contracts(req)

    def get_option_contracts_by_type(self, underlying_symbols, option_type="put", days_forward=(1, 60), limit=100):
        """Fetches option contracts of a specific type (put or call).

        Args:
            underlying_symbols: A list of underlying asset symbols.
            option_type: The type of options to retrieve ("put" or "call").
            days_forward: A tuple specifying the range of days in the future for expiration dates.
            limit: The maximum number of contracts to return.
        """
        now = datetime.now(tz=ZoneInfo("America/New_York"))
        req = GetOptionContractsRequest(
            underlying_symbols=underlying_symbols,
            status=AssetStatus.ACTIVE,
            expiration_date_gte=now.date() + timedelta(days=days_forward[0]),
            expiration_date_lte=(now + timedelta(days=days_forward[1])).strftime("%Y-%m-%d"),
            type=option_type,
            style=ExerciseStyle.AMERICAN,  # Assuming American-style options
            limit=limit,
        )
        return self.trade_client.get_option_contracts(req).option_contracts

    def get_historical_option_data(self, symbol, days_back=5, timeframe=TimeFrame(1, TimeFrameUnit.Hour)):
        """Retrieves historical option bar data.

        Args:
            symbol: The option contract symbol.
            days_back: The number of days to look back for historical data.
            timeframe: The timeframe of the bars (e.g., 1 hour).
        """
        now = datetime.now(tz=ZoneInfo("America/New_York"))
        bars_req = OptionBarsRequest(symbol, timeframe, start=now - timedelta(days=days_back))
        return self.historical_client.get_option_bars(bars_req).df
    
    def get_option_snapshot(self, symbols):
        """Retrieves the latest snapshot data for the specified options symbols.
        
        Args:
            symbols: A list of option contract symbols to fetch snapshots for.
        """
        req = OptionSnapshotRequest(symbol_or_symbols=symbols)
        return self.historical_client.get_option_snapshot(req)

    def get_option_chain(self, underlying_symbol):
        """Retrieves the option chain data for the specified underlying symbol.

        Args:
            underlying_symbol: The underlying asset symbol (e.g., "AAPL").
        """
        req = OptionChainRequest(underlying_symbol=underlying_symbol)
        return self.historical_client.get_option_chain(req)

    # ... (Add other methods for streaming data or analysis as needed)
