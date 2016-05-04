from PyQt4.QtGui import *
import Client
from PyQt4 import QtGui
from PyQt4 import QtCore
import sys


class Console(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Console, self).__init__(parent)
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.grid = QGridLayout(self.centralWidget())
        self.l2 = QLabel("Port")
        self.l1 = QLabel("Host")
        self.l3 = QLabel("Nickname")
        self.t1 = QLineEdit("localhost")
        self.t2 = QLineEdit("8888")
        self.t3 = QLineEdit("")
        self.l1.setAlignment(QtCore.Qt.AlignCenter)
        self.l2.setAlignment(QtCore.Qt.AlignCenter)
        self.l3.setAlignment(QtCore.Qt.AlignCenter)
        self.t1.setAlignment(QtCore.Qt.AlignCenter)
        self.t2.setAlignment(QtCore.Qt.AlignCenter)
        self.t3.setAlignment(QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.l1, 0, 0)
        self.grid.addWidget(self.l2, 0, 1)
        self.grid.addWidget(self.l3, 0, 2)
        self.grid.addWidget(self.t1, 1, 0)
        self.grid.addWidget(self.t2, 1, 1)
        self.grid.addWidget(self.t3, 1, 2)
        self.button = QPushButton("Create Client")
        self.grid.addWidget(self.button, 2, 2)
        self.button.clicked.connect(self.createUser)
        self.setWindowTitle("Client Console")
        self.CLIENT_WIN = []
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        css = """
        .QWidget {
            border: 2px solid black;
            border-radius: 15px 50px 0px 0px;
            background-color: rgb(255,255,255);
            }
        QPushButton {
            color: white;
            background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #88d, stop: 0.1 #99e, stop: 0.49 #77c, stop: 0.5 #66b, stop: 1 #77c);
            border-width: 1px;
            border-color: #339;
            border-style: solid;
            border-radius: 7;
            padding: 3px;
            padding-left: 5px;
            padding-right: 5px;
            min-width: 50px;
            max-width: 100px;
            }
        QLineEdit {
            padding: 1px;
            border-style: solid;
            border: 2px solid gray;
            border-radius: 8px;
            text-align: center
            }
        QLabel {
            height: 13px;
            font-size: 15px;
            }
        """
        self.central.setStyleSheet(css)
        self.show()

    def createUser(self):
        client = Client.ClientThread(self.t1.text(), int(self.t2.text()), self.t3.text())
        if client.isconnected == 1:
            n = client.nickValidate(self.t3.text())
            if n[0] != '0':
                cbox = Client.ChatBox(client)
                client.start()
            else:
                QMessageBox.about(self, "Nickname Error", n[1])
        else:
            QMessageBox.about(self, "Server Error", "Couldn't Connect")

app = QApplication(sys.argv)
Console1 = Console()
sys.exit(app.exec_())



