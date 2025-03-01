import cv2
import numpy as np
class ImageScissor:

    def __init__(self):
        self.mask = None
        self.current_image = None
        self.rect = (0, 0, 0) # Bounding box rectangle (width, height, top_left)

    def create_mask(self, image):
        self.current_image = image
        np.zeros(image.shape[:2], np.uint8)

    def get_rect(self, start, end):
        left_x = min(start[0], end[0])
        right_x = max(start[0], end[0])

        left_y = min(start[1], end[1])
        right_y = max(start[1], end[1])
        return (left_x, left_y, right_x, right_y)