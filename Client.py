from PyQt4.QtGui import *
from PyQt4 import QtCore
import socket
from threading import Thread
from BREA import BREA
from RSA import RSA


class ClientThread(Thread):
    def __init__(self, HOST, PORT, NICK):
        super(ClientThread, self).__init__()
        self.ONLINE_LIST = []
        self.nick = NICK
        self.cbox = None
        self.RSA_Scheme = RSA()
        self.BREA_Scheme = BREA()
        self.receiver = "broadcast"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sep = chr(7)
        self.broadcast = 1
        self.HOST = socket.gethostbyname(str(HOST))
        self.PORT = PORT
        self.isconnected = 1
        self.root = 0
        self.online_list = []
        try:
            self.sock.connect((self.HOST, self.PORT))
        except:
            self.isconnected = 0

    def reconnect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.HOST, self.PORT))
            self.sock.send('2' + self.sep + self.nick + self.sep + self.RSA_Scheme.getPublicKey())
            data = self.sock.recv(4096)
            self.online_list = data.split(self.sep)
            if self.online_list[0] == '2':
                for i in range(1, len(self.online_list), 2):
                    self.cbox.online.addItem(self.online_list[i])
                    self.ONLINE_LIST.append((self.online_list[i], self.online_list[i+1]))
        except:
            pass

    def run(self):
        while True:
            try:
                msg = self.sock.recv(4096)
            except:
                self.ONLINE_LIST = []
                self.online_list = []
                self.cbox.online.clear()
                self.reconnect()
                continue
            ins = msg.split(self.sep)
            if ins[0] == '1':
                if self.cbox.connected.text() == "Connected to " + ins[1]:
                    self.cbox.connected.setText("Connected to <No User>")
                for i in range(self.cbox.online.count()):
                    if self.cbox.online.item(i).text() == ins[1]:
                        self.cbox.online.takeItem(i)
                        break
                for i in self.ONLINE_LIST:
                    if i[0] == ins[1]:
                        self.ONLINE_LIST.remove(i)
                        break
            elif ins[0] == '2':
                for i in range(1, len(ins), 2):
                    self.cbox.online.addItem(ins[i])
                    self.ONLINE_LIST.append((ins[i], ins[i+1]))
            elif ins[0] == '3':
                if ins[2] == self.nick or self.root == 1:
                    key = ins[4]
                    msg = self.BREA_Scheme.decrypt(ins[3], self.RSA_Scheme.decrypt(key))
                    self.cbox.win.append("[" + ins[1] + "] " + msg)
            elif ins[0] == "4":
                self.cbox.win.append("[" + ins[1] + "] " + ins[2])

    def nickValidate(self, txt):
        sent = "2" + self.sep + txt + self.sep + self.RSA_Scheme.getPublicKey()
        self.sock.send(sent)
        ret = self.sock.recv(4096)
        ret = ret.split(self.sep)
        self.online_list = ret
        return ret


class ChatBox(QWidget):
    def __init__(self, client):
        super(ChatBox, self).__init__()
        self.sep = chr(7)
        self.client = client
        client.cbox = self
        self.client.cbox = self
        self.grid = QGridLayout()
        self.send = QPushButton("Send")
        self.chat = QLineEdit()
        self.win = QTextEdit()
        self.online = QListWidget()
        self.connected = QLabel("Connected to Broadcast")
        self.setBroadcast = QCheckBox("Connected to Broadcast")
        self.chat.setAlignment(QtCore.Qt.AlignCenter)
        self.setRoot = QCheckBox("See All Messages")
        self.setBroadcast.setChecked(True)
        self.setRoot.setChecked(False)
        if self.client.online_list[0] == '2':
            for i in range(1, len(self.client.online_list), 2):
                self.online.addItem(self.client.online_list[i])
                self.client.ONLINE_LIST.append((self.client.online_list[i], self.client.online_list[i+1]))
        self.grid.addWidget(self.send, 2, 1)
        self.send.clicked.connect(self.sendmsg)
        self.online.itemDoubleClicked.connect(self.getReceiver)
        self.setBroadcast.toggled.connect(self.setTobroadcast)
        self.setRoot.toggled.connect(self.setRootfunc)
        self.grid.addWidget(self.connected, 34, 1)
        self.grid.addWidget(self.chat, 2, 0)
        self.grid.addWidget(self.win, 1, 0)
        self.grid.addWidget(self.online, 1, 1)
        self.grid.addWidget(self.send, 2, 1)
        self.grid.addWidget(self.connected, 2, 0)
        self.grid.addWidget(self.setBroadcast, 0, 1)
        self.grid.addWidget(self.setRoot, 0, 0)
        self.setWindowTitle(self.client.nick)
        self.setGeometry(100, 100, 500, 600)
        self.setLayout(self.grid)
        css = """
        QWidget {
            background: QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #eef, stop: 1 #ccf);
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
        QTextEdit {
            padding: 1px;
            border-style: solid;
            border: 2px solid gray;
            border-radius: 8px;
            text-align: center
            }
        QListWidget {
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
        self.setStyleSheet(css)
        self.setWindowTitle(self.client.nick)
        self.show()

    def sendmsg(self):
        self.win.append("[Me"+"]"+self.chat.text())
        if self.client.broadcast == 1:
            text = str(self.chat.text())
            msg = "4"+self.sep+self.client.nick+self.sep+text
            self.client.sock.send(msg)
        else:
            text = str(self.chat.text())
            RECK = self.getKey(self.client.receiver)
            msg = "3"+self.sep+self.client.nick+self.sep+self.client.receiver
            text = self.client.BREA_Scheme.encrypt(text)
            msg += self.sep+text+self.sep
            msg += self.client.RSA_Scheme.encrypt(self.client.BREA_Scheme.getKey(), RECK)
            self.client.sock.send(msg)
        self.chat.clear()

    def setTobroadcast(self):
        if self.setBroadcast.isChecked():
            self.connected.setText("Connected to Broadcast")
            self.client.broadcast = 1
        else:
            self.connected.setText("Connected to <No User> ")
            self.client.broadcast = 0

    def setRootfunc(self):
        if self.setRoot.isChecked():
            self.client.root = 1
        else:
            self.client.root = 0

    def getKey(self, rec):
        for i in self.client.ONLINE_LIST:
            if i[0] == rec:
                return i[1]

    def getReceiver(self, item):
        self.setBroadcast.setChecked(False)
        self.client.broadcast = 0
        self.client.receiver = item.text()
        self.connected.setText("Connected to " + self.client.receiver)

    def closeEvent(self, QCloseEvent):
        self.client.sock.send('1' + self.sep + self.client.nick)
        QCloseEvent.accept()

# app = QApplication(sys.argv)
# client = ClientThread("localhost",8888,"")
# cbox = ChatBox(client)
# client.start()
# sys.exit(app.exec_())
