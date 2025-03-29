from PyQt5.QtCore import pyqtSignal, QEasingCurve, QPropertyAnimation
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QProgressBar, QGraphicsOpacityEffect


class StatusWindow(QLabel):
    status_data = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.animation = None
        self.init_status()

    def init_status(self):
        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(0, 0, 0, 0)

        self.experience_progress = QProgressBar()
        self.experience_progress.setStyleSheet("""
            QProgressBar {text-align: center;font-size: 12px;color: black;border: none;}
        """)

        self.mood_progress = QProgressBar()
        self.mood_progress.setStyleSheet("""
            QProgressBar {text-align: center;font-size: 12px;color: black;border: none;}
        """)

        self.hunger_progress = QProgressBar()
        self.hunger_progress.setStyleSheet("""
            QProgressBar {text-align: center;font-size: 12px;color: black;border: none;}
        """)

        status_layout.addWidget(self.experience_progress)
        status_layout.addWidget(self.mood_progress)
        status_layout.addWidget(self.hunger_progress)

        self.setFixedSize(180, status_layout.count() * 15)
        self.setLayout(status_layout)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        # self.setStyleSheet('background: blue;')

        self.installEventFilter(self)

        self.hide()

    def show_status(self, data):
        self.experience_progress.setFormat(f"经验值:{data['experience']}/100")
        self.experience_progress.setValue(data['experience'])
        self.mood_progress.setFormat(f"😊心情值:{data['mood']}/100")
        self.mood_progress.setValue(data['mood'])
        self.hunger_progress.setFormat(f"🍔饱食度:{data['hunger']}/100")
        self.hunger_progress.setValue(data['hunger'])

        self.show()

    def hide_status(self):
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.Linear)
        self.animation.finished.connect(self.hide)
        self.animation.start()

    def stop_hide_animation(self):
        if self.animation and self.animation.state() == QPropertyAnimation.Running:
            self.animation.stop()
            self.animation.updateCurrentValue(1.0)

