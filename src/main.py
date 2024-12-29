import pyttsx3
import PyPDF2
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Initialize Tk root window and hide it
root = Tk()


book = askopenfilename()
pdfreader = PyPDF2.pdfFileReader(book)
pages = pdfreader.numPages

for num in range(0, pages):
    page = pdfreader.getPage(num)
    text = page.extractText()
    player = pyttsx3.init()
    player.runAndWait()

