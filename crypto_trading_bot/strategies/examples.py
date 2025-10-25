import pandas as pd
import numpy as np
from .base import AlphaStrategy

class MovingAverageCrossover(AlphaStrategy):
    """
    A moving average crossover strategy.
    """
    def __init__(self, short_window=40, long_window=100):
        super().__init__({'short_window': short_window, 'long_window': long_window})

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        # Create short and long simple moving averages
        signals['short_mavg'] = data.iloc[:, 0].rolling(window=self.params['short_window'], min_periods=1, center=False).mean()
        signals['long_mavg'] = data.iloc[:, 0].rolling(window=self.params['long_window'], min_periods=1, center=False).mean()

        # Generate signal when short MA crosses above long MA
        signals['signal'][self.params['short_window']:] = np.where(signals['short_mavg'][self.params['short_window']:]
                                                                    > signals['long_mavg'][self.params['short_window']:], 1.0, 0.0)

        # Generate trading orders
        signals['positions'] = signals['signal'].diff()
        return signals


class MeanReversion(AlphaStrategy):
    """
    A mean reversion strategy.
    """
    def __init__(self, window=20, std_dev=2):
        super().__init__({'window': window, 'std_dev': std_dev})

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        # Calculate moving average and standard deviation
        signals['mavg'] = data.iloc[:, 0].rolling(window=self.params['window']).mean()
        signals['std'] = data.iloc[:, 0].rolling(window=self.params['window']).std()

        # Calculate upper and lower Bollinger Bands
        signals['upper_band'] = signals['mavg'] + (signals['std'] * self.params['std_dev'])
        signals['lower_band'] = signals['mavg'] - (signals['std'] * self.params['std_dev'])

        # Generate signals
        signals['signal'] = np.where(data.iloc[:, 0] < signals['lower_band'], 1.0, 0.0)
        signals['signal'] = np.where(data.iloc[:, 0] > signals['upper_band'], -1.0, signals['signal'])

        signals['positions'] = signals['signal']
        return signals