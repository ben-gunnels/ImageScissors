import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import matplotlib.pyplot as plt
# Create main window

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Editor")
        self.root.geometry("800x600")

        self.image = None
        self.tk_image = None
        self.canvas = tk.Canvas(root, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill=tk.X)

        btn_open = tk.Button(btn_frame, text="Open", command=self.open_image)
        btn_open.pack(side=tk.LEFT, padx=5, pady=5)

        btn_grayscale = tk.Button(btn_frame, text="Grayscale", command=self.apply_grayscale)
        btn_grayscale.pack(side=tk.LEFT, padx=5, pady=5)

        btn_save = tk.Button(btn_frame, text="Save", command=self.save_image)
        btn_save.pack(side=tk.LEFT, padx=5, pady=5)
        
    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image()

    def display_image(self):
        if self.image:
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(400, 300, image=self.tk_image, anchor=tk.CENTER)

    def apply_grayscale(self):
        if self.image:
            self.image = self.image.convert("L")
            self.display_image()

    def save_image(self):
        if self.image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("All Files", "*.*")])
            if save_path:
                self.image.save(save_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()