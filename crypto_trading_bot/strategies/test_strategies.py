import pandas as pd
from crypto_trading_bot.data.fetch_data import fetch_ohlcv
from crypto_trading_bot.strategies.examples import MovingAverageCrossover, MeanReversion

def run_strategy_test():
    """
    Tests the example strategies to ensure they run without errors.
    """
    # Fetch some sample data
    data = fetch_ohlcv('BTC/USDT', '1d', 200)
    if data is None:
        print("Failed to fetch data for strategy test.")
        return

    print("Testing Moving Average Crossover Strategy...")
    ma_crossover = MovingAverageCrossover(short_window=20, long_window=50)
    ma_signals = ma_crossover.generate_signals(data)

    if ma_signals is not None and not ma_signals.empty:
        print("Moving Average Crossover Strategy generated signals successfully.")
        print(ma_signals.tail())
    else:
        print("Moving Average Crossover Strategy failed to generate signals.")

    print("\nTesting Mean Reversion Strategy...")
    mean_reversion = MeanReversion(window=20, std_dev=2)
    mr_signals = mean_reversion.generate_signals(data)

    if mr_signals is not None and not mr_signals.empty:
        print("Mean Reversion Strategy generated signals successfully.")
        print(mr_signals.tail())
    else:
        print("Mean Reversion Strategy failed to generate signals.")

if __name__ == '__main__':
    run_strategy_test()