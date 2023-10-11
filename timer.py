from PyQt5.QtCore import QTimer, QTime, pyqtSignal

class PomodoroTimer:
    time_changed = pyqtSignal(QTime)
    timer_finished = pyqtSignal()

    def __init__(self):
        self.timer = QTimer()
        self.time_left = QTime(0, 25)
        self.timer.timeout.connect(self.update_time)

    def start(self):
        self.timer.start(1000)

    def stop(self):
        self.timer.stop()

    def update_time(self):
        self.time_left = self.time_left.addSecs(-1)
        self.time_changed.emit(self.time_left)
        
        if self.time_left == QTime(0, 0):
            self.stop()
            self.timer_finished.emit()
