# from datetime import datetime, timedelta
#
# from config.influxdb_config import InfluxDBConfig
# from influxdb_client import Point, WriteOptions
# import pandas as pd
# from influxdb_client.rest import ApiException
#
#
# class InfluxDBService:
#     """
#     Service class to manage interactions with InfluxDB, including writing, reading, and deleting data in chunks.
#     """
#
#     def __init__(self):
#         # Initialize the InfluxDBConfig and get the client
#         self.config = InfluxDBConfig()
#         self.client = self.config.get_client()
#         self.bucket = self.config.bucket
#         self.org = self.config.org
#
#     def write_data_chunk(self, data_chunk):
#         """
#         Writes a chunk of data (pandas DataFrame) to InfluxDB.
#         :param data_chunk: A pandas DataFrame containing the data chunk to be written.
#         """
#         try:
#             write_api = self.client.write_api(write_options=WriteOptions(batch_size=5000, flush_interval=1000))
#             points = self._convert_dataframe_to_points(data_chunk)
#             write_api.write(bucket=self.bucket, org=self.org, record=points)
#             write_api.flush()
#             print(f"Data chunk written successfully to InfluxDB (Bucket: {self.bucket}).")
#         except ApiException as e:
#             print(f"Error writing data chunk to InfluxDB: {e}")
#
#     def read_data_chunk(self, symbol=None, start_date=None, end_date=None, limit=1000):
#         """
#         Reads a chunk of data from InfluxDB based on optional filters such as symbol, date range, and limit.
#         :param symbol: Stock symbol to filter by (optional).
#         :param start_date: Start date to filter by (optional).
#         :param end_date: End date to filter by (optional).
#         :param limit: The maximum number of records to return (default: 1000).
#         :return: A pandas DataFrame with the data chunk.
#         """
#         query = f'from(bucket: "{self.bucket}") |> range(start: -1y)'
#
#         # Apply filters if provided
#         if start_date and end_date:
#             query = f'from(bucket: "{self.bucket}") |> range(start: {start_date}, stop: {end_date})'
#
#         if symbol:
#             query += f' |> filter(fn: (r) => r["Symbol"] == "{symbol}")'
#
#         query += f' |> limit(n: {limit})'
#
#         try:
#             query_api = self.client.query_api()
#             tables = query_api.query(query)
#
#             # Convert results to pandas DataFrame
#             results = []
#             for table in tables:
#                 for record in table.records:
#                     results.append({
#                         "Symbol": record['Symbol'],
#                         "Date": record['_time'],
#                         "Open": record['_value'] if record['_field'] == 'Open' else None,
#                         "High": record['_value'] if record['_field'] == 'High' else None,
#                         "Low": record['_value'] if record['_field'] == 'Low' else None,
#                         "Close": record['_value'] if record['_field'] == 'Close' else None,
#                         "Volume": record['_value'] if record['_field'] == 'Volume' else None
#                     })
#
#             df = pd.DataFrame(results)
#             print(f"Data chunk read successfully from InfluxDB (Bucket: {self.bucket}).")
#             return df
#
#         except ApiException as e:
#             print(f"Error reading data chunk from InfluxDB: {e}")
#             return None
#
#     def estimate_deletion_count(self, symbol=None, start_date=None, end_date=None):
#         """
#         Estimate the total number of points that match the given symbol and date range.
#         :param symbol: The stock symbol to filter (optional).
#         :param start_date: The start date for the query (optional).
#         :param end_date: The end date for the query (optional).
#         :return: The estimated number of points to delete.
#         """
#         try:
#             query_api = self.client.query_api()
#
#             start_date = "1970-01-01T00:00:00Z"  # Start from epoch time to delete all data
#             end_date = datetime.now().isoformat() + "Z"  # Set the end date to the current time
#             # Construct the Flux query to count the points
#             flux_query = f'''
#             from(bucket: "{self.bucket}")
#                 |> range(start: {start_date}, stop: {end_date})
#                 |> filter(fn: (r) => r["_measurement"] == "stock_data")
#             '''
#
#             # Add symbol filter if specified
#             if symbol:
#                 flux_query += f' |> filter(fn: (r) => r["Symbol"] == "{symbol}")'
#
#             flux_query += '''
#                 |> count()
#             '''
#
#             # Execute the query and fetch the results
#             result = query_api.query(flux_query)
#
#             # Extract the count from the result
#             total_count = 0
#             for table in result:
#                 for record in table.records:
#                     total_count += record.get_value()
#
#             return total_count
#
#         except Exception as e:
#             print(f"Error estimating deletion count: {e}")
#             return 0
#
#     def delete_data_chunks(self, symbol=None, start_date=None, end_date=None, chunk_size=100000):
#         """
#         Deletes chunks of data from InfluxDB based on the given filters (symbol, date range, chunk size).
#         :param symbol: Stock symbol to filter by (optional).
#         :param start_date: Start date for the data to be deleted (optional).
#         :param end_date: End date for the data to be deleted (optional).
#         :param chunk_size: The number of points to delete in one batch.
#         """
#         try:
#             delete_api = self.client.delete_api()
#
#             # Break the time range into smaller time intervals based on the chunk size
#             start = start_date or "1970-01-01T00:00:00"
#             stop = end_date or datetime.now().isoformat()
#
#             # Estimate total points to delete
#             total_points = self.estimate_deletion_count(symbol, start, stop)
#             points_per_day = total_points // ((datetime.fromisoformat(stop) - datetime.fromisoformat(start)).days or 1)
#             days_per_chunk = max(1, (chunk_size // points_per_day) if points_per_day > 0 else 1)
#
#             current_start = datetime.fromisoformat(start)
#             current_stop = current_start + timedelta(days=days_per_chunk)
#
#             while current_start < datetime.fromisoformat(stop):
#                 # Format the time range for this chunk
#                 formatted_start = current_start.isoformat() + "Z"
#                 formatted_stop = current_stop.isoformat() + "Z"
#
#                 # Predicate for deletion based on measurement and symbol
#                 predicate = f'_measurement="stock_data"'
#                 if symbol:
#                     predicate += f' AND Symbol="{symbol}"'
#
#                 # Perform deletion in chunks
#                 delete_api.delete(start=formatted_start, stop=formatted_stop, bucket=self.bucket, org=self.org,
#                                   predicate=predicate)
#                 print(f"Deleted data between {formatted_start} and {formatted_stop}")
#
#                 # Move the time window forward
#                 current_start = current_stop
#                 current_stop = min(datetime.fromisoformat(stop), current_stop + timedelta(days=days_per_chunk))
#
#         except ApiException as e:
#             print(f"Error deleting data chunks from InfluxDB: {e}")
#
#     def _convert_dataframe_to_points(self, df):
#         """
#         Helper function to convert a pandas DataFrame into InfluxDB points.
#         :param df: DataFrame with stock data.
#         :return: List of InfluxDB points.
#         """
#         points = []
#         for _, row in df.iterrows():
#             point = (
#                 Point("stock_data")
#                 .tag("Symbol", row["Symbol"])
#                 .field("Open", row["Open"])
#                 .field("High", row["High"])
#                 .field("Low", row["Low"])
#                 .field("Close", row["Close"])
#                 .field("Volume", row["Volume"])
#                 .time(row["Date"])
#             )
#             points.append(point)
#         return points
