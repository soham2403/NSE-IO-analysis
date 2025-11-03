# NSE Option Chain OI Analysis Tool

A tool to analyze Open Interest (OI) buildup in NSE-listed stocks using real-time option chain data. It identifies stocks with significant OI increases to help understand market trends.

## Overview

Identifies and ranks NSE-listed stocks with the highest percentage increase in Open Interest compared to previous trading sessions. This analysis helps track market sentiment and potential price movements.

## Features

- Automated stock symbol fetching from NSE
- Real-time option chain data collection
- OI percentage change calculations
- Rate-limited data fetching
- JSON and CSV output formats
- Clean, tabulated reports

## Tech Stack

- Python 3.7+
- Libraries: `requests`, `pandas`
- Runs seamlessly on Google Colab (no local setup needed!)

## Setup

### Using Google Colab

1. Open NSE_OI_Analysis.ipynb in Colab
2. Run all cells
3. Download results

### Local Setup

```bash
git clone https://github.com/yourusername/nse-oi-analysis.git
cd nse-oi-analysis
pip install -r requirements.txt
```

## Sample Output

```
============================================================
TOP 5 STOCKS WITH HIGHEST OI PERCENTAGE INCREASE
============================================================
Rank   Symbol          % Change     Current OI      Previous OI     Change
------------------------------------------------------------
1      TATAMOTORS        45.23%      1,234,567       850,000        384,567
2      RELIANCE          32.15%      9,876,543     7,500,000      2,376,543
3      INFY              28.90%      2,345,678     1,820,000        525,678
4      TCS               24.67%      3,456,789     2,775,000        681,789
5      HDFCBANK          21.34%      4,567,890     3,765,000        802,890
============================================================
```

## Implementation

### Data Collection

- Set up session with headers and cookies
- Fetch NSE equity symbols
- Collect option chain data
- Calculate OI changes
- Store in JSON format

### Analysis

- Process JSON data
- Calculate OI percentage changes
- Rank stocks by OI increase
- Generate reports in CSV format

## Configuration

```python
MAX_SYMBOLS = 100    # Symbols to process
MAX_WORKERS = 5      # Concurrent threads
RATE_LIMIT = 0.5     # Request delay
TOP_N = 5            # Stocks to display
```


