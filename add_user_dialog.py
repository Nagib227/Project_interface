# ADD_user_dialog
from AddUser_UI import Ui_Dialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog, QListWidgetItem


class User_Dialog(QDialog, Ui_Dialog):
    def __init__(self, move, parent=None, change=[]):
        super(User_Dialog, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)

        for i in self.parent.coaches():
            self.comboBox.addItem(i[0])
        for i in self.parent.days():
            self.comboBox_3.addItem(i[0])
        for i in self.parent.times():
            self.comboBox_4.addItem(i[0])
        self.pushButton_3.clicked.connect(self.add_record)
        self.pushButton_2.clicked.connect(self.del_record)
        if move == 'ADD':
            self.pushButton.setText("Добавить")
            self.pushButton.clicked.connect(self.parent.closeAddUser)
        elif move == 'change':
            self.line_name.setText(change[1])
            self.line_data.setText(change[2])
            self.comboBox.setCurrentIndex(change[4])
            self.pushButton.setText("Сохранить")
            self.pushButton.clicked.connect(self.parent.close_change_user)#######
            for i in sorted(self.parent.records(change[0], self.comboBox.currentText())):
                self.listWidget.addItem(f"{i[0]} {i[1]}")
            self.change_records_comboBox()

    def del_record(self):
        items = [self.listWidget.item(i).text() for i in range(self.listWidget.count())]
        if not self.comboBox_2.currentText() in items:
            return None
        self.listWidget.takeItem(items.index(self.comboBox_2.currentText()))
        self.change_records_comboBox()

    def change_records_comboBox(self):
        self.comboBox_2.clear()
        items = [self.listWidget.item(i).text() for i in range(self.listWidget.count())]
        for i in items:
            self.comboBox_2.addItem(i)

    def add_record(self):
        items = [self.listWidget.item(i).text() for i in range(self.listWidget.count())]
        text = f"{self.comboBox_3.currentText()} {self.comboBox_4.currentText()}"
        if text in items:
            return None
        self.listWidget.addItem(text)
        self.change_records_comboBox()
        

    def returnVal(self):
        return [self.line_name.text(), self.line_data.text(),
                [self.listWidget.item(i).text() for i in range(self.listWidget.count())],
                self.comboBox.currentText()]

    def closeEvent(self, event):
        self.parent.show()
