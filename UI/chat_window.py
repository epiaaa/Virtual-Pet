from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QPixmap, QFont, QTextDocument, QTextOption
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QPushButton, QLineEdit, QHBoxLayout


class ChatWindow(QWidget):
    ai_chat = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.__chat_init__()

    def __chat_init__(self):
        # self.setGeometry(500, 300, 300, 500)
        self.setFixedSize(300, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 窗口无边框
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.chat_area_init()
        self.sendMessage_area_init()

        # ⚪⚫🔴🔵
        self.close_button = QPushButton('🔴')
        self.close_button.setFixedSize(30, 30)
        self.close_button.setStyleSheet("background: transparent;")
        self.close_button.clicked.connect(self.close)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.addWidget(self.close_button, alignment=Qt.AlignRight | Qt.AlignTop)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.sendMessage, alignment=Qt.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 30)
        self.setLayout(main_layout)

    def chat_area_init(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_area.setStyleSheet("background: transparent;border: 0px")

        self.container = QWidget()
        self.scroll_area.setWidget(self.container)

        self.layout = QVBoxLayout(self.container)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(10, 5, 10, 0)
        self.layout.setAlignment(Qt.AlignTop)

        self.layout.addWidget(DialogBox('你好啊，找我有什么事？', self))
        # self.layout.addWidget(DialogBox('你好啊，找我有什么事？你好啊，找我有什么事？', self))
        # self.layout.addWidget(DialogBox('你好啊，找我有什么事？你好啊，找我有什么事？你好啊，找我有什么事？', self))
        # self.layout.addWidget(DialogBox('你好啊，找我有什么事？你好啊，找我有什么事？你好啊，找我有什么事？你好啊，找我有什么事？你好啊，找我有什么事？你好啊，找我有什么事？你好啊，找我有什么事？', self))

    def sendMessage_area_init(self):
        self.sendMessage = QWidget()
        self.sendMessage.setFixedSize(self.width() - 20, 40)
        self.lineEdit = QLineEdit()
        self.lineEdit.setFixedSize(self.width() - 90, 30)
        self.lineEdit.editingFinished.connect(lambda: self.sendMessage_clicked(self.lineEdit.text()))

        sendPushButton = QPushButton('发送')
        sendPushButton.setStyleSheet("background: #77FF01;border-radius: 15px;")
        sendPushButton.setFixedSize(40, 30)
        sendPushButton.clicked.connect(lambda: self.sendMessage_clicked(self.lineEdit.text()))

        sendMessage_layout = QHBoxLayout()
        sendMessage_layout.setSpacing(5)
        sendMessage_layout.addWidget(self.lineEdit)
        sendMessage_layout.addWidget(sendPushButton)
        self.sendMessage.setLayout(sendMessage_layout)

    def chat_window_show(self):
        self.show()

    def sendMessage_clicked(self, text):
        if text:
            print(f'chat_window.py sendMessage_clicked print: {text}')
            # self.layout.addWidget(DialogBox(text, self))
            self.layout.addWidget(DialogBox(text, self, bg_pic=r"assets/chat_dialogbox2.png"))  # 添加对话框到布局
            self.lineEdit.clear()  # 清空输入框
            self.ai_chat.emit(text)
            # 使用 QTimer 延迟执行滚动操作
            QTimer.singleShot(0, self.scroll_to_bottom)

    def resMessage(self, message):
        self.layout.addWidget(DialogBox(message, self))
        QTimer.singleShot(0, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pixmap = QPixmap(r"assets/chat_background.png")
        if pixmap.isNull():
            print("图片加载失败！请检查路径和文件名")
            return
        pixmap = pixmap.scaled(self.width(), self.height())
        painter.drawPixmap(0, 0, pixmap)


class DialogBox(QLabel):
    def __init__(self, text, parent, bg_pic=None):
        super().__init__()
        self.parent = parent
        self.txt = text
        self.bg_pic = bg_pic
        # self.setScaledContents(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        doc = QTextDocument()
        doc.setDefaultFont(QFont("SimSun", 10))
        doc.setTextWidth(self.width() - 20)
        doc.setPlainText(self.txt)
        doc.setDefaultTextOption(QTextOption(Qt.AlignLeft | Qt.AlignVCenter))

        # print(doc.size().height())
        self.setFixedSize(self.parent.width()-20, int(doc.size().height()-18)//6*7+45)
        # if doc.size().height() > 35:
        #     self.setFixedSize(self.parent.width()-20, int(doc.size().height()-7)//23*29+28)
        # else:
        #     self.setFixedSize(doc.size().height(), 29+28)

        if self.bg_pic is None:
            self.bg_pic = r"assets/chat_dialogbox.png"
        pixmap = QPixmap(self.bg_pic)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(self.width(), self.height(), Qt.IgnoreAspectRatio,
                                          Qt.SmoothTransformation)
            painter.drawPixmap(0, 0, scaled_pixmap)
        painter.translate(15, 8)
        doc.drawContents(painter)


if __name__ == '__main__':
    print('this is chat_window.py')
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    chat_window = ChatWindow()
    chat_window.show()
    sys.exit(app.exec_())
