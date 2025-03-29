from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

from .components import *


class MainWindow(QMainWindow):
    closed = pyqtSignal()
    feed = pyqtSignal(str, bool)

    def __init__(self, position):
        super().__init__()
        self.position = position
        self.PetWindow_init()

    def PetWindow_init(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # 窗口无边框
        self.setAcceptDrops(True)  # 允许拖拽
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setStyleSheet("background: red;")  # 调试背景颜色
        self.setGeometry(self.position.x(), self.position.y(), 500, 500)

        self.pet = PetWindow()
        self.pet.setGeometry(150, 150, 200, 200)
        self.pet.installEventFilter(self)

        self.play_menu = PlayMenuWindow()
        self.play_menu.setFixedSize(self.size())

        self.menu = MenuWindow(self)

        # 状态栏固定长度180
        self.status = StatusWindow()
        self.status.move(160, 120)

        self.game_menu = GameMenuWindow(['吹泡泡', '猜数字', 'Xtest', 'Xtest', 'Xtest', 'Xtest'])

        self.pet.setParent(self)
        self.menu.setParent(self)
        self.status.setParent(self)
        self.play_menu.setParent(self)
        self.game_menu.setParent(self)

    def mousePressEvent(self, event):
        """
        :param event:
        :return:
        """
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
        elif event.button() == Qt.RightButton:
            self.menu.show_menu(event.globalPos())
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.feed.emit(file_path, True)
            event.acceptProposedAction()

    def eventFilter(self, obj, event):
        if obj == self.pet:
            if event.type() == event.Enter:
                self.status.stop_hide_animation()
                self.status.status_data.emit()
            elif event.type() == event.Leave:
                self.status.hide_status()
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    print("this is Pet_UI.py")
