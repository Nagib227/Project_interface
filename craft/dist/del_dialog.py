import sqlite3
import sys

from ChangeDialog_UI import Ui_Dialog
from PyQt5.QtWidgets import QApplication, QAbstractItemView
from PyQt5.QtWidgets import QDialog, QTableWidgetItem


class Del_Dialog(QDialog, Ui_Dialog):
    def __init__(self, ADMIN, parent=None):
        self.ADMIN = ADMIN
        super(Del_Dialog, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.connection = sqlite3.connect("db/yand_db.db")
        self.comboBox.currentTextChanged.connect(self.changeComboBox)
        self.pushButton.setText("Удалить")
        self.pushButton.clicked.connect(self.open_del)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.select_users()

    def changeComboBox(self):
        if self.comboBox.currentText() == "Занимающиеся":
            self.select_users()
        elif self.comboBox.currentText() == "Дни недели":
            self.select_day()
        elif self.comboBox.currentText() == "Время":
            self.select_time()
        else:
            self.select_coach()

    def select_day(self):
        res = self.connection.cursor().execute(f"""SELECT * FROM daysweek
""").fetchall()
        title = ["ID", "ДЕНЬ НЕДЕЛИ"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(sorted(res, key=lambda x: x[0])):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
                self.x = i
                self.y = j
        self.tableWidget.resizeColumnsToContents()

    def select_coach(self):
        res = self.connection.cursor().execute(f"""SELECT * FROM coaches
""").fetchall()
        title = ["ID", "ИМЯ"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(sorted(res, key=lambda x: x[0])):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                if type(elem) == list:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(", ".join(elem)))
                elif elem:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(''))
                self.x = i
                self.y = j
        self.tableWidget.resizeColumnsToContents()

    def select_time(self):
        res = self.connection.cursor().execute(f"""SELECT * FROM times
""").fetchall()
        title = ["ID", "ВРЕМЯ"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(sorted(res, key=lambda x: x[0])):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                if type(elem) == list:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(", ".join(elem)))
                elif elem:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(''))
                self.x = i
                self.y = j
        self.tableWidget.resizeColumnsToContents()

    def select_users(self):
        ids = self.connection.cursor().execute("""SELECT users.id,
    daysweek.id,
    coaches.id,
    times.id
FROM
    users, coaches, join_table j, daysweek, times
WHERE
    j.user_id = users.id
AND
    j.dayweek_id = daysweek.id
AND
    j.coach_id = coaches.id
AND
    j.time_id = times.id""").fetchall()
        res = []
        for i in ids:
            use = self.connection.cursor().execute(f"""SELECT users.id,
    users.name,
    users.birthday,
    d.title,
    t.time,
    coaches.name
FROM
    users, coaches, join_table j, daysweek d, times t
WHERE
    j.user_id = users.id
AND
    users.id = {i[0]}
AND
    j.coach_id = coaches.id
AND
    coaches.id = {i[2]}
AND
    j.dayweek_id = d.id
AND
    d.id = {i[1]}
AND
    j.time_id = t.id
AND
    t.id = {i[3]}""").fetchall()
            res.append(list(use[0]))
        title = ["ID", "ИМЯ", "ДАТА РОЖДЕНИЯ", "ДЕНЬ НЕДЕЛИ", "ВРЕМЯ", "ТРЕНЕР"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(sorted(res, key=lambda x: [x[0], list(map(lambda x: x[0], self.days())).index(x[3]),
                                                           x[4]])):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                if type(elem) == list:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(", ".join(elem)))
                elif elem:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(''))
                self.x = i
                self.y = j
        self.tableWidget.resizeColumnsToContents()

    def open_del(self):
        if self.comboBox.currentText() == "Занимающиеся":
            self.open_del_user()
        elif not self.ADMIN:
            self.label.setText('Вы не ADMIN')
            return None
        elif self.comboBox.currentText() == "Дни недели":
            self.open_del_day()
        elif self.comboBox.currentText() == "Время":
            self.open_del_time()
        else:
            self.open_del_coach()

    def open_del_time(self):
        xs = []
        cells = 0
        prov = False
        for i in range(self.x + 1):
            for j in range(self.y + 1):
                if self.tableWidget.item(i, j).isSelected() and i not in xs:
                    cells += 1
                    xs.append(i)
                    prov = True
        if not prov:
            self.label.setText('Выберете ячейку')
            return None
        elif cells > 1:
            self.label.setText('Выберете одну ячейку')
            return None
        for it in self.tableWidget.selectedItems():
            x = it.row()
        change = []
        for i in range(self.y + 1):
            change.append(self.tableWidget.item(x, i).text())
        self.id = change[0]
        self.dell = change
        self.close_del_time()

    def close_del_time(self):
        self.connection.cursor().execute(f"""DELETE FROM times
WHERE id = {self.id}""")
        self.connection.cursor().execute(f"""DELETE FROM join_table
WHERE time_id = {self.id}""")
        users = self.connection.cursor().execute(f"""SELECT users.id
FROM users""").fetchall()
        for i in users:
            use = self.connection.cursor().execute(f"""SELECT user_id
FROM join_table
WHERE user_id = {i[0]}""").fetchall()
            if not use:
                self.connection.cursor().execute(f"""DELETE FROM users
WHERE id = {i[0]}""")
        self.changeComboBox()
        self.connection.commit()
        self.parent.changeTable()
        self.parent.changeComboBox()
        self.select_time()

    def open_del_coach(self):
        xs = []
        cells = 0
        prov = False
        for i in range(self.x + 1):
            for j in range(self.y + 1):
                if self.tableWidget.item(i, j).isSelected() and i not in xs:
                    cells += 1
                    xs.append(i)
                    prov = True
        if not prov:
            self.label.setText('Выберете ячейку')
            return None
        elif cells > 1:
            self.label.setText('Выберете одну ячейку')
            return None
        for it in self.tableWidget.selectedItems():
            x = it.row()
        change = []
        for i in range(self.y + 1):
            change.append(self.tableWidget.item(x, i).text())
        self.id = change[0]
        self.dell = change
        self.close_del_coach()

    def close_del_coach(self):
        self.connection.cursor().execute(f"""DELETE FROM coaches
WHERE id = {self.id}""")
        self.connection.cursor().execute(f"""DELETE FROM join_table
WHERE coach_id = {self.id}""")
        users = self.connection.cursor().execute(f"""SELECT users.id
FROM users""").fetchall()
        for i in users:
            use = self.connection.cursor().execute(f"""SELECT user_id
FROM join_table
WHERE user_id = {i[0]}""").fetchall()
            if not use:
                self.connection.cursor().execute(f"""DELETE FROM users
WHERE id = {i[0]}""")
        self.changeComboBox()
        self.connection.commit()
        self.parent.changeTable()
        self.parent.changeComboBox()

    def open_del_day(self):
        xs = []
        cells = 0
        prov = False
        for i in range(self.x + 1):
            for j in range(self.y + 1):
                if self.tableWidget.item(i, j).isSelected() and i not in xs:
                    cells += 1
                    xs.append(i)
                    prov = True
        if not prov:
            self.label.setText('Выберете ячейку')
            return None
        elif cells > 1:
            self.label.setText('Выберете одну ячейку')
            return None
        for it in self.tableWidget.selectedItems():
            x = it.row()
        change = []
        for i in range(self.y + 1):
            change.append(self.tableWidget.item(x, i).text())
        self.id = change[0]
        self.change = change
        self.close_del_day()

    def close_del_day(self):
        self.connection.cursor().execute(f"""DELETE FROM daysweek
WHERE id = {self.id}""")
        self.connection.cursor().execute(f"""DELETE FROM join_table
WHERE dayweek_id = {self.id}""")
        users = self.connection.cursor().execute(f"""SELECT users.id
FROM users""").fetchall()
        for i in users:
            use = self.connection.cursor().execute(f"""SELECT user_id
FROM join_table
WHERE user_id = {i[0]}""").fetchall()
            if not use:
                self.connection.cursor().execute(f"""DELETE FROM users
WHERE id = {i[0]}""")
        self.changeComboBox()
        self.connection.commit()
        self.parent.changeTable()
        self.parent.changeComboBox()

    def open_del_user(self):
        xs = []
        cells = 0
        prov = False
        for i in range(self.x + 1):
            for j in range(self.y + 1):
                if self.tableWidget.item(i, j).isSelected() and i not in xs:
                    cells += 1
                    xs.append(i)
                    prov = True
        if not prov:
            self.label.setText('Выберете ячейку')
            return None
        elif cells > 1:
            self.label.setText('Выберете одну ячейку')
            return None
        for it in self.tableWidget.selectedItems():
            x = it.row()
        change = []
        for i in range(self.y + 1):
            change.append(self.tableWidget.item(x, i).text())
        self.id = change[0]
        self.change = change
        self.close_del_user()

    def close_del_user(self):
        self.connection.cursor().execute(f"""DELETE FROM users
WHERE id = {self.id}""")
        self.connection.cursor().execute(f"""DELETE FROM join_table
WHERE user_id = {self.id}""")
        self.changeComboBox()
        self.connection.commit()
        self.parent.changeTable()
        self.parent.changeComboBox()

    def coaches(self):
        return self.parent.coaches()

    def days(self):
        return self.parent.days()

    def closeEvent(self, event):
        self.parent.show()
        self.connection.commit()
        self.connection.close()

