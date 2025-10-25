import ccxt
import pandas as pd
from datetime import datetime
import time

def convert_symbol_to_kucoin(symbol):
    """Converts a standard symbol like 'BTC/USDT' to KuCoin's perpetuals format."""
    if symbol.upper() == 'BTC/USDT':
        return 'XBTUSDTM'
    return symbol.upper().replace('/', '') + 'M'

def convert_symbol_to_gateio(symbol):
    """Converts a standard symbol like 'BTC/USDT' to Gate.io's perpetuals format."""
    return symbol.upper().replace('/', '_')

def fetch_paginated_ohlcv(exchange, symbol, timeframe, limit):
    """Fetches OHLCV data with pagination to get a large number of candles."""
    all_ohlcv = []
    since = None

    while len(all_ohlcv) < limit:
        # Some exchanges have a max limit per request (e.g., 1000)
        fetch_limit = min(limit - len(all_ohlcv), 1000)

        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, fetch_limit)
            if not ohlcv:
                break  # No more data available

            all_ohlcv.extend(ohlcv)
            since = ohlcv[-1][0] + 1  # Start next fetch from the next millisecond

            # Respect rate limits
            time.sleep(exchange.rateLimit / 1000)

        except Exception as e:
            print(f"  An error occurred during pagination for {symbol}: {e}")
            break

    return all_ohlcv

def fetch_ohlcv(symbol, timeframe='1h', since=None, limit=100):
    """
    Fetches historical OHLCV data from Binance, with fallbacks to KuCoin and Gate.io.
    """
    exchanges = {
        'binance': {'exchange': ccxt.binanceusdm, 'symbol_converter': lambda s: s},
        'kucoin': {'exchange': ccxt.kucoinfutures, 'symbol_converter': convert_symbol_to_kucoin},
        'gateio': {'exchange': ccxt.gateio, 'symbol_converter': convert_symbol_to_gateio}
    }

    for name, config in exchanges.items():
        try:
            print(f"Attempting to fetch {symbol} from {name}...")
            exchange = config['exchange']({
                'rateLimit': 1200,
                'enableRateLimit': True,
                'options': {'defaultType': 'future'} if name != 'gateio' else {'defaultType': 'swap'}
            })

            converted_symbol = config['symbol_converter'](symbol)

            # Use pagination to fetch the required limit
            ohlcv = fetch_paginated_ohlcv(exchange, converted_symbol, timeframe, limit)

            if ohlcv:
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                # Some exchanges return more data than requested, so trim it
                df = df.iloc[-limit:]
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                df.set_index('timestamp', inplace=True)
                print(f"Successfully fetched {len(df)} data points for {symbol} from {name}.")
                return df
            else:
                raise ccxt.ExchangeError("No data returned")

        except (ccxt.NetworkError, ccxt.ExchangeError) as e:
            print(f"  {name.capitalize()} fetch failed for {symbol}: {e}")
            continue # Try the next exchange
        except Exception as e:
            print(f"  An unexpected error occurred with {name} for {symbol}: {e}")
            continue

    print(f"All exchanges failed for {symbol}.")
    return None

if __name__ == '__main__':
    # Example usage
    print("--- Testing BTC/USDT ---")
    btc_data = fetch_ohlcv('BTC/USDT', timeframe='1d', limit=500)
    if btc_data is not None:
        print(f"Fetched {len(btc_data)} records.")
        print(btc_data.head())
        print(btc_data.tail())
    else:
        print("Failed to fetch BTC data from all exchanges.")