from datetime import date
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt


def calculate_age(birthdate):
    today = date.today()
    if birthdate is None:
        return "None"
    else:
        birthdate = birthdate.date if birthdate.date is not None else "None"
        if birthdate is None:
            return "None"
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return str(age)


def get_tests(file_name):
    tests = []
    with open(file_name) as my_file:
        for line in my_file:
            tests.append(line)
    return tests


class CheckableComboBox(QComboBox):
    tests_ordered = []

    def __init__(self):
        super().__init__()
        self._changed = False # track any change that has been made
        # manually handle when the dropdown open and close
        self.view().pressed.connect(self.handle_item_pressed)

    # check box indicator
    def set_item_checked(self, index, checked=False):
        # combobox model first
        row = self.model().item(index, self.modelColumn())
        if checked:
            row.setCheckState(Qt.Checked)

        else:
            row.setCheckState(Qt.Unchecked)



    # handle when the menu open and close
    def handle_item_pressed(self, index):
        row = self.model().itemFromIndex(index)
        if row.checkState() == Qt.Checked:
            row.setCheckState(Qt.Unchecked)
            self.tests_ordered.remove(row.text())
        else:
            row.setCheckState(Qt.Checked)
            self.tests_ordered.append(row.text())

        self._changed = True

    # prevent menu from automatically closing
    def hide_popup(self):
        if not self._changed:
            super().hidePopup()
        self._changed = False

    def item_checked(self, index):
        item = self.model().item(index, self.modelColumn())
        return item.checkState() == Qt.Checked






