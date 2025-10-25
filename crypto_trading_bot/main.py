import pandas as pd
from datetime import timedelta

from data.fetch_data import fetch_ohlcv
from strategies.examples import MovingAverageCrossover
from portfolio.hrp import get_hrp_weights
from backtesting.engine import WalkForwardBacktester
from utils.metrics import calculate_sharpe_ratio, calculate_calmar_ratio

def main():
    """
    Main function to run the crypto trading backtest.
    """
    # --- Configuration ---
    symbols = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT']
    timeframe = '1d'
    data_limit = 500
    train_period = timedelta(days=90)
    test_period = timedelta(days=30)
    strategy = MovingAverageCrossover(short_window=20, long_window=50)

    # --- Data Fetching ---
    print("Fetching data...")
    all_data = {}
    for symbol in symbols:
        data = fetch_ohlcv(symbol, timeframe, data_limit)
        if data is not None:
            all_data[symbol] = data['close']
        else:
            print(f"Could not fetch data for {symbol}.")
            return

    if not all_data:
        print("No data fetched. Exiting.")
        return

    price_df = pd.DataFrame(all_data)
    price_df.dropna(inplace=True)

    # --- Backtesting ---
    start_date = price_df.index.min()
    end_date = price_df.index.max()

    backtester = WalkForwardBacktester(
        data=price_df,
        strategy=strategy,
        portfolio_optimizer=get_hrp_weights,
        start_date=start_date,
        end_date=end_date,
        train_period=train_period,
        test_period=test_period
    )

    print("\nRunning backtest...")
    results = backtester.run_backtest()

    # --- Performance Analysis ---
    if not results:
        print("Backtest did not produce any results.")
        return

    print("\n--- Backtest Results ---")
    all_returns = []
    for res in results:
        fold = res['fold']
        performance = res['performance']
        returns = performance['returns']
        all_returns.append(returns)

        sharpe = calculate_sharpe_ratio(returns)
        calmar = calculate_calmar_ratio(returns)

        print(f"\nFold: {fold[0].date()} to {fold[1].date()}")
        print(f"  Final NAV: {performance['nav'].iloc[-1]:.4f}")
        print(f"  Sharpe Ratio: {sharpe:.4f}")
        print(f"  Calmar Ratio: {calmar:.4f}")

    # --- Overall Performance ---
    overall_returns = pd.concat(all_returns)
    overall_sharpe = calculate_sharpe_ratio(overall_returns)
    overall_calmar = calculate_calmar_ratio(overall_returns)
    overall_nav = (1 + overall_returns).cumprod()

    print("\n--- Overall Performance ---")
    print(f"  Final NAV: {overall_nav.iloc[-1]:.4f}")
    print(f"  Overall Sharpe Ratio: {overall_sharpe:.4f}")
    print(f"  Overall Calmar Ratio: {overall_calmar:.4f}")

if __name__ == '__main__':
    main()