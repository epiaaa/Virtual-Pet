import os
import sys
import threading

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication

from core import *
from UI import *


class PetPresenter:

    def __init__(self, data, ui):
        self.data = data
        self.ui = ui
        self.ai = Conversation(self.data.config['API'], data.config['base_url'])
        self.load_animation()
        self.__presenter_init__()

    def __presenter_init__(self):
        self.ui.game_menu.createSubItems(self.data.launch["picture_path"], )

        self.ui.closed.connect(self.on_window_closed)
        self.ui.feed.connect(self.feed_pet)
        self.ui.status.status_data.connect(self.show_status)
        self.ui.play_menu.handleClick.connect(self.get_play)
        self.ui.game_menu.select_Click.connect(self.get_play)

        self.ui.menu.settings_window.config_get.connect(self.settings_window_get_data)
        self.ui.menu.settings_window.config_save.connect(self.settings_window_save_data)
        self.ui.menu.chatting_window.ai_chat.connect(self.ai_chatting)

        self.init_timer()

        self.blowing_bubbles = BlowingBubbles()
        self._resolve_methods()

    def load_animation(self):
        gif_path = r"assets/pet/stand.gif"

        if not os.path.exists(gif_path):
            raise FileNotFoundError(f"GIF 文件路径不存在: {gif_path}")

        # print(QPixmap(gif_path).size())

        # self.ui.setGeometry(self.data.infos['position'][0],
        #                  self.data.infos['position'][1],
        #                  QPixmap(gif_path).size().width(),
        #                  QPixmap(gif_path).size().height())

        self.movie = QMovie(gif_path)
        if not self.movie.isValid():
            raise FileNotFoundError("无法加载GIF文件")

        self.ui.pet.set_movie(self.movie)

    def _resolve_methods(self):
        for i in ['type', 'game_function']:
            for key, path in self.data.launch[i].items():
                parts = path.split(".")
                obj = self
                for part in parts:
                    obj = getattr(obj, part, None)
                    if obj is None:
                        break
                if callable(obj):
                    self.data.launch[i][key] = obj
                else:
                    self.data.launch[i][key] = None

    def init_timer(self):
        self.thread = threading.Timer(120, self.over_time_thread)
        self.thread.start()

    def over_time_thread(self):
        self.thread = threading.Timer(120, self.over_time_thread)
        self.thread.start()
        self.data.over_time()

    def stop_timer(self):
        if self.thread.is_alive():
            self.thread.cancel()

    def feed_pet(self, file_path, remove_file=False):
        # print(f"喂食文件: {file_path}")
        self.data.infos['hunger'] = min(self.data.infos['hunger'] + 1, 100)
        if remove_file:
            os.remove(file_path)
        # print(self.data.hunger)

    def show_status(self):
        """
        显示状态栏
        :return:
        """
        data = {
            "hunger": self.data.infos["hunger"],
            "experience": self.data.infos["experience"],
            "mood": self.data.infos["mood"],
        }

        self.ui.status.show_status(data)

    def get_play(self, play_name, attr_name):
        # print(f"presenters.py get_play: 接收到参数 - play_name: {play_name}")
        if play_name in self.data.launch[attr_name]:
            method = self.data.launch[attr_name][play_name]
            if callable(method):
                # print(f"正在执行 {play_name} 对应的方法")
                method()
            else:
                print(f"错误：{play_name} 对应的方法不可调用")
        else:
            print(f"错误：未找到 {play_name} 对应的动作")

    def get_settings(self, configs):
        """
        获取 config.json 中的配置
        :param configs: 要获取配置名
        :return: 字典：{配置名：配置值}
        """
        res = {}
        for key in configs:
            if key in self.data.config:
                res[key] = self.data.config[key]
            else:
                print(f"错误：未找到 {key} ")
        return res

    def settings_window_get_data(self, option):
        data = {}
        if option == "常规":
            # data = self.get_settings([''])
            self.ui.menu.settings_window.standing_content(**data)
        elif option == "配置":
            data = self.get_settings(['API'])
            self.ui.menu.settings_window.config_content(**data)
        elif option == "关于":
            data = self.get_settings(['version', 'url'])
            self.ui.menu.settings_window.about_content(**data)
        else:
            # data = self.get_settings([''])
            self.ui.menu.settings_window.other_content(**data)

    def settings_window_save_data(self, data):
        for key in data:
            self.data.config[key] = data[key]
        self.data.update_config()

    def on_window_closed(self):
        self.data.infos['position'] = [self.ui.x(), self.ui.y()]
        self.stop_timer()
        self.data.save_Pet_infos()
        print("宠物退出")

    def ai_chatting(self, text):
        response = self.ai.conversation(text, model='deepseek-chat', stream=False, print_content=False)
        self.ui.menu.chatting_window.resMessage(response)


def presenter_start():
    app = QApplication(sys.argv)

    data = PetModel()
    position = QPoint(data.infos['position'][0], data.infos['position'][1])
    UI = MainWindow(position)

    presenter = PetPresenter(data, UI)

    UI.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    print("this is presenters")
    presenter_start()
