import qpageview

from PyQt5.Qt import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPalette


class Read:
    file_path = ""

    def on_PDF_received(self, event):
        print(f'Received PDF! --> {event.src_path}')
        self.DisplayGUI(event.src_path)

    def on_view_PDF_button_clicked(self):
        v = qpageview.View()
        v.show()
        v.loadPdf(self.PDF_file_path)

    def on_upload_to_EHR_button_clicked(self):
        # do something
        pass

    def DisplayGUI(self, file_path):
        self.file_path = file_path
        # Create GUI
        app = QApplication(["Lab Results"])
        app.setStyle('Fusion')
        palette = QPalette()
        palette.setColor(QPalette.ButtonText, Qt.red)
        app.setPalette(palette)
        view_button = QPushButton('View PDF')
        upload_button = QPushButton('Upload To EHR')
        window = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(view_button)
        layout.addWidget(upload_button)
        window.setLayout(layout)
        view_button.clicked.connect(self.on_view_PDF_button_clicked)
        upload_button.clicked.connect(self.on_upload_to_EHR_button_clicked)
        window.show()
        app.exec()
