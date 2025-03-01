from .config import WINDOW_SIZE
from PIL import Image, ImageTk, ImageEnhance

class Rescale:
    def __init__(self):
        self.new_size = None

    def rescale_image(self, window_size: tuple, image):
        if image.size[1] > window_size[1]:
            scale_ratio = self._get_ratio(window_size, image.size)
            new_size = (int(image.size[0] * scale_ratio), int(image.size[1] * scale_ratio))
            self.new_size = new_size
            self.anchor = self._get_anchor()
            return image.resize(new_size)

    def _get_ratio(self, window_size, image_size):
        return window_size[1] / image_size[1]
    
    def _get_anchor(self):
        return (self.new_size[0] // 2, self.new_size[1] // 2)


def main():
    rescale = Rescale()
    print(rescale.size)

if __name__ == "__main__":
    main()