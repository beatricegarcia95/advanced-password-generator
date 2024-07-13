import sys
import random
import string
import pyperclip
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QCheckBox, QSlider, QSpinBox, QFrame, QProgressBar, QToolTip)
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve

class PasswordGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.dark_mode = True
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Advanced Password Generator')
        self.setGeometry(300, 300, 450, 500)
        self.setWindowIcon(QIcon('lock.png'))
        self.apply_style()

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Password display
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setFont(QFont('Segoe UI', 14))
        self.password_display.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.password_display)

        # Copy to clipboard button
        self.copy_btn = QPushButton('Copy to Clipboard')
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_btn)

        # Password strength meter
        self.strength_bar = QProgressBar()
        self.strength_bar.setTextVisible(False)
        layout.addWidget(self.strength_bar)

        # Separator
        layout.addWidget(self.create_separator())

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
        self.exclude_similar_cb = QCheckBox('Exclude similar')
        
        for cb in [self.uppercase_cb, self.lowercase_cb, self.numbers_cb, self.symbols_cb, self.exclude_similar_cb]:
            cb.setChecked(True)
            checkbox_layout.addWidget(cb)
            cb.setToolTip(self.get_tooltip(cb))
        
        layout.addLayout(checkbox_layout)

        # Generate button
        self.generate_btn = QPushButton('Generate Password')
        self.generate_btn.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_btn)

        # Save password button
        self.save_btn = QPushButton('Save Password')
        self.save_btn.clicked.connect(self.save_password)
        layout.addWidget(self.save_btn)

        # Dark/Light mode toggle
        self.mode_toggle = QPushButton('Toggle Dark/Light Mode')
        self.mode_toggle.clicked.connect(self.toggle_mode)
        layout.addWidget(self.mode_toggle)

        self.setLayout(layout)

    def apply_style(self):
        if self.dark_mode:
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
                QProgressBar {
                    border: 1px solid #7f8c8d;
                    border-radius: 4px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #3498db;
                    width: 10px;
                    margin: 0.5px;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #ecf0f1;
                    color: #2c3e50;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }
                QLineEdit, QSpinBox {
                    background-color: white;
                    border: 1px solid #bdc3c7;
                    border-radius: 4px;
                    padding: 5px;
                    color: #2c3e50;
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
                    border: 1px solid #bdc3c7;
                    height: 8px;
                    background: white;
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
                QProgressBar {
                    border: 1px solid #bdc3c7;
                    border-radius: 4px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #3498db;
                    width: 10px;
                    margin: 0.5px;
                }
            """)

    def create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        return separator

    def get_tooltip(self, checkbox):
        tooltips = {
            self.uppercase_cb: "Include uppercase letters (A-Z)",
            self.lowercase_cb: "Include lowercase letters (a-z)",
            self.numbers_cb: "Include numbers (0-9)",
            self.symbols_cb: "Include symbols (!@#$%^&*)",
            self.exclude_similar_cb: "Exclude similar characters (l, 1, I, 0, O)"
        }
        return tooltips.get(checkbox, "")

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

        all_chars = ''.join(char_sets)
        if self.exclude_similar_cb.isChecked():
            all_chars = ''.join(c for c in all_chars if c not in 'l1IO0')

        password = ''.join(random.choice(all_chars) for _ in range(length))
        
        self.animate_password_display(password)
        self.update_strength_meter(password)

    def animate_password_display(self, password):
        self.animation = QPropertyAnimation(self.password_display, b"styleSheet")
        self.animation.setDuration(500)
        self.animation.setStartValue("background-color: #2ecc71; color: #2c3e50;")
        self.animation.setEndValue("background-color: #34495e; color: #ecf0f1;" if self.dark_mode else "background-color: white; color: #2c3e50;")
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()
        self.password_display.setText(password)

    def update_strength_meter(self, password):
        strength = 0
        if any(c.isupper() for c in password):
            strength += 1
        if any(c.islower() for c in password):
            strength += 1
        if any(c.isdigit() for c in password):
            strength += 1
        if any(c in string.punctuation for c in password):
            strength += 1
        if len(password) >= 12:
            strength += 1

        self.strength_bar.setValue(strength * 20)
        self.strength_bar.setStyleSheet(f"""
            QProgressBar::chunk {{
                background-color: {'#27ae60' if strength > 3 else '#f39c12' if strength > 2 else '#e74c3c'};
            }}
        """)

    def copy_to_clipboard(self):
        password = self.password_display.text()
        if password and password != "Select at least one option":
            pyperclip.copy(password)

    def save_password(self):
        # This is a placeholder for the save password functionality
        # In a real application, you would implement secure local storage
        password = self.password_display.text()
        if password and password != "Select at least one option":
            print(f"Password saved: {password}")  # Replace with secure storage logic

    def toggle_mode(self):
        self.dark_mode = not self.dark_mode
        self.apply_style()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PasswordGenerator()
    ex.show()
    sys.exit(app.exec_())
