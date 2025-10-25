import pandas as pd
import numpy as np

def calculate_sharpe_ratio(returns, periods_per_year=252):
    """
    Calculates the Sharpe ratio of a returns stream.

    :param returns: A pandas Series of returns.
    :param periods_per_year: The number of trading periods in a year.
    :return: The annualized Sharpe ratio.
    """
    if returns.std() == 0:
        return 0.0
    return np.sqrt(periods_per_year) * (returns.mean() / returns.std())

def calculate_calmar_ratio(returns, periods_per_year=252):
    """
    Calculates the Calmar ratio of a returns stream.

    :param returns: A pandas Series of returns.
    :return: The Calmar ratio.
    """
    cumulative_returns = (1 + returns).cumprod()
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns / peak) - 1
    max_drawdown = drawdown.min()

    if max_drawdown == 0:
        return np.inf

    annualized_return = (1 + returns.mean()) ** periods_per_year - 1
    return annualized_return / abs(max_drawdown)

def walk_forward_backtest(data, strategy_func, portfolio_func, train_size, test_size, step_size):
    """
    Performs a walk-forward cross-validation backtest.

    :param data: A dictionary of pandas DataFrames, where keys are asset symbols and values are OHLCV data.
    :param strategy_func: A function that takes data and returns trading signals.
    :param portfolio_func: A function that takes returns and returns portfolio weights.
    :param train_size: The size of the training set for each fold.
    :param test_size: The size of the test set for each fold.
    :param step_size: The number of periods to step forward for the next fold.
    :return: A dictionary with backtesting results.
    """
    all_symbols = list(data.keys())
    # Use an inner join to ensure we only use timestamps where all assets have data
    price_data = pd.concat([df['close'] for df in data.values()], axis=1, keys=all_symbols, join='inner')

    # Drop any remaining NaN rows that might have slipped through
    price_data.dropna(inplace=True)

    num_periods = len(price_data)

    fold_results = []
    all_portfolio_returns = []

    start = 0
    while start + train_size + test_size <= num_periods:
        train_end = start + train_size
        test_end = train_end + test_size

        train_set = price_data.iloc[start:train_end]
        test_set = price_data.iloc[train_end:test_end]

        # 1. Determine portfolio weights based on historical returns of the training set
        train_returns_for_hrp = train_set.pct_change().dropna()
        weights = portfolio_func(train_returns_for_hrp)

        # 2. Generate signals for the test set by passing the full OHLCV data
        test_signals = pd.DataFrame()
        for sym in all_symbols:
            # Reconstruct the original OHLCV dataframe for the test period
            asset_test_data = data[sym].loc[test_set.index]
            test_signals[sym] = strategy_func(asset_test_data)

        # 3. Calculate portfolio returns on the test set
        # Shift signals to prevent lookahead bias within the same candle
        test_returns = test_set.pct_change()
        portfolio_returns = (test_returns * test_signals.shift(1) * weights).sum(axis=1).dropna()
        all_portfolio_returns.append(portfolio_returns)

        # 5. Calculate performance for the fold
        sharpe = calculate_sharpe_ratio(portfolio_returns)
        calmar = calculate_calmar_ratio(portfolio_returns)
        cumulative_return = (1 + portfolio_returns).prod() - 1

        fold_results.append({
            'fold': len(fold_results) + 1,
            'train_start': train_set.index[0],
            'train_end': train_set.index[-1],
            'test_start': test_set.index[0],
            'test_end': test_set.index[-1],
            'sharpe_ratio': sharpe,
            'calmar_ratio': calmar,
            'cumulative_return': cumulative_return,
        })

        start += step_size

    # Combine all portfolio returns
    total_returns = pd.concat(all_portfolio_returns)

    # Calculate overall performance
    overall_sharpe = calculate_sharpe_ratio(total_returns)
    overall_calmar = calculate_calmar_ratio(total_returns)

    return {
        'overall_sharpe': overall_sharpe,
        'overall_calmar': overall_calmar,
        'fold_results': fold_results,
        'portfolio_returns': total_returns
    }

if __name__ == '__main__':
    # This is a simplified example. In a real scenario, you would import your actual modules.

    # Mock strategy function
    def mock_strategy(data):
        return pd.Series(np.random.choice([-1, 0, 1], size=len(data)), index=data.index)

    # Mock portfolio function
    def mock_portfolio(returns):
        num_assets = returns.shape[1]
        weights = np.ones(num_assets) / num_assets
        return pd.Series(weights, index=returns.columns)

    # Generate sample data for multiple assets
    num_assets = 5
    num_periods = 1000
    symbols = [f'ASSET_{i}' for i in range(num_assets)]
    data = {sym: pd.DataFrame({'close': 100 + np.random.randn(num_periods).cumsum()},
                              index=pd.date_range('2021-01-01', periods=num_periods)) for sym in symbols}

    # Run walk-forward backtest
    results = walk_forward_backtest(
        data=data,
        strategy_func=mock_strategy,
        portfolio_func=mock_portfolio,
        train_size=200,
        test_size=50,
        step_size=50
    )

    print(f"Overall Sharpe Ratio: {results['overall_sharpe']:.4f}")
    print(f"Overall Calmar Ratio: {results['overall_calmar']:.4f}")
    print("\nFold-by-Fold Performance:")
    for fold in results['fold_results']:
        print(f"  Fold {fold['fold']}: Sharpe={fold['sharpe_ratio']:.2f}, Calmar={fold['calmar_ratio']:.2f}, Return={fold['cumulative_return']:.2%}")