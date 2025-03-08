import math

from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QRadialGradient, QBrush, QFont
from PyQt5.QtWidgets import QWidget


class SubMenuItem(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, action, parent=None):
        super().__init__()
        self.action = action
        self.initUI()

    def initUI(self):
        # self.scale = 1.0
        self.normalColor = QColor(100, 100, 100, 200)
        self.hoverColor = QColor(200, 200, 200, 200)

    def setScale(self, value):
        self.scale = value
        self.update()

    def animateScale(self, target):
        print("animateScale")
        anim = QPropertyAnimation(self, b"scale")
        anim.setDuration(2000)
        anim.setStartValue(self.scale)
        anim.setEndValue(target)
        anim.start()

    def animateClick(self):
        anim = QPropertyAnimation(self, b"scale")
        anim.setDuration(2000)
        anim.setStartValue(1.0)
        anim.setEndValue(0.5)
        anim.setEasingCurve(QEasingCurve.OutQuad)
        anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 动态缩放
        painter.scale(self.scale, self.scale)
        offset = (1 - self.scale) * 25

        # 绘制背景
        path = QPainterPath()
        path.addEllipse(0, 0, 50, 50)
        # 高光
        gradient = QRadialGradient(25, 25, 25)
        gradient.setColorAt(0, self.hoverColor if self.underMouse() else self.normalColor)
        gradient.setColorAt(1, QColor(100, 100, 100, 100))

        painter.fillPath(path, QBrush(gradient))

        # 绘制图标
        painter.setPen(Qt.red)
        painter.setFont(QFont("Arial", 20))
        painter.drawText(0, 0, 20, 20, Qt.AlignCenter, self.action)
        print(f"{self.action} is painted")

    def enterEvent(self, event):
        super().enterEvent(event)  # 确保调用父类的 enterEvent
        self.animateScale(1.2)

    def leaveEvent(self, event):
        super().leaveEvent(event)  # 确保调用父类的 enterEvent
        self.animateScale(1.0)

    def mousePressEvent(self, event):
        self.clicked.emit(self.action)
        self.animateClick()


class BubbleMenu(QWidget):

    def __init__(self, actions):
        super().__init__()
        self.actions = actions
        self.isExpanded = False
        self.subItems = []
        self.initUI()

    def initUI(self):
        self.createSubItems()
        self.expandMenu()
        self.show()

    def createSubItems(self):
        for action in self.actions:
            print(f"{action} is created")
            item = SubMenuItem(action, self)
            item.clicked.connect(lambda x=action: self.handleClick(x))
            self.subItems.append(item)
            item.move(self.pos())
            item.hide()

    def expandMenu(self):
        print("expandMenu")
        self.isExpanded = True
        radius = 50  # 展开半径
        angle_step = 360 / len(self.subItems)

        for i, item in enumerate(self.subItems):
            angle = math.radians(i * angle_step)
            x = self.x() + 30 + radius * math.cos(angle) - 25 + self.width()//2
            y = self.y() + 30 + radius * math.sin(angle) - 25 + self.height()//2

            x = int(x)
            y = int(y)

            item.move(x, y)

            # 显示并启动动画
            item.show()
            anim = QPropertyAnimation(item, b"pos")
            anim.setDuration(3000)
            anim.setStartValue(self.pos())
            anim.setEndValue(QPoint(int(x), int(y)))
            anim.setEasingCurve(QEasingCurve.OutBack)
            anim.start()

    def paintEvent(self, event):
        print("paintEvent")
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制主按钮
        path = QPainterPath()
        path.addEllipse(0, 0, 60, 40)

        # 添加高光效果
        gradient = QRadialGradient(30, 30, 30)
        gradient.setColorAt(0, QColor(100, 100, 100, 200))
        gradient.setColorAt(1, QColor(50, 120, 200, 200))

        painter.fillPath(path, QBrush(gradient))

        # 绘制菜单图标
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 24))
        painter.drawText(self.rect(), Qt.AlignCenter, "＋")
        self.show()

    def paintEvent(self, event):
        for action in self.actions:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            # 动态缩放
            painter.scale(1, 1)
            offset = (1 - 1) * 25

            # 绘制背景
            path = QPainterPath()
            path.addEllipse(0, 0, 50, 50)
            # 高光
            gradient = QRadialGradient(25, 25, 25)
            gradient.setColorAt(0, QColor(100, 100, 100, 100))
            gradient.setColorAt(1, QColor(100, 100, 100, 100))

            painter.fillPath(path, QBrush(gradient))

            # 绘制图标
            painter.setPen(Qt.red)
            painter.setFont(QFont("Arial", 20))
            painter.drawText(0, 0, 80, 40, Qt.AlignCenter, action)
            print(f"{action} is painted")

    def mousePressEvent(self, event):
        if self.isExpanded:
            self.collapseMenu()
        else:
            self.expandMenu()

    def collapseMenu(self):
        print("collapseMenu")
        self.isExpanded = False
        for item in self.subItems:
            anim = QPropertyAnimation(item, b"pos")
            anim.setDuration(300)
            anim.setStartValue(item.pos())
            anim.setEndValue(self.pos())
            anim.finished.connect(item.hide)
            anim.start()

    def handleClick(self, icon):
        print(f"Selected: {icon}")
        self.collapseMenu()


if __name__ == "__main__":
    print("this is bubble_menu.py")
