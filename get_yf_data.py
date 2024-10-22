import pandas as pd
import os
import yfinance as yf
from datetime import datetime

def symbol_to_path(year, symbol, base_dir=os.path.join(".", "data")):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, f"{symbol}.csv")

def get_data_yf_symbol(symbol, start_date, end_date):
    """Fetch stock data (adjusted close) for the given symbol from Yahoo Finance."""
    df = yf.download(
        symbol,
        interval="1d",
        start=start_date,
        end=end_date
    )
    return df

if __name__ == '__main__':

    # Ask the user to input the stock symbol and range
    symbol = input("Enter the stock symbol (e.g., TSLA): ").upper()
    start_year = input("Enter the start year: ").upper()
    end_year = input("Enter the end year: ").upper()

    date_start = f'{start_year}-01-01'
    date_end = f'{end_year}-12-31'

    print(f"Fetching data for {symbol} from {date_start} to {date_end}")
    df = get_data_yf_symbol(symbol, date_start, date_end)

    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)

    datafile = symbol_to_path(end_year, symbol)
    print(f"Writing data to {datafile}")
    df.to_csv(datafile, sep=',', index=True, encoding='utf-8')
