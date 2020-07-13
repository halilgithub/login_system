from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QWidget, QTableWidget, QTableWidgetItem, QMessageBox
from datetime import datetime
from user import User
import sys


def show_warning(message_text, informative_text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(message_text)
    msg.setInformativeText(informative_text)
    msg.setWindowTitle("Warning")
    msg.exec_()


def show_information(message_text, informative_text=''):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message_text)
    msg.setInformativeText(informative_text)
    msg.setWindowTitle("Information")
    msg.exec_()


def show_last_seen(userid):
    last_seen = 'No log yet'
    with open('txt/log_tracks.txt', 'r') as f:
        for line in f:
            line = line.split()
            if userid in line:
                last_seen = line[1] + '  ' + line[2]
    return last_seen


class AdminPanel(QDialog):
    def __init__(self, parent=None):
        super(AdminPanel, self).__init__(parent)
        uic.loadUi("ui/admin_panel.ui", self)
        self.tabs.setCurrentWidget(self.tabs.findChild(QWidget, 'users'))
        self.fill_user_table()
        self.handle_buttons()

    def handle_buttons(self):
        self.refreshButton.clicked.connect(self.fill_user_table)
        self.addButton.clicked.connect(self.add_user)
        self.finduserButton.clicked.connect(self.find_user)
        self.updateuserButton.clicked.connect(self.update_user)
        self.deleteuserButton.clicked.connect(self.delete_user)
        self.logoutButton.clicked.connect(self.admin_logout)

    def fill_user_table(self):
        for i in reversed(range(self.usertable.rowCount())):
            self.usertable.removeRow(i)
        with open('txt/user_tracks.txt', 'r') as file:
            line = file.readline()
            row_count = 0
            while line:
                self.usertable.insertRow(row_count)
                line = line.split()
                self.usertable.setItem(row_count, 0, QTableWidgetItem(line[0]))
                self.usertable.setItem(row_count, 1, QTableWidgetItem(line[1]))
                self.usertable.setItem(row_count, 2, QTableWidgetItem(line[2]))
                self.usertable.setItem(row_count, 3, QTableWidgetItem(line[3]))
                self.usertable.setItem(row_count, 4, QTableWidgetItem(show_last_seen(line[0])))
                line = file.readline()
                row_count += 1
        self.usertable.verticalHeader().setVisible(False)
        header = self.usertable.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

    def add_user(self):
        email = self.addemail.text()
        password = self.addpass.text()
        first = self.addfirst.text()
        last = self.addlast.text()
        self.addemail.setText('')
        self.addpass.setText('')
        self.addfirst.setText('')
        self.addlast.setText('')
        user = User(email, password, first, last)
        with open('txt/user_tracks.txt', 'a') as f:
            f.write(user.printout())
            f.write('\n')
        message_text = "User has been added"
        show_information(message_text)

    def find_user(self):
        email = self.findbyemail.text()
        with open('txt/user_tracks.txt', 'r') as f:
            for line in f:
                line = line.split()
                if email in line:
                    self.getuserid.setText(line[0])
                    self.getfirst.setText(line[1])
                    self.getlast.setText(line[2])
                    break

    def update_user(self):
        email = self.findbyemail.text()
        with open("txt/user_tracks.txt", "r+") as f:
            new_f = f.readlines()
            f.seek(0)
            for line in new_f:
                if email not in line:
                    f.write(line)
                else:
                    info_list = line.split()
                    info_list[0] = self.getuserid.text()
                    info_list[1] = self.getfirst.text()
                    info_list[2] = self.getlast.text()
                    updated_line = ' '.join(info_list)
                    f.write(updated_line)
            f.truncate()
        self.clean_upd_del()

    def delete_user(self):
        email = self.findbyemail.text()
        with open("txt/user_tracks.txt", "r+") as f1:
            new_f = f1.readlines()
            f1.seek(0)
            for line in new_f:
                if email not in line:
                    f1.write(line)
                else:
                    with open('txt/deletion_tracks.txt', 'a') as f2:
                        f2.write(line)
            f1.truncate()
        self.clean_upd_del()

    def clean_upd_del(self):
        self.findbyemail.setText('')
        self.getuserid.setText('')
        self.getfirst.setText('')
        self.getlast.setText('')

    def admin_logout(self):
        self.close()


class UserPanel(QDialog):
    def __init__(self, info_list, parent=None):
        super(UserPanel, self).__init__(parent)
        uic.loadUi("ui/user_panel.ui", self)
        self.userid = info_list[0]
        self.first = info_list[1]
        self.last = info_list[2]
        self.email = info_list[3]
        self.password = info_list[4]
        self.password_changed = False
        self.last_seen = ''
        self.customize_user_panel()
        self.handle_buttons()

    def handle_buttons(self):
        self.chpassButton.clicked.connect(self.change_password)
        self.logoutButton.clicked.connect(self.user_logout)

    def customize_user_panel(self):
        self.setWindowTitle('{} {} logged in'.format(self.first, self.last))
        self.wellcomemessage.setText('Welcome {}'.format(self.first))
        self.lastseenvalue.setText(show_last_seen(self.userid))

    def change_password(self):
        new_password = self.newpass.text()
        if new_password == '':
            print("geldi")
            message_text = "Password isn't valid"
            informative_text = 'Please enter a valid password'
            show_warning(message_text, informative_text)
            return
        with open('txt/user_tracks.txt', 'r') as f:
            for line in f:
                line = line.split()
                if self.userid in line:
                    old_password = line[4]
                    break
        if new_password == old_password:
            message_text = "Password isn't valid"
            informative_text = "Old Password can't be used"
            show_warning(message_text, informative_text)
            self.newpass.setText('')
            return
        else:
            with open("txt/user_tracks.txt", "r+") as f:
                new_f = f.readlines()
                f.seek(0)
                for line in new_f:
                    if self.userid not in line:
                        f.write(line)
                    else:
                        info_list = line.split()
                        info_list[4] = new_password
                        updated_line = ' '.join(info_list)
                        f.write(updated_line)
                        f.write('\n')
                f.truncate()
            self.password_changed = True
            message_text = "Password has been changed"
            show_information(message_text)
            self.newpass.setText('')
            return

    def insert_log_data(self):
        now = datetime.now()
        # dd-mm-YY H:M:S
        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
        action = "Password changed" if self.password_changed else "No Action"
        log = '{} {} {}'.format(self.userid, dt_string, action)
        with open('txt/log_tracks.txt', 'a') as f:
            f.write(log)
            f.write('\n')

    def user_logout(self):
        self.insert_log_data()
        self.close()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('ui/mainwindow.ui', self)
        self.handel_buttons()

    def handel_buttons(self):
        self.loginButton.clicked.connect(self.login)

    def login(self):
        email = self.email.text()
        password = self.password.text()
        if email == 'admin' and password == 'admin':
            adminpanel = AdminPanel()
            adminpanel.exec_()
        else:
            info_list = self.user_login(email, password)
            if info_list is not None:
                userpanel = UserPanel(info_list)
                userpanel.exec_()
            else:
                message_text = "Email and/or Password is False"
                informative_text = 'Please enter a valid email address and a password'
                show_warning(message_text, informative_text)
        self.email.setText('')
        self.password.setText('')

    def user_login(self, email, password):
        with open('txt/user_tracks.txt', 'r') as f:
            for line in f:
                line = line.split()
                if email == line[3] and password == line[4]:
                    return line


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
