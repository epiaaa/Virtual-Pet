from PyQt5.QtWidgets import QAction, QMenu
from .sub_menu.study_menu_window import StudyMenuWindow


class MenuWindow(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.__initUI__()

    def __initUI__(self):
        self.study_menus = StudyMenuWindow(self.parent)

        action_study = QAction("活动", self)
        action_study.triggered.connect(self.study_menus.show_menu)

        action_work = QAction("X打工", self)
        action_game = QAction("X小游戏", self)
        action_settings = QAction("X设置", self)

        action_exit = QAction("退出", self)
        action_exit.triggered.connect(self.parent.close)

        self.addAction(action_study)
        self.addAction(action_work)
        self.addAction(action_game)
        self.addAction(action_settings)
        self.addSeparator()
        self.addAction(action_exit)

    def show_menu(self, pos):
        self.exec_(pos)

