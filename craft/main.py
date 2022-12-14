import sqlite3
import sys

from Main_UI import Ui_MainWindow
# from PyQt5 import uic

from PyQt5.QtWidgets import QApplication, QAbstractItemView, QAction
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from add_user_dialog import User_Dialog
from add_day_dialog import Day_Dialog
from add_time_dialog import Time_Dialog
from add_coach_dialog import Coach_Dialog
from change_dialog import Change_Dialog
from del_dialog import Del_Dialog
from info_dialog import Info_Dialog
from ADMIN_dialog import ADMIN_Dialog
from pie import Pie


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ADMIN = False
        self.connection = sqlite3.connect("db/yand_db.db")
        self.comboBox.currentTextChanged.connect(self.changeComboBox)
        self.comboBox_2.currentTextChanged.connect(self.changeTable)
        self.pushButton.clicked.connect(self.open_add)
        self.pushButton_2.clicked.connect(self.open_change)
        self.pushButton_3.clicked.connect(self.open_del)

        self.action_pie.triggered.connect(self.drawPie)
        self.action_info.triggered.connect(self.open_info)
        self.action_ADMIN.triggered.connect(self.open_ADMIN)

        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.select_users()

    def open_ADMIN(self):
        self.Use_Dialog = ADMIN_Dialog(self)
        self.Use_Dialog.show()

    def closeADMIN(self):
        pas = self.Use_Dialog.returnVal()[0]
        password = self.connection.cursor().execute(f"""SELECT password
FROM admin""").fetchall()[0][0]
        if password != pas:
            self.statusBar().showMessage('Вы ввели не правильный пароль')
        else:
            self.ADMIN = True
            self.statusBar().showMessage('Вы ADMIN')
            self.action_ADMIN.disconnect()
            self.action_ADMIN.setText("LEAVE ADMIN")
            self.action_ADMIN.triggered.connect(self.leave_ADMIN)
        self.Use_Dialog.destroy()
        self.changeComboBox()

    def leave_ADMIN(self):
        self.ADMIN = False
        self.statusBar().showMessage('Вы вышли из ADMIN')
        self.action_ADMIN.disconnect()
        self.action_ADMIN.setText("ADMIN")
        self.action_ADMIN.triggered.connect(self.open_ADMIN)
        
    def open_info(self):
        self.Use_Dialog = Info_Dialog(self)
        self.Use_Dialog.show()

    def drawPie(self):
        coaches = self.connection.cursor().execute(f"""SELECT id, name
FROM coaches""").fetchall()
        num_users = len(self.connection.cursor().execute(f"""SELECT id
FROM users""").fetchall())
        num_lessons = []
        for i in coaches:
            coach_users = len(self.connection.cursor().execute(f"""SELECT id
FROM join_table
WHERE coach_id = {i[0]}""").fetchall())
            num_lessons.append(max([0.2, coach_users]))
        coaches = list(map(lambda x: x[1], coaches))
        Pie(coaches, num_lessons)
        # Pie([1, 2], [90, 20])
#
    def changeTable(self):
        if self.comboBox_2.currentText() == "Все":
            self.select_users()
        elif self.comboBox.currentText() == "Тренер":
            self.select_coach(self.comboBox_2.currentText())
        elif self.comboBox.currentText() == "Дни недели":
            self.select_day(self.comboBox_2.currentText())
        elif self.comboBox.currentText() == "Время":
            self.select_time(self.comboBox_2.currentText())

    def changeComboBox(self):
        self.comboBox_2.disconnect()
        self.comboBox_2.clear()
        if self.comboBox.currentText() == "Занимающиеся":
            self.comboBox_2.addItem("Все")
        elif self.comboBox.currentText() == "Дни недели":
            res = self.connection.cursor().execute("""SELECT title FROM daysweek""").fetchall()
            self.comboBox_2.addItem("Все")
            for i in res:
                self.comboBox_2.addItem(i[0])
        elif self.comboBox.currentText() == "Время":
            res = self.connection.cursor().execute("""SELECT time FROM times""").fetchall()
            self.comboBox_2.addItem("Все")
            for i in res:
                self.comboBox_2.addItem(i[0])
        else:
            res = self.connection.cursor().execute("""SELECT name FROM coaches""").fetchall()
            self.comboBox_2.addItem("Все")
            for i in res:
                self.comboBox_2.addItem(i[0])
        self.changeTable()
        self.comboBox_2.currentTextChanged.connect(self.changeTable)
#
    def select_time(self, time):
        ids = self.connection.cursor().execute(f"""SELECT users.id,
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
    j.time_id = times.id
AND
    j.time_id = (SELECT id FROM times WHERE time = '{time}')""").fetchall()
        res = []
        for i in ids:
            use = self.connection.cursor().execute(f"""SELECT users.id,
    users.name,
    users.birthday,
    d.title,
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
        title = ["ID", "ИМЯ", "ДАТА РОЖДЕНИЯ", "ДЕНЬ НЕДЕЛИ", "ТРЕНЕР"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(sorted(res, key=lambda x: [x[0], list(map(lambda x: x[0], self.days())).index(x[3])])):
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
        
    def select_day(self, day):
        ids = self.connection.cursor().execute(f"""SELECT users.id,
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
    j.dayweek_id = (SELECT id FROM daysweek WHERE title = '{day}')
AND
    j.coach_id = coaches.id
AND
    j.time_id = times.id""").fetchall()
        res = []
        for i in ids:
            use = self.connection.cursor().execute(f"""SELECT users.id,
    users.name,
    users.birthday,
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
        title = ["ID", "ИМЯ", "ДАТА РОЖДЕНИЯ", "ВРЕМЯ", "ТРЕНЕР"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(sorted(res, key=lambda x: [x[0], x[4]])):
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

    def select_coach(self, coach_name):
        ids = self.connection.cursor().execute(f"""SELECT users.id,
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
    j.coach_id = (SELECT id FROM coaches WHERE name = '{coach_name}')
AND
    j.time_id = times.id""").fetchall()
        res = []
        for i in ids:
            use = self.connection.cursor().execute(f"""SELECT users.id,
    users.name,
    users.birthday,
    d.title,
    t.time
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
        title = ["ID", "ИМЯ", "ДАТА РОЖДЕНИЯ", "ДЕНЬ НЕДЕЛИ", "ВРЕМЯ"]
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
                if elem:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(''))
                self.x = i
                self.y = j
        self.tableWidget.resizeColumnsToContents()
#
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
        return self.connection.cursor().execute("""SELECT name FROM coaches""").fetchall()

    def days(self):
        return self.connection.cursor().execute("""SELECT title FROM daysweek""").fetchall()

    def times(self):
        return self.connection.cursor().execute("""SELECT time FROM times""").fetchall()

    def open_del(self):
        self.Use_Dialog = Del_Dialog(self.ADMIN, self)
        self.Use_Dialog.show()
        
    def open_change(self):
        self.Use_Dialog = Change_Dialog(self.ADMIN, self)
        self.Use_Dialog.show()
        
    def open_add(self):
        if self.comboBox.currentText() == "Занимающиеся":
            self.open_add_user()
        elif not self.ADMIN:
            self.statusBar().showMessage('Вы не ADMIN')
            return None
        elif self.comboBox.currentText() == "Дни недели":
            self.open_add_day()
        elif self.comboBox.currentText() == "Время":
            self.open_add_time()
        elif self.comboBox.currentText() == "Тренер":
            self.open_add_coach()

    def open_add_time(self):
        self.create_Dialog(Time_Dialog, 'ADD')

    def closeAddTime(self):
        print(1)
        use = self.Use_Dialog.returnVal()
        if not use[0]:
            self.statusBar().showMessage('Некорректные данные')
            self.Use_Dialog.destroy()
            return None
        self.connection.cursor().execute(f"""INSERT INTO times(time)
VALUES('{use[0]}')""")# add time
        self.Use_Dialog.destroy()
        self.changeComboBox()
        self.connection.commit()

    def open_add_coach(self):
        self.create_Dialog(Coach_Dialog, 'ADD')

    def closeAddCoach(self):
        use = self.Use_Dialog.returnVal()
        if not use[0]:
            self.statusBar().showMessage('Некорректные данные')
            self.Use_Dialog.destroy()
            return None
        self.connection.cursor().execute(f"""INSERT INTO coaches(name)
VALUES('{use[0]}')""")# add coach
        self.Use_Dialog.destroy()
        self.changeComboBox()
        self.connection.commit()

    def open_add_day(self):
        self.create_Dialog(Day_Dialog, 'ADD')

    def closeAddDay(self):
        use = self.Use_Dialog.returnVal()
        if not use[0]:
            self.statusBar().showMessage('Некорректные данные')
            self.Use_Dialog.destroy()
            return None
        self.connection.cursor().execute(f"""INSERT INTO daysweek(title)
VALUES('{str(use[0])}')""")
        self.Use_Dialog.destroy()
        self.changeComboBox()
        self.connection.commit()
        
    def open_add_user(self):
        self.create_Dialog(User_Dialog, 'ADD')
        
    def closeAddUser(self):
        use = self.Use_Dialog.returnVal()
        if not use[0] or not use[2]:
            self.statusBar().showMessage('Некорректные данные')
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
        self.connection.cursor().execute(f"""INSERT INTO users(name, birthday)
VALUES('{use[0]}', '{use[1]}')""")# add user
        user_id = max(list(map(lambda x: x[0], self.connection.cursor().execute(f"""SELECT id FROM users WHERE
name = '{use[0]}' AND birthday = '{use[1]}'""").fetchall())))
        for i in sorted(days, key=lambda x: int(x[0])):
            self.connection.cursor().execute(f"""INSERT INTO join_table(user_id, dayweek_id, coach_id, time_id)
VALUES('{user_id}', '{i[0]}', '{coach_id}', '{i[1]}')""")# add in join_table
        self.Use_Dialog.destroy()
        self.changeTable()
        self.connection.commit()

    def create_Dialog(self, dialog, move, change=[]):
        self.Use_Dialog = dialog(move, self, change)
        self.Use_Dialog.show()
#
    def closeEvent(self, event):
        self.connection.commit()
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
