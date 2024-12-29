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
        self.root.geometry("900x700")  # Increased window size
        
        # Configure style
        style = ttk.Style()
        style.configure("TButton", padding=6, font=('Helvetica', 10))
        style.configure("TFrame", background="#f0f0f0")
        
        # Create main frame with better padding
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for better resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Buttons with improved layout
        self.btn_frame = ttk.Frame(self.main_frame)
        self.btn_frame.grid(row=0, column=0, columnspan=2, pady=10)
        
        self.open_btn = ttk.Button(self.btn_frame, text="Open PDF", command=self.open_pdf)
        self.open_btn.grid(row=0, column=0, padx=10)
        
        self.read_btn = ttk.Button(self.btn_frame, text="Read Aloud", command=self.read_text)
        self.read_btn.grid(row=0, column=1, padx=10)
        
        # Text area with improved formatting
        self.text_area = scrolledtext.ScrolledText(
            self.main_frame,
            width=80,
            height=35,
            wrap=tk.WORD,
            font=('Helvetica', 11),
            padx=10,
            pady=10,
            background="#2E2E2E",  # Dark gray background
            foreground="#FFFFFF"    # White text
        )
        self.text_area.grid(row=1, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text area grid weights
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.current_pdf = None
        self.pdf_text = ""
        # Add voice selection frame
        self.voice_frame = ttk.Frame(self.main_frame)
        self.voice_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # Voice selection dropdown
        self.voice_label = ttk.Label(self.voice_frame, text="Select Voice:")
        self.voice_label.grid(row=0, column=0, padx=5)

        self.voice_var = tk.StringVar()
        self.voice_combo = ttk.Combobox(self.voice_frame, textvariable=self.voice_var)
        self.voice_combo.grid(row=0, column=1, padx=5)
        
        # Speed control
        self.speed_label = ttk.Label(self.voice_frame, text="Speed:")
        self.speed_label.grid(row=0, column=2, padx=5)
        
        self.speed_var = tk.DoubleVar(value=175)  # Default speed
        self.speed_scale = ttk.Scale(
            self.voice_frame, 
            from_=100, 
            to=250, 
            variable=self.speed_var, 
            orient='horizontal'
        )
        self.speed_scale.grid(row=0, column=3, padx=5)

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.update_voice_list()

    def update_voice_list(self):
        # Get available voices
        voices = self.engine.getProperty('voices')
        self.voices = voices
        # Update combobox with voice names
        voice_names = [voice.name for voice in voices]
        self.voice_combo['values'] = voice_names
        
        # Set default voice (usually index 0 is male, 1 is female)
        if len(voice_names) > 0:
            self.voice_combo.set(voice_names[0])
            
    def open_pdf(self):
        file_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                self.current_pdf = PyPDF2.PdfReader(file_path)
                self.pdf_text = ""
                for page in self.current_pdf.pages:
                    text = page.extract_text()
                    # Improve text formatting
                    text = ' '.join(text.split())  # Remove extra whitespace and preserve single spaces
                    text = text.replace('. ', '.\n\n')  # Add paragraph breaks after sentences
                    self.pdf_text += text
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

