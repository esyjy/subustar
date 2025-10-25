import pandas as pd
import numpy as np

# Import from other modules in the project
from data.fetch_data import fetch_ohlcv
from strategies.technical_analysis import (
    moving_average_crossover_strategy,
    rsi_strategy,
    bollinger_bands_strategy,
    macd_strategy,
    stochastic_oscillator_strategy
)
from portfolio.hrp import get_hrp_weights
from backtesting.walk_forward import walk_forward_backtest

def main():
    """
    Main function to run the crypto trading backtest.
    """
    # --- Configuration ---
    symbols = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'LTC/USDT', 'ADA/USDT']
    timeframe = '1d'
    # Fetch a larger amount of data to have enough for walk-forward
    data_limit = 2000

    # Walk-forward parameters
    train_size = 365  # 1 year of training data
    test_size = 90    # 3 months of testing data
    step_size = 90    # Step forward by 3 months

    # --- Data Fetching ---
    print("Fetching data...")
    all_data = {}
    for symbol in symbols:
        print(f"  Fetching {symbol}...")
        df = fetch_ohlcv(symbol, timeframe=timeframe, limit=data_limit)
        if df is not None and not df.empty:
            all_data[symbol] = df
        else:
            print(f"Could not fetch data for {symbol}. Skipping.")

    if len(all_data) < 2:
        print("\nNot enough data to run a portfolio backtest. Exiting.")
        return

    # --- Backtesting ---
    print("\nStarting walk-forward backtest...")

    # Choose the strategy to use
    # You can switch between strategies like:
    # moving_average_crossover_strategy, rsi_strategy, bollinger_bands_strategy,
    # macd_strategy, stochastic_oscillator_strategy
    strategy_to_use = moving_average_crossover_strategy

    results = walk_forward_backtest(
        data=all_data,
        strategy_func=strategy_to_use,
        portfolio_func=get_hrp_weights,
        train_size=train_size,
        test_size=test_size,
        step_size=step_size
    )

    # --- Results ---
    print("\n--- Backtest Results ---")
    if results:
        print(f"Overall Sharpe Ratio: {results['overall_sharpe']:.4f}")
        print(f"Overall Calmar Ratio: {results['overall_calmar']:.4f}")

        print("\nFold-by-Fold Performance:")
        if results['fold_results']:
            for fold in results['fold_results']:
                print(
                    f"  Fold {fold['fold']}: "
                    f"Sharpe={fold['sharpe_ratio']:.2f}, "
                    f"Calmar={fold['calmar_ratio']:.2f}, "
                    f"Return={fold['cumulative_return']:.2%}"
                )
        else:
            print("No folds were completed.")

        # You could also plot the portfolio returns here
        # results['portfolio_returns'].cumsum().plot(title='Portfolio Cumulative Returns')
        # import matplotlib.pyplot as plt
        # plt.show()
    else:
        print("Backtest did not produce any results.")


if __name__ == '__main__':
    main()