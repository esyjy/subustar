import ccxt
import pandas as pd

def fetch_ohlcv(symbol, timeframe='1h', limit=1000):
    """
    Fetches historical OHLCV data from KuCoin Futures.
    Binance is unavailable in this environment, so we use KuCoin as an alternative.

    :param symbol: The trading pair symbol (e.g., 'BTC/USDT'). For KuCoin, this will be converted (e.g., to 'XBTUSDTM').
    :param timeframe: The timeframe for the data (e.g., '1h', '4h', '1d').
    :param limit: The number of data points to fetch.
    :return: A pandas DataFrame with OHLCV data.
    """
    exchange = ccxt.kucoinfutures()

    # KuCoin uses different symbols for perpetual futures (e.g., XBTUSDTM for BTC/USDT)
    # This is a simple conversion, might need to be more robust for other pairs.
    kucoin_symbol = symbol.replace('/USDT', 'USDTM')
    if 'BTC' in kucoin_symbol:
        kucoin_symbol = kucoin_symbol.replace('BTC', 'XBT')


    try:
        print(f"Fetching data for {kucoin_symbol} from KuCoin Futures...")
        ohlcv = exchange.fetch_ohlcv(kucoin_symbol, timeframe, limit=limit)
        print(f"Successfully fetched data for {kucoin_symbol}.")
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except ccxt.NetworkError as e:
        print(f"Network error: {e}")
        return None
    except ccxt.ExchangeError as e:
        print(f"Exchange error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    # Note: Using 'BTC/USDT' which will be converted to 'XBTUSDTM' for KuCoin.
    btc_data = fetch_ohlcv('BTC/USDT', '1d', 100)
    if btc_data is not None:
        print(btc_data.head())
        print(f"\nFetched {len(btc_data)} data points.")