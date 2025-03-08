import sys

from PyQt5.QtWidgets import QApplication
from UI import PetWindow
from core.pet import PetModel
import presenters

if __name__ == "__main__":
    print("main.py")
    app = QApplication(sys.argv)

    pet_model = PetModel()
    pet_window = PetWindow()

    presenter = presenters.PetPresenter(pet_model, pet_window)

    pet_window.show()
    sys.exit(app.exec_())

