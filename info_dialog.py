from aboutProgram_UI import Ui_Dialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog, QListWidgetItem


class Info_Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Info_Dialog, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        with open("info.txt", "r", encoding="utf8") as f:
            for i in f.read().split("/n"):
                self.textBrowser.append(i)

    def closeEvent(self, event):
        self.parent.show()
