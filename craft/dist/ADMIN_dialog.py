# ADD_ADMIN_dialog
from ADMIN_UI import Ui_Dialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog


class ADMIN_Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(ADMIN_Dialog, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.pushButton.clicked.connect(self.parent.closeADMIN)

    def returnVal(self):
        return [self.line_pass.text()]

    def closeEvent(self, event):
        self.parent.show()
