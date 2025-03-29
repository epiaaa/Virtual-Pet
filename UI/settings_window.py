from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout, QLabel, QLineEdit


class SettingsWindow(QWidget):
    config_get = pyqtSignal(str)
    config_save = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.option_buttons = []
        self.selected_button = None
        self.__set_window_init__()

    def __set_window_init__(self):
        self.setFixedSize(1000, 600)
        self.setWindowTitle('设置')
        self.setStyleSheet("QWidget{background-color:white;font-family:SimSun;font-size: 18px;}")

        self.options_layout = QVBoxLayout()
        self.options_layout.setContentsMargins(0, 0, 0, 0)
        self.options_layout.setSpacing(0)
        self.create_buttons(['常规', '配置', 'X测试', 'X测试', 'X设置', '关于'])

        self.content = QWidget()
        self.content.setStyleSheet("QWidget{font-family:SimSun;font-size: 18px;}")

        self.main_layout = QGridLayout()
        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 3)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(0, 0, 20, 0)

    def settings_window_show(self, init=0):
        self.update_selected_button(self.option_buttons[init])
        self.show()

    def create_buttons(self, button_names):
        for button_name in button_names:
            button = OptionButton(f'{button_name}', self)
            self.option_buttons.append(button)
            self.options_layout.addWidget(button)

    def update_selected_button(self, button):
        if self.selected_button:
            self.selected_button.setStyleSheet("QPushButton{background-color:#E3E3E3;border-radius:10px;"
                                               "color:#666666}")
        self.selected_button = button
        self.selected_button.setStyleSheet("QPushButton{background-color:white;border-radius:10px;"
                                           "color:black}")
        self.update_content(button.text())

    def update_content(self, option):
        self.parts = []
        self.content_layout = QVBoxLayout()
        self.content_layout.setAlignment(Qt.AlignTop)

        self.config_get.emit(option)

        for part in self.parts:
            self.content_layout.addWidget(part)
        self.content = QWidget()
        self.content.setLayout(self.content_layout)
        self.main_layout.addLayout(self.options_layout, 0, 0)
        self.main_layout.addWidget(self.content, 0, 1)
        self.setLayout(self.main_layout)

    def standing_content(self, **kwargs):
        self.other_content(**kwargs)

    def config_content(self, **kwargs):
        label = QLabel()
        label.setText('DeepSeek API Key')
        self.parts.append(label)

        lineEdit = QLineEdit()
        lineEdit.setText(kwargs['API'])
        lineEdit.textChanged.connect(self.save_event)

        self.parts.append(lineEdit)

    def about_content(self, **kwargs):
        label = QLabel()
        label.setText('开发者： epi')
        label2 = QLabel()
        label2.setText(f'版本： v {kwargs["version"]}')
        url_label = QLabel()
        url_label.setText(f'Github： <a href="{kwargs["url"]}">{kwargs["url"]}</a>')
        url_label.setOpenExternalLinks(True)
        self.parts.append(label)
        self.parts.append(label2)
        self.parts.append(url_label)

    def other_content(self, **kwargs):
        label = QLabel()
        label.setText('这里什么也没有')
        self.parts.append(label)

    def save_event(self, data):
        self.config_save.emit({'API': data})

class OptionButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__()
        self.parent = parent
        self.setText(text)
        self.setFixedHeight(100)
        self.setStyleSheet("QPushButton{background-color:#E3E3E3;border-radius:10px;"
                           "color:#666666}")
        self.clicked.connect(self.clicked_event)

    def clicked_event(self):
        if self.parent:
            self.parent.update_selected_button(self)


if __name__ == '__main__':
    print("this is settings_window.py")
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec_())
