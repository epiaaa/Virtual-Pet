import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QBrush, QPainterPath, QFont


class BubbleMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.subItems = []
        self.initUI()
        self.isExpanded = False

    def initUI(self):
        # 主按钮设置
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(60, 60)

        # 初始位置居中
        screen = QDesktopWidget().availableGeometry()
        self.move(screen.width() // 2 - 30, screen.height() // 2 - 30)

        # 创建子菜单项
        self.createSubItems(["🏠", "📷", "📧", "⚙️", "❤️"])

        self.show()

    def createSubItems(self, icons):
        angle_step = 360 / len(icons)
        for i, icon in enumerate(icons):
            item = SubMenuItem(icon, self)
            item.clicked.connect(lambda x=icon: self.handleClick(x))
            self.subItems.append(item)

            # 初始位置与主按钮重合
            item.move(self.pos())
            item.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制主按钮
        path = QPainterPath()
        path.addEllipse(0, 0, 60, 60)

        # 添加高光效果
        gradient = QRadialGradient(30, 30, 30)
        gradient.setColorAt(0, QColor(100, 180, 255, 200))
        gradient.setColorAt(1, QColor(50, 120, 200, 200))

        painter.fillPath(path, QBrush(gradient))

        # 绘制菜单图标
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 24))
        painter.drawText(self.rect(), Qt.AlignCenter, "＋")

    def mousePressEvent(self, event):
        if self.isExpanded:
            self.collapseMenu()
        else:
            self.expandMenu()

    def expandMenu(self):
        self.isExpanded = True
        radius = 100  # 展开半径
        angle_step = 360 / len(self.subItems)

        for i, item in enumerate(self.subItems):
            angle = math.radians(i * angle_step)
            x = self.x() + 30 + radius * math.cos(angle) - 25
            y = self.y() + 30 + radius * math.sin(angle) - 25

            # 显示并启动动画
            item.show()
            anim = QPropertyAnimation(item, b"pos")
            anim.setDuration(500)
            anim.setStartValue(self.pos())
            anim.setEndValue(QPoint(int(x), int(y)))
            anim.setEasingCurve(QEasingCurve.OutBack)
            anim.start()

    def collapseMenu(self):
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


class SubMenuItem(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, icon, parent=None):
        super().__init__(parent)
        self.icon = icon
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(50, 50)

        # 悬停动画准备
        self.scale = 1.0
        self.normalColor = QColor(255, 255, 255, 200)
        self.hoverColor = QColor(255, 220, 100, 220)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 动态缩放
        painter.scale(self.scale, self.scale)
        offset = (1 - self.scale) * 25

        # 绘制背景
        path = QPainterPath()
        path.addEllipse(0, 0, 50, 50)
        gradient = QRadialGradient(25, 25, 25)
        gradient.setColorAt(0, self.hoverColor if self.underMouse() else self.normalColor)
        gradient.setColorAt(1, QColor(200, 200, 200, 100))
        painter.fillPath(path, QBrush(gradient))

        # 绘制图标
        painter.setPen(Qt.darkGray)
        painter.setFont(QFont("Arial", 20))
        painter.drawText(5, 5, 40, 40, Qt.AlignCenter, self.icon)

    def enterEvent(self, event):
        self.animateScale(1.2)

    def leaveEvent(self, event):
        self.animateScale(1.0)

    def mousePressEvent(self, event):
        self.clicked.emit(self.icon)
        self.animateClick()

    def animateScale(self, target):
        anim = QPropertyAnimation(self, b"scale")
        anim.setDuration(200)
        anim.setStartValue(self.scale)
        anim.setEndValue(target)
        anim.start()

    def animateClick(self):
        anim = QPropertyAnimation(self, b"scale")
        anim.setDuration(100)
        anim.setStartValue(1.0)
        anim.setEndValue(0.8)
        anim.setEasingCurve(QEasingCurve.OutQuad)
        anim.start()

    def setScale(self, value):
        self.scale = value
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = BubbleMenu()
    sys.exit(app.exec_())