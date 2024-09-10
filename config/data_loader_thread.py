from PyQt5.QtCore import pyqtSignal, QThread


class DataLoaderThread(QThread):
    update_table = pyqtSignal(int, int, str)  # Signal to update the table (row, column, value)
    update_progress = pyqtSignal(int)  # Signal to update progress bar
    update_row_count = pyqtSignal(int)  # Signal to update the row count

    def __init__(self, data_chunk, start_row, batch_size=100):  # Add batch_size
        super(DataLoaderThread, self).__init__()
        self.data_chunk = data_chunk
        self.start_row = start_row
        self.batch_size = batch_size

    def run(self):

        """
        Process the data chunk and emit signals to update the table.
        :return:
        """
        if self.data_chunk is None or len(self.data_chunk) == 0:
            return  # If chunk is empty, return early

        total_rows = len(self.data_chunk)
        last_progress = -1

        batch = []
        for i, (index, row) in enumerate(self.data_chunk.iterrows()):
            for j, (column, value) in enumerate(row.items()):
                batch.append((self.start_row + i, j, str(value)))

            # If we've reached batch size, update the table and clear the batch
            if (i + 1) % self.batch_size == 0 or i == total_rows - 1:
                for row_data in batch:
                    self.update_table.emit(*row_data)  # Emit each item in the batch
                batch.clear()  # Clear batch after emitting

                # Emit progress as a percentage
                progress = int((i + 1) / total_rows * 100)
                if progress != last_progress:
                    self.update_progress.emit(progress)
                    last_progress = progress

        # Emit the final row count after processing is complete
        self.update_row_count.emit(self.start_row + total_rows)
