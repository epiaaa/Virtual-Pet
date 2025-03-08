import os
import threading

from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication

from core.pet import PetModel
from UI import PetWindow


class PetPresenter:

    def __init__(self, data, ui):
        self.data = data
        self.ui = ui
        self.load_animation()

        self.ui.closed.connect(self.on_window_closed)
        self.ui.feed.connect(self.feed_pet)
        self.ui.status_window.status_data.connect(self.show_status)

        self.init_timer()

    def load_animation(self):
        gif_path = r"./core/pet/pictures/bird.gif"

        if not os.path.exists(gif_path):
            raise FileNotFoundError(f"GIF 文件路径不存在: {gif_path}")

        self.movie = QMovie(gif_path)
        if not self.movie.isValid():
            raise FileNotFoundError("无法加载GIF文件")

        self.ui.pet_label.setMovie(self.movie)
        self.movie.start()

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
        self.data.hunger = min(self.data.hunger + 1, 100)
        if remove_file:
            os.remove(file_path)
        # print(self.data.hunger)

    def show_status(self):
        data = {
            "hunger": self.data.hunger,
            "experience": self.data.experience,
            "mood": self.data.mood,
        }

        self.ui.status_window.show_status(data)

    def on_window_closed(self):
        self.data.position = [self.ui.x(), self.ui.y()]
        self.stop_timer()
        self.data.save_Pet_infos()


if __name__ == '__main__':
    print("this is presenters")
    import sys

    app = QApplication(sys.argv)

    pet_model = PetModel()
    pet_window = PetWindow(pet_model.position)

    presenter = PetPresenter(pet_model, pet_window)

    pet_window.show()
    sys.exit(app.exec_())
