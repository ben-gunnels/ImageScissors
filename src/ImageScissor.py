import cv2
from PIL import Image
import numpy as np
from .config import (NUMBER_ITERATIONS)

class ImageScissor:
    def __init__(self):
        pass
    def create_mask(self, image, rect, anchor):
        """
            Draws a mask around the image based on the rectangle drawn by the user. Must account for the current anchor point of the image
            to determine starting position. 
            By default the image is anchored at its center. The anchor parameter tells the function where the center of the image is. 
            Parameters: image (PIL image), rect (Rect), anchor (int, int)
        """
        import numpy as np

    def create_mask(self, image, rect, anchor):
        """
        Draws a mask around the image based on the rectangle drawn by the user.
        Must account for the current anchor point of the image to determine the starting position.
        
        Parameters:
        - image (PIL Image): Input image
        - rect (Rect): Bounding box with attributes (left_x, right_x, top_y, bot_y)
        - anchor (tuple): Anchor point (x, y)
        """
        # Convert image to RGBA to support transparency (4 channels)
        img_array = np.array(image)
        img_array_with_alpha = np.array(image.convert("RGBA"))

        print(img_array.shape)  # Check the shape of the array

        # Create an initial mask (binary: 0 or 2 for background, 1 for foreground)
        mask = np.zeros(img_array.shape[:2], np.uint8)

        # Ensure rectangle coordinates are within bounds
        bounds = self._get_image_bounds(image, anchor)
        rect.left_x = max(rect.left_x, bounds.left)
        rect.right_x = min(rect.right_x, bounds.right)
        rect.top_y = max(rect.top_y, bounds.top)
        rect.bot_y = min(rect.bot_y, bounds.bot)

        # Create background/foreground models for grabCut
        backgroundModel = np.zeros((1, 65), np.float64)
        foregroundModel = np.zeros((1, 65), np.float64)

        # Apply GrabCut segmentation
        cv2.grabCut(img_array, mask, (rect.left_x, rect.top_y, rect.right_x, rect.bot_y),  
                    backgroundModel, foregroundModel, NUMBER_ITERATIONS, cv2.GC_INIT_WITH_RECT)

        # Convert mask to binary: Foreground (1), Background (0)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

        # Apply mask to image, keeping only foreground
        img_array_with_alpha[:, :, 3] = mask2 * 255  # Modify the alpha channel (4th channel) for transparency

        # Convert back to PIL image
        image_segmented = Image.fromarray(img_array_with_alpha)

        return image_segmented
        

    def get_rect(self, start, end):
        """
            Generates a rectangle based on the selection of two points within a frame.
            Creates the proper orientation (left, right, top, bottom)
            Parameters: start (int, int), end (int, ind)
            Returns: Rect (obj)
        """
        class Rect:
            def __init__(self, left_x, right_x, top_y, bot_y):
                self.left_x = left_x
                self.right_x = right_x
                self.top_y = top_y
                self.bot_y = bot_y
        left_x = min(start[0], end[0])
        right_x = max(start[0], end[0])

        bot_y = max(start[1], end[1])
        top_y = min(start[1], end[1])
        return Rect(left_x, right_x, top_y, bot_y)
    
    def _get_image_bounds(self, image, anchor):
        """
            Gets the bounds of an image based on the anchor point
            Parameters: image (PIL image), anchor (int, int)
            Returns: Bounds (obj)
        """
        class Bounds:
            def __init__(self, left, right, top, bot):
                self.left = left
                self.right = right
                self.top = top
                self.bot = bot
        left = anchor[0] - image.size[0] // 2
        right = anchor[0] + image.size[0] // 2  
        top = anchor[1] - image.size[1] // 2
        bot = anchor[1] + image.size[1] // 2
        return Bounds(left, right, top, bot)

