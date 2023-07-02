#!/usr/bin/python
try:
    import os
    import shiboken6
    from PySide6 import QtWidgets
    from PySide6.QtCore import QDate
    import ui
except ModuleNotFoundError as e:
    print("imports failed, see error")
    print(e)
    quit()


class SolventGUI(QtWidgets.QWidget):
    # im writing this after fialing to take a nap. if you want
    def __init__(self):  # cleaner looking code, im sorry.
        super().__init__()
        self.ui = ui.Ui_Main()
        self.ui.setupUi(self)

        self.refreshingCustomers(False)
        self.ui.customerRefreshButton.clicked.connect(
            lambda: self.refreshingCustomers()
        )
        self.ui.searchBar.returnPressed.connect(lambda: self.refreshingCustomers())
        self.ui.customerSelection.activated.connect(lambda: self.updateCreator())
        self.ui.creationButton.clicked.connect(lambda: self.createCustomerFile())

    def refreshingCustomers(self, subs=True):
        if subs:
            for button in self.custbutts:
                self.CButtonframes.removeWidget(button)
                shiboken6.delete(button)
            shiboken6.delete(self.CButtonframes)
            self.ui.customerSelection.clear()  # yes this is all stolen from Javier
            self.ui.alertCustomer.clear()
            del self.CButtonframes

        self.CButtonframes = QtWidgets.QVBoxLayout(self.ui.customerArea)
        self.CButtonframes.setContentsMargins(0, 0, 0, 0)
        self.custbutts = []

        custlist = os.listdir("./customers/")
        self.ui.customerLabel.setText(f"{len(custlist)} Customers")
        self.ui.customerSelection.addItem("New")
        self.ui.customerSelection.setCurrentIndex(0)
        self.ui.customerSelection.addItems(custlist)
        self.ui.alertCustomer.addItems(custlist)
        for cust in custlist:
            skip = False
            if not os.path.isfile("./customers/" + cust):
                continue

            if self.ui.searchBar.text() != "":
                searches = self.ui.searchBar.text().split(",")
                data = open("./customers/" + cust, "r")
                metadata = data.read().lower()
                data.close()
                print("reading from: " + cust)
                print(searches)
                for search in searches:
                    search = search.strip().lower()
                    if search not in metadata and search not in cust.lower():
                        skip = True
            if skip:
                continue
            self.custbutton = QtWidgets.QToolButton(text=cust)
            self.custbutton.clicked.connect(lambda _=False, d=cust: self.updateText(d))
            self.custbutts.append(self.custbutton)
            self.CButtonframes.addWidget(self.custbutton)
        # if len(self.custbutts) < 12:  # max height is 291
        height = int(700 / (len(self.custbutts) + 0.1) - 10)
        height = 30 if height < 30 else height
        for i in range(0, len(self.custbutts)):
            self.custbutts[i].setFixedSize(250, height)

    def updateText(self, file):
        customerfile = open("./customers/" + file, "r")
        self.ui.informationBrowser.setText(customerfile.read())
        customerfile.close()

    def updateCreator(self):
        if self.ui.customerSelection.currentText() == "New":
            self.ui.firstNameEnter.clear()
            self.ui.lastNameEnter.clear()
            self.ui.brandEnter.clear()
            self.ui.itemDetailEnter.clear()
            self.ui.contactEnter.clear()
            self.ui.dateEdit.clear()
            self.ui.extraDetailEnter.clear()
        else:
            oldfile = open("./customers/" + self.ui.customerSelection.currentText())
            data = oldfile.readlines()
            oldfile.close()
            self.ui.firstNameEnter.setText(data.pop(0).split(":")[1].strip())
            self.ui.lastNameEnter.setText(data.pop(0).split(":")[1].strip())
            self.ui.brandEnter.setText(data.pop(0).split(":")[1].strip())
            self.ui.itemDetailEnter.setText(data.pop(0).split(":")[1].strip())
            self.ui.contactEnter.setText(data.pop(0).split(":")[1].strip())

            self.ui.dateEdit.setDate(
                QDate.fromString(data.pop(0).split(":")[1].strip(), "MM/dd/yyyy")
            )
            data.pop(0)
            lines = ""
            for line in data:
                lines = lines + line
            self.ui.extraDetailEnter.setPlainText(lines)

    def createCustomerFile(self):
        failstate = False
        if self.ui.customerSelection.currentText() == "New":
            name = self.ui.firstNameEnter.text() + " " + self.ui.lastNameEnter.text()
            if name == " " or name == "required required":
                self.ui.firstNameEnter.setText("required")
                self.ui.lastNameEnter.setText("required")
                failstate = True
            if (
                self.ui.brandEnter.text() == ""
                or self.ui.brandEnter.text() == "required"
            ):
                self.ui.brandEnter.setText("required")
                failstate = True
            if failstate:
                return
            filename = name + " | " + self.ui.brandEnter.text() + ".txt"
            newfile = open(
                "./customers/" + filename, "w"
            )
        else:
            filename = self.ui.customerSelection.currentText()
            newfile = open(
                "./customers/" + self.ui.customerSelection.currentText(), "w"
            )
        newfile.write("First Name: " + self.ui.firstNameEnter.text())
        newfile.write("\nLast Name: " + self.ui.lastNameEnter.text())
        newfile.write("\nItem: " + self.ui.brandEnter.text())
        newfile.write("\nItem Details: " + self.ui.itemDetailEnter.text())
        newfile.write("\nContact Information: " + self.ui.contactEnter.text())
        newfile.write("\nBirthday: " + self.ui.dateEdit.text())
        newfile.write("\nExtra Details:\n" + self.ui.extraDetailEnter.toPlainText())
        newfile.close()
        self.refreshingCustomers()
        self.ui.customerSelection.setCurrentText(filename)


app = QtWidgets.QApplication()
widget = SolventGUI()


widget.show()
app.exec()
