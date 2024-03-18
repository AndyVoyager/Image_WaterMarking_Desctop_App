# gui.py
__author__ = "AndyVoyager"

import customtkinter as ctk
from PIL import Image, ImageTk, ImageFont, ImageDraw
import tkinter as tk
from tkinter import filedialog
from brain import Brain

FONT = "Arial"
WATERMARK_COLOR = ["white", "black", "red", "green", "blue"]
TEXT_POSITION = ["Top Left", "Top Center", "Top Right", "Bottom Left",
                 "Bottom Center", "Bottom Right",
                 "Center Left", "Center", "Center Right"]


class App(ctk.CTk):
    ctk.set_appearance_mode("system")

    def __init__(self):
        super().__init__()

        self.image_size = None
        self.download_button = None
        self.show_size_label = None
        self.text_size_label = None
        self.brain = None
        self.position = None
        self.text_font = None
        self.filepath = None
        self.watermark_image = None
        self.add_watermark_button = None
        self.top_level = None
        self.top_level_img = None
        self.input_text = None
        self.watermark_text_color = None

        self.setup_download_button()

        self.geometry("800x800+100+50")
        self.title("Watermarker Image App")

        # Create a Watermark Image label:
        self.watermark_label = ctk.CTkLabel(self, text="Watermark IMAGE",
                                            font=(FONT, 28, "bold"),
                                            width=250, height=80)
        self.watermark_label.grid(row=0, column=0, padx=20, pady=0, sticky="n")

        # Create a Description Label:
        self.description_label = ctk.CTkLabel(self, text="Watermark JPG or PNG files. \n"
                                                         "Stamp images or text over your images at once.",
                                              font=(FONT, 20))
        self.description_label.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="n")

        # Add and set Image Example to App:
        self.image = tk.PhotoImage(file="static/img/example_img.png")
        self.image_label = tk.Label(self, image=self.image)
        self.image_label.grid(row=2, column=0, padx=80, pady=0)

        # Create a "Select Image" button:
        self.select_button = ctk.CTkButton(self, text="Select Image",
                                           width=200, height=50,
                                           font=(FONT, 20, "bold"),
                                           command=self.add_image)
        self.select_button.grid(row=3, column=0, pady=20)

        self.grid_columnconfigure(0, weight=1)  # Setting the weight for the first column
        self.grid_rowconfigure(0, weight=1)  # Setting the weight for the first row

    def set_text_position(self):
        return self.brain.get_text_position(input_text=self.input_text.get(),
                                            font=self.text_font,
                                            position=self.position.get())

    def set_watermark_text_size(self, orig_img):
        text_size = self.text_size_label.get()
        image_size = orig_img.size
        return self.brain.get_text_size(size=text_size, image_size=image_size)

    def show_watermark_image(self, image):
        image.thumbnail(size=(600, 600), resample=Image.BICUBIC)
        watermark_image = ImageTk.PhotoImage(image)

        self.image_label.configure(image=watermark_image)
        self.image_label.image = watermark_image

    def save_image(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png")
        if filename:
            self.watermark_image.save(filename)

    def add_text(self):
        self.watermark_image = Image.open(self.filepath)
        orig_img = self.watermark_image.copy()
        orig_img.thumbnail((600, 600), Image.ADAPTIVE)

        self.text_font = ImageFont.truetype(font=FONT, size=self.set_watermark_text_size(orig_img))

        watermark_draw = ImageDraw.Draw(im=orig_img)
        watermark_draw.text(xy=self.set_text_position(), text=self.input_text.get(),
                            font=self.text_font, fill=self.watermark_text_color)

        orig_img.save("static/img/watermarked.png")

        self.show_watermark_image(orig_img)

        self.input_text.delete(0, 'end')

        self.download_button.grid(row=4, column=0, pady=10)

        self.top_level.destroy()

    def setup_download_button(self):
        self.download_button = ctk.CTkButton(self, text="Download", command=self.save_image)

    def update_text_size_label(self, event=None):
        text_size = round(self.text_size_label.get())
        self.show_size_label.configure(text=f"Text Size: {text_size}")

    def new_window(self, filepath):
        ctk.set_appearance_mode("system")
        self.top_level = tk.Toplevel(self)
        self.top_level.geometry("500x650+900+50")
        self.top_level.title("Watermark Image")
        self.top_level.grid_columnconfigure(0, weight=1)
        self.top_level.grid_rowconfigure(0, weight=1)

        self.brain = Brain(self.filepath)

        def option_menu_colors(choice):
            self.watermark_text_color = choice

        original_image_watermark = Image.open(filepath)
        self.image_size = original_image_watermark.size

        original_image_watermark.thumbnail((500, 500), Image.ADAPTIVE)

        self.top_level_img = ImageTk.PhotoImage(original_image_watermark)

        image_watermark_label = tk.Label(self.top_level, image=self.top_level_img, text=filepath)
        image_watermark_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        options_colors = ctk.CTkOptionMenu(self.top_level, values=WATERMARK_COLOR, width=150, height=40,
                                           command=option_menu_colors)
        options_colors.set("Select Color")
        options_colors.set(self.watermark_text_color)
        options_colors.grid(row=1, column=0, rowspan=2, padx=10, pady=(10, 0), sticky="w")

        self.position = ctk.CTkOptionMenu(self.top_level, values=TEXT_POSITION, width=150, height=40)
        self.position.set("Select Position")
        self.position.grid(row=1, column=1, rowspan=2, padx=10, pady=(10, 0), sticky="w")

        self.input_text = ctk.CTkEntry(self.top_level, placeholder_text="Begin typing",
                                       font=(FONT, 14), width=320, height=40)
        self.input_text.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 40), sticky="w")

        self.add_watermark_button = ctk.CTkButton(self.top_level, text="Abracadabra!", width=150, height=40,
                                                  command=self.add_text)
        self.add_watermark_button.grid(row=3, column=2, padx=10, pady=(10, 40), sticky="e")

        self.text_size_label = ctk.CTkSlider(self.top_level, width=150, height=20, from_=0, to=100, number_of_steps=100)
        self.text_size_label.grid(row=2, column=2, padx=10, pady=(10, 0), sticky="w")

        self.show_size_label = ctk.CTkLabel(self.top_level, height=20, font=(FONT, 14),
                                            text=f"Text Size: {round(self.text_size_label.get())}")
        self.show_size_label.grid(row=1, column=2, padx=10, pady=(10, 0), sticky="w")

        self.text_size_label.bind("<Motion>", self.update_text_size_label)

    def add_image(self):
        filepath = filedialog.askopenfilename()
        self.filepath = filepath
        if filepath:
            new_image = Image.open("static/img/magic.png")
            new_image.thumbnail((self.image.width(), self.image.height()), Image.NEAREST)
            new_photo = ImageTk.PhotoImage(new_image)
            self.image_label.configure(image=new_photo)
            self.image_label.image = new_photo

            self.new_window(filepath)
