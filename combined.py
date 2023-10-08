################################################################################
# File: main.py
################################################################################

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtWidgets import QRubberBand, QDesktopWidget
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor, QPalette, QBrush

class RedBorderManager:

    def __init__(self):
        self.screens = []
        self.borders = []
        self.border_thickness = 10

    def draw_red_borders(self):
        desktop = QDesktopWidget()

        # Loop over all screens
        for i in range(desktop.screenCount()):
            screen_geometry = desktop.screenGeometry(i)
            
            # Top border
            top_border = QRubberBand(QRubberBand.Rectangle)
            top_border.setGeometry(QRect(screen_geometry.left(), screen_geometry.top(), screen_geometry.width(), self.border_thickness))
            self.borders.append(top_border)

            # Bottom border
            bottom_border = QRubberBand(QRubberBand.Rectangle)
            bottom_border.setGeometry(QRect(screen_geometry.left(), screen_geometry.bottom() - 5, screen_geometry.width(), self.border_thickness))
            self.borders.append(bottom_border)

            # Left border
            left_border = QRubberBand(QRubberBand.Rectangle)
            left_border.setGeometry(QRect(screen_geometry.left(), screen_geometry.top(), self.border_thickness, screen_geometry.height()))
            self.borders.append(left_border)

            # Right border
            right_border = QRubberBand(QRubberBand.Rectangle)
            right_border.setGeometry(QRect(screen_geometry.right() - 5, screen_geometry.top(), self.border_thickness, screen_geometry.height()))
            self.borders.append(right_border)

        # Set color to red and show
        palette = QPalette()
        palette.setBrush(QPalette.Highlight, QBrush(QColor("red")))
        for border in self.borders:
            border.setPalette(palette)
            border.show()

    def remove_borders(self):
        for border in self.borders:
            border.hide()
        self.borders.clear()

class PomodoroApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.red_border_manager = RedBorderManager()
        # Timer and initial state
        self.timer = QTimer(self)
        self.is_focus_period = True  # Focus period when True, rest when False
        self.time_left = QTime(0, 25)  # Default to 25 minutes

        # Start button
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_timer)
        #self.red_border_manager.draw_red_borders()

        # Stop button
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_timer)
        #self.red_border_manager.remove_borders()
        
        # Countdown Label
        self.countdown_label = QLabel(self)
        self.countdown_label.setText(self.time_left.toString())

        # Dropdown for focus and rest periods
        self.focus_dropdown = QComboBox(self)
        self.rest_dropdown = QComboBox(self)
        for i in range(1, 13):  # 5 to 60 in 5-minute increments
            self.focus_dropdown.addItem(f"{i * 5} minutes")
            self.rest_dropdown.addItem(f"{i * 5} minutes")
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.countdown_label)
        layout.addWidget(QLabel("Focus Period:"))
        layout.addWidget(self.focus_dropdown)
        layout.addWidget(QLabel("Rest Period:"))
        layout.addWidget(self.rest_dropdown)
        
        container = QWidget()
        container.setLayout(layout)
        
        self.setCentralWidget(container)
        self.setWindowTitle("Pomodoro Timer")
        self.show()

        self.focus_dropdown.currentIndexChanged.connect(self.update_initial_time)
        self.rest_dropdown.currentIndexChanged.connect(self.update_initial_time)


    def start_timer(self):
        # Set the timer's timeout to 1 second (1000 ms)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()
        self.red_border_manager.remove_borders()

    def update_time(self):
        self.time_left = self.time_left.addSecs(-1)
        self.countdown_label.setText(self.time_left.toString())

        if self.time_left == QTime(0, 0):
            self.stop_timer()
            self.is_focus_period = not self.is_focus_period  # Switch between focus and rest
            if self.is_focus_period:
                mins = int(self.focus_dropdown.currentText().split()[0])
            else:
                mins = int(self.rest_dropdown.currentText().split()[0])
            self.time_left = QTime(0, mins)

    def update_initial_time(self):
        if self.is_focus_period:
            mins = int(self.focus_dropdown.currentText().split()[0])
        else:
            mins = int(self.rest_dropdown.currentText().split()[0])
        self.time_left = QTime(0, mins)
        self.countdown_label.setText(self.time_left.toString())

    def start_timer(self):
        self.red_border_manager.draw_red_borders()
        # Set the timer's timeout to 1 second (1000 ms)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)


app = QApplication(sys.argv)
app.setStyle("Fusion")
window = PomodoroApp()
sys.exit(app.exec_())


