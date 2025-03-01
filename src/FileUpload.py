import tkinter as tk
from tkinter import filedialog, messagebox
import shutil
import os
from PIL import Image, ImageTk, ImageEnhance


# Ensure upload directory exists
upload_dir = "uploads"
os.makedirs(upload_dir, exist_ok=True)

class FileUpload:
    def __init__(self):
        self.out_file = None

    
        