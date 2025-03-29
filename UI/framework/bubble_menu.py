import math

from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, pyqtSignal, QEvent
from PyQt5.QtGui import QColor, QPainter, QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication


class BubbleMenu(QWidget):
    handleClick = pyqtSignal(str, str)

    def __init__(self, actions):
        super().__init__()
        self.isExpanded = False
        self.actions = actions
        self.subItems = []
        self.subItems_anim = []

        self.initUI()

    def initUI(self):
        self.createSubItems()
        self.installEventFilter(self)

    def createSubItems(self):
        for action in self.actions:
            item = SubMenuItem(action, parent=self)
            item.clicked.connect(lambda x: self.handleClick.emit(x, 'type'))
            self.subItems.append(item)

            # item.move(self.pos())
            # item.hide()

    def expandMenu(self):
        self.isExpanded = True
        self.subItems_anim = []
        radius = 120  # 展开半径
        angle_step = 180 / (len(self.subItems) - 1)

        for i, item in enumerate(self.subItems):
            angle = math.radians(i * angle_step)
            x = self.width() // 2 - radius * math.cos(angle) - item.width // 2
            y = self.height() // 2 - radius * math.sin(angle) - item.height // 2

            x = int(x)
            y = int(y)
            item.move(x, y)

            # 显示并启动动画
            item.show()
            anim = QPropertyAnimation(item, b"pos")
            anim.setDuration(500)
            anim.setStartValue(QPoint(self.width() // 2 - item.width // 2,
                                      self.height() // 2 - item.height // 2))
            anim.setEndValue(QPoint(x, y))
            anim.setEasingCurve(QEasingCurve.OutQuad)
            anim.start()
            self.subItems_anim.append(anim)

        QApplication.instance().installEventFilter(self)

    def collapseMenu(self):
        self.isExpanded = False
        self.subItems_anim = []
        for item in self.subItems:
            anim = QPropertyAnimation(item, b"pos")
            anim.setDuration(500)
            anim.setStartValue(item.pos())
            anim.setEndValue(QPoint(self.width() // 2 - item.width // 2,
                                    self.height() // 2 - item.height // 2))
            anim.finished.connect(item.hide)
            anim.start()
            self.subItems_anim.append(anim)

    def close_menu(self):
        QApplication.instance().removeEventFilter(self)
        self.collapseMenu()
        self.subItems_anim[-1].finished.connect(self.close)

    # def handleClick(self, item):
    #
    #     print(f"bubble_menu.py handleClick: print: Selected: {item}, the next action is ?")
    #     print(f"bubble_menu.py handleClick: print: {self.parent})")

    def eventFilter(self, obj, event):
        if self.isExpanded and event.type() == QEvent.MouseButtonPress:
            self.close_menu()
        return super().eventFilter(obj, event)


class SubMenuItem(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, action, parent=None):
        super().__init__(parent)
        self.action = action
        self.animate = None
        self.initUI()

    def initUI(self):
        self.width = len(self.action) * 40
        self.height = 100
        self.setFixedSize(self.width, self.height)

        self.scale = 1.0
        self.normalColor = QColor(200, 200, 200, 200)
        self.hoverColor = QColor(50, 50, 50, 220)

    def setScale(self, value):
        self.scale = value
        self.update()

    def animateScale(self, target):
        self.animate = QPropertyAnimation(self, b"scale")
        self.animate.setDuration(500)
        self.animate.setStartValue(self.scale)
        self.animate.setEndValue(target)
        self.animate.start()

    def animateClick(self):
        self.animate = QPropertyAnimation(self, b"scale")
        self.animate.setDuration(500)
        self.animate.setStartValue(1.0)
        self.animate.setEndValue(0.5)
        self.animate.setEasingCurve(QEasingCurve.OutQuad)
        self.animate.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 动态缩放
        painter.scale(self.scale, self.scale)

        # 图片作为背景
        pixmap = QPixmap("assets/bubble_cloud.png")
        if not pixmap.isNull():
            # 缩放图片以适应窗口大小
            scaled_pixmap = pixmap.scaled(self.width, self.height, Qt.IgnoreAspectRatio,
                                          Qt.SmoothTransformation)
            painter.drawPixmap(8, -10, scaled_pixmap)
        # brush = QBrush(pixmap)
        # self.setAutoFillBackground(True)
        # palette = self.palette()
        # palette.setBrush(self.backgroundRole(), brush)
        # self.setPalette(palette)

        # 笔刷绘制背景
        # path = QPainterPath()
        # path.addEllipse(0, 0, self.width, self.height)
        #
        # # 高光
        # gradient = QRadialGradient(50, 50, 50)
        # gradient.setColorAt(0, self.hoverColor if self.underMouse() else self.normalColor)
        # gradient.setColorAt(1, QColor(200, 200, 200, 220))
        #
        # painter.fillPath(path, QBrush(gradient))

        # 绘制图标
        painter.setPen(Qt.red)
        painter.setFont(QFont("Arial", 12))
        painter.drawText(0, 0, self.width, self.height, Qt.AlignCenter, self.action)

    # def enterEvent(self, event):
    #     super().enterEvent(event)
    #     self.animateScale(1.2)
    #
    # def leaveEvent(self, event):
    #     super().leaveEvent(event)
    #     self.animateScale(1.0)

    def mousePressEvent(self, event):
        self.clicked.emit(self.action)
        self.animateClick()


if __name__ == "__main__":
    print("this is bubble_menu.py")
