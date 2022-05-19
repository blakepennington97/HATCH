from readGUI import Read
from labMonitor import Watchdog
from fhirclient import client
import fhirclient.models.patient as patient
import fhirclient.models.humanname as humanname
import fhirclient.models.appointment as appointment
import fhirclient.models.age as age
import sys
# library for GUI
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import gui_helper as gui_helper
import json
import fhirclient.models.medication as medication
from functools import partial

settings = {
    'app_id': 'my_web_app',
    'api_base': 'http://wildfhir4.aegis.net/fhir4-0-1'
}

smart = client.FHIRClient(settings=settings)

# -------------- pull patient information from EHR --------------------
# TODO: initialize patient and physician data
patient_id = 'pat1'
physician_id = ''
# TODO: do you really need physician id to fetch patient data?

# get patient from EHR
patient = patient.Patient.read(patient_id, smart.server)

# patient information
first_name = None
last_name = None
birth_date = None
age = None
gender = None
telecom = None
# medication = medication.Medication.where(struct={"recipient": "Patient/" + patient_id})
# print(type(medication))

# check None
if patient is not None:
    if patient.name is not None and patient.name[0] is not None and patient.name[0].given is not None:
        first_name = ""
        for name in patient.name[0].given:
            first_name += name
            first_name += " "
        first_name.strip()

    if patient.name is not None and patient.name[0] is not None and patient.name[0].family is not None:
        last_name = patient.name[0].family

    if patient.birthDate is not None:
        birth_date = patient.birthDate.isostring

    if birth_date is not None:
        age = gui_helper.calculate_age(patient.birthDate)

    if gender is not None:
        gender = patient.gender

    if patient.contact is not None and patient.contact[0] is not None and patient.contact[0].telecom is not None and \
            patient.contact[0].telecom[0] is not None and patient.contact[0].telecom[0].value is not None:
        telecom = patient.contact[0].telecom[0].value

    # TODO: display address
    # address = patient.address[0].line[0] if patient.address[0].line[0] is not None else ""
    # address += ",\a" + patient.address[0].postalCode if patient.address[0].postalCode is not None else "" + "\n"
    # address += "\n" + patient.address[0].state if patient.address[0].state is not None else ""
    # address += ",\a" + patient.address[0].city if patient.address[0].city is not None else ""
    # address += ",\a" + patient.address[0].country if patient.address[0].country is not None else ""

print(first_name, last_name, birth_date, age, gender, telecom)


# TODO: GUI generate a list of test that the physician can select from

# -------------- create GUI --------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.tests_ordered = []
        self.setWindowTitle("Start A New Order")
        layout = QVBoxLayout()

        # TODO: null checker
        patient_info = {"Patient ID: ": patient_id if patient_id is not None else "None",
                        "First Name: ": first_name if first_name is not None else "None",
                        "Last Name: ": last_name if last_name is not None else "None",
                        "Birth Date: ": birth_date if birth_date is not None else "None",
                        "Age: ": age if age is not None else "None",
                        "Gender: ": gender if gender is not None else "None",
                        "Contact: ": telecom if telecom is not None else "None"
                        # TODO: add medication
                        # "Medications": medication if medication is not None else "None"
                        }
        # "Marital Status": patient.maritalStatus.coding[0].code,
        # "Address":     address}
        # TODO: include current medication
        # TODO: doctor is able to choose additional information to display
        for key, val in patient_info.items():
            horizontal_layout = QHBoxLayout()
            horizontal_layout.addWidget(QLabel(key))
            horizontal_layout.addWidget(QLabel(val))
            layout.addLayout(horizontal_layout)

        # add checkable dropdown box for tests to order
        # TODO: implement searching function
        self.combo = gui_helper.CheckableComboBox()

        tests_file_loc = "../help_data/tests_to_order.txt"
        tests = gui_helper.get_tests(tests_file_loc)

        for i in range(len(tests)):
            self.combo.addItem('{0}'.format(tests[i]))
            self.combo.set_item_checked(i, False)
            self.combo.setEditable(True)
            self.combo.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
            self.combo.lineEdit().setAlignment(QtCore.Qt.AlignVCenter)

        self.prompt_select = QLabel("\nPlease select tests to order")
        self.prompt_select.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.prompt_select)
        layout.addWidget(self.combo)

        self.order_status_title = QLabel("List of Tests Selected")
        self.order_status_title.setAlignment(QtCore.Qt.AlignCenter)
        self.order_status_title.setVisible(False)
        layout.addWidget(self.order_status_title)

        self.order_info = QLabel("")
        self.order_info.setVisible(False)
        layout.addWidget(self.order_info)

        self.order_status = QLabel("")
        self.order_status.setAlignment(QtCore.Qt.AlignCenter)
        self.order_status.setVisible(False)
        layout.addWidget(self.order_status)

        self.button_generate = QPushButton("Order")
        self.button_generate.clicked.connect(self.generate_button_is_clicked)
        layout.addWidget(self.button_generate)
        #
        # self.new_order_button = QPushButton("New Order")
        # self.new_order_button.clicked.connect(self.new_order_button_is_clicked)
        # self.new_order_button.setVisible(False)
        # layout.addWidget(self.new_order_button)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def generate_button_is_clicked(self):
        dictionary = {'testsOrdered': self.combo.tests_ordered}
        json_string = json.dumps(dictionary, indent=4)
        file_name = "../orders/" + first_name + last_name + "_tests_ordered.txt"
        self.print_tests(json_string)
        f = open(file_name, "w")
        f.write(json_string)
        f.close()

        self.order_status_title.setVisible(True)
        self.order_info.setText(self.combo.tests_ordered_info)
        self.order_info.setVisible(True)

        if self.button_generate.text() == "Order":
            self.order_status.setVisible(True)
            self.order_status.setText("Please confirm tests ordered")
            self.button_generate.setText("Confirmed")
        elif self.button_generate.text() == "Confirmed":
            self.button_generate.setText("New Order")
            self.order_status_title.setText("List of Tests Ordered")
            self.order_status.setText("Tests ordered!")
            # self.new_order_button.setVisible(True)
        else:
            self.restart()
            self.close()

    def restart(self):

        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        QApplication.quit()
        print(status)

    def print_tests(self, json_string):
        for test in self.combo.tests_ordered:
            print(test)
        print(json_string)


# class ConfirmPage(MainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Confirm Page")


#     layout = QVBoxLayout()
#
#     for test in test_ordered:
#         layout.addWidget(QLabel(str(test)))
#     layout.addWidget(QLabel("Are you sure that you want to generate the info?"))
#     button_yes = QPushButton("Yes")
#     button_no = QPushButton("No")
#     horizontal_layout = QHBoxLayout(button_yes, button_no)
#     layout.addLayout(horizontal_layout)
#     widget = QWidget()
#     widget.setLayout(layout)


# class MainPage(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("BurnFhirBurn")
#
#         button_generate.clicked.connect(self.generate_button_is_clicked)
#         layout = QVBoxLayout()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
    Watchdog().Start() # begin looking for new PDFs
    sys.exit(app.exec_())
