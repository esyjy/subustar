import numpy as np
import pandas as pd

def calculate_sharpe_ratio(returns, annualization_factor=252):
    """
    Calculates the Sharpe ratio of a returns series.

    :param returns: A pandas Series of portfolio returns.
    :param annualization_factor: The factor to annualize the Sharpe ratio (e.g., 252 for daily returns).
    :return: The annualized Sharpe ratio.
    """
    if returns.std() == 0:
        return 0.0
    return np.sqrt(annualization_factor) * (returns.mean() / returns.std())

def calculate_max_drawdown(nav_series):
    """
    Calculates the maximum drawdown of a Net Asset Value (NAV) series.

    :param nav_series: A pandas Series representing the portfolio's NAV over time.
    :return: The maximum drawdown value.
    """
    running_max = nav_series.expanding().max()
    drawdown = (nav_series - running_max) / running_max
    return drawdown.min()

def calculate_calmar_ratio(returns, annualization_factor=252):
    """
    Calculates the Calmar ratio of a returns series.

    :param returns: A pandas Series of portfolio returns.
    :param annualization_factor: The factor to annualize the returns.
    :return: The Calmar ratio.
    """
    nav = (1 + returns).cumprod()
    max_drawdown = calculate_max_drawdown(nav)
    if max_drawdown == 0:
        return np.nan

    annualized_return = nav.iloc[-1] ** (annualization_factor / len(nav)) - 1
    return annualized_return / abs(max_drawdown)

if __name__ == '__main__':
    # Example Usage
    np.random.seed(42)
    returns = pd.Series(np.random.randn(252) / 100)
    nav = (1 + returns).cumprod()

    sharpe = calculate_sharpe_ratio(returns)
    max_dd = calculate_max_drawdown(nav)
    calmar = calculate_calmar_ratio(returns)

    print(f"Sample Metrics:")
    print(f"  Sharpe Ratio: {sharpe:.4f}")
    print(f"  Maximum Drawdown: {max_dd:.4%}")
    print(f"  Calmar Ratio: {calmar:.4f}")