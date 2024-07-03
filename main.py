from src.alpaca_data import DataCollector 
import dotenv
import os

dotenv.load_dotenv()
api_key = os.getenv('API_KEY')
secret_key = os.getenv('API_SECRET')

if __name__ == '__main__':
    collector = DataCollector(api_key, secret_key, '1D', 30)
    #collector.stocks_to_watch()
    print(collector.watchlist)
    print(collector.get_stock_data('AAPL'))
    print(collector.get_option_chain_data('AAPL'))
    print(collector.get_stock_data('AAPL').bars[0].close)