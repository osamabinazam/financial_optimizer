import pandas as pd
from datetime import datetime, timedelta
import os

def generate_data(start_index, num_records):
    """Generates dummy financial data."""
    timestamps = [datetime.now() - timedelta(minutes=i) for i in range(start_index, start_index + num_records)]
    data = {
        'timestamp': [timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3] + 'Z' for timestamp in timestamps],  # ISO8601 format
        'symbol': ['AAPL'] * num_records,
        'quantity': [100 + i % 10 for i in range(num_records)],
        'price': [150.0 + i * 0.01 for i in range(num_records)],
        'side': ['B' if i % 2 == 0 else 'S' for i in range(num_records)]  # 'B' for Buy, 'S' for Sell
    }
    return pd.DataFrame(data)

def save_data_to_file(df, file_path):
    """Saves the DataFrame to a CSV file."""
    df.to_csv(file_path, index=False)

def main():
    total_records = 10_000_000
    records_per_file = 400
    directory = './data/in'
    os.makedirs(directory, exist_ok=True)  # Create directory if it does not exist

    file_count = 0
    for start in range(0, total_records, records_per_file):
        num_records = min(records_per_file, total_records - start)
        df = generate_data(start, num_records)
        file_path = os.path.join(directory, f'stock_data_{file_count + 1}.csv')
        save_data_to_file(df, file_path)
        file_count += 1
        if file_count % 1000 == 0:
            print(f'Generated {file_count * records_per_file} records...')

    print(f'Total files created: {file_count}')

if __name__ == '__main__':
    main()
