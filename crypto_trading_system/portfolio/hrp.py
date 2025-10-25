import pandas as pd
import numpy as np
from pyhrp.hrp import build_tree
from pyhrp.algos import risk_parity

def get_hrp_weights(returns):
    """
    Calculates portfolio weights using the Hierarchical Risk Parity (HRP) algorithm.

    :param returns: A pandas DataFrame of asset returns, where each column represents an asset.
    :return: A pandas Series with the HRP weights for each asset.
    """
    if not isinstance(returns, pd.DataFrame) or returns.empty:
        raise ValueError("Returns must be a non-empty pandas DataFrame.")

    # Drop columns with all NaN values and rows with any NaN values
    returns = returns.dropna(axis=1, how='all').dropna(axis=0)

    if returns.shape[1] < 2:
        # HRP requires at least two assets
        if returns.shape[1] == 1:
            return pd.Series(1.0, index=returns.columns)
        else:
            return pd.Series(dtype=float)

    # HRP calculation
    cov, cor = returns.cov(), returns.corr()

    # Build the hierarchical tree
    dendrogram = build_tree(cor, method='ward')

    # Compute the weights
    root = risk_parity(root=dendrogram.root, cov=cov)
    # The weights are stored in the 'portfolio' attribute of the root node
    weights = root.portfolio.weights

    return weights

if __name__ == '__main__':
    # Create sample returns data for several assets
    np.random.seed(42)
    num_assets = 10
    num_days = 252
    asset_names = [f'ASSET_{i}' for i in range(num_assets)]
    returns_data = np.random.randn(num_days, num_assets) * 0.01
    returns_df = pd.DataFrame(returns_data, columns=asset_names, index=pd.date_range('2021-01-01', periods=num_days))

    # Introduce some missing data to test robustness
    returns_df.iloc[10:20, 0] = np.nan

    print("Sample Returns Data Head:")
    print(returns_df.head())

    try:
        # Calculate HRP weights
        hrp_weights = get_hrp_weights(returns_df)

        print("\nHRP Weights:")
        print(hrp_weights)

        print(f"\nSum of weights: {hrp_weights.sum():.2f}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")