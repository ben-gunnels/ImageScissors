import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import matplotlib.pyplot as plt
from .config import WINDOW_SIZE
from .FileUpload import FileUpload
from .Rescale import Rescale
from .ImageScissor import ImageScissor
# Create main window

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Editor")
        self.root.geometry(WINDOW_SIZE)

        self.image = None
        self.scaled_image = None
        self.tk_image = None

        # Scissor properties
        self.scissor_active = False
        self.scissor_rect_start = None
        self.rect = None
        self.corner_point = None


        self.canvas = tk.Canvas(root, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Local objects
        self.uploader = FileUpload()
        self.rescale = Rescale()
        self.image_scissor = ImageScissor()

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill=tk.X)

        btn_open = tk.Button(btn_frame, text="Open", command=self.open_image)
        btn_open.pack(side=tk.LEFT, padx=5, pady=5)

        btn_grayscale = tk.Button(btn_frame, text="Grayscale", command=self.apply_grayscale)
        btn_grayscale.pack(side=tk.LEFT, padx=5, pady=5)

        btn_save = tk.Button(btn_frame, text="Save", command=self.save_image)
        btn_save.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_scissor = tk.Button(btn_frame, text="Scissor", command=self.scissor)
        self.btn_scissor.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_clear = tk.Button(btn_frame, text="Clear", command=self.clear_scissor)
        self.btn_clear.pack(side=tk.LEFT, padx=5, pady=5)

        self.button_default_bckgd = self.btn_scissor.cget("background")

        self.canvas.bind("<Configure>", self.on_resize)
        self.canvas.bind("<Button-1>", self.on_click)


    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;")])
        if file_path:
            self.image = Image.open(file_path)
            self.rescale_image()  
            self.display_image()

    def rescale_image(self):
        if self.image:
            self.scaled_image = self.rescale.rescale_image((self.canvas.winfo_width(), self.canvas.winfo_height()), self.image)

    def display_image(self):
        if self.scaled_image:
            self.tk_image = ImageTk.PhotoImage(self.scaled_image)
            self.canvas.create_image(self.rescale.anchor[0], self.rescale.anchor[1], image=self.tk_image, anchor=tk.CENTER)

    def apply_grayscale(self):
        if self.image:
            self.image = self.image.convert("L")
            self.display_image()
        

    def save_image(self):
        if self.scaled_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg"),
                                                                ("All Files", "*.*")])
            if save_path:
                self.scaled_image.save(save_path)

    def scissor(self):
        if not self.scissor_active:
            self.scissor_active = True
            self.btn_scissor.config(bg="grey")
        else:
            self.scissor_active = False
            self.btn_scissor.config(bg=self.button_default_bckgd)

    def clear_scissor(self):
        self.scissor_rect_start = None
        if self.rect:
            self.canvas.delete(self.rect)
            self.rect = None
        
        if self.corner_point:
            self.canvas.delete(self.corner_point)
            self.corner_point = None


    def on_resize(self, event):
        # Ensure the canvas does not overlap the button frame
        canvas_height = event.height  # Adjust only if needed
        canvas_width = event.width

        # If an image exists, resize it
        if hasattr(self, 'scaled_image') and self.scaled_image:
            self.rescale_image()
            self.display_image()

    def on_click(self, event):
        if self.scissor_active:
            if not self.scissor_rect_start:
                if self.rect:
                    self.canvas.delete(self.rect)
                self.scissor_rect_start = [event.x, event.y]
                self.corner_point = self.canvas.create_oval(event.x, event.y, event.x+6, event.y+6, outline="black", fill="black")
            else:
                self.canvas.delete(self.corner_point)
                self.draw_rect([event.x, event.y])
                self.scissor_rect_start = None # Reset after rectangle drawn

    def draw_rect(self, scissor_rect_end):
        bounds = self.image_scissor.get_rect(self.scissor_rect_start, scissor_rect_end)
        self.rect = self.canvas.create_rectangle(*bounds, outline="black", fill="black", width=2, stipple="gray50")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()