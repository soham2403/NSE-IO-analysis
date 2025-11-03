import json
import sys
import pandas as pd
from datetime import datetime


def load_data(filepath):
    """Load JSON data."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f).get("data", [])
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)


def analyze_oi(data):
    """Calculate OI percentage changes."""
    print("Analyzing...")
    results = []
    
    for rec in data:
        if rec.get("status") != "success":
            continue
        
        curr = rec.get("oi_current", 0)
        prev = rec.get("oi_previous", 0)
        chg = rec.get("oi_change", 0)
        
        if prev > 0 and chg > 0:
            pct = (chg / prev) * 100
            results.append({
                "symbol": rec["symbol"],
                "oi_current": curr,
                "oi_previous": prev,
                "oi_change": chg,
                "pct_change": pct
            })
    
    print(f"✓ Found {len(results)} stocks with OI increases")
    return results


def display_top(analysis, n=5):
    """Display top N stocks."""
    ranked = sorted(analysis, key=lambda x: x["pct_change"], reverse=True)[:n]
    
    print("\n" + "=" * 80)
    print(f"TOP {n} STOCKS WITH HIGHEST OI INCREASE")
    print("=" * 80)
    print(f"{'Rank':<6} {'Symbol':<15} {'% Change':<12} {'Current OI':<15} "
          f"{'Previous OI':<15} {'Change':<15}")
    print("-" * 80)
    
    for i, stock in enumerate(ranked, 1):
        print(f"{i:<6} {stock['symbol']:<15} {stock['pct_change']:>10.2f}% "
              f"{stock['oi_current']:>14,} {stock['oi_previous']:>14,} "
              f"{stock['oi_change']:>14,}")
    
    print("=" * 80)
    
    # Save CSV
    filename = f"nse_oi_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    pd.DataFrame(ranked).to_csv(filename, index=False)
    print(f"\n✓ Saved: {filename}")
    
    return ranked


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_oi.py <json_file>")
        sys.exit(1)
    
    print("=" * 60)
    print("NSE OI ANALYSIS")
    print("=" * 60)
    
    data = load_data(sys.argv[1])
    analysis = analyze_oi(data)
    
    if not analysis:
        print("No data to analyze")
        sys.exit(1)
    
    display_top(analysis)


if __name__ == "__main__":
    main()
