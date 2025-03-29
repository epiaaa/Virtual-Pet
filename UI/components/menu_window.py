from PyQt5.QtWidgets import QAction, QMenu
from ..settings_window import SettingsWindow
from ..chat_window import ChatWindow


class MenuWindow(QMenu):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_Menu()

    def init_Menu(self):
        self.settings_window = SettingsWindow()
        self.chatting_window = ChatWindow()

        action_play = QAction("玩法", self)
        action_play.triggered.connect(self.parent.play_menu.show_menu)

        action_mall = QAction("X商场", self)
        action_backpack = QAction("X背包", self)

        action_chat = QAction("聊天", self)
        action_chat.triggered.connect(self.chatting_window.chat_window_show)

        action_settings = QAction("设置", self)
        action_settings.triggered.connect(self.settings_window.settings_window_show)

        action_exit = QAction("退出", self)
        action_exit.triggered.connect(self.parent.close)

        self.addAction(action_play)
        self.addAction(action_mall)
        self.addAction(action_backpack)
        self.addAction(action_chat)
        self.addSeparator()
        self.addAction(action_settings)
        self.addSeparator()
        self.addAction(action_exit)

    def show_menu(self, pos):
        self.exec_(pos)
