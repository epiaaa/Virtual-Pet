from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel


class PetWindow(QLabel):
    def __init__(self):
        super().__init__()
        self.PetWindow_init()

    def PetWindow_init(self):
        self.setScaledContents(True)  # 图片自适应
        # self.setStyleSheet("background: blue;")  # 调试背景颜色
        self.setAlignment(Qt.AlignCenter)  # 设置居中
        self.installEventFilter(self)

    def set_movie(self, movie):
        self.setMovie(movie)
        movie.start()
