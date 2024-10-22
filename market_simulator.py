import sys
import pandas as pd
from datetime import datetime

sys.path.insert(0, './portfolio')
from portfolio.get_data import get_data, plot_data

def compute_portvals(orders_file, start_val=1000000, commission=9.95, impact=0.005):
    orders = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    symbols = orders['Symbol'].unique()
    dates = pd.date_range(orders.index.min(), orders.index.max())
    prices = get_data(symbols, dates, path="./data")

    # Initialize shit
    cash = start_val
    holdings = {symbol: 0 for symbol in symbols}
    portvals = pd.DataFrame(index=prices.index, columns=['Portfolio Value'])

    for date in portvals.index:
        # Check if fuckin order for the current date
        if date in orders.index:
            order_data = orders.loc[date]
            if isinstance(order_data, pd.Series):  # If one order `orders.loc[date]` will return a Series
                order_data = pd.DataFrame([order_data])
            # Process each fuckin order
            for _, row in order_data.iterrows():
                symbol = row['Symbol']
                order = row['Order']
                shares = row['Shares']
                price = prices.loc[date, symbol]

                if order == 'BUY':
                    # Buy shares, reduce cash
                    cash -= (price * shares) * (1 + impact) + commission
                    holdings[symbol] += shares
                elif order == 'SELL':
                    # Sell shares, increase cash
                    cash += (price * shares) * (1 - impact) - commission
                    holdings[symbol] -= shares

        # Calculate portfolio value for the day: cash + value of holdings
        stock_value = sum(holdings[sym] * prices.loc[date, sym] for sym in holdings)
        portvals.loc[date, 'Portfolio Value'] = cash + stock_value

    return portvals

def compute_daily_returns(portvals):
    # daily_returns = portvals.pct_change().iloc[1:]  # Drop the first day to avoid the 0 return
    # daily_returns = daily_returns.fillna(0)  # Fill NaN values with 0
    daily_returns = (portvals / portvals.shift(1)) - 1  # Calculate percentage change manually
    daily_returns = daily_returns.iloc[1:]  # Drop the first row (NaN from the shift)
    daily_returns = daily_returns.apply(pd.to_numeric, errors='coerce')  # Convert any non-numeric data to NaN
    daily_returns = daily_returns.fillna(0)  # Fill any NaN values (e.g., from division by zero)
    return daily_returns


def calculate_sharpe_ratio(daily_returns, samples_per_year=252, risk_free_rate=0.0):
    mean_daily_ret = daily_returns.mean()
    std_daily_ret = daily_returns.std()
    sharpe_ratio = (mean_daily_ret - risk_free_rate) / std_daily_ret
    # Annualize the SHit on 252 trading days XD
    return sharpe_ratio * (samples_per_year ** 0.5)

def calculate_cumulative_return(portvals):
    cumulative_return = (portvals.iloc[-1] / portvals.iloc[0]) - 1
    return cumulative_return

def calculate_std_daily_ret(daily_returns):
    return daily_returns.std()

def calculate_avg_daily_ret(daily_returns):
    return daily_returns.mean()


def test_code(orders_file, spx_file, start_value=1000000):
    print(f"\nRunning Market Simulator for {orders_file}...\n")

    # Compute portfolio values
    portvals = compute_portvals(orders_file=orders_file, start_val=start_value)

    # Load SPX data from CSV and ensure the correct column is used
    spx_prices = pd.read_csv(spx_file, index_col='Date', parse_dates=True)

    if 'Adj Close' not in spx_prices.columns:
        print("Error: 'Adj Close' column not found in SPX data. Please verify the CSV.")
        return

    spx_values = spx_prices['Adj Close']
    spx_values = spx_values.reindex(portvals.index).ffill()  # Reindex to match the dates in the portfolio

    # Calculate daily returns for the portfolio and SPX
    daily_returns_fund = compute_daily_returns(portvals['Portfolio Value'])
    daily_returns_spx = compute_daily_returns(spx_values)

    # Calculate performance metrics for the portfolio (fund)
    sharpe_ratio_fund = calculate_sharpe_ratio(daily_returns_fund)
    cum_ret_fund = calculate_cumulative_return(portvals['Portfolio Value'])
    std_daily_ret_fund = calculate_std_daily_ret(daily_returns_fund)
    avg_daily_ret_fund = calculate_avg_daily_ret(daily_returns_fund)

    # Calculate performance metrics for SPX
    sharpe_ratio_spx = calculate_sharpe_ratio(daily_returns_spx)
    cum_ret_spx = calculate_cumulative_return(spx_values)
    std_daily_ret_spx = calculate_std_daily_ret(daily_returns_spx)
    avg_daily_ret_spx = calculate_avg_daily_ret(daily_returns_spx)

    # Print Portfolio vs SPX statistics
    print()
    print("--- begin statistics ------------------------------------------------- ")
    print(f"Date Range: {portvals.index.min().date()} to {portvals.index.max().date()} (portfolio)")
    print(f"Number of Trading Days:             {len(portvals):14d}")
    print(f"Sharpe Ratio of Fund:               {sharpe_ratio_fund:+.11f}")
    print(f"Sharpe Ratio of SPX:                {sharpe_ratio_spx:+.11f}")
    print(f"Cumulative Return of Fund:          {cum_ret_fund:+.11f}")
    print(f"Cumulative Return of SPX:           {cum_ret_spx:+.11f}")
    print(f"Standard Deviation of Fund:         {std_daily_ret_fund:+.11f}")
    print(f"Standard Deviation of SPX:          {std_daily_ret_spx:+.11f}")
    print(f"Average Daily Return of Fund:       {avg_daily_ret_fund:+.11f}")
    print(f"Average Daily Return of SPX:        {avg_daily_ret_spx:+.11f}")
    final_portval = portvals.iloc[-1]
    print(f"\nFinal Portfolio Value:        {final_portval['Portfolio Value']:+,.11f}")

    # Plotting the portfolio and SPX values for visual comparison
    plot_data(
        portvals['Portfolio Value'],
        title=f"Portfolio Value for {orders_file}",
        xlabel="Date",
        ylabel="Portfolio Value"
    )

    plot_data(
        spx_values,
        title=f"SPX/GSPC Value for {spx_file}",
        xlabel="Date",
        ylabel="SPX/GSPC Value"
    )


if __name__ == "__main__":

    # Call for 2011 data using $SPX.csv
    test_code(orders_file='./orders/orders-short.csv', spx_file='./data/$SPX.csv')
    test_code(orders_file='orders/*orders_2021.csv', spx_file='./data/^GSPC_2021.csv')
    test_code(orders_file='orders/*orders_2024.csv', spx_file='./data/^GSPC_2024.csv')
