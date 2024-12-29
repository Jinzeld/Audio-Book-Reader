import pyttsx3
import PyPDF2
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import scrolledtext

class PDFReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Reader")
        self.root.geometry("800x600")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Buttons
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_frame.grid(row=0, column=0, columnspan=2, pady=5)
        
        self.open_btn = ttk.Button(self.btn_frame, text="Open PDF", command=self.open_pdf)
        self.open_btn.grid(row=0, column=0, padx=5)
        
        self.read_btn = ttk.Button(self.btn_frame, text="Read Aloud", command=self.read_text)
        self.read_btn.grid(row=0, column=1, padx=5)
        
        # Text area for PDF content
        self.text_area = scrolledtext.ScrolledText(self.main_frame, width=70, height=30)
        self.text_area.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.current_pdf = None
        self.pdf_text = ""

    def open_pdf(self):
        file_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                self.current_pdf = PyPDF2.PdfReader(file_path)
                self.pdf_text = ""
                for page in self.current_pdf.pages:
                    self.pdf_text += page.extract_text()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, self.pdf_text)
            except Exception as e:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, f"Error opening PDF: {str(e)}")

    def read_text(self):
        if self.pdf_text:
            player = pyttsx3.init()
            player.say(self.pdf_text)
            player.runAndWait()

def main():
    root = tk.Tk()
    app = PDFReaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

