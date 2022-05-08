import sys
from labMonitor import Consumer
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow, QWidget, QApplication, QComboBox, QPushButton
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import Qt
from main import Main, WriteWindow
from readGUI import ReadGUI


class Program(QMainWindow):
    def __init__(self):
        super().__init__()
        self.writeWindow = WriteWindow()

        l = QVBoxLayout()

        self.start_new_order_button = QPushButton("Start New Order")
        self.view_orders_button = QPushButton("View Orders")
        self.start_new_order_button.clicked.connect(self.toggle_write_window)
        self.view_orders_button.clicked.connect(self.toggle_read_window)

        l.addWidget(self.start_new_order_button)
        l.addWidget(self.view_orders_button)

        w = QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)

    def toggle_write_window(self, checked):
        if self.writeWindow.isVisible():
            self.writeWindow.hide()
        else:
            self.writeWindow.show()

    def toggle_read_window(self, checked):
        Consumer().Start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Program()
    w.show()
    app.exec()
