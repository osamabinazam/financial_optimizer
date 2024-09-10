import os

from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QAction, QMenu, QFileDialog

from config.delete_data_thread_conf import MultiprocessingDataDeletionThread
from config.file_import_thread_conf import FileImportThread
from gui.widgets.home_screen_widget import HomeScreenWidget
from gui.widgets.data_visualization_widget import DataVisualizationWidget
from utils.ui_utils import display_message_box
from services.questdb_service import QuestDBService


def update_deletion_progress(value):
    print(f"Deletion progress: {value}%")


class MainWindow(QMainWindow):
    def __init__(self):

        """
        Initializes the main window of the application.
        """
        super().__init__()
        self.file_import_thread = None
        self._create_menu()
        self.setWindowTitle("Financial Optimizer")          # Set the window title
        self.setGeometry(100, 100, 800, 600)
        self.delete_thread = None  # Initialize thread instance to None# Set the window dimensions
        self.file_paths = None  # Initialize folder path to None
        self.central_widget = QStackedWidget()              # Create a QStackedWidget to hold multiple screens in the central widget area
        self.setCentralWidget(self.central_widget)          # Set the central widget of the main window

        # Create instances of your screens
        self.home_screen = HomeScreenWidget(self)
        self.data_visualization_screen = DataVisualizationWidget(self)  # Pass the main window instance to the screen

        # Add screens to the QStackedWidget
        self.central_widget.addWidget(self.home_screen)                 # Add the home screen
        self.central_widget.addWidget(self.data_visualization_screen)   # Add the data visualization screen

        # Show the home screen initially
        self.central_widget.setCurrentWidget(self.data_visualization_screen)


    def _create_menu(self):
        """
        Create the menu bar for the main window.
        :return: None
        """
        # Create the menu bar
        menubar = self.menuBar()
        # menubar.setNativeMenuBar(False)

        # Create the File menu
        file_menu = menubar.addMenu('&File')
        help_menu = menubar.addMenu("&Help")
        # Create the Import Data action
        import_action = QAction('Import Data', self)
        import_action.triggered.connect(self._import_data)
        file_menu.addAction(import_action)

        # Create the Export Data Submenu
        export_menu = QMenu('Export Data', self)

        # HTML Action
        to_html = QAction('To HTML', self)
        to_html.setToolTip("Export data to html file...")
        to_html.triggered.connect(self._export_data)

        # CSV Action
        to_csv = QAction('To CSV', self)
        to_csv.setToolTip("Export data to csv file...")
        to_csv.triggered.connect(self._export_data)

        export_menu.addAction(to_html)
        export_menu.addAction(to_csv)

        file_menu.addMenu(export_menu)

        # Create the Exit action
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)





    def _import_data(self):
        """
        Import data action handler.
        :return: None
        """
        print("Import data action triggered.")
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder Containing CSV/TXT Files", options=options)

        if not folder_path:
            display_message_box(self, "Cancelled", "No folder selected")
            return

        self.file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('.csv', '.txt'))]
        if not self.file_paths:
            display_message_box(self, "No Files Found", "The selected folder contains no CSV or TXT files.")
            return

        self.data_visualization_screen.loading_label.setVisible(True)
        self.data_visualization_screen.loading_label.setText("Deleting data from database...")
        self.data_visualization_screen.spinner_svg.setVisible(True)

        self.delete_thread = MultiprocessingDataDeletionThread(
            symbol=None,  # No symbol filter
            start_date=None,  # No start date filter
            end_date=None  # No end date filter
        )

        self.delete_thread.progress.connect(update_deletion_progress)
        self.delete_thread.finished.connect(self.on_deletion_finished)
        self.delete_thread.start()

    def on_deletion_finished(self):
        """Handle actions when the deletion is finished."""
        self.data_visualization_screen.loading_label.setVisible(True)
        self.data_visualization_screen.loading_label.setText("Deleted data...")
        self.data_visualization_screen.spinner_svg.setVisible(True)
        print(f"Successfully Deleted the data...")
        print(QuestDBService.query_data(base_url="http://localhost:9000", query="select * from stock_prices"))
        self.start_data_import()  # Start import after deletion is completed
        # print("Readingn data from db ", QuestDBService.query_data(base_url="http://localhost:9000", query="select * from stock_data"))

    def start_data_import(self):
        """
        Start the data import process after deletion is finished.
        """
        print("Starting data import.")

        self.data_visualization_screen.loading_label.setVisible(True)
        self.data_visualization_screen.loading_label.setText("Importing data from files...")
        self.data_visualization_screen.spinner_svg.setVisible(True)
        if not self.file_paths:
            display_message_box(self, "No Files Found", "The selected folder contains no CSV or TXT files.")
            return

        columns = ['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']

        # Create and start file import thread
        self.file_import_thread = FileImportThread(self.file_paths)
        self.file_import_thread.finished.connect(self.on_import_finished)
        self.file_import_thread.start()



    def on_import_finished(self):
        """
        Handle actions when the import process is finished.
        """
        print("Data import process finished.")
        # (self, "Data Import Complete", "Data import process finished.")
        self.data_visualization_screen.load_data_form_database()  # Load data into the data visualization screen
        # self.navigate_to(self.data_visualization_screen)



    def _export_data(self):

        """
        Export data action handler.
        :return: None
        """
        print("Export data action triggered.")
    def navigate_to(self, screen):
        """
        Navigate to the specified screen.
        :param screen: The screen to navigate to.
        :return: None
        """
        self.central_widget.setCurrentWidget(screen)
