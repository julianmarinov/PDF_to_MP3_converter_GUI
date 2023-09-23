import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import PyPDF3
import pdfplumber
from gtts import gTTS
import os
from tqdm import tqdm
import threading
import mutagen

class PDFtoMP3Converter(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PDF to MP3 Converter")
        self.geometry("400x250")

        self.create_widgets()

    def create_widgets(self):
        # Labels and Entries
        ttk.Label(self, text="PDF File Path:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.pdf_file_path = tk.StringVar()
        ttk.Entry(self, textvariable=self.pdf_file_path, width=40).grid(row=0, column=1, padx=10)
        ttk.Button(self, text="Browse", command=self.browse_pdf).grid(row=0, column=2, padx=10)

        ttk.Label(self, text="Save MP3 As:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.mp3_file_path = tk.StringVar()
        ttk.Entry(self, textvariable=self.mp3_file_path, width=40).grid(row=1, column=1, padx=10)
        ttk.Button(self, text="Browse", command=self.browse_mp3).grid(row=1, column=2, padx=10)

        # Convert button
        self.convert_btn = ttk.Button(self, text="Convert", command=self.start_conversion_thread)
        self.convert_btn.grid(row=2, column=1, pady=20)

        # Progress bar
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=200, mode="determinate")
        self.progress.grid(row=3, column=1, pady=20)

    def browse_pdf(self):
        file_path = filedialog.askopenfilename(title="Choose a PDF file", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.pdf_file_path.set(file_path)

    def browse_mp3(self):
        file_path = filedialog.asksaveasfilename(title="Save MP3 As", defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
        if file_path:
            self.mp3_file_path.set(file_path)

    def start_conversion_thread(self):
        # Disable the button to prevent multiple threads
        self.convert_btn.configure(state=tk.DISABLED)

        thread = threading.Thread(target=self.convert_pdf_to_mp3)
        thread.start()

    def convert_pdf_to_mp3(self):
        book = open(self.pdf_file_path.get(), 'rb')
        pdfReader = PyPDF3.PdfFileReader(book)
        pages = pdfReader.numPages
        finalText = ""

        with pdfplumber.open(self.pdf_file_path.get()) as pdf:
            for i in range(0, pages):
                page = pdf.pages[i]
                text = page.extract_text()
                finalText += text if text else ''
                self.update_progress((i+1) * 100 / pages)

        tts = gTTS(text=finalText, lang='en')
        tts.save(self.mp3_file_path.get())

        self.convert_btn.configure(state=tk.NORMAL)
        self.update_progress(0)
        messagebox.showinfo("Info", "Conversion completed!")

    def update_progress(self, value):
        self.progress['value'] = value
        self.update_idletasks()

if __name__ == "__main__":
    app = PDFtoMP3Converter()
    app.mainloop()
