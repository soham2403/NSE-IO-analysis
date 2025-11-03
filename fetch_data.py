import requests
import time
import json
import csv
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import StringIO

# Configuration
EQUITY_CSV_URL = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"
OPTION_CHAIN_API = "https://www.nseindia.com/api/option-chain-equities?symbol={}"
MAX_SYMBOLS = 100  # Set to None for all stocks
MAX_WORKERS = 5
RATE_LIMIT = 0.5

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.nseindia.com/option-chain"
}

session = requests.Session()
session.headers.update(HEADERS)


def init_session():
    """Initialize NSE session."""
    try:
        print("Initializing session...")
        session.get("https://www.nseindia.com", timeout=10)
        time.sleep(1)
        print("✓ Session ready")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False


def get_stock_list():
    """Fetch NSE stock symbols."""
    try:
        print("\nFetching stock list...")
        resp = session.get(EQUITY_CSV_URL, timeout=15)
        resp.raise_for_status()
        
        reader = csv.DictReader(StringIO(resp.text))
        symbols = [row.get('SYMBOL') or row.get('Symbol') 
                   for row in reader if row.get('SYMBOL') or row.get('Symbol')]
        
        print(f"✓ Found {len(symbols)} stocks")
        return symbols
    except Exception as e:
        print(f"✗ Failed: {e}")
        return []


def fetch_option_chain(symbol):
    """Fetch option chain for one symbol."""
    try:
        url = OPTION_CHAIN_API.format(symbol)
        resp = session.get(url, timeout=20)
        
        if resp.status_code != 200:
            return {"symbol": symbol, "status": "failed", 
                    "error": f"HTTP {resp.status_code}"}
        
        data = resp.json()
        records = data.get("records", {}).get("data", [])
        
        oi_curr = oi_chg = 0
        for rec in records:
            for side in ("CE", "PE"):
                if side in rec:
                    oi_curr += rec[side].get("openInterest", 0)
                    oi_chg += rec[side].get("changeinOpenInterest", 0)
        
        return {
            "symbol": symbol,
            "oi_current": int(oi_curr),
            "oi_previous": int(oi_curr - oi_chg),
            "oi_change": int(oi_chg),
            "status": "success"
        }
    except Exception as e:
        return {"symbol": symbol, "status": "failed", "error": str(e)}


def fetch_all(symbols):
    """Fetch all option chains concurrently."""
    print(f"\nFetching {len(symbols)} option chains...")
    results = []
    success = fail = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_option_chain, s): s for s in symbols}
        
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            
            if result["status"] == "success":
                success += 1
            else:
                fail += 1
            
            if i % 10 == 0:
                print(f"  {i}/{len(symbols)} | OK: {success} | Failed: {fail}")
            
            time.sleep(RATE_LIMIT)
    
    print(f"\n✓ Done: {success} successful, {fail} failed")
    return results


def save_data(data):
    """Save data to JSON."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"nse_option_chain_data_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump({"fetched_at": datetime.now().isoformat(),
                   "total": len(data), "data": data}, f, indent=2)
    
    print(f"✓ Saved: {filename}")
    return filename


def main():
    print("=" * 60)
    print("NSE OPTION CHAIN DATA FETCHER")
    print("=" * 60)
    
    if not init_session():
        sys.exit(1)
    
    symbols = get_stock_list()
    if not symbols:
        sys.exit(1)
    
    if MAX_SYMBOLS:
        symbols = symbols[:MAX_SYMBOLS]
    
    data = fetch_all(symbols)
    filename = save_data(data)
    
    print(f"\n✓ Use: python analyze_oi.py {filename}")


if __name__ == "__main__":
    main()
