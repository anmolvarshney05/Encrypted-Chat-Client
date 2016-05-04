import socket
import select
from PyQt4.QtGui import *
from PyQt4 import QtCore
from threading import *
from format import *
import sys


class ClientHandleThread(Thread):
    def __init__(self, server, GUI):
        self.GUI = GUI
        super(ClientHandleThread, self).__init__()
        self.server = server
        self.NICK_LIST = []
        self.USERS = []
        self.sep = chr(7)
        self.CON_LIST = server.CON_LIST
        self.readable_sockets = []

    def run(self):
        while True:
            self.readable_sockets, _, _ = select.select(self.server.CON_LIST, [], [])
            for sock in self.readable_sockets:
                if sock == self.server.sock:
                    conn, addr = self.server.sock.accept()
                    if conn not in self.server.CON_LIST:
                        self.server.CON_LIST.append(conn)
                else:
                    try:
                        data = sock.recv(4096)
                        data = u8(data)
                    except:
                        for i in range(len(self.CON_LIST)):
                            if self.CON_LIST[i] == sock:
                                break
                        self.server.CON_LIST.remove(sock)
                        t = self.NICK_LIST[i-1]
                        self.NICK_LIST.remove(t)
                        for i in self.USERS:
                            if i[0] == t:
                                self.USERS.remove(i)
                                break
                        self.broadcast_data(sock, '1' + self.sep + t)
                        sock.close()
                        continue
                    ins = data.split(chr(7))
                    if ins[0] == '1':
                        self.broadcast_data(sock, data)
                        self.broadcast_data(sock, '4' + self.sep + 'Broadcast' + self.sep + ins[1] + ' is disconnected')
                        self.GUI.chat.append('Client ' + ins[1] + ' is disconnected')
                        self.CON_LIST.remove(sock)
                        self.NICK_LIST.remove(ins[1])
                        for x in self.USERS:
                            if x[0] == ins[1]:
                                self.USERS.remove(x)
                                break
                        sock.close()
                    elif ins[0] == '2':
                        if ins[1] == "":
                            sock.send('0' + self.sep + 'Nickname cannot be empty')
                            sock.close()
                            self.CON_LIST.remove(sock)
                        elif ins[1].lower() == 'me' or ins[1].lower() == 'broadcast' or ins[1].lower() == 'server':
                            sock.send('0' + self.sep + 'Reserved Nickname')
                            sock.close()
                            self.CON_LIST.remove(sock)
                        elif ins[1] not in self.NICK_LIST:
                            self.NICK_LIST.append(ins[1])
                            self.broadcast_data(sock, data)
                            self.GUI.chat.append('Client ' + ins[1] + ' is Connected')
                            msg = "2"
                            for x in self.USERS:
                                msg += self.sep + x[0] + self.sep + x[1]
                            sock.send(msg)
                            self.USERS.append((ins[1], ins[2]))
                            sock.send('4' + self.sep + 'Server' + self.sep + 'Welcome ' + ins[1])
                            self.broadcast_data(sock, '4' + self.sep + 'Server' + self.sep + ins[1] + ' entered the Chat Room')
                        else:
                            sock.send("0" + self.sep + "Nickname Exists")
                            sock.close()
                            self.CON_LIST.remove(sock)
                    elif ins[0] == '3':
                        self.GUI.chat.append(ins[1] + " sent message to " + ins[2])
                        self.broadcast_data(sock, data)
                    elif ins[0] == '4':
                        self.broadcast_data(sock, data)
        self.server.sock.close()

    def broadcast_data(self, x, msg):
        for s in self.server.CON_LIST:
            if s != self.server.sock and s != x:
                try:
                    s.send(msg)
                except:
                    print "ServerError"
                    for i in range(len(self.CON_LIST)):
                        if self.CON_LIST[i] == s:
                            break
                    self.CON_LIST.remove(s)
                    t = self.NICK_LIST[i-1]
                    self.NICK_LIST.remove(t)
                    for i in self.USERS:
                        if i[0] == t:
                            self.USERS.remove(i)
                            break
                    self.broadcast_data(s, '1' + self.sep + t)
                    s.close()


class ServerBox(QWidget):
    def __init__(self, server):
        super(ServerBox, self).__init__()
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.chat = QTextEdit()
        self.grid.addWidget(self.chat, 0, 0)
        self.setWindowTitle('Server')
        self.setLayout(self.grid)
        css = """
        QTextEdit {
            padding: 1px;
            border-style: solid;
            border: 2px solid gray;
            border-radius: 8px;
            text-align: center
            }
        """
        self.setStyleSheet(css)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.show()


class Server:
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.bind((self.HOST, self.PORT))
            self.sock.listen(10)
            self.CON_LIST = []
            self.CON_LIST.append(self.sock)
        except:
            sys.exit()


app = QApplication(sys.argv)
server = Server(socket.gethostbyname('localhost'), 8888)
sbox = ServerBox(server)
Handler = ClientHandleThread(server, sbox)
Handler.start()
sys.exit(app.exec_())

