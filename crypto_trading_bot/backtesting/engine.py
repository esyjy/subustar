import pandas as pd
import numpy as np

class WalkForwardBacktester:
    """
    A walk-forward backtesting engine.
    """
    def __init__(self, data, strategy, portfolio_optimizer, start_date, end_date, train_period, test_period):
        self.data = data
        self.strategy = strategy
        self.portfolio_optimizer = portfolio_optimizer
        self.start_date = start_date
        self.end_date = end_date
        self.train_period = train_period
        self.test_period = test_period
        self.results = []

    def run_backtest(self):
        """
        Runs the walk-forward backtest.
        """
        current_date = self.start_date
        print(f"Starting backtest from {self.start_date.date()} to {self.end_date.date()}")
        while current_date + self.train_period + self.test_period <= self.end_date:
            train_start = current_date
            train_end = train_start + self.train_period
            test_start = train_end
            test_end = test_start + self.test_period

            print(f"\nProcessing fold:")
            print(f"  Train: {train_start.date()} to {train_end.date()}")
            print(f"  Test:  {test_start.date()} to {test_end.date()}")

            # Get training and testing data
            train_data = self.data.loc[train_start:train_end]
            test_data = self.data.loc[test_start:test_end]

            if train_data.empty or test_data.empty:
                print("  Skipping fold due to empty data.")
                break

            # 1. Optimize portfolio on training data prices
            weights = self.portfolio_optimizer(train_data)

            # 2. Simulate trading on test data
            # The strategy is applied inside _simulate_trading to avoid lookahead bias
            fold_results = self._simulate_trading(train_data, test_data, weights)
            self.results.append({
                'fold': (train_start, test_end),
                'performance': fold_results
            })

            current_date += self.test_period

        return self.results

    def _simulate_trading(self, train_data, test_data, weights):
        """
        Simulates trading for a single fold on a day-by-day basis.
        """
        all_asset_signals = pd.DataFrame(index=test_data.index)

        for asset in self.data.columns:
            # Combine train and test data to calculate indicators without lookahead bias
            full_data = pd.concat([train_data[asset], test_data[asset]])
            full_data = full_data[~full_data.index.duplicated(keep='first')]

            # Generate signals for the combined data
            asset_signals = self.strategy.generate_signals(full_data.to_frame())
            all_asset_signals[asset] = asset_signals['signal'].loc[test_data.index]

        # Combine signals with a majority vote
        # 1 if majority of signals are buy, 0 otherwise
        combined_signals = all_asset_signals.sum(axis=1).apply(lambda x: 1 if x > 0 else 0)

        # Get the daily returns for the assets in the test period
        asset_returns = test_data.pct_change()

        # Create a portfolio to track performance
        portfolio = pd.DataFrame(index=asset_returns.index)
        # Use yesterday's signal to trade today to avoid lookahead bias.
        portfolio['positions'] = combined_signals.shift(1)
        portfolio.fillna(0, inplace=True)

        # Calculate portfolio returns
        # When position is 1, we are long the HRP portfolio. When 0, we are in cash.
        portfolio['returns'] = asset_returns.dot(weights) * portfolio['positions']
        portfolio.fillna(0, inplace=True)

        # Calculate Net Asset Value (NAV) over the test period
        portfolio['nav'] = (1 + portfolio['returns']).cumprod()
        portfolio.fillna(1, inplace=True) # NAV starts at 1

        return portfolio

if __name__ == '__main__':
    # Example Usage
    from crypto_trading_bot.data.fetch_data import fetch_ohlcv
    from crypto_trading_bot.strategies.examples import MovingAverageCrossover
    from crypto_trading_bot.portfolio.hrp import get_hrp_weights
    from datetime import timedelta

    # Fetch data for multiple assets
    symbols = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT']
    all_data = {}
    for symbol in symbols:
        data = fetch_ohlcv(symbol, '1d', 500)
        if data is not None:
            all_data[symbol] = data['close']

    if not all_data:
        print("Could not fetch data for backtesting.")
    else:
        price_df = pd.DataFrame(all_data)

        # Define parameters
        start_date = price_df.index.min()
        end_date = price_df.index.max()
        train_period = timedelta(days=90)
        test_period = timedelta(days=30)
        print(f"Total days in dataset: {(end_date - start_date).days}")
        print(f"Required days for one fold: {train_period.days + test_period.days}")

        # Initialize components
        strategy = MovingAverageCrossover(short_window=20, long_window=50)

        # In a real scenario, you would apply the strategy to each asset
        # For simplicity, we'll apply it to the first asset to get signals
        # and then use HRP for allocation.

        def portfolio_optimizer(prices):
            return get_hrp_weights(prices)

        # Run backtest
        backtester = WalkForwardBacktester(price_df, strategy, portfolio_optimizer,
                                           start_date, end_date, train_period, test_period)

        results = backtester.run_backtest()

        # Print results
        for res in results:
            fold = res['fold']
            performance = res['performance']
            print(f"Fold: {fold[0].date()} to {fold[1].date()}")
            print(f"  Final NAV: {performance['nav'].iloc[-1]:.4f}")
            print("-" * 30)