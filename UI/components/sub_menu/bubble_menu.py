import math

from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve, pyqtSignal, QEvent
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QRadialGradient, QBrush, QFont
from PyQt5.QtWidgets import QWidget


class BubbleMenu(QWidget):

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
            item.clicked.connect(lambda x=action: self.handleClick(x))
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

    def show_menu(self):
        self.show()
        self.expandMenu()

    def close_menu(self):
        self.collapseMenu()
        self.subItems_anim[-1].finished.connect(self.close)

    def handleClick(self, action):
        print(f"bubble_menu.py handleClick: print: Selected: {action}, the next action is ?")
        self.close_menu()

    # def eventFilter(self, obj, event):
    #     if event.type() == QEvent.MouseButtonPress:
    #         print(f"bubble_menu.py eventFilter: print: {self.isExpanded}")
    #         if not self.isExpanded:
    #             return super().eventFilter(obj, event)
    #
    #     pos = event.globalPos()
    #     if not self.geometry().contains(pos):
    #         self.close_menu()
    #         return True


class SubMenuItem(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, action, position=None, parent=None):
        super().__init__(parent)
        if position is None:
            position = [0, 0]
        self.position = position
        self.action = action
        self.animate = None
        self.initUI()

    def initUI(self):
        self.width = len(self.action) * 30
        self.height = 50
        self.setGeometry(self.position[0], self.position[1],
                         self.width, self.height)

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

        # 绘制背景
        path = QPainterPath()
        path.addEllipse(0, 0, self.width, self.height)

        # 高光
        gradient = QRadialGradient(50, 50, 50)
        gradient.setColorAt(0, self.hoverColor if self.underMouse() else self.normalColor)
        gradient.setColorAt(1, QColor(200, 200, 200, 220))

        painter.fillPath(path, QBrush(gradient))

        # 绘制图标
        painter.setPen(Qt.red)
        painter.setFont(QFont("Arial", 12))
        painter.drawText(0, 0, self.width, self.height, Qt.AlignCenter, self.action)

    def enterEvent(self, event):
        super().enterEvent(event)  # 确保调用父类的 enterEvent
        # print("bubble_menu.py enterEvent: print: enterEvent")
        self.animateScale(1.2)

    def leaveEvent(self, event):
        super().leaveEvent(event)  # 确保调用父类的 enterEvent
        # print("bubble_menu.py leaveEvent: print: leaveEvent")
        self.animateScale(1.0)

    def mousePressEvent(self, event):
        self.clicked.emit(self.action)
        self.animateClick()


if __name__ == "__main__":
    print("this is bubble_menu.py")
