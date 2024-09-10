import pandas as pd
from PyQt5.QtCore import QThread, pyqtSignal
from services.questdb_service import QuestDBService
from time import  sleep


class DatabaseQueryThread(QThread):

    quried_data = pyqtSignal(pd.DataFrame)  # Signal to emit the queried data
    def __init__(self, base_url,query, parent=None):
        """
        Initialize the thread to query the database.
        :param query: The query string to execute.
        :param parent: Optional parent widget.
        """
        super().__init__(parent)
        self.query = query
        self.base_url = base_url

    def run(self):
        """
        Execute the query.
        """
        try:
            sleep(1)
            data = QuestDBService.query_data(self.base_url,self.query)
            self.quried_data.emit(data)
        except Exception as e:
            print(f"Error querying data: {e}")
            self.quried_data.emit(pd.DataFrame())
