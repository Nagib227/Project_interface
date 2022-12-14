import sqlite3
import sys

from ChangeDialog_UI import Ui_Dialog
from PyQt5.QtWidgets import QApplication, QAbstractItemView
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QMainWindow

from add_user_dialog import User_Dialog
from add_day_dialog import Day_Dialog
from add_time_dialog import Time_Dialog
from add_coach_dialog import Coach_Dialog


class Change_Dialog(QDialog, Ui_Dialog):
    def __init__(self, ADMIN, parent=None):
        self.ADMIN = ADMIN
        super(Change_Dialog, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.connection = sqlite3.connect("db/yand_db.db")
        self.comboBox.currentTextChanged.connect(self.changeComboBox)
        self.pushButton.clicked.connect(self.open_change)
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

    def open_change(self):
        if self.comboBox.currentText() == "Занимающиеся":
            self.label.setText('')
            self.open_change_user()
        elif not self.ADMIN:
            self.label.setText('Вы не ADMIN')
            return None
        elif self.comboBox.currentText() == "Дни недели":
            self.open_change_day()
        elif self.comboBox.currentText() == "Время":
            self.open_change_time()
        else:
            self.open_change_coach()

    def open_change_time(self):
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
        self.create_Dialog(Time_Dialog, 'change', change[1:])

    def close_change_time(self):
        use = self.Use_Dialog.returnVal()
        if not use[0]:
            self.label.setText('Некорректные данные')
            self.Use_Dialog.destroy()
            return None
        self.connection.cursor().execute(f"""UPDATE times
SET time = '{use[0]}'
WHERE id = {self.id}""")
        self.Use_Dialog.destroy()
        self.changeComboBox()
        self.connection.commit()
        self.parent.changeTable()
        self.parent.changeComboBox()
        
    def open_change_coach(self):
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
        self.create_Dialog(Coach_Dialog, 'change', change[1:])

    def close_change_coach(self):
        use = self.Use_Dialog.returnVal()
        if not use[0]:
            self.label.setText('Некорректные данные')
            self.Use_Dialog.destroy()
            return None
        self.connection.cursor().execute(f"""UPDATE coaches
SET name = '{use[0]}'
WHERE id = {self.id}""")
        self.Use_Dialog.destroy()
        self.changeComboBox()
        self.connection.commit()
        self.parent.changeTable()
        self.parent.changeComboBox()

    def open_change_day(self):
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
        self.create_Dialog(Day_Dialog, 'change', change[1:])

    def close_change_day(self):
        use = self.Use_Dialog.returnVal()
        if not use[0]:
            self.label.setText('Некорректные данные')
            self.Use_Dialog.destroy()
            return None
        self.connection.cursor().execute(f"""UPDATE daysweek
SET title = '{use[0]}'
WHERE id = {self.id}""")
        self.Use_Dialog.destroy()
        self.changeComboBox()
        self.connection.commit()
        self.parent.changeTable()
        self.parent.changeComboBox()

    def open_change_user(self):
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
        self.change = change[:]
        change[5] = list(map(lambda x: x[0], self.parent.coaches())).index(change[5])
        self.create_Dialog(User_Dialog, 'change', change[:4] + [change[5]])

    def close_change_user(self):
        use = self.Use_Dialog.returnVal()
        if not use[0] or not use[2]:
            self.label.setText('Некорректные данные')
            self.Use_Dialog.destroy()
            return None
        days = []
        for i in use[2]:
            days.append([self.connection.cursor().execute(f"""SELECT id FROM daysweek WHERE
title = '{i.split()[0]}'""").fetchall()[0][0],
                         self.connection.cursor().execute(f"""SELECT id FROM times WHERE
time = '{i.split()[1]}'""").fetchall()[0][0]])
        coach_id = self.connection.cursor().execute(f"""SELECT id FROM coaches WHERE
name = '{use[-1]}'""").fetchall()[0][0]
        self.connection.cursor().execute(f"""UPDATE users
SET name = '{use[0]}',
birthday = '{use[1]}'
WHERE id = {self.id}""")
        self.connection.cursor().execute(f"""DELETE FROM join_table
WHERE user_id = {self.id} AND coach_id = (SELECT id FROM coaches WHERE
name = '{self.change[5]}')""")
        for i in sorted(days):
            self.connection.cursor().execute(f"""INSERT INTO join_table(user_id, dayweek_id, coach_id, time_id)
VALUES('{self.id}', '{i[0]}', '{coach_id}', '{i[1]}')""")
        self.Use_Dialog.destroy()
        self.changeComboBox()
        self.connection.commit()
        self.parent.changeTable()

    def records(self, ID, coach_name):
        use = self.connection.cursor().execute(f"""SELECT
    d.title,
    t.time
FROM
    users, coaches, join_table j, daysweek d, times t
WHERE
    j.user_id = users.id
AND
    users.id = {ID}
AND
    j.coach_id = coaches.id
AND
    j.coach_id = (SELECT id FROM coaches WHERE name = '{coach_name}')
AND
    j.dayweek_id = d.id
AND
    j.time_id = t.id""").fetchall()
        return use

    def coaches(self):
        return self.parent.coaches()

    def days(self):
        return self.parent.days()
    
    def times(self):
        return self.parent.times()

    def create_Dialog(self, dialog, move, change=[]):
        self.Use_Dialog = dialog(move, self, change)
        self.Use_Dialog.show()

    def closeEvent(self, event):
        self.parent.show()
        self.connection.commit()
        self.connection.close()
