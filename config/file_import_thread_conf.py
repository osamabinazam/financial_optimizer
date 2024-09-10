from PyQt5.QtCore import QThread, pyqtSignal
import pandas as pd

from services.questdb_service import QuestDBService
from .file_process import FileImportManager


class FileImportThread(QThread):
    progress = pyqtSignal(int)  # Signal to emit progress
    finished = pyqtSignal()  # Signal to emit when finished

    def __init__(self, file_paths):
        super().__init__()
        self.file_paths = file_paths

    def run(self):
        """
        Start file processing using FileImportManager.
        The actual multiprocessing is handled inside FileImportManager.
        """
        file_manager = FileImportManager(self.file_paths)
        file_manager.process_files()  # This method will use multiprocessing

        # Emit finished signal after processing is complete
        self.finished.emit()

# class FileImportThread(QThread):
#     progress = pyqtSignal(int)  # Signal to update progress in the UI
#     finished = pyqtSignal()  # Signal to indicate that the file import is complete
#
#     def __init__(self, file_paths, column_names, parent=None):
#         super().__init__(parent)
#         self.file_paths = file_paths  # List of CSV/TXT file paths
#         self.column_names = column_names  # Column names to use for the imported data
#         self.questdb_service = QuestDBService()  # Instance of QuestDBService to handle data writes
#         self.file_process = FileProcessor()
#     def run(self):
#         """
#         Entry point for the thread. This function runs when the thread starts.
#         It processes each file in a separate process using a multiprocessing Pool.
#         """
#         with Pool(cpu_count()) as pool:
#             results = pool.map(self.file_process.process_file, enumerate(self.file_paths))
#             for result in results:
#                 print(result)  # Log result
#
#         # Emit signal indicating that all files have been processed
#         self.finished.emit()

# def process_file(self, file_info):
#     index, file_path = file_info
#     """
#     Reads a CSV file, processes the data, and writes it to QuestDB using the QuestDBService.
#     :param file_path: Path to the CSV file.
#     :param index: Index of the file being processed.
#     :return: Status message indicating success or failure.
#     """
#     try:
#         # Load CSV data into a DataFrame
#         df = pd.read_csv(xxfile_path, header=None, names=self.column_names)
#
#         # Convert 'Date' column to datetime format and ensure numeric columns are properly typed
#         df['Date'] = pd.to_datetime(df['Date'])
#         df[['Open', 'High', 'Low', 'Close', 'Volume']] = df.select_dtypes(include=[float])
#
#         # Insert data to the database
#         self.questdb_service.insert_data(conf='http::addr=localhost:9000;', table_name='stock_prices', data=df,
#                                          batch_size=1000)
#
#         # Calculate progress
#         self.progress.emit(int((index + 1) / len(self.file_paths) * 100))
#         return f"File {file_path} processed successfully."
#
#     except Exception as e:
#         return f"Error processing file {file_path}: {e}"


# from PyQt5.QtCore import QThread, pyqtSignal
# import pandas as pd
# import concurrent.futures
# # from services.influxdb_service import InfluxDBService
# from services.questdb_service import QuestDBService
#
#
# class FileImportThread(QThread):
#     """
#     Thread responsible for importing CSV files into the application.
#     Processes each file concurrently and writes the data to InfluxDB using the InfluxDBService.
#     """
#     progress = pyqtSignal(int)  # Signal to update progress in the UI
#     finished = pyqtSignal()  # Signal to indicate that the file import is complete
#
#     def __init__(self, file_paths, column_names, parent=None):
#         super().__init__(parent)
#         self.file_paths = file_paths  # List of CSV/TXT file paths
#         self.column_names = column_names  # Column names to use for the imported data
#         # self.influx_service = InfluxDBService()  # Instance of InfluxDBService to handle data writes
#         self.questdb_service = QuestDBService()  # Instance of QuestDBService to handle data writes
#
#     def run(self):
#         """
#         Entry point for the thread. This function runs when the thread starts.
#         It processes each file in a separate thread using ThreadPoolExecutor.
#         """
#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             # Process each file concurrently
#             futures = [executor.submit(self.process_file, file_path, index)
#                        for index, file_path in enumerate(self.file_paths)]
#
#             for future in concurrent.futures.as_completed(futures):
#                 try:
#                     result = future.result()
#                     print(result)  # Log file processing results
#                 except Exception as e:
#                     print(f"Error processing file: {e}")  # Log any errors encountered
#
#         # Emit signal indicating that all files have been processed
#         self.finished.emit()
#
#     def process_file(self, file_path, index):
#         """
#         Reads a CSV file, processes the data, and writes it to InfluxDB using the InfluxDBService.
#
#         :param file_path: Path to the CSV file.
#         :param index: Index of the file being processed.
#         :return: Status message indicating success or failure.
#         """
#         try:
#             # Load CSV data into a DataFrame
#             df = pd.read_csv(file_path, header=None, names=self.column_names)
#
#             # Convert 'Date' column to datetime format
#             df['Date'] = pd.to_datetime(df['Date'])
#
#             # Ensure numeric columns are properly typed
#             df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].astype(
#                 float)
#
#             # Use the InfluxDBService to write the data chunk to the database
#             # self.influx_service.write_data_chunk(df)
#             self.questdb_service.insert_data(conf='http::addr=localhost:9000;', table_name='stock_data', data=df,
#                                              batch_size=1000)
#
#             # Update the progress as a percentage of files processed
#             self.progress.emit(int((index + 1) / len(self.file_paths) * 100))
#             return f"File {file_path} processed successfully."
#
#         except Exception as e:
#             return f"Error processing file {file_path}: {e}"
