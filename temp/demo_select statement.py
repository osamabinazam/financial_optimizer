# # import pandas as pd
# # import os
# # from questdb.ingress import Sender, TimestampNanos
# #
# #
# # def load_data(directory):
# #     """Load CSV and TXT files from the specified directory into a single DataFrame."""
# #     data_frames = []
# #     columns = ['Symbol', 'Date', 'Low', 'High', 'Open', 'Close', 'Volume']
# #     for filename in os.listdir(directory):
# #         if filename.endswith(('.csv', '.txt')):
# #             file_path = os.path.join(directory, filename)
# #             df = pd.read_csv(file_path, header=None, names=columns)
# #             data_frames.append(df)
# #     # return pd.concat(data_frames, ignore_index=True)
# #
# #
# # def batch_ingest(df, batch_size, table_name):
# #     """Ingest data into QuestDB in batches."""
# #     conf = 'http::addr=localhost:9000;'
# #     with Sender.from_conf(conf) as sender:
# #         # Convert 'Date' to datetime and ensure it is in the correct format
# #         df['Date'] = pd.to_datetime(df['Date'])
# #
# #         # Process DataFrame in chunks
# #         for start in range(0, df.shape[0], batch_size):
# #             end = start + batch_size
# #             chunk = df.iloc[start:end]
# #             for index, row in chunk.iterrows():
# #                 sender.row(
# #                     table_name=table_name,
# #                     symbols={'Symbol': row['Symbol']},
# #                     columns={
# #                         'Open': row['Open'],
# #                         'Low': row['Low'],
# #                         'High': row['High'],
# #                         'Close': row['Close'],
# #                         'Volume': row['Volume']
# #                     },
# #                     at=TimestampNanos.from_datetime(row['Date'])
# #                 )
# #             # Flush after each batch
# #             sender.flush()
# #             print(f'Batch from {start} to {end} sent successfully')
# #
# #
# # if __name__ == '__main__':
# #     directory = './data/in'  # Update this path to your files directory
# #
# #     print("Loading data from files...")
# #     load_data(directory)
# #     batch_size = 1000  # Define the batch size based on your system's capacity
# #     table_name = 'stock_data'  # Ensure this table name matches your database schema
# #
# #     print("Data loaded successfully.")
# #
# #     # Perform the batch ingestion
# #     print("Ingesting data into QuestDB...")
# #     batch_ingest(df_stocks, batch_size, table_name)
# #     print("All data has been successfully ingested into the database.")
#
#
#
# import pandas as pd
# import os
# from multiprocessing import Pool
# from questdb.ingress import Sender, TimestampNanos
#
# def read_file(file_path):
#     columns = ['Symbol', 'Date', 'Low', 'High', 'Open', 'Close', 'Volume']
#     return pd.read_csv(file_path, header=None, names=columns)
#
# def load_data(directory):
#     files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('.csv', '.txt'))]
#     with Pool(8) as p:  # Adjust the number of processes based on your system's capabilities
#         data_frames = p.map(read_file, files)
#     return pd.concat(data_frames, ignore_index=True)
#
# def batch_ingest(df, batch_size, table_name):
#     conf = 'http::addr=localhost:9000;'
#     with Sender.from_conf(conf) as sender:
#         df['Date'] = pd.to_datetime(df['Date'])
#         for start in range(0, df.shape[0], batch_size):
#             end = start + batch_size
#             chunk = df.iloc[start:end]
#             for index, row in chunk.iterrows():
#                 sender.row(
#                     table_name=table_name,
#                     symbols={'Symbol': row['Symbol']},
#                     columns={
#                         'Open': row['Open'],
#                         'Low': row['Low'],
#                         'High': row['High'],
#                         'Close': row['Close'],
#                         'Volume': row['Volume']
#                     },
#                     at=TimestampNanos.from_datetime(row['Date'])
#                 )
#             sender.flush()
#
# if __name__ == '__main__':
#     directory = './data/in'
#     df_stocks = load_data(directory)
#     batch_size = 1000
#     table_name = 'stock_data'
#
#     # inserting data
#     print("Inserting data")
#     batch_ingest(df_stocks, batch_size, table_name)
#     print("All data has been successfully ingested into the database.")
#


# import pandas as pd
# import os
# from multiprocessing import Pool, cpu_count
# from questdb.ingress import Sender, TimestampNanos
#
#
# def process_and_ingest_file(file_path):
#     """This function will read, process, and ingest the data for a single file."""
#     try:
#         columns = ['Symbol', 'Date', 'Low', 'High', 'Open', 'Close', 'Volume']
#         df = pd.read_csv(file_path, header=None, names=columns)
#         df['Date'] = pd.to_datetime(df['Date'])
#
#         conf = 'http::addr=localhost:9000;'  # Configuration for QuestDB
#         table_name = 'stock_data'  # Database table name
#
#         with Sender.from_conf(conf) as sender:
#             for index, row in df.iterrows():
#                 sender.row(
#                     table_name=table_name,
#                     symbols={'Symbol': row['Symbol']},
#                     columns={
#                         'Open': row['Open'],
#                         'Low': row['Low'],
#                         'High': row['High'],
#                         'Close': row['Close'],
#                         'Volume': row['Volume']
#                     },
#                     at=TimestampNanos.from_datetime(row['Date'])
#                 )
#             sender.flush()
#         print(f"Data from {file_path} ingested successfully.")
#     except Exception as e:
#         print(f"Failed to process {file_path}: {e}")
#
#
# def load_and_ingest_data(directory):
#     files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('.csv', '.txt'))]
#     # Use the number of CPUs available for parallel processing, or limit it if necessary
#     num_processors = cpu_count()
#     print(f"Using {num_processors} processors.")
#     with Pool(num_processors) as p:
#         p.map(process_and_ingest_file, files)
#
#
# if __name__ == '__main__':
#     directory = './data/in'  # Update this path to your files directory
#     load_and_ingest_data(directory)


import pandas as pd
import os
from multiprocessing import Pool, cpu_count, current_process
from questdb.ingress import Sender, TimestampNanos
import requests
import  time


def clear_table(base_url, table_name):

    s = time.time()
    """Clear all data from the specified table using QuestDB's REST API."""
    url = f"{base_url}/exec"
    params = {'query': f'TRUNCATE TABLE {table_name};'}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # This will raise an exception for HTTP error codes
        print(f"Successfully cleared data from {table_name}.")

    except requests.RequestException as e:
        print(f"Failed to clear data from {table_name}: {e}")

    print(f"Time taken to clear table: {time.time() - s} seconds.")


def process_and_ingest_file(file_path):
    """Process and ingest file data."""
    process_id = current_process().pid
    print(f"Process ID {process_id} is processing {file_path}")

    columns = ['Symbol', 'Date', 'Low', 'High', 'Open', 'Close', 'Volume']
    df = pd.read_csv(file_path, header=None, names=columns)
    df['Date'] = pd.to_datetime(df['Date'])

    conf = 'http::addr=localhost:9000;'
    table_name = 'stock_data'

    with Sender.from_conf(conf) as sender:
        for index, row in df.iterrows():
            sender.row(
                table_name=table_name,
                symbols={'Symbol': row['Symbol']},
                columns={
                    'Open': row['Open'],
                    'Low': row['Low'],
                    'High': row['High'],
                    'Close': row['Close'],
                    'Volume': row['Volume']
                },
                at=TimestampNanos.from_datetime(row['Date'])
            )
        sender.flush()
    # print(f"Data from {file_path} successfully ingested by Process ID {process_id}.")


def load_and_ingest_data(directory):
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('.csv', '.txt'))]
    num_processors = cpu_count()
    print(f"Using {num_processors} processors.")
    with Pool(num_processors) as p:
        p.map(process_and_ingest_file, files)


if __name__ == '__main__':
    directory = './data/in'
    conf = 'http::addr=localhost:9000;'
    table_name = 'stock_data'
    base_url = 'http://localhost:9000'

    # Clear the table before ingesting new data
    clear_table(base_url, table_name)

    s = time.time()
    # Load and ingest new data
    load_and_ingest_data(directory)

    print(f"Time taken to ingest data: {time.time() - s} seconds.")


# import pandas as pd
# import os
# from multiprocessing import Pool, cpu_count, current_process
# import requests
# import time
# from questdb.ingress import Sender, TimestampNanos
#
#
# def clear_table(base_url, table_name):
#     """Clear all data from the specified table using QuestDB's REST API."""
#     s = time.time()
#     url = f"{base_url}/exec"
#     params = {'query': f'TRUNCATE TABLE {table_name};'}
#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()  # This will raise an exception for HTTP error codes
#         print(f"Successfully cleared data from {table_name}.")
#     except requests.RequestException as e:
#         print(f"Failed to clear data from {table_name}: {e}")
#     print(f"Time taken to clear table: {time.time() - s} seconds.")
#
#
# def process_and_ingest_file(file_path):
#     """Process and ingest file data."""
#     process_id = current_process().pid
#     print(f"Process ID {process_id} is processing {file_path}")
#
#     columns = ['Symbol', 'Date', 'Low', 'High', 'Open', 'Close', 'Volume']
#     df = pd.read_csv(file_path, header=None, names=columns)
#     df['Date'] = pd.to_datetime(df['Date'])
#
#     conf = 'http::addr=localhost:9000;'
#     table_name = 'stock_data'
#
#     batch_size = 1000  # Batch size for batch inserts
#     data_batches = []
#
#     with Sender.from_conf(conf) as sender:
#         for index, row in df.iterrows():
#             data_batches.append((
#                 row['Symbol'], row['Open'], row['Low'], row['High'], row['Close'], row['Volume'],
#                 TimestampNanos.from_datetime(row['Date'])
#             ))
#
#             # Send data in batches
#             if len(data_batches) >= batch_size:
#                 sender.insert(table_name, data_batches)
#                 data_batches.clear()
#
#         # Insert any remaining data
#         if data_batches:
#             sender.insert(table_name, data_batches)
#
#     print(f"Data from {file_path} successfully ingested by Process ID {process_id}.")
#
#
# def load_and_ingest_data(directory):
#     files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('.csv', '.txt'))]
#     num_processors = cpu_count()
#     print(f"Using {num_processors} processors.")
#     with Pool(num_processors) as p:
#         p.map(process_and_ingest_file, files)
#
#
# if __name__ == '__main__':
#     directory = './data/in'
#     conf = 'http::addr=localhost:9000;'
#     table_name = 'stock_data'
#     base_url = 'http://localhost:9000'
#
#     # Clear the table before ingesting new data
#     clear_table(base_url, table_name)
#
#     s = time.time()
#     # Load and ingest new data
#     load_and_ingest_data(directory)
#     print(f"Time taken to ingest data: {time.time() - s} seconds.")
