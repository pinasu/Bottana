import sys, os, time
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QTextCursor
from botana import BotAna
import threading

class WindowTwo(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.isInTest = False
        self.parent = parent
        self.parent.activate_green_screen_button(False)
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(450,450)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setStyleSheet("WindowTwo{background-color:#0f0;}")
        self.setWindowTitle('BotAnaImage')
        self.setWindowIcon(QtGui.QIcon('res/Gui/icon.ico'))
        self.img = QtWidgets.QLabel()

        v_box = QtWidgets.QVBoxLayout()
        v_box.setContentsMargins(0,0,0,0)
        v_box.addWidget(self.img)
        self.setLayout(v_box)
        self.show()

    def closeEvent(self, event):
        self.parent.activate_green_screen_button(True)
        self.set_button_test_image_active(False)
        event.accept()

    def set_button_test_image_active(self, bo):
        self.isInTest = bo
        self.parent.set_button_test_image(bo)

    def trigger_test_image(self):
        if not self.isInTest:
            self.img.setPixmap(QtGui.QPixmap("res/ShowImages/test.png"))
            self.set_button_test_image_active(True)
        else:
            self.img.clear()
            self.set_button_test_image_active(False)


    def show_image(self, path):
        if self.isVisible() and not self.isInTest:
            threading.Thread(target=self.process, args=[path]).start()

    def process(self, path):
        self.img.setPixmap(QtGui.QPixmap(path))
        time.sleep(10)
        if not self.isInTest:
            self.img.clear()

class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.is_afk = False
        self.init_ui()
        self.secondWind = WindowTwo(self)
        self.move_center()
        self.bot = BotAna()
        self.bot.sign.connect(self.print_on_text_area)
        self.bot.sign2.connect(self.show_image)
        self.bot.start()
        self.activateWindow()

    def init_ui(self):

        sshFile="res/style.css"
        with open(sshFile,"r") as fh:
            self.setStyleSheet(fh.read())

        self.setWindowIcon(QtGui.QIcon('res/Gui/icon.ico'))

        self.setGeometry(0,0,950, 450)
        self.setMinimumSize(700,300)
        self.logo = QtWidgets.QLabel()
        self.logo.setObjectName("logo")
        self.logo.setPixmap(QtGui.QPixmap('res/Gui/botana.png'))

        self.creators = QtWidgets.QLabel()
        self.creators.setPixmap(QtGui.QPixmap('res/Gui/creators.png'))

        self.textarea = QtWidgets.QTextEdit()
        self.textarea.setReadOnly(True)
        self.textarea.setObjectName("textarea")
        self.inputText = QtWidgets.QLineEdit()
        self.inputText.setObjectName("inputText")
        self.sendButton = QtWidgets.QPushButton('INVIA')
        self.sendButton.setCursor (Qt.PointingHandCursor)
        self.sendButton.setObjectName("sendButton")
        self.sendButton.setProperty('class','button')
        self.greenScreenButton = QtWidgets.QPushButton("")
        self.greenScreenButton.setIcon(QtGui.QIcon('res/Gui/greenScreenButton.png'))
        self.greenScreenButton.setIconSize(QtCore.QSize(40,40))
        self.greenScreenButton.setCursor (Qt.PointingHandCursor)
        self.greenScreenButton.setProperty('class','button gridButton')
        self.greenScreenButton.setToolTip("Mostra finestra green screen")
        self.logErrorButton = QtWidgets.QPushButton("")
        self.logErrorButton.setIcon(QtGui.QIcon('res/Gui/errorLogButton.png'))
        self.logErrorButton.setIconSize(QtCore.QSize(40,40))
        self.logErrorButton.setCursor (Qt.PointingHandCursor)
        self.logErrorButton.setProperty('class','button gridButton')
        self.logErrorButton.setToolTip("Apri file log degli errori")
        self.msgLog = QtWidgets.QMessageBox()
        self.msgLog.setIcon(QMessageBox.Information)
        self.msgLog.setText("Nessun log di errore presente")
        self.msgLog.setWindowTitle("Info")
        self.msgLog.setWindowIcon(QtGui.QIcon('res/Gui/icon.ico'))
        self.testImageGreenScreen = QtWidgets.QPushButton("")
        self.testImageGreenScreen.setIcon(QtGui.QIcon('res/Gui/testImageGreenScreen.png'))
        self.testImageGreenScreen.setIconSize(QtCore.QSize(40,40))
        self.testImageGreenScreen.setCursor (Qt.PointingHandCursor)
        self.testImageGreenScreen.setProperty('class','button gridButton')
        self.testImageGreenScreen.setToolTip("Mostra/Nascondi immagine di test del green screen")
        self.restartBtn = QtWidgets.QPushButton("")
        self.restartBtn.setIcon(QtGui.QIcon('res/Gui/restart.png'))
        self.restartBtn.setIconSize(QtCore.QSize(40,40))
        self.restartBtn.setCursor (Qt.PointingHandCursor)
        self.restartBtn.setProperty('class','button gridButton')
        self.restartBtn.setToolTip("Riavvia")
        self.afkBtn = QtWidgets.QPushButton("")
        self.afkBtn.setIcon(QtGui.QIcon('res/Gui/afk.png'))
        self.afkBtn.setIconSize(QtCore.QSize(40,40))
        self.afkBtn.setCursor (Qt.PointingHandCursor)
        self.afkBtn.setProperty('class','button gridButton')
        self.afkBtn.setToolTip("Modifica titolo stream")

        g_box = QtWidgets.QGridLayout()
        g_box.addWidget(self.greenScreenButton, 0 , 0)
        g_box.addWidget(self.testImageGreenScreen, 0 , 1)
        g_box.addWidget(self.logErrorButton, 1 , 0)
        g_box.addWidget(self.afkBtn, 1 , 1)
        g_box.addWidget(self.restartBtn, 2 , 0, 2, 2)

        v_box = QtWidgets.QVBoxLayout()
        v_box.setContentsMargins(7,7,14,0)
        v_box.addWidget(self.logo)
        v_box.addLayout(g_box)
        v_box.addStretch()
        v_box.addWidget(self.creators)

        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addWidget(self.inputText)
        h_box2.addWidget(self.sendButton)


        v_box2 = QtWidgets.QVBoxLayout()
        v_box2.addWidget(self.textarea)
        v_box2.addLayout(h_box2)


        h_box = QtWidgets.QHBoxLayout()
        h_box.addLayout(v_box)
        h_box.addLayout(v_box2)

        self.setLayout(h_box)
        self.setWindowTitle('BotAna')

        self.sendButton.clicked.connect(self.btn_click)
        self.greenScreenButton.clicked.connect(self.open_green_screen)
        self.logErrorButton.clicked.connect(self.open_error_log)
        self.testImageGreenScreen.clicked.connect(self.trigger_test_image)
        self.restartBtn.clicked.connect(self.restart)
        self.afkBtn.clicked.connect(self.afk)

        self.show()

    def restart(self):
        self.bot.restart()

    def afk(self):
        if self.is_afk:
            self.bot.in_game()
            self.afkBtn.setIcon(QtGui.QIcon('res/Gui/afk.png'))
            self.is_afk = False
        else:
            self.bot.afk()
            self.afkBtn.setIcon(QtGui.QIcon('res/Gui/inGame.png'))
            self.is_afk = True

    def set_button_test_image(self, active):
        if active:
            self.testImageGreenScreen.setIcon(QtGui.QIcon('res/Gui/testImageGreenScreenX.png'))
        else:
            self.testImageGreenScreen.setIcon(QtGui.QIcon('res/Gui/testImageGreenScreen.png'))

    def trigger_test_image(self):
        self.secondWind.trigger_test_image()

    def open_error_log(self):
        if os.path.exists('LogError.txt'):
            os.startfile('LogError.txt')
        else:
            self.msgLog.exec_()

    def activate_green_screen_button(self, bo):
        self.greenScreenButton.setEnabled(bo)
        self.testImageGreenScreen.setEnabled(not bo)

    def open_green_screen(self):
        self.secondWind = WindowTwo(self)
        self.move_green_screen_wind()

    def show_image(self, path):
        self.secondWind.show_image(path)

    def closeEvent(self, event):
        self.secondWind.close()
        event.accept()

    def print_on_text_area(self, msg):
        if(msg != ""):
            self.textarea.append(msg)

    def keyPressEvent(self, event):
        if(event.key() == Qt.Key_Return and self.inputText.hasFocus()):
            self.btn_click()

    def btn_click(self):
        msg = self.inputText.text()
        if(msg != ""):
            self.bot.send_message(msg)
            self.inputText.setText("")

    def move_green_screen_wind(self):
        if (self.pos().x() - self.secondWind.width()) >= 0:
            self.secondWind.move(self.pos().x() - self.secondWind.width(), self.pos().y())
        else:
            self.secondWind.move(0,0)

    def move_center(self):
        width = ((QDesktopWidget().availableGeometry().width()/2) - (self.width()/2)) + self.secondWind.width()/2
        height = (QDesktopWidget().availableGeometry().height()/2) - (self.height()/2)
        self.move(width, height)
        self.move_green_screen_wind()

app = QtWidgets.QApplication(sys.argv)
a_window = Window()
os._exit(app.exec_())
