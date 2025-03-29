from PyQt5.QtCore import Qt, QEvent, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QScrollArea, QVBoxLayout, QScrollBar, QApplication


class SelectMenu(QWidget):
    select_Click = pyqtSignal(str, str)

    def __init__(self, items):
        super().__init__()
        self.items = items
        self.menu = False
        self.__select_menu__init__()

    def __select_menu__init__(self):
        self.__scroll_area_init__()

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.horizontal_scrollbar)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

        self.installEventFilter(self)
        self.hide()

    def __scroll_area_init__(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # 创建一个中间容器
        self.container = QWidget()
        self.scroll_area.setWidget(self.container)

        # 创建布局并设置到 self
        self.layout = QHBoxLayout(self.container)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(8, 5, 8, 5)

        # 创建自定义的水平滚动条
        self.horizontal_scrollbar = QScrollBar(Qt.Horizontal)
        self.horizontal_scrollbar.setStyleSheet("""
            QScrollBar:horizontal {
                background: #75E6EF;
                height: 10px;
            }
            QScrollBar::handle:horizontal {
                background: #F69D0E;
                min-width: 20px;
            }
        """)
        # 将自定义滚动条与 scroll_area 关联
        self.scroll_area.setHorizontalScrollBar(self.horizontal_scrollbar)

    def createSubItems(self, items):
        for item in self.items:
            if item in items:
                option = SubMenuItem(item, items[item])
                option.clicked.connect(lambda x: self.select_clicked(x))
                # option.clicked.connect(lambda x: print(x, 'game_function'))
            else:
                option = SubMenuItem(item, '')
            self.layout.addWidget(option)

    def show_menu(self):
        self.show()
        QApplication.instance().installEventFilter(self)
        self.menu = True

    def hide_menu(self):
        QApplication.instance().removeEventFilter(self)
        self.hide()
        self.menu = False

    def select_clicked(self, item):
        self.select_Click.emit(item, 'game_function')
        self.hide_menu()

    def eventFilter(self, obj, event):
        if self.menu and event.type() == QEvent.MouseButtonPress:
            local_pos = self.mapFromGlobal(event.globalPos())
            # 判断点击位置是否在菜单区域外
            if not self.rect().contains(local_pos):
                # print("点击外部关闭菜单")
                self.hide_menu()
                return True  # 阻止事件继续传递
        return super().eventFilter(obj, event)


class SubMenuItem(QWidget):
    clicked = pyqtSignal(str)

    def __init__(self, name, path):
        super().__init__()
        self.name = name
        self.path = path
        self.__select_submenu_init__()

    def __select_submenu_init__(self):
        self.setFixedSize(100, 120)

        self.txt = QLabel(self.name, self)
        self.txt.setFixedHeight(20)
        self.txt.setFont(QFont('Arial', 11))
        self.txt.setAlignment(Qt.AlignCenter)

        pix = QPixmap(self.path)
        self.pic = QLabel(self)
        self.pic.setPixmap(pix)
        self.pic.setScaledContents(True)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.pic)
        self.layout.addWidget(self.txt)
        self.setLayout(self.layout)
        # print(f'select_menu.py SubMenuItem init print: {self.item}')

    def mousePressEvent(self, event):
        self.clicked.emit(self.name)


if __name__ == '__main__':
    print('this is select_menu.py')
    import sys
    app = QApplication(sys.argv)
    window = SelectMenu(['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7', 'item8', 'item9', 'item10', 'item11',])
    window.show()
    sys.exit(app.exec_())
