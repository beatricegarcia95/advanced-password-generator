import sys
import random
import string
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QCheckBox, QSlider, QSpinBox, QFrame)
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve

class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Advanced Password Generator')
        self.setGeometry(300, 300, 400, 400)
        self.setWindowIcon(QIcon('lock.png'))
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit, QSpinBox {
                background-color: #34495e;
                border: 1px solid #7f8c8d;
                border-radius: 4px;
                padding: 5px;
                color: #ecf0f1;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #7f8c8d;
                height: 8px;
                background: #34495e;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3498db;
                border: 1px solid #2980b9;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Password display
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setFont(QFont('Segoe UI', 14))
        self.password_display.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.password_display)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        # Length slider
        length_layout = QHBoxLayout()
        length_layout.addWidget(QLabel('Length:'))
        self.length_slider = QSlider(Qt.Horizontal)
        self.length_slider.setRange(8, 32)
        self.length_slider.setValue(12)
        self.length_slider.setTickPosition(QSlider.TicksBelow)
        self.length_slider.setTickInterval(4)
        length_layout.addWidget(self.length_slider)
        self.length_spinbox = QSpinBox()
        self.length_spinbox.setRange(8, 32)
        self.length_spinbox.setValue(12)
        length_layout.addWidget(self.length_spinbox)
        layout.addLayout(length_layout)

        # Connect slider and spinbox
        self.length_slider.valueChanged.connect(self.length_spinbox.setValue)
        self.length_spinbox.valueChanged.connect(self.length_slider.setValue)

        # Character type checkboxes
        checkbox_layout = QHBoxLayout()
        self.uppercase_cb = QCheckBox('ABC')
        self.lowercase_cb = QCheckBox('abc')
        self.numbers_cb = QCheckBox('123')
        self.symbols_cb = QCheckBox('#$&')
        
        for cb in [self.uppercase_cb, self.lowercase_cb, self.numbers_cb, self.symbols_cb]:
            cb.setChecked(True)
            checkbox_layout.addWidget(cb)
        
        layout.addLayout(checkbox_layout)

        # Generate button
        self.generate_btn = QPushButton('Generate Password')
        self.generate_btn.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_btn)

        self.setLayout(layout)

    def generate_password(self):
        length = self.length_slider.value()
        char_sets = []
        
        if self.uppercase_cb.isChecked():
            char_sets.append(string.ascii_uppercase)
        if self.lowercase_cb.isChecked():
            char_sets.append(string.ascii_lowercase)
        if self.numbers_cb.isChecked():
            char_sets.append(string.digits)
        if self.symbols_cb.isChecked():
            char_sets.append(string.punctuation)

        if not char_sets:
            self.password_display.setText("Select at least one option")
            return

        password = [random.choice(char_set) for char_set in char_sets]
        for _ in range(length - len(password)):
            password.append(random.choice(random.choice(char_sets)))
        random.shuffle(password)
        
        self.animate_password_display(''.join(password))

    def animate_password_display(self, password):
        self.animation = QPropertyAnimation(self.password_display, b"styleSheet")
        self.animation.setDuration(500)
        self.animation.setStartValue("background-color: #2ecc71; color: #2c3e50;")
        self.animation.setEndValue("background-color: #34495e; color: #ecf0f1;")
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()
        self.password_display.setText(password)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordGenerator()
    ex.show()
    sys.exit(app.exec_())