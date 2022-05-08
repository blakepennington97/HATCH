from readGUI import Read
from labMonitor import Consumer
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
        telecom = patient.contact[0].telecome[0].value

    # TODO: display address
    # address = patient.address[0].line[0] if patient.address[0].line[0] is not None else ""
    # address += ",\a" + patient.address[0].postalCode if patient.address[0].postalCode is not None else "" + "\n"
    # address += "\n" + patient.address[0].state if patient.address[0].state is not None else ""
    # address += ",\a" + patient.address[0].city if patient.address[0].city is not None else ""
    # address += ",\a" + patient.address[0].country if patient.address[0].country is not None else ""

print(first_name, last_name, birth_date, age, gender, telecom)


# TODO: GUI should have a list of the patient's data
# assume that right now all the patient data is pulled
# TODO: GUI generate a list of test that the physician can select from

# -------------- create GUI --------------------
class WriteWindow(QWidget):
    def __init__(self):
        super().__init__()
        #self.tests_ordered = []
        self.setWindowTitle("Start A New Order")
        layout = QVBoxLayout()

        # TODO: null checker
        patient_info = {"Patient ID": patient_id if patient_id is not None else "None",
                        "First Name": first_name if first_name is not None else "None",
                        "Last Name": last_name if last_name is not None else "None",
                        "Birth Date": birth_date if birth_date is not None else "None",
                        "Age": age if age is not None else "None",
                        "Gender": gender if gender is not None else "None",
                        "Contact": telecom if telecom is not None else "None"
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

        layout.addWidget(self.combo)
        button_generate = QPushButton("Generate")
        button_generate.clicked.connect(self.generate_button_is_clicked)
        # self.dialog = ConfirmPage()
        layout.addWidget(button_generate)

        self.setLayout(layout)


    def generate_button_is_clicked(self):
        for test in self.combo.tests_ordered:
            print(test)


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

class Main:
    def new_order_button_clicked(self):
        write_window = WriteWindow()



    def view_orders_button_clicked(self):
        # Read
        Consumer().Start()  # begin looking for new PDFs







# window = QWidget()
# layout = QVBoxLayout()
# layout.addWidget(QPushButton('Get Patient Data from EHR'))
# TODO: add logic for getting patient data


# layout.addWidget(button_generateData)
# window.setLayout(layout)
# window.show()


# TODO: double check information with the physician before sending the file


#
# self.active = None
# """ Whether this patient's record is in active use.
# Type `bool`. """
#
# self.address = None
# """ Addresses for the individual.
# List of `Address` items (represented as `dict` in JSON). """
#
# self.animal = None
# """ This patient is known to be an animal (non-human).
# Type `PatientAnimal` (represented as `dict` in JSON). """
#
# self.birthDate = None
# """ The date of birth for the individual.
# Type `FHIRDate` (represented as `str` in JSON). """
#
# self.communication = None
# """ A list of Languages which may be used to communicate with the
# patient about his or her health.
# List of `PatientCommunication` items (represented as `dict` in JSON). """
#
# self.contact = None
# """ A contact party (e.g. guardian, partner, friend) for the patient.
# List of `PatientContact` items (represented as `dict` in JSON). """
#
# self.deceasedBoolean = None
# """ Indicates if the individual is deceased or not.
# Type `bool`. """
#
# self.deceasedDateTime = None
# """ Indicates if the individual is deceased or not.
# Type `FHIRDate` (represented as `str` in JSON). """
#
# self.gender = None
# """ male | female | other | unknown.
# Type `str`. """
#
# self.generalPractitioner = None
# """ Patient's nominated primary care provider.
# List of `FHIRReference` items referencing `Organization, Practitioner` (represented as `dict` in JSON). """
#
# self.identifier = None
# """ An identifier for this patient.
# List of `Identifier` items (represented as `dict` in JSON). """
#
# self.link = None
# """ Link to another patient resource that concerns the same actual
# person.
# List of `PatientLink` items (represented as `dict` in JSON). """
#
# self.managingOrganization = None
# """ Organization that is the custodian of the patient record.
# Type `FHIRReference` referencing `Organization` (represented as `dict` in JSON). """
#
# self.maritalStatus = None
# """ Marital (civil) status of a patient.
# Type `CodeableConcept` (represented as `dict` in JSON). """
#
# self.multipleBirthBoolean = None
# """ Whether patient is part of a multiple birth.
# Type `bool`. """
#
# self.multipleBirthInteger = None
# """ Whether patient is part of a multiple birth.
# Type `int`. """
#
# self.name = None
# """ A name associated with the patient.
# List of `HumanName` items (represented as `dict` in JSON). """
#
# self.photo = None
# """ Image of the patient.
# List of `Attachment` items (represented as `dict` in JSON). """
#
# self.telecom = None
# """ A contact detail for the individual.
# List of `ContactPoint` items (represented as `dict` in JSON). """
