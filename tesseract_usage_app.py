import os
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox,
    QTextEdit, QFileDialog, QCheckBox, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette
from PIL import Image
import pytesseract
import cv2

# Set the Tesseract path
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

class OCRApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Tesseract OCR Application")
        self.setGeometry(100, 100, 600, 400)

        # Set the default dark theme
        self.set_light_theme()

        # Theme switching button
        self.theme_button = QPushButton("Switch Theme")
        self.theme_button.clicked.connect(self.toggle_theme)

        # Language selection
        self.language_label = QLabel("Select Language:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(["eng", "rus", "equ"])
        self.language_combo.setCurrentIndex(0)

        # Advanced preprocessing options
        self.advanced_label = QLabel("Advanced Preprocessing:")
        self.grayscale_checkbox = QCheckBox("Grayscale")
        self.thresholding_checkbox = QCheckBox("Thresholding")
        self.denoising_checkbox = QCheckBox("Denoising")
        self.binarization_checkbox = QCheckBox("Binarization")

        # Open file button
        self.open_button = QPushButton("Open Image")
        self.open_button.clicked.connect(self.open_file)

        # Extract text button
        self.extract_button = QPushButton("Extract Text")
        self.extract_button.clicked.connect(self.extract_text)

        # Display the selected file
        self.file_label = QLabel("Selected File: None")

        # Result text display
        self.result_label = QLabel("Extracted Text:")
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.theme_button)  # Add theme button
        layout.addWidget(self.language_label)
        layout.addWidget(self.language_combo)
        layout.addWidget(self.advanced_label)
        layout.addWidget(self.grayscale_checkbox)
        layout.addWidget(self.thresholding_checkbox)
        layout.addWidget(self.denoising_checkbox)
        layout.addWidget(self.binarization_checkbox)
        layout.addWidget(self.open_button)
        layout.addWidget(self.extract_button)
        layout.addWidget(self.file_label)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_text)
        self.setLayout(layout)

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(35, 35, 35))  # Dark background color
        palette.setColor(QPalette.ColorRole.Button, QColor(186, 220, 88))  # Button color (interesting green)
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)  # Button text color
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)  # Text color
        self.setPalette(palette)

        font = QFont("Segoe UI", 12)  # Change font to a modern one
        self.setFont(font)

    def set_light_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))  # Light background color
        palette.setColor(QPalette.ColorRole.Button, QColor(255, 0, 150))  # Button color (interesting magenta)
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)  # Button text color
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)  # Text color
        self.setPalette(palette)

        font = QFont("Segoe UI", 12)  # Change font to a modern one
        self.setFont(font)

    def toggle_theme(self):
        # Toggle between dark and light themes by comparing color names
        current_color_name = self.palette().color(QPalette.ColorRole.Window).name()
        dark_color_name = QColor(35, 35, 35).name()

        if current_color_name == dark_color_name:
            self.set_light_theme()
        else:
            self.set_dark_theme()


    def open_file(self):
        global filename
        options = QFileDialog.Option.ReadOnly
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp);;All Files (*)", options=options)
        self.file_label.setText(f"Selected File: {os.path.basename(filename)}")

    def extract_text(self):
        lang = self.language_combo.currentText()
        custom_config = f'-l {lang} --oem 3 --psm 6'

        # Preprocess the image
        image = cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Check the state of each preprocessing checkbox and apply the selected options
        if self.grayscale_checkbox.isChecked():
            # Apply grayscale conversion
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if self.thresholding_checkbox.isChecked():
            # Apply thresholding
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        if self.denoising_checkbox.isChecked():
            # Apply denoising (e.g., Gaussian blur)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)

        if self.binarization_checkbox.isChecked():
            # Apply binarization
            _, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Save the preprocessed image
        temp_filename = f"{os.getpid()}.png"
        cv2.imwrite(temp_filename, gray)

        # Convert the image to text using Tesseract
        text = pytesseract.image_to_string(Image.open(temp_filename), config=custom_config)

        # Remove the temporary image file
        if os.path.isfile(temp_filename):
            os.remove(temp_filename)

        # Display the extracted text
        self.result_text.setPlainText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ocr_app = OCRApplication()
    ocr_app.show()
    sys.exit(app.exec())