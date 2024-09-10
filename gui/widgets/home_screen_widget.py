import os
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMainWindow, QProgressBar

from config.file_import_thread_conf import FileImportThread
from config.delete_data_thread_conf import MultiprocessingDataDeletionThread  # Use deletion thread
from utils.ui_utils import display_message_box, create_label, create_button, create_rounded_pixmap, display_snackbar, \
    display_toaster
# from config.influxdb_config import InfluxDBConfig
# from services.influxdb_service import InfluxDBService


class HomeScreenWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.folder_path = None
        self.file_paths = None
        self.file_import_thread = None
        self.deletion_thread = None  # Add deletion thread
        # self.influxdb_service = InfluxDBService()  # Initialize InfluxDBService

        # UI Components
        self.layout = None
        self.logo_label = None
        self.greeting_label = None
        self.import_button = None
        self.progress_bar = None

        self.init_ui()

        # Check InfluxDB connection when the home screen is initialized
        # self.check_influxdb_connection()

    def init_ui(self):
        """Initialize the UI components and layout."""
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        # Add logo
        self.logo_label = QLabel(self)
        logo_pixmap = QPixmap("assets/images/logo.webp")  # Path to the logo image
        rounded_pixmap = create_rounded_pixmap(logo_pixmap, 100, 100, 20)  # 100x100 size with 20px radius
        self.logo_label.setPixmap(rounded_pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo_label)

        # Add greeting label
        self.greeting_label = create_label("Welcome to Financial Optimizer", object_name="GreetingLabel")
        self.greeting_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.greeting_label)

        # Add import button
        self.import_button = create_button("Import Data from CSV", "ImportButton", width=200,
                                           action_func=self.import_data)
        self.import_button.setDisabled(False)  # Initially disabled
        self.import_button.setCursor(Qt.ForbiddenCursor)  # Cursor set to forbidden when disabled
        self.layout.addWidget(self.import_button)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.layout.addWidget(self.progress_bar)

    def check_influxdb_connection(self):
        """Check the connection to InfluxDB and update the UI accordingly."""
        # try:
        # influxdb_client = InfluxDBConfig().get_client()
        # if influxdb_client.ping():
        #     display_toaster(self, "Connected to InfluxDB successfully!")
        self.enable_import_button()
        # else:
        #     display_toaster(self, "Failed to connect to InfluxDB.", is_error=True, closable=True)
        # except Exception as e:
        #     display_toaster(self, f"Error connecting to InfluxDB: {e}", is_error=True, closable=True)

    def enable_import_button(self):
        """Enable the import button and update its cursor."""
        self.import_button.setDisabled(False)  # Enable the import button
        self.import_button.setCursor(Qt.PointingHandCursor)  # Change cursor to pointing hand on hover

    def import_data(self):
        """Trigger the file import process and handle file selection."""
        options = QFileDialog.Options()
        self.folder_path = QFileDialog.getExistingDirectory(self, "Select Folder Containing CSV/TXT Files",
                                                            options=options)

        if not self.folder_path:
            display_message_box(self, "Cancelled", "No folder selected")
            return

        # Get all CSV/TXT file paths in the selected folder
        self.file_paths = [os.path.join(self.folder_path, file) for file in os.listdir(self.folder_path) if
                           file.endswith(('.csv', '.txt'))]
        if not self.file_paths:
            display_message_box(self, "No Files Found", "The selected folder contains no CSV or TXT files.")
            return

        # Start data deletion before importing new data
        self.start_data_deletion()

    def start_data_deletion(self):
        """Start the complete data deletion process in the background."""
        # We will delete all data without using any filters
        display_toaster(self, "Deleting all data from the database...")


        # Start deletion in the background using MultiprocessingDataDeletionThread
        self.deletion_thread = MultiprocessingDataDeletionThread(
            symbol=None,  # No symbol filter
            start_date=None,  # No start date filter
            end_date=None  # No end date filter
        )
        self.deletion_thread.progress.connect(self.update_deletion_progress)
        self.deletion_thread.finished.connect(self.on_deletion_finished)
        self.deletion_thread.start()

    def update_deletion_progress(self, value):
        """Update the progress bar with the current value of the deletion process."""
        self.progress_bar.setValue(value)
        print(f"Deletion progress: {value}%")

    def on_deletion_finished(self):
        """Handle actions when the deletion is finished."""
        display_toaster(self, "All data deleted! You can now start the data import.")
        self.progress_bar.setValue(100)
        self.start_data_import()  # Start import after deletion is completed

    def start_data_import(self, folder_path=None):
        """Start the data import process after deletion is finished."""
        display_toaster(self, "Starting data import.")

        # Open file dialog again to select the folder for importing new files

        # Get all CSV/TXT file paths in the selected folder
        # self.file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.csv', '.txt'))]
        if not self.file_paths:
            display_message_box(self, "No Files Found", "The selected folder contains no CSV or TXT files.")
            return

        # Define the column names that correspond to the data in the files
        column_names = ['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']

        # Create and start the FileImportThread
        self.file_import_thread = FileImportThread(self.file_paths)
        self.file_import_thread.progress.connect(self.update_import_progress)
        self.file_import_thread.finished.connect(self.on_import_finished)
        self.file_import_thread.start()

    def update_import_progress(self, value):
        """Update the progress bar with the current value of the import process."""
        self.progress_bar.setValue(value)

    def on_import_finished(self):
        """Handle actions when the import is finished."""
        print("Import finished!")
        self.progress_bar.setValue(100)

        # Assuming data visualization widget expects the data in a specific format
        main_window = self.find_main_window()

        if main_window:
            # display_snackbar(self, "Data imported successfully!", "success")
            main_window.navigate_to(main_window.data_visualization_screen)
        else:
            display_message_box(self, "Error", "Main window not found")

    def find_main_window(self):
        """Helper function to find and return the main window."""
        parent = self.parent()
        while parent is not None:
            if isinstance(parent, QMainWindow):
                return parent
            parent = parent.parent()
        return None
