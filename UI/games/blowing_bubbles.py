import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QPoint
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap


class BlowingBubbles:
    def __init__(self):
        self.number = 50

    def create_bubbles(self):
        self.bubble = [Bubble() for _ in range(self.number)]


class Bubble(QWidget):
    def __init__(self):
        super().__init__()
        self.__bubble_init__()

    def __bubble_init__(self):
        # 窗口设置
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 随机参数
        self.diameter = random.randint(30, 80)
        self.speed = QPoint(random.randint(-2, 2), random.randint(-2, 2))
        self.color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 40)

        # 初始位置
        screen_geometry = QApplication.desktop().availableGeometry()
        x = random.randint(0, screen_geometry.width() - self.diameter)
        y = random.randint(0, screen_geometry.height() - self.diameter)
        self.move(x, y)

        # 窗口大小
        self.resize(self.diameter, self.diameter)

        # 加载图片
        self.pixmap = QPixmap(r"assets/game/colored_bubble.png").scaled(self.diameter, self.diameter)

        # 动画定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_bubble)
        self.timer.start(30)
        # 显示窗口
        self.show()

    def bubbles_disappear(self):
        # 渐隐动画
        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(2000)
        self.fade_animation.setStartValue(1.0)
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.finished.connect(self.close)
        self.fade_animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.setBrush(QBrush(self.color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.diameter, self.diameter)

    def move_bubble(self):
        new_pos = self.pos() + self.speed
        screen = QApplication.desktop().availableGeometry()

        # 边界检测
        if new_pos.x() <= 0 or new_pos.x() >= screen.width() - self.diameter:
            self.speed.setX(-self.speed.x())
        if new_pos.y() <= 0 or new_pos.y() >= screen.height() - self.diameter:
            self.speed.setY(-self.speed.y())

        self.move(new_pos)

    def mousePressEvent(self, event):
        self.bubbles_disappear()

    def closeEvent(self, event):
        self.timer.stop()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建多个气泡
    bubbles = BlowingBubbles()
    bubbles.create_bubbles()
    sys.exit(app.exec_())
