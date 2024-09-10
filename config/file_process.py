from multiprocessing import cpu_count, Pool, current_process
import pandas as pd
from services.questdb_service import QuestDBService
import sys


class FileImportManager:
    """
    A class that handles file processing and database interactions separately from the PyQt framework.
    """

    def __init__(self, file_paths):
        self.file_paths = file_paths
        print("File Paths: ", self.file_paths)
        self.questdb_service = QuestDBService()  # Initialize the QuestDB service here

    def process_files(self):
        num_processors = cpu_count()
        with Pool(num_processors) as pool:
            results = pool.map(self.process_file, self.file_paths)
            # Check results to see if any error occurred
            for result in results:
                print("Result: ",result)

    def process_file(self, file_info):
        file_path = file_info
        process_id = current_process().pid
        try:
            print(f"Process ID {process_id} is processing {file_path}")
            column_names = ['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            df = pd.read_csv(file_path, header=None, names=column_names)
            df['Date'] = pd.to_datetime(df['Date'])

            # Insert data into the database
            self.insert_data(df)

            print(f"File {file_path} processed and data written successfully.")

        except Exception as e:
            return f"Error processing file {file_path}: {e}"

    def insert_data(self, data):
        """
        Insert data into the database. This function simulates a database write operation.
        """
        try:
            # Example connection and insertion logic
            conf = 'http::addr=localhost:9000;'
            table_name = 'stock_prices'
            batch_size = 1000
            self.questdb_service.insert_data(conf, table_name, data, batch_size)
            print(f"Data inserted to database for table {table_name}", flush=True)
        except Exception as e:
            print(f"Error inserting data into the database: {e}", file=sys.stderr, flush=True)


