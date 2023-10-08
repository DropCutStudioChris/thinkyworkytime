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