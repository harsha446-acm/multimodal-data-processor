import pytesseract
import platform

# Configure Tesseract path for Windows
if platform.system() == 'Windows':
    # Update this path if your installation location is different
    pytesseract.pytesseract.tesseract_cmd = r'C://Program Files//Tesseract-OCR//tesseract.exe'