import concurrent.futures

from PyQt5.QtCore import QThread, pyqtSignal
from multiprocessing import Pool, cpu_count
# from services.influxdb_service import InfluxDBService
from services.questdb_service import QuestDBService
from datetime import datetime, timedelta


def delete_chunk(args):
    """
    Function to delete a chunk of data in a separate process.
    """
    symbol, start_date, end_date = args
    # influx_service = InfluxDBService()
    # influx_service.delete_data_chunks(symbol, start_date, end_date)
    return start_date, end_date


class MultiprocessingDataDeletionThread(QThread):
    """
    A QThread that handles data deletion using multiprocessing for faster performance.
    """
    progress = pyqtSignal(int)  # Signal to update progress in the UI
    finished = pyqtSignal()  # Signal emitted when deletion is done

    def __init__(self, symbol=None, start_date=None, end_date=None, chunk_size=50000, parent=None):
        """
        Initialize the thread to delete data using multiprocessing.
        :param symbol: Stock symbol to filter.
        :param start_date: Start date for deletion.
        :param end_date: End date for deletion.
        :param chunk_size: Number of points to delete per chunk.
        :param parent: Optional parent widget.
        """
        super().__init__(parent)
        self.symbol = symbol
        self.start_date = start_date or "2023-01-01T00:00:00Z"  # Default start date
        self.end_date = end_date or datetime.now().isoformat() + "Z"  # Default end date
        self.chunk_size = chunk_size
        self.questdb_service = QuestDBService()

    def run(self):
        """
        Perform the deletion process using multiprocessing.
        """
        try:
            # influx_service = InfluxDBService()

            # Step 1: Estimate total points to delete
            # total_points = influx_service.estimate_deletion_count(self.symbol, self.start_date, self.end_date)
            # if total_points == 0:
            #     print("No data points found for deletion.")
            #     self.finished.emit()
            #     return

            # Step 2: Calculate the number of chunks
            # total_chunks = (total_points // self.chunk_size) + (1 if total_points % self.chunk_size != 0 else 0)
            #
            # # Step 3: Calculate time range per chunk
            # start_time = datetime.fromisoformat(self.start_date.rstrip("Z"))
            # end_time = datetime.fromisoformat(self.end_date.rstrip("Z"))
            # total_duration = end_time - start_time
            # time_range_per_chunk = total_duration / total_chunks
            #
            # # Step 4: Prepare chunk ranges (each chunk gets a distinct time range)
            # chunk_ranges = [
            #     (
            #         self.symbol,
            #         (start_time + i * time_range_per_chunk).isoformat(),
            #         (start_time + (i + 1) * time_range_per_chunk).isoformat()
            #     )
            #     for i in range(total_chunks)
            # ]

            # Step 5: Use multiprocessing Pool to parallelize deletion
            # with Pool(cpu_count()) as pool:
            #     for i, (start, end) in enumerate(pool.imap(delete_chunk, chunk_ranges)):
            #         progress = int((i + 1) / total_chunks * 100)
            #         self.progress.emit(progress)

            try:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    # Submit a single deletion task to the ThreadPoolExecutor
                    future = executor.submit(
                        self.questdb_service.delete_data,
                        'http://localhost:9000',
                        table_name='stock_prices'
                    )

                    # Wait for the future to complete and get the result
                    try:
                        result = future.result()
                        print(result)  # Log deletion results
                    except Exception as e:
                        print(f"Error processing deletion: {e}")

                self.finished.emit()  # Emit the finished signal once the deletion is complete

            except Exception as e:
                print(f"Error during deletion: {e}")
                self.finished.emit()  # Ensure that the finished signal is emitted even on error

        except Exception as e:
            print(f"Error during deletion: {e}")
            self.finished.emit()  # Ensure that the finished signal is emitted even on error
