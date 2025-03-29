from PyQt5.QtCore import Qt
from ..framework import SelectMenu


class GameMenuWindow(SelectMenu):
    def __init__(self, games):
        super().__init__(games)
        self.__game_menu_window_init__()

    def __game_menu_window_init__(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # self.setAttribute(Qt.WA_TranslucentBackground, False)

        self.setStyleSheet("""
            background: rgba(14, 234, 246, 0.5);
            border-radius: 10px;
            margin: 0px;
        """)
        self.setGeometry(0, 300, 500, 150)


if __name__ == '__main__':
    print('this is game_menu_window.py')
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = GameMenuWindow(['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7', 'item8', 'item9', 'item10', 'item11',])
    window.show()
    sys.exit(app.exec_())
