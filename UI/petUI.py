import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMenu, QAction, QDialog, QVBoxLayout, QProgressBar
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5.QtGui import QMovie, QDragEnterEvent, QDropEvent, QFont


class PetWindow(QMainWindow):
    _timer = None  # 类变量
    instances = []  # 类变量，用于存储所有实例

    @classmethod
    def start_timer(cls):
        if cls._timer is None:
            cls._timer = QTimer()
            cls._timer.timeout.connect(cls.loss_of_time_handler)
            cls._timer.start(1000 * 60)

    @staticmethod
    def loss_of_time_handler():
        for instance in PetWindow.instances:
            instance.loss_of_time()

    def __init__(self, pet_model):
        super().__init__()
        self.pet_model = pet_model
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setStyleSheet("background: yellow;")
        self.setGeometry(self.pet_model.position[0], self.pet_model.position[1], 304, 370)
        self.setAcceptDrops(True)

        self.load_animation()

        self.status_label_init()
        PetWindow.instances.append(self.pet_model)
        PetWindow.start_timer()
        # self.show_status()

    def load_animation(self):
        self.movie = QMovie(r"../core/pet/pictures/bird.gif")
        if not self.movie.isValid():
            raise FileNotFoundError("无法加载GIF文件")
        self.movie.jumpToFrame(0)
        movie_width = self.movie.frameRect().size().width()
        movie_height = self.movie.frameRect().size().height()

        self.label = QLabel(self)
        self.label.setGeometry(int((self.width() - movie_width) / 2), int((self.height() - movie_height) / 2),
                               movie_width, movie_height)
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignCenter)
        # self.label.setStyleSheet("background: red;")  # 设置标签透明
        self.label.installEventFilter(self)  # 连接鼠标悬停事件
        self.label.setMovie(self.movie)
        self.movie.start()
        # 调试信息输出
        # print("GIF尺寸:", self.movie.frameRect().size())
        # print("总帧数:", self.movie.frameCount())

    def show_context_menu(self, pos):
        context_menu = QMenu(self)
        action1 = QAction("test1", self)
        action2 = QAction("test2", self)
        action3 = QAction("退出", self)
        action3.triggered.connect(self.close)

        context_menu.addAction(action1)
        context_menu.addAction(action2)
        context_menu.addSeparator()
        context_menu.addAction(action3)

        context_menu.exec_(pos)

    def status_label_init(self):
        self.status_label = QLabel(self)
        # self.status_label.setGeometry(self.label.x(), self.label.y(), int(self.width()/2), 30)
        # self.status_label.setStyleSheet('background: blue;')
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # font = QFont()
        # font.setPointSize(8)

        self.mood_progress = QProgressBar()
        # self.mood_progress.setTextVisible(True)
        # self.mood_progress.setFont(font)
        self.mood_progress.setStyleSheet("""
            QProgressBar {
                text-align: center;
                font-size: 12px;
                color: black;
                border: none;
            }
        """)

        self.hunger_progress = QProgressBar()
        # self.hunger_progress.setTextVisible(True)
        # self.hunger_progress.setFont(font)
        self.hunger_progress.setStyleSheet("""
            QProgressBar {
                text-align: center;
                font-size: 12px;
                color: black;
                border: none;
            }
        """)

        layout.addWidget(self.mood_progress)
        layout.addWidget(self.hunger_progress)
        self.status_label.setLayout(layout)

        self.status_label.hide()

    def show_status(self):
        self.mood_progress.setFormat(f"😊心情值:{self.pet_model.mood}/100")
        self.mood_progress.setValue(self.pet_model.mood)
        self.hunger_progress.setFormat(f"🍔饱食度:{self.pet_model.hunger}/100")
        self.hunger_progress.setValue(self.pet_model.hunger)

        self.status_label.show()

    def hide_status(self):
        self.status_label.hide()
        # self.animation.setDuration(3000)  # 动画持续时间 3 秒
        # self.animation.setStartValue(1.0)  # 起始不透明度
        # self.animation.setEndValue(0.0)  # 结束不透明度
        # self.animation.setEasingCurve(QEasingCurve.Linear)  # 线性渐变
        # self.animation.finished.connect(self.status_label.hide)
        # self.animation.start()

    def closeEvent(self, event):
        self.pet_model.position = [self.x(), self.y()]
        self.pet_model.save_Pet_infos()
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
        elif event.button() == Qt.RightButton:
            self.show_context_menu(event.globalPos())

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.feed_pet(file_path, True)
            event.acceptProposedAction()

    def feed_pet(self, file_path, remove_file=False):
        # print(f"喂食文件: {file_path}")
        self.pet_model.hunger = min(self.pet_model.hunger + 1, 100)
        if remove_file:
            os.remove(file_path)

    def eventFilter(self, obj, event):
        if obj == self.label:
            if event.type() == event.Enter:
                self.show_status()
            elif event.type() == event.Leave:
                self.hide_status()
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    print("this is Pet_UI.py")
    import sys
    from core.pet.model import PetModel
    Pet = PetModel()
    app = QApplication(sys.argv)
    pet_window = PetWindow(Pet)
    pet_window.show()
    sys.exit(app.exec_())
