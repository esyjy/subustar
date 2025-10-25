from abc import ABC, abstractmethod
import pandas as pd

class AlphaStrategy(ABC):
    """
    Abstract base class for an alpha strategy.
    """
    def __init__(self, params):
        self.params = params

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generates trading signals for the given data.

        :param data: A pandas DataFrame with OHLCV data.
        :return: A pandas DataFrame with a 'signal' column (-1 for sell, 1 for buy, 0 for hold).
        """
        pass