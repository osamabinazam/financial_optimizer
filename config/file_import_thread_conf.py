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
