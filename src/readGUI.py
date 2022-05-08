import subprocess
from PyQt5.Qt import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QComboBox
from PyQt5.QtGui import QPalette
import os
from fhirclient import server
from fhirclient import client
import fhirclient.server as fhir_server
from pdfminer.high_level import extract_text
from time import time


class ReadGUI(QWidget):
    def __init__(self):
        super().__init__()
        # Buttons & combobox widgets
        view_button = QPushButton('View PDF')
        upload_button = QPushButton('Upload To EHR')
        combo = QComboBox()
        patients = [f'PatientId: {str(patientId)}, DoctorId: {str(doctorId)}' for patientId, doctorId in
                    Read().get_lab_results().keys()]
        combo.addItems(patients)
        combo.activated[str].connect(Read.on_combobox_changed)

        # More setup
        layout = QVBoxLayout()

        # Add widgets to GUI
        layout.addWidget(view_button)
        layout.addWidget(upload_button)
        layout.addWidget(combo)

        self.setLayout(layout)
        view_button.clicked.connect(Read.on_view_PDF_button_clicked)
        upload_button.clicked.connect(Read.on_upload_to_EHR_button_clicked)
        #self.show()


class Read:
    lab_results = dict()  # (doctorID, patientID) --> PDF file name
    file_path = ""
    current_selected_patient = ""
    patient_Id = ""
    doctor_Id = ""

    def on_files_received(self, event):
        self.write_to_lab_results(event.src_path)

    def write_to_lab_results(self, file_path):
        if '.txt' in file_path:
            self.patient_Id, self.doctor_Id = self.parse_id_file(file_path)
        elif '.pdf' in file_path:
            self.file_path = file_path
        if (self.patient_Id != "" and '.pdf' in file_path) or (self.file_path != "" and '.txt' in file_path):
            print(f'Received patientID {self.patient_Id} lab results!')
            # We have received both id file and PDF file
            file_name = file_path.split('/')[-1]
            self.lab_results[(self.patient_Id, self.doctor_Id)] = file_name
            # Reset our saved ids and file path, so they can be used for later results
            self.patient_Id = self.doctor_Id = -1
            file_path = ""
            reader = ReadGUI()
            reader.show()

    def parse_id_file(self, file_path):
        patientId = doctorId = -1
        print(file_path)
        with open(file_path) as f:
            lines = f.readlines()  # list containing lines of file
            for line in lines:
                id = line.rstrip('\n').split(' : ')[-1]
                if 'patient' in line:
                    patientId = id
                elif 'doctor' in line:
                    doctorId = id
            return patientId, doctorId

    def on_view_PDF_button_clicked(self):
        file_name = self.lab_results[self.current_selected_patient]
        # TODO: Fix this file pathing
        # cwd = os.getcwd()
        # path_to_PDF = cwd + "..\\labFiles\\" + file_name
        path = r'..\labFiles\test_pdf1.pdf'
        subprocess.Popen([path], shell=True)

    def on_upload_to_EHR_button_clicked(self):
        self.parse_PDF_data()

    def parse_PDF_data(self):
        # TODO: Fix this file pathing
        # file_name = self.lab_results[self.current_selected_patient]
        # cwd = os.getcwd()
        # path_to_PDF = cwd + "..\\labFiles\\" + file_name
        path = r'..\labFiles\test_pdf1.pdf'
        data = extract_text(path)
        # progressBar = QProgressBar()
        # progressBar.setGeometry(0, 0, 300, 100)
        # progressBar.setMaximum(100)
        # progressBar.show()
        # count = 0
        # while count < 100:
        #     count += 1
        #     time.sleep(1)
        #     progressBar.setValue(count)
        print(data)

    def upload_to_EHR(self):
        settings = {
            'app_id': 'my_web_app',
            'api_base': 'http://wildfhir4.aegis.net/fhir4-0-1'
        }
        smart_client = client.FHIRClient(settings=settings)
        # smart_server = server.FHIRServer(smart_client, base_uri='http://wildfhir4.aegis.net/fhir4-0-1')
        #
        # smart_server.pos
        #
        #
        # patient = p.Patient.read('f001', smart.server)
        # print('Birth Date', patient.birthDate.isostring)
        # print('Patient Name', smart.human_name(patient.name[0]))

    def on_combobox_changed(self, text):
        patientId = doctorId = ''
        ids = text.split(', ')
        for id in ids:
            if 'Patient' in id:
                patientId = id.split(': ')[-1]
            elif 'Doctor' in id:
                doctorId = id.split(': ')[-1]
        self.current_selected_patient = (patientId, doctorId)

    def get_lab_results(self):
        return self.lab_results
