from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QLineEdit, QDesktopWidget
from PyQt5.QtCore import Qt
from utils.ui_utils import  create_label, create_button, spacer_item


class FilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Apply Filters")

        # Remove fixed size, allow the dialog to resize dynamically
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFixedSize(300, 300)

        # UI Elements
        self.layout = None
        self.label = None
        self.apply_button = None
        self.cancel_button = None

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # Label to indicate filters
        self.label = create_label("Apply Filters", "FilterLabel")
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)

        # Filter inputs (e.g., date range, symbol, etc.)
        symbol_filter = QLineEdit(self)
        symbol_filter.setPlaceholderText("Filter by Symbol")
        symbol_filter.setObjectName("FilterInput")
        self.layout.addWidget(symbol_filter)

        date_filter = QLineEdit(self)
        date_filter.setPlaceholderText("Filter by Date (YYYY-MM-DD)")
        date_filter.setObjectName("FilterInput")
        self.layout.addWidget(date_filter)

        # Button layout for Apply and Cancel
        button_layout = QHBoxLayout()

        self.apply_button = create_button( "Apply", "FilterButton")
        self.apply_button.clicked.connect(lambda: self.apply_filters(symbol_filter.text(), date_filter.text()))
        button_layout.addWidget(self.apply_button)

        self.cancel_button = create_button("Cancel", "FilterButton", action_func=self.reject)
        button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(button_layout)

        # Spacer to push buttons and label upwards
        self.layout.addSpacerItem(spacer_item(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(self.layout)

    def apply_filters(self, symbol, date):
        # Here you would add the actual logic to apply the filters to the data.
        # For now, we'll just print the filters and close the dialog.
        print(f"Applying filters - Symbol: {symbol}, Date: {date}")
        self.accept()
