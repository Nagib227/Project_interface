# ADD_time_dialog
from AddTime_UI import Ui_Dialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog


class Time_Dialog(QDialog, Ui_Dialog):
    def __init__(self, move, parent=None, change=[]):
        super(Time_Dialog, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        
        if move == 'ADD':
            self.pushButton.setText("Добавить")
            self.pushButton.clicked.connect(self.parent.closeAddTime)
        elif move == 'change':
            self.line_name.setText(change[0])
            self.pushButton.setText("Сохранить")
            self.pushButton.clicked.connect(self.parent.close_change_time)

    def returnVal(self):
        return [self.line_name.text()]

    def closeEvent(self, event):
        self.parent.show()
