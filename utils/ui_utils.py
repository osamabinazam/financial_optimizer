from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QRectF, Qt, QPropertyAnimation, QSequentialAnimationGroup, QPauseAnimation, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath
from PyQt5.QtWidgets import QMessageBox, QComboBox, QPushButton, QLabel, QSpacerItem, QSizePolicy, QTableWidget, \
    QHeaderView, QVBoxLayout, QFrame


def display_message_box(parent, title, message):
    """
    Displays a message box with the specified title and message.
    :param parent:  The parent widget for the message box.
    :param title:  The title of the message box.
    :param message:  The message to display.
    :return:
    """
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()


def create_combo_box(items=None, object_name=None, current_index=0):
    """
    Creates a QComboBox with the specified items and object name.

    :param items: List of items to add to the combo box.
    :param object_name: The object name for the combo box.
    :param current_index: The default selected index.
    :return: QComboBox instance.
    """
    combo_box = QComboBox()
    if object_name:
        combo_box.setObjectName(object_name)
    if items:
        combo_box.addItems(items)
    combo_box.setCurrentIndex(current_index)
    return combo_box


def create_button(text, object_name=None, width=100, action_func=None):
    """
    Creates a QPushButton with the specified text, object name, and width.

    :param action_func: The function to connect to the button's clicked signal.
    :param text: The text to display on the button.
    :param object_name: The object name for the button.
    :param width: The width of the button.
    :return: QPushButton instance.
    """
    if not text:
        raise ValueError("Button text cannot be empty.")

    button = QPushButton(text)
    if object_name:
        button.setObjectName(object_name)
    if action_func:
        button.clicked.connect(action_func)
    if width:
        button.setFixedWidth(width)
    return button


def create_label(text, object_name=None):
    """
    Creates a QLabel with the specified text and object name.
    :param text: The text to display on the label.
    :param object_name: The object name for the label.
    :return: QLabel instance.
    """
    label = QLabel(text)
    if object_name:
        label.setObjectName(object_name)
    return label


def spacer_item(width, height, horizontal_policy=QSizePolicy.Minimum, vertical_policy=QSizePolicy.Minimum):
    """
    Creates a spacer item with the specified width and height.
    :param vertical_policy:
    :param horizontal_policy:
    :param width: The width of the spacer item.
    :param height: The height of the spacer item.
    :return: QSpacerItem instance.
    """
    return QSpacerItem(width, height, horizontal_policy, vertical_policy)


def create_rounded_pixmap(pixmap, width, height, radius):

    """
    
    :param pixmap:
    :param width:
    :param height:
    :param radius:
    :return:
    """
    rounded_pixmap = QPixmap(width, height)
    rounded_pixmap.fill(Qt.transparent)

    painter = QPainter(rounded_pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.SmoothPixmapTransform)

    # Create a rounded rectangle path
    path = QPainterPath()
    path.addRoundedRect(QRectF(0, 0, width, height), radius, radius)  # Use QRectF for floating-point precision

    # Clip the painter to the rounded path
    painter.setClipPath(path)

    # Draw the original pixmap into the rounded path
    painter.drawPixmap(0, 0, width, height, pixmap)

    painter.end()
    return rounded_pixmap


def create_table(object_name=None, column_count=0, header_labels=None):
    table_widget = QTableWidget()
    if object_name:
        table_widget.setObjectName(object_name)
    if column_count:
        table_widget.setColumnCount(column_count)

    if header_labels:
        table_widget.setHorizontalHeaderLabels(header_labels)

    table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    return table_widget


# SnackBar class for showing messages


class Snackbar(QFrame):
    def __init__(self, parent, message, error=False, duration=3000):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.ToolTip)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Styling based on the message type
        if error:
            bg_color = "rgba(255, 0, 0, 200)"  # Red for errors
        else:
            bg_color = "rgba(50, 50, 50, 200)"  # Default dark for regular messages

        label = QLabel(message)
        label.setStyleSheet("color: white; padding: 10px;")
        self.setStyleSheet(f"background-color: {bg_color}; border-radius: 5px;")
        layout.addWidget(label)

        # Snackbar dimensions
        snackbar_width = 300
        snackbar_height = 50
        margin = 20  # Distance from the edges

        # Calculate position relative to the parent widget
        parent_rect = parent.rect()
        global_pos = parent.mapToGlobal(parent_rect.bottomRight())

        x = global_pos.x() - snackbar_width - margin
        y = global_pos.y() - snackbar_height - margin

        # Convert global coordinates back to parent's local coordinates
        local_pos = parent.mapFromGlobal(QPoint(x, y))

        # Apply geometry to position the snackbar
        self.setGeometry(local_pos.x(), local_pos.y(), snackbar_width, snackbar_height)

        print(f"Snackbar Geometry: {self.geometry()}")  # Debugging line

        # Animation for showing and hiding the snackbar
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)

        self.show_animation = QSequentialAnimationGroup()
        self.show_animation.addAnimation(self.animation)
        self.show_animation.addAnimation(QPauseAnimation(duration))
        self.show_animation.finished.connect(self.close)

    def show(self):
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.show_animation.start()
        super().show()
        print("Snackbar is being shown")  # Debugging line


# Utility function to show snackbar in any widget
def display_snackbar(parent, message, error=False):
    snackbar = Snackbar(parent, message, error)
    snackbar.show()
    print(f"Snackbar displayed: {snackbar.isVisible()}")  # Debugging line



class QToaster(QtWidgets.QFrame):
    closed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(QToaster, self).__init__(parent)
        QtWidgets.QHBoxLayout(self)

        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum,
                           QtWidgets.QSizePolicy.Maximum)

        self.setStyleSheet('''
            QToaster {
                border-radius: 10px; 
                background-color: white;
            }
        ''')

        self.timer = QtCore.QTimer(singleShot=True, timeout=self.hide)

        if self.parent():
            self.opacityEffect = QtWidgets.QGraphicsOpacityEffect()
            self.setGraphicsEffect(self.opacityEffect)
            self.opacityAni = QtCore.QPropertyAnimation(self.opacityEffect, b'opacity')
            self.parent().installEventFilter(self)
        else:
            self.opacityAni = QtCore.QPropertyAnimation(self, b'windowOpacity')
        self.opacityAni.setStartValue(0.)
        self.opacityAni.setEndValue(1.)
        self.opacityAni.setDuration(100)
        self.opacityAni.finished.connect(self.checkClosed)

        self.corner = QtCore.Qt.TopRightCorner
        self.margin = 10

    def checkClosed(self):
        if self.opacityAni.direction() == self.opacityAni.Backward:
            self.close()

    def restore(self):
        self.timer.stop()
        self.opacityAni.stop()
        if self.parent():
            self.opacityEffect.setOpacity(1)
        else:
            self.setWindowOpacity(1)

    def hide(self):
        self.opacityAni.setDirection(self.opacityAni.Backward)
        self.opacityAni.setDuration(500)
        self.opacityAni.start()

    def eventFilter(self, source, event):
        if source == self.parent() and event.type() == QtCore.QEvent.Resize:
            self.opacityAni.stop()
            parentRect = self.parent().rect()
            geo = self.geometry()
            geo.moveTopRight(
                parentRect.topRight() + QtCore.QPoint(-self.margin, self.margin))
            self.setGeometry(geo)
            self.restore()
            self.timer.start()
        return super(QToaster, self).eventFilter(source, event)

    def enterEvent(self, event):
        self.restore()

    def leaveEvent(self, event):
        self.timer.start()

    def closeEvent(self, event):
        self.deleteLater()

    def resizeEvent(self, event):
        super(QToaster, self).resizeEvent(event)
        if not self.parent():
            path = QtGui.QPainterPath()
            path.addRoundedRect(QtCore.QRectF(self.rect()).translated(-.5, -.5), 4, 4)
            self.setMask(QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon()))
        else:
            self.clearMask()

    @staticmethod
    def showMessage(parent, message, is_error=False, margin=10, closable=True, timeout=5000):
        if parent:
            parent = parent.window()

        self = QToaster(parent)
        self.timer.setInterval(timeout)

        # Set the message label with the appropriate text color
        self.label = QtWidgets.QLabel(message)
        if is_error:
            self.label.setStyleSheet('color: red;')
        else:
            self.label.setStyleSheet('color: green;')
        self.layout().addWidget(self.label)

        if closable:
            self.closeButton = QtWidgets.QToolButton()
            self.layout().addWidget(self.closeButton)
            closeIcon = self.style().standardIcon(QtWidgets.QStyle.SP_TitleBarCloseButton)
            self.closeButton.setIcon(closeIcon)
            self.closeButton.setAutoRaise(True)
            self.closeButton.clicked.connect(self.close)

        self.adjustSize()

        geo = self.geometry()
        geo.moveTopRight(parent.rect().topRight() + QtCore.QPoint(-margin, margin))

        self.setGeometry(geo)
        self.show()
        self.opacityAni.start()

        return self


def display_toaster(parent, message, is_error=False, duration=5000, closable=True):
    QToaster.showMessage(parent, message, is_error=is_error, closable=closable, timeout=duration)
