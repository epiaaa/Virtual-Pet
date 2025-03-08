from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

from .components.menu_window import MenuWindow
from .components.status_window import StatusWindow


class PetWindow(QMainWindow):
    closed = pyqtSignal()
    feed = pyqtSignal(str, bool)

    def __init__(self, position):
        super().__init__()
        self.position = position
        self.__initUI__()

    def __initUI__(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setGeometry(self.position[0], self.position[1], 152, 185)
        self.setAcceptDrops(True)

        self.pet_label = QLabel(self)
        self.pet_label.setGeometry(0, 0, 152, 185)
        self.pet_label.setScaledContents(True)
        self.pet_label.setAlignment(Qt.AlignCenter)
        # self.pet_label.setStyleSheet("background: red;")  # 调试背景颜色
        self.pet_label.installEventFilter(self)

        self.menu_window = MenuWindow(self)
        self.status_window = StatusWindow(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
        elif event.button() == Qt.RightButton:
            self.menu_window.show_menu(event.globalPos())
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
        if obj == self.pet_label:
            if event.type() == event.Enter:
                self.status_window.stop_hide_animation()
                self.status_window.status_data.emit()
            elif event.type() == event.Leave:
                self.status_window.hide_status()
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    print("this is Pet_UI.py")


