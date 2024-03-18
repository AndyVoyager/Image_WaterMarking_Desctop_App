# brain.py
__author__ = "AndyVoyager"

from PIL import Image, ImageDraw


class Brain:
    def __init__(self, filepath):
        self.text_size = None
        self.image_height = None
        self.image_width = None
        self.filepath = filepath

    def get_image_and_text_size(self, text, font):
        image = Image.open(self.filepath)
        draw = ImageDraw.Draw(image)

        self.image_width, self.image_height = image.size
        print(image.size)

        return draw.textlength(text=text, font=font)

    def get_text_position(self, input_text, font, position):
        text_length = self.get_image_and_text_size(text=input_text, font=font)
        padding_ratio = 0.02

        padding_width = int(self.image_width * padding_ratio)
        padding_height = int(self.image_height * padding_ratio)

        if position == "Top Left":
            return padding_width, padding_height
        elif position == "Top Center":
            return (self.image_width - text_length) // 2, padding_height
        elif position == "Top Right":
            return self.image_width - text_length - padding_width, padding_height
        elif position == "Bottom Left":
            return padding_width, self.image_height - self.text_size - padding_height
        elif position == "Bottom Center":
            return (self.image_width - text_length) // 2, self.image_height - self.text_size - padding_height
        elif position == "Bottom Right":
            return self.image_width - text_length - padding_width, self.image_height - self.text_size - padding_height
        elif position == "Center Left":
            return padding_width, (self.image_height - self.text_size) // 2
        elif position == "Center":
            return (self.image_width - text_length) // 2, (self.image_height - self.text_size) // 2
        elif position == "Center Right":
            return self.image_width - text_length - padding_width, (self.image_height - self.text_size) // 2

    def get_text_size(self, size, image_size):
        self.text_size = size
        width, height = image_size
        proportion = min(width, height) / max(width, height)
        return int(size * proportion)
