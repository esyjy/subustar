import pandas as pd
import numpy as np
from pyhrp.hrp import hrp
from pyhrp.cluster import Cluster

def get_hrp_weights(prices: pd.DataFrame):
    """
    Calculates portfolio weights using the Hierarchical Risk Parity (HRP) algorithm.

    :param prices: A pandas DataFrame of asset prices.
    :return: A pandas Series with the optimal portfolio weights.
    """
    if not isinstance(prices, pd.DataFrame) or prices.empty:
        raise ValueError("Prices must be a non-empty pandas DataFrame.")

    # The pyhrp library expects a prices dataframe
    root = hrp(prices)
    weights = root.portfolio.weights

    return weights

if __name__ == '__main__':
    # Example Usage
    # Create a sample prices DataFrame
    # Generate a sample price DataFrame
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', periods=100)
    prices_data = {
        'Asset1': 100 + np.random.randn(100).cumsum(),
        'Asset2': 150 + np.random.randn(100).cumsum(),
        'Asset3': 200 + np.random.randn(100).cumsum(),
    }
    prices_df = pd.DataFrame(prices_data, index=dates)


    try:
        hrp_weights = get_hrp_weights(prices_df)
        print("HRP Portfolio Weights:")
        print(hrp_weights)
    except ValueError as e:
        print(f"Error: {e}")