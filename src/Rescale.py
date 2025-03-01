from .config import WINDOW_SIZE
from PIL import Image, ImageTk, ImageEnhance

class Rescale:
    def __init__(self):
        self.size = (self._parse_size())
        self.new_size = None

    def rescale_image(self, image):
        if image.size[1] > self.size[1]:
            scale_ratio = self._get_ratio(image.size)
            new_size = (int(image.size[0] * scale_ratio), int(image.size[1] * scale_ratio))
            self.new_size = new_size
            return image.resize(new_size)

    def _get_ratio(self, size):
        return self.size[1] / size[1]


    def _parse_size(self):
        assert(len(WINDOW_SIZE.split("x")) == 2)
        return tuple(int(sz) for sz in WINDOW_SIZE.split("x"))


def main():
    rescale = Rescale()
    print(rescale.size)

if __name__ == "__main__":
    main()