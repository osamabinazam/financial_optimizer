import pandas as pd
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

# Step 1: Define the column names and data
column_names = ['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']

data = """
A,06/23/2023,117.76,119.25,117.58,118.88,1912
A,06/22/2023,118.84,118.95,117.17,118.68,17359
A,06/21/2023,117.79,119.11,117.27,118.33,13875
A,06/20/2023,117.87,118.79,116.88,118.16,20239
"""  #

# Step 2: Convert the data to a list of lists and create a DataFrame
data_lines = [line.split(',') for line in data.strip().split('\n')]
df = pd.DataFrame(data_lines, columns=column_names)

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Convert numeric columns to appropriate data types
df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)

print("connecting...")
# Step 3: Set up InfluxDB client and connection
bucket = "stock"
org = "Digitonic"
token = "sJ-OKSsIh99b6Yw-Yp5ocmVp0eNshMR94M-Gpbbg2HNquITyF-YHqsCXyUYTQBxMfS8HJtR6OdHdlBNzWMHz-Q=="
url = "http://localhost:8086"  # Replace with your InfluxDB URL

client = InfluxDBClient(url=url, token=token, org=org, timeout=60_000)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Step 4: Write data to InfluxDB
for _, row in df.iterrows():
    point = (
        Point("stock_data")
        .tag("Symbol", row["Symbol"])
        .field("Open", row["Open"])
        .field("High", row["High"])
        .field("Low", row["Low"])
        .field("Close", row["Close"])
        .field("Volume", row["Volume"])
        .time(row["Date"])
    )
    # write_api.write(bucket=bucket, org=org, record=point)

# print("Data written to InfluxDB successfully!")
try:
    client = InfluxDBClient(url=url, token=token, org=org)
    query_api = client.query_api()
    # delete_api = client.delete_api()

    query = f'from(bucket: "{bucket}") |> range(start: 2022-01-01T00:00:00Z)'
    tables = query_api.query(query)

    if not tables:
        print("No data returned.")
    else:
        for table in tables:
            for record in table.records:
                print(record.values)

    # delete_api.delete(start="1970-01-01T00:00:00Z", stop="2030-01-01T00:00:00Z", bucket=bucket, org=org,
    #                   predicate='_measurement="stock_data"')
    print("All data deleted from InfluxDB successfully!")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client.close()
# Close the connection
client.close()
