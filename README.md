# Market Simulator

This project implements a Market Simulator to evaluate stock portfolios based on user-defined trade orders. The simulator computes portfolio values over time, calculates performance metrics, and compares results with benchmark indices like SPX.

### Features

- **Portfolio Value Calculation**:
  - Simulates a portfolio starting with an initial cash balance.
  - Processes BUY/SELL orders with customizable commission and market impact.
  - Tracks portfolio value, including cash and stock holdings.

- **Performance Metrics**:
  - **Sharpe Ratio**: Measures risk-adjusted return.
  - **Cumulative Return**: Total portfolio growth.
  - **Daily Returns**: Includes average and standard deviation.

- **SPX Benchmark Comparison**:
  - Aligns SPX data with portfolio date ranges for meaningful comparison.
  - Computes SPX performance metrics for side-by-side evaluation.

- **Visualization**:
  - Plots portfolio value and benchmark (SPX) trends for analysis.

### Dependencies

- **Python Libraries**:
  - `pandas`: Data manipulation and analysis.
  - `matplotlib`: Data visualization.

### How to Use

1. Place order files in the `orders` directory and benchmark data in `data`.
2. Change the test_code calls in market_simulaor.py to call your desired order and data files
3. Run the script:
   ```bash
   python market_simulator.py
