import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QFileDialog
from PyQt5.QtCore import Qt
from utils.file_utils import export_to_csv, export_to_html, generate_basic_excel_report
from utils.ui_utils import create_label, create_button, spacer_item


class ExportDialog(QDialog):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.data = data
        self.setWindowTitle("Export Data")
        self.setFixedSize(500, 150)

        # Set the default export directory
        self.default_export_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/out')
        os.makedirs(self.default_export_dir, exist_ok=True)  # Ensure the directory exists

        # UI elements to be used
        self.layout = None
        self.label = None
        self.csv_button = None
        self.excel_button = None
        self.html_button = None

        self.initUI()

    def initUI(self):
        """
        Initialize the UI elements for the export dialog.
        :return: None
        """

        # Main layout
        self.layout = QVBoxLayout()

        # Label to ask user to choose export format
        self.label = create_label("Choose the export format:", "ExportLabel")
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)

        # Button layout
        button_layout = QHBoxLayout()

        # Export buttons
        self.csv_button = create_button("Export as CSV", "ExportButton", width=150, action_func=self.export_csv)
        button_layout.addWidget(self.csv_button)

        self.excel_button = create_button("Export as Excel", "ExportButton", width=150, action_func=self.export_excel)
        button_layout.addWidget(self.excel_button)

        self.html_button = create_button("Export as HTML", "ExportButton", width=150, action_func=self.export_html)
        button_layout.addWidget(self.html_button)

        self.layout.addLayout(button_layout)

        # Spacer to push buttons and label upwards
        self.layout.addSpacerItem(spacer_item(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(self.layout)

    def export_csv(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save CSV", self.default_export_dir, "CSV Files (*.csv)")
        if filepath:
            export_to_csv(self.data, filepath)

    def export_excel(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Excel", self.default_export_dir, "Excel Files (*.xlsx)")
        if filepath:
            generate_basic_excel_report(self.data, filepath)

    def export_html(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save HTML", self.default_export_dir, "HTML Files (*.html)")
        if filepath:
            export_to_html(self.data, filepath)
