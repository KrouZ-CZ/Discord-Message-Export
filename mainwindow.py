# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py

from ui_form import Ui_MainWindow
import requests
import json
import pickle
import os

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.users = []
        self.ui.listWidget.clicked.connect(self.loadMessages)

        self.ui.pushButton.clicked.connect(self.loadProfiles)
        self.ui.pushButton_2.clicked.connect(self.copyText)
        self.ui.pushButton_3.clicked.connect(self.copyName)
        self.ui.pushButton_4.clicked.connect(self.copyAll)

        self.ui.actionClear.triggered.connect(lambda: self.ui.listWidget_2.clear())
        self.ui.actionClear_all.triggered.connect(lambda: self.ui.listWidget_2.clear())
        self.ui.actionClear_all.triggered.connect(lambda: self.ui.listWidget.clear())
        self.ui.actionAbout_me.triggered.connect(lambda: os.system("start https://github.com/KrouZ-CZ"))
        self.ui.actionHow_to_get_token.triggered.connect(lambda: os.system("start https://www.androidauthority.com/get-discord-token-3149920/"))

        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionOpen.triggered.connect(self.open)

    def loadProfiles(self):
        resp = requests.get("https://discord.com/api/v9/users/@me/channels", headers={"authorization": self.ui.lineEdit.text()})

        for user in json.loads(resp.text):
            try:
                self.users.append(user['id'])
                self.ui.listWidget.addItem(user['recipients'][0]['username'])
            except:
                self.users.pop(len(self.users)-1)


    def loadMessages(self):
        self.ui.listWidget_2.clear()

        id = self.users[self.ui.listWidget.currentIndex().row()]

        url = f"https://discord.com/api/v9/channels/{id}/messages"
        while True:
            r = requests.get(url=url, headers={"authorization": self.ui.lineEdit.text()})
            text = json.loads(r.text)
            if len(text) == 0:
                break
            for item in text:
                if item['content'] != "":
                    self.ui.listWidget_2.insertItem(0, f"{item['author']['username']}: \n{item['content']}")
                idd = item['id']
            url = f"https://discord.com/api/v9/channels/{id}/messages?before={idd}&limit=50"

    def copyText(self):
        try:
            ln = len(self.ui.listWidget_2.currentItem().text().split(":")[0]) + 1
            QApplication.clipboard().setText(self.ui.listWidget_2.currentItem().text()[ln:].strip())
        except:
            pass

    def copyName(self):
        try:
            QApplication.clipboard().setText(self.ui.listWidget_2.currentItem().text().split(":")[0])
        except:
            pass

    def copyAll(self):
        try:
            QApplication.clipboard().setText(self.ui.listWidget_2.currentItem().text())
        except:
            pass

    def save(self):
        fp, _ = QFileDialog.getSaveFileName(self, 'Save File', filter='DAT files (*.dat)')
        if len(fp) == 0: return

        lst = []
        for index in range(self.ui.listWidget_2.count()):
             lst.append(self.ui.listWidget_2.item(index).text())

        with open(fp, 'wb') as f:
            pickle.dump(lst, f)

    def open(self):
        fp, _ = QFileDialog.getOpenFileName(self, 'Open File', filter='DAT files (*.dat)')
        if len(fp) == 0: return
        with open(fp, 'rb') as f:
            msg = pickle.load(f)

        self.ui.listWidget_2.clear()
        self.ui.listWidget_2.addItems(msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
