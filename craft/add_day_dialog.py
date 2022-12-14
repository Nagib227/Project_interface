# ADD_day_dialog
from AddDay_UI import Ui_Dialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog


class Day_Dialog(QDialog, Ui_Dialog):
    def __init__(self, move, parent=None, change=[]):
        super(Day_Dialog, self).__init__(parent)
        self.parent = parent
        
        self.setupUi(self)
        if move == 'ADD':
            self.pushButton.clicked.connect(self.parent.closeAddDay)
        elif move == 'change':
            self.line_name.setText(change[0])
            self.pushButton.setText("Сохранить")
            self.pushButton.clicked.connect(self.parent.close_change_day)

    def returnVal(self):
        return [self.line_name.text()]
    
    def closeEvent(self, event):
        self.parent.show()
