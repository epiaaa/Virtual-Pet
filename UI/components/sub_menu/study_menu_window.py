from PyQt5.QtCore import Qt
from .bubble_menu import BubbleMenu


class StudyMenuWindow(BubbleMenu):
    def __init__(self, pet_window):
        super().__init__(["学习", "打工", "玩游戏"])
        self.pet_window = pet_window
        # print(self.position)
        self.__initUI__()

    def __initUI__(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setStyleSheet("background: yellow;")  # 调试背景颜色

        self.position = self.pet_window.position
        width = self.pet_window.width()*3
        height = self.pet_window.width()*2

        # print(f"study_menu_window.show_menu has a Bug{self.position}")
        self.setGeometry(self.position[0]-width//2+self.pet_window.width()//2,
                         self.position[1]-height//2+self.pet_window.height()//2,
                         width,
                         height)



