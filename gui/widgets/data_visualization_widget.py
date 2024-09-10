from threading import Thread

from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QComboBox, QLabel, \
    QPushButton, QHeaderView, QFileDialog, QSizePolicy, QSpacerItem, QProgressBar
from PyQt5.QtCore import Qt, QMutex, QThread
import pandas as pd

from config.data_loader_thread import DataLoaderThread
from config.database_query_thread import DatabaseQueryThread
from gui.widgets.export_dialog_widget import ExportDialog
from gui.widgets.filter_dialog_widget import FilterDialog
from utils.texts_utils import get_text_for_risk_metrics_combo_box, get_text_for_algorithms_combo_box
from utils.texts_utils import description
from utils.ui_utils import create_combo_box, create_button, create_label, create_table
import multiprocessing as mp
from services.questdb_service import QuestDBService


class DataVisualizationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Data
        # self.update_progress = None

        self.reset_button = None
        self.bottom_actions_layout = None
        self.query_thread = None
        self.spinner_svg = None
        self.loading_label = None
        self.progress_bar = None
        self.data = None

        # UI Elements
        self.main_layout = None
        self.action_layout = None
        self.footer_layout = None
        self.run_layout = None
        self.risk_averse_layout = None
        self.select_algorithm_layout = None
        self.algorithm_layout = None
        self.bottom_layout = None
        self.headline_label = None
        self.description_label = None
        self.row_count_label = None

        self.delete_button = None
        self.filter_button = None
        self.export_button = None
        self.run_button = None

        self.symbol_combo_box = None
        self.risk_matrics_combo_box = None

        self.algorithm_combo_box = None
        self.table_widget = None

        # Threads
        self.loader_threads = []
        self.mutex = QMutex()  # Mutex for thread-safe table updates

        self.initUI()

    def initUI(self):
        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        # self.readDataFromDatabase()

        # Headline and description
        self.headline_label = create_label("Financial Data Overview", "Headline")
        self.description_label = create_label(description(), "Description")
        self.main_layout.addWidget(self.headline_label)
        self.main_layout.addWidget(self.description_label)

        # Actions and Symbol Selection
        self.action_layout = QHBoxLayout()

        # Action buttons
        # self.delete_button = create_button("Delete", "ActionButton", width=100, action_func=self.open_delete_dialog)
        # self.filter_button = create_button("Filters", "ActionButton", width=100, action_func=self.open_filter_dialog)
        # self.export_button = create_button("Export", "ActionButton", width=100, action_func=self.open_export_dialog)
        # self.action_layout.addWidget(self.delete_button)
        # self.action_layout.addWidget(self.filter_button)
        # self.action_layout.addWidget(self.export_button)

        # Loading label and spinner
        self.loading_label = QLabel("", self)
        self.loading_label.setVisible(False)
        self.spinner_svg = QSvgWidget("assets/images/spinner.svg")  # Path to your SVG file
        self.spinner_svg.setVisible(False)
        self.spinner_svg.setFixedSize(40, 40)

        self.action_layout.addWidget(self.spinner_svg)
        self.action_layout.addWidget(self.loading_label)
        # Spacer to push the symbol combo box to the right
        self.action_layout.addStretch()

        self.symbol_combo_box = create_combo_box(object_name="SymbolComboBox")
        # self.symbol_combo_box.currentIndexChanged.connect(self.filter_data)
        self.action_layout.addWidget(self.symbol_combo_box)

        self.main_layout.addLayout(self.action_layout)

        # Table widget to display data
        self.table_widget = create_table(object_name="DataTable", column_count=7,
                                         header_labels=['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

        self.main_layout.addWidget(self.table_widget)

        # Progress bar for loading
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)  # Initialize the progress bar with 0% progress
        self.main_layout.addWidget(self.progress_bar)  # Add the progress bar to the layout

        # Footer layout for displaying the number of rows
        self.footer_layout = QHBoxLayout()
        self.footer_layout.addStretch()  # Push the label to the right

        self.row_count_label = create_label("Total Rows: 0", "RowCountLabel")
        self.footer_layout.addWidget(self.row_count_label)

        self.main_layout.addLayout(self.footer_layout)

        # Creating horizontal layouts for Risk Averse and Algorithm selections
        self.risk_averse_layout = QHBoxLayout()
        self.select_algorithm_layout = QVBoxLayout()

        self.risk_averse_layout.addWidget(create_label("Risk Averse:", "RiskAverseLabel"))

        # Risk Averse combo box
        self.risk_matrics_combo_box = create_combo_box(items=get_text_for_risk_metrics_combo_box(),
                                                       object_name="RisksMatrixComboBox")
        self.risk_averse_layout.addWidget(self.risk_matrics_combo_box)

        # Add the risk averse layout to the vertical layout
        self.select_algorithm_layout.addLayout(self.risk_averse_layout)

        # Algorithm selection label and combo box (in horizontal layout)
        self.algorithm_layout = QHBoxLayout()

        self.algorithm_layout.addWidget(create_label("Select Algorithm:", "AlgorithmLabel"))

        # Algorithm combo box
        self.algorithm_combo_box = create_combo_box(items=get_text_for_algorithms_combo_box(),
                                                    object_name="AlgorithmComboBox")
        self.algorithm_layout.addWidget(self.algorithm_combo_box)

        # Add the algorithm layout to the vertical layout
        self.select_algorithm_layout.addLayout(self.algorithm_layout)

        # Horizontal layout to include the vertical layout and the Run button
        self.bottom_actions_layout = QHBoxLayout()
        self.bottom_actions_layout.addLayout(self.select_algorithm_layout)

        # Spacer to create space between combo boxes and the Run button
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.bottom_actions_layout.addItem(spacer)

        self.run_layout = QVBoxLayout()
        # Run button
        self.run_button = create_button("Run", "RunButton", 100, self.run_algorithm)
        self.run_layout.addWidget(self.run_button)

        # Reset Button
        self.reset_button = create_button("Reset", "ResetButton", 100, self.rest_ui)
        self.run_layout.addWidget(self.reset_button)

        self.bottom_actions_layout.addLayout(self.run_layout)
        # Add the final horizontal layout to the main layout
        self.main_layout.addLayout(self.bottom_actions_layout)

        # Set the layout for the widget
        self.setLayout(self.main_layout)

        self.load_data_form_database()
        # Load data (simulate loading data from CSV)
        # self.load_data()

    def load_data_form_database(self):
        """
        Load data from the database.
        :return:
        """
        self.loading_label.setVisible(True)
        self.loading_label.setText("Loading data from database...")
        self.spinner_svg.setVisible(True)

        # Start a thread to load data from database
        self.query_thread = DatabaseQueryThread(base_url="http://localhost:9000", query="SELECT * FROM stock_prices")
        self.query_thread.quried_data.connect(self.on_data_loaded)
        self.query_thread.start()

    def on_data_loaded(self, data):
        """
        Slot to handle when data is loaded from the database.
        """
        if data is None:
            self.loading_label.setText("Error loading data from the database.")
            self.loading_label.setColor(Qt.red)
            return

        self.data = data
        self.loading_label.setText("Populating table...")
        self.table_widget.setRowCount(len(self.data))
        self.update_row_count()
        self.loading_label.setText(f"Loaded {len(self.data)} rows from the database. ")
        self.spinner_svg.setVisible(False)

    def load_data(self, data=None):
        print("It's timee to load data bruh ")
        # if data is not None:
        #     self.data = data
        #     self.table_widget.setRowCount(len(self.data))
        #
        #     # Split the data into chunks for multiprocessing
        #     chunk_size = len(self.data) // mp.cpu_count()
        #     chunks = [self.data.iloc[i:i + chunk_size] for i in range(0, len(self.data), chunk_size)]
        #
        #     # Ensure that any remaining rows are included in the last chunk
        #     if len(self.data) % chunk_size != 0:
        #         chunks[-1] = self.data.iloc[len(self.data) - len(self.data) % chunk_size:]
        #
        #     # Use multiprocessing to process chunks in parallel
        #     for i, chunk in enumerate(chunks):
        #         start_row = i * chunk_size
        #         self.process_chunk(chunk, start_row)
        #
        # # Populate the dropdown with symbols, including an "All" option
        # self.symbol_combo_box.clear()
        # self.symbol_combo_box.addItem("All")
        # symbols = self.data['Symbol'].unique()
        # self.symbol_combo_box.addItems(symbols)
        #
        # # Ensure the combo box is connected to the filter function
        # self.symbol_combo_box.currentIndexChanged.connect(self.filter_data)

    def readDataFromDatabase(self):
        self.data = QuestDBService.query_data(base_url="http://localhost:9000", query="SELECT * FROM stock_prices")

    def process_chunk(self, chunk, start_row):
        if chunk is None or len(chunk) == 0:
            return  # Skip empty chunks

        # Create and start a thread for each chunk
        loader_thread = DataLoaderThread(chunk, start_row)

        # Connect signals
        loader_thread.update_table.connect(self.populate_table)
        loader_thread.update_progress.connect(self.update_progress)
        loader_thread.update_row_count.connect(self.update_row_count)

        # Start the thread
        loader_thread.start()

        # Store the thread reference to prevent garbage collection
        self.loader_threads.append(loader_thread)

        # Ensure the thread finishes before being deleted
        loader_thread.finished.connect(lambda: self.clean_up_thread(loader_thread))

    def populate_table(self, row, column, value):
        """
        Populate the table with the given value at the specified row and column.
        :param row: row index
        :param column: column index
        :param value: value to populate
        :return: None
        """
        self.table_widget.setItem(row, column, QTableWidgetItem(value))

    def update_row_count(self):
        """Update the row count label with the current number of rows in the table."""
        row_count = self.table_widget.rowCount()
        self.row_count_label.setText(f"Total Rows: {row_count}")

    # def update_progress(self, value):
    #     """Slot to update the progress bar."""
    #     self.progress_bar.setValue(value)

    def filter_data(self):
        # Get the selected symbol
        selected_symbol = self.symbol_combo_box.currentText()
        print(selected_symbol)

    def open_export_dialog(self):
        # Open the export dialog
        dialog = ExportDialog(self, self.data)
        dialog.exec_()

    def open_filter_dialog(self):
        # Open the filter dialog
        dialog = FilterDialog(self)
        dialog.exec_()

    def open_delete_dialog(self):
        # Open the delete dialog
        print("Delete button clicked")

    def run_algorithm(self):
        """
        Run the selected algorithm on the data.
        """
        # Get the selected risk metric and algorithm
        risk_metric = self.risk_matrics_combo_box.currentText()
        algorithm = self.algorithm_combo_box.currentText()

        # Get the data to run the algorithm on
        data = self.data

        # Ensure the data is not empty
        if data is None or len(data) == 0:
            print("No data to run the algorithm on.")
            return

        print(f"Running algorithm: {algorithm} with risk metric: {risk_metric}\n")

        #Print the data
        print(data.head())

        # Start a thread to run the algorithm

        # thread = Thread(target=self.run_algorithm_thread, args=(data, risk_metric, algorithm))
        # thread.start()

    def clean_up_thread(self, thread):
        """Ensure the thread finishes and then remove it from the list."""
        thread.wait()  # Wait for the thread to finish
        print(f"Thread {thread} finished.")
        self.loader_threads.remove(thread)  # Remove the finished thread from the list


    def rest_ui(self):
        print("Reset button clicked")
        self.symbol_combo_box.setCurrentIndex(0)
        self.risk_matrics_combo_box.setCurrentIndex(0)
        self.algorithm_combo_box.setCurrentIndex(0)
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)
        self.row_count_label.setText("Total Rows: 0")
        self.progress_bar.setValue(0)
        self.loading_label.setText("")