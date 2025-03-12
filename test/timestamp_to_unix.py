import argparse
from datetime import datetime
import pytz

def convert_to_unix(timestamp: str) -> int:
    dt = datetime.fromisoformat(timestamp)
    return int(dt.timestamp())

def main():
    parser = argparse.ArgumentParser(description="Convert datetime to Unix timestamp.")
    parser.add_argument("timestamp", type=str, nargs='?', help="Datetime in ISO format (YYYY-MM-DD HH:MM:SS+TZ)")
    args = parser.parse_args()
    
    if args.timestamp:
        timestamp = args.timestamp
    else:
        timestamp = input("Enter datetime (YYYY-MM-DD HH:MM:SS+TZ): ")
    
    try:
        unix_timestamp = convert_to_unix(timestamp)
        print(unix_timestamp)
    except ValueError:
        print("Invalid datetime format. Please use 'YYYY-MM-DD HH:MM:SS+TZ'")

if __name__ == "__main__":
    main()
