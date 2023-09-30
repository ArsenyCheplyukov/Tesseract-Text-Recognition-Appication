import os
from PIL import Image
import pytesseract
import cv2

# Set the Tesseract path and language
pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR/tesseract.exe"
tessdata_dir_config = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata"'

image = 'tests3.png'
preprocess = "thresh"

# Load and preprocess the image
image = cv2.imread(image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
if preprocess == "thresh":
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# Save the preprocessed image
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

# Set the Tesseract configuration
custom_config = r'-l rus --oem 3 --psm 6'

# Convert the image to text using Tesseract
text = pytesseract.image_to_string(Image.open(filename), config=custom_config)

# Remove the temporary image file
if os.path.isfile(filename):
    os.remove(filename)
else:
    # If it fails, inform the user.
    print("Error: %s file not found" % filename)

# Print the extracted text
print(text)
