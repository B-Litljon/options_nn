import dotenv
import os
from src.alpaca_data import MarketDataCollector

dotenv.load_dotenv()
api_key = os.getenv('API_KEY')
secret_key = os.getenv('API_SECRET')

if __name__ == '__main__':
    # Create a MarketDataCollector instance
    market_collector = MarketDataCollector(api_key, secret_key, '1D', 30)

    # Populate the watchlist
    market_collector.populate_watchlist()

    # Print the watchlist
    watchlist = market_collector.stock_collector.get_watchlist()
    print("Watchlist:", watchlist)

    # Collect data for the entire watchlist
    watchlist_data = market_collector.collect_data_for_watchlist()

    # Print summary of collected data
    print(f"Data collected for {len(watchlist_data)} symbols in the watchlist")

    # Example of how to access and print data for each symbol in the watchlist
    for symbol in watchlist_data:
        stock_data = watchlist_data[symbol]['stock_data']
        option_data = watchlist_data[symbol]['option_chain_data']

        print(f"\nData for {symbol}:")
        
        if stock_data.bars:
            print(f"Latest closing price: {stock_data.bars[-1].close}")
        else:
            print("No stock data available")

        if option_data:
            print(f"Number of option contracts: {len(option_data)}")
        else:
            print("No option data available")