import pandas as pd
import numpy as np

def moving_average_crossover_strategy(data, short_window=40, long_window=100):
    """
    Generates trading signals based on a moving average crossover strategy.

    :param data: A pandas DataFrame with a 'close' price column.
    :param short_window: The window for the short-term moving average.
    :param long_window: The window for the long-term moving average.
    :return: A pandas Series with trading signals (1 for buy, -1 for sell, 0 for hold).
    """
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0

    signals['short_mavg'] = data['close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = data['close'].rolling(window=long_window, min_periods=1, center=False).mean()

    # Use .iloc for positional slicing to avoid TypeError and FutureWarnings.
    # This ensures we only generate signals after the initial window period.
    if len(signals) > short_window:
        signal_col_idx = signals.columns.get_loc('signal')

        # Generate buy signals (1.0 where short > long, else 0.0)
        buy_signals = np.where(
            signals['short_mavg'].iloc[short_window:] > signals['long_mavg'].iloc[short_window:],
            1.0,
            0.0
        )

        # Generate final signals (-1.0 for sell, otherwise use buy_signals)
        final_signals = np.where(
            signals['short_mavg'].iloc[short_window:] < signals['long_mavg'].iloc[short_window:],
            -1.0,
            buy_signals
        )

        signals.iloc[short_window:, signal_col_idx] = final_signals

    return signals['signal']

def rsi_strategy(data, rsi_period=14, rsi_overbought=70, rsi_oversold=30):
    """
    Generates trading signals based on the Relative Strength Index (RSI).

    :param data: A pandas DataFrame with a 'close' price column.
    :param rsi_period: The period for calculating RSI.
    :param rsi_overbought: The RSI level considered overbought.
    :param rsi_oversold: The RSI level considered oversold.
    :return: A pandas Series with trading signals (1 for buy, -1 for sell, 0 for hold).
    """
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0

    close_delta = data['close'].diff()
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    ma_up = up.ewm(com=rsi_period - 1, adjust=True, min_periods=rsi_period).mean()
    ma_down = down.ewm(com=rsi_period - 1, adjust=True, min_periods=rsi_period).mean()

    rsi = 100 - (100 / (1 + ma_up / ma_down))

    signals['rsi'] = rsi
    # Use .loc to avoid chained assignment warnings
    signals.loc[signals['rsi'] < rsi_oversold, 'signal'] = 1.0
    signals.loc[signals['rsi'] > rsi_overbought, 'signal'] = -1.0

    return signals['signal']

def bollinger_bands_strategy(data, window=20, num_std_dev=2):
    """
    Generates trading signals based on Bollinger Bands.

    :param data: A pandas DataFrame with a 'close' price column.
    :param window: The moving average window.
    :param num_std_dev: The number of standard deviations for the bands.
    :return: A pandas Series with trading signals (1 for buy, -1 for sell, 0 for hold).
    """
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0

    rolling_mean = data['close'].rolling(window=window).mean()
    rolling_std = data['close'].rolling(window=window).std()

    upper_band = rolling_mean + (rolling_std * num_std_dev)
    lower_band = rolling_mean - (rolling_std * num_std_dev)

    signals.loc[data['close'] < lower_band, 'signal'] = 1.0  # Buy signal
    signals.loc[data['close'] > upper_band, 'signal'] = -1.0 # Sell signal

    return signals['signal']

def macd_strategy(data, fast_period=12, slow_period=26, signal_period=9):
    """
    Generates trading signals based on the MACD indicator.
    """
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0

    fast_ema = data['close'].ewm(span=fast_period, adjust=False).mean()
    slow_ema = data['close'].ewm(span=slow_period, adjust=False).mean()

    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()

    signals.loc[macd_line > signal_line, 'signal'] = 1.0
    signals.loc[macd_line < signal_line, 'signal'] = -1.0

    return signals['signal']

def stochastic_oscillator_strategy(data, k_period=14, d_period=3, overbought=80, oversold=20):
    """
    Generates trading signals based on the Stochastic Oscillator.
    """
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0

    low_min = data['low'].rolling(window=k_period).min()
    high_max = data['high'].rolling(window=k_period).max()

    k_line = 100 * ((data['close'] - low_min) / (high_max - low_min))
    d_line = k_line.rolling(window=d_period).mean()

    signals.loc[k_line < oversold, 'signal'] = 1.0
    signals.loc[k_line > overbought, 'signal'] = -1.0

    return signals['signal']


if __name__ == '__main__':
    # Create a sample dataframe with high and low for stochastic
    sample_data = {
        'open': np.random.rand(200) * 100 + 1000,
        'high': np.random.rand(200) * 10 + 1050,
        'low': np.random.rand(200) * 10 + 950,
        'close': np.random.rand(200) * 100 + 1000,
        'volume': np.random.rand(200) * 1000
    }
    data = pd.DataFrame(sample_data, index=pd.date_range('2021-01-01', periods=200))

    # Test moving average crossover
    ma_signals = moving_average_crossover_strategy(data)
    print("Moving Average Crossover Signals:")
    print(ma_signals.value_counts())

    # Test RSI strategy
    rsi_signals = rsi_strategy(data)
    print("\nRSI Signals:")
    print(rsi_signals.value_counts())

    # Test Bollinger Bands strategy
    bb_signals = bollinger_bands_strategy(data)
    print("\nBollinger Bands Signals:")
    print(bb_signals.value_counts())

    # Test MACD strategy
    macd_signals = macd_strategy(data)
    print("\nMACD Signals:")
    print(macd_signals.value_counts())

    # Test Stochastic Oscillator strategy
    stoch_signals = stochastic_oscillator_strategy(data)
    print("\nStochastic Oscillator Signals:")
    print(stoch_signals.value_counts())