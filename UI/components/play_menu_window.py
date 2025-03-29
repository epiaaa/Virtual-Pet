from PyQt5.QtCore import Qt, pyqtSignal

from UI.framework.bubble_menu import BubbleMenu


class PlayMenuWindow(BubbleMenu):

    def __init__(self):
        super().__init__(['X学习', 'X打工', '玩游戏'])
        self.__play_menu_init__()

    def __play_menu_init__(self):
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setStyleSheet("background: yellow;")  # 调试背景颜色
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.hide()

    def show_menu(self):
        self.show()
        self.expandMenu()

    # def mousePressEvent(self, event):
    #     """
    #     :param event:
    #     :return:
    #     """
    #     print(f"bubble_menu.py BubbleMenu mousePressEvent print: mouse is pressed")
    #     super().mousePressEvent(event)

    # def eventFilter(self, obj, event):
    #     if obj == self:
    #         if event.type() == QEvent.MouseButtonPress:
    #             print(f"bubble_menu.py BubbleMenu eventFilter print:")
    #             if not self.isExpanded:
    #                 print(f"bubble_menu.py eventFilter: 4")
    #                 return super().eventFilter(obj, event)
    #
    #             print(f"bubble_menu.py eventFilter: print: {self.isExpanded}")
    #             pos = event.globalPos()
    #             if not self.geometry().contains(pos):
    #                 self.close_menu()
    #         # print(f"bubble_menu.py eventFilter: {event.type()}")
    #     return super().eventFilter(obj, event)

