import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os

# Ensure upload directory exists
upload_dir = "uploads"
os.makedirs(upload_dir, exist_ok=True)

class FileUpload:
    def __init__(self):
        self.out_file = None

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg")])  # Open file dialog
        if file_path:
            file_name = os.path.basename(file_path)
            if file_name.lower().endswith((".jpg", ".png")):
                shutil.copy(file_path, os.path.join(upload_dir, file_name))  # Copy file to 'uploads' directory
                messagebox.showinfo("Success", f"File '{file_name}' uploaded successfully!")
                self.out_file = file_path
            else:
                messagebox.showerror("Error", "Invalid file type! Please upload a .png or .jpg file.")
        